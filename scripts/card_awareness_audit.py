"""Did the user simulator SEE the character card?

Why it matters: if the user turns were generated with card access, the simulator is a
COLLABORATIVE partner, not a user. A collaborator does not probe the seams -- it knows
who the character is and plays along. That systematically UNDER-detects drift, which
biases every consistency metric in the catalogue. Stream 8 flagged this as a bigger
threat to validity than off-policyness itself.

Design. For each dialogue:
  - take distinctive terms from that character's OWN card that the AI never uttered
  - count how many appear in the USER turns                            -> "own leak"
  - do the same with a RANDOM OTHER character's card                   -> "control leak"
If the simulator is card-blind, own ~= control (both are chance). If it saw the card,
own >> control.

The control is the whole experiment. Raw "own leak" alone is meaningless: user turns
naturally echo the AI's vocabulary, and cards share generic words.
"""
import json, collections, random, re, statistics as st
random.seed(0)

STOP_EN = set("""a an the and or but if then than that this these those of in on at to for with by from up
about into over after is are was were be been being have has had do does did will would shall should may
might must can could i you he she it we they them his her its their my your our not no yes as so very
just also more most much many some any all each every other another such own same too own who whom whose
which what when where why how there here now new old good bad man woman men women person people""".split())

def terms(text, lang):
    if lang == 'en':
        ws = re.findall(r"[a-z']{4,}", text.lower())
        return {w for w in ws if w not in STOP_EN}
    # zh: character bigrams are a reasonable proxy for content terms
    t = re.sub(r'[^一-鿿]', '', text)
    return {t[i:i+2] for i in range(len(t) - 1)}

for lang in ('en', 'zh'):
    seeds = {}
    with open(f'data/{lang}/seeds.jsonl') as f:
        for line in f:
            r = json.loads(line); seeds[r['id']] = r
    ids = sorted(seeds)

    own_rates, ctl_rates = [], []
    per_seed = collections.defaultdict(list)

    with open(f'data/{lang}/dialogues.jsonl') as f:
        for line in f:
            r = json.loads(line)
            if r['run_id'] != 'run_1':
                continue
            d = json.loads(r['dialogue'])
            ai_text = ' '.join(t['text'] for t in d if t['role'] == 'ai')
            user_text = ' '.join(t['text'] for t in d if t['role'] == 'user')
            ai_terms, user_terms = terms(ai_text, lang), terms(user_text, lang)

            # control: a different character's card, matched by construction (same corpus)
            other = random.choice([i for i in ids if i != r['seed_id']])

            def leak(seed_id):
                card = terms(seeds[seed_id]['ai_setting'], lang)
                # distinctive = in the card, never said by the AI in this dialogue
                distinctive = card - ai_terms
                if not distinctive:
                    return None
                return len(distinctive & user_terms) / len(distinctive)

            o, c = leak(r['seed_id']), leak(other)
            if o is None or c is None:
                continue
            own_rates.append(o); ctl_rates.append(c)
            per_seed[r['seed_id']].append(o - c)

    n = len(own_rates)
    own_m, ctl_m = st.mean(own_rates), st.mean(ctl_rates)
    diffs = [a - b for a, b in zip(own_rates, ctl_rates)]

    # paired permutation test: randomly flip the sign of each paired difference
    obs = st.mean(diffs)
    hits = 0; TRIALS = 20000
    for _ in range(TRIALS):
        m = st.mean(d if random.random() < .5 else -d for d in diffs)
        if abs(m) >= abs(obs):
            hits += 1
    p = (hits + 1) / (TRIALS + 1)

    lift = own_m / ctl_m if ctl_m else float('inf')
    print(f"=== {lang.upper()} — card-awareness audit (n={n} dialogues, run_1) ===")
    print(f"  own-card term leak into user turns     : {own_m:.4f}")
    print(f"  control (random other card)            : {ctl_m:.4f}")
    print(f"  lift (own / control)                   : {lift:.2f}x")
    print(f"  paired difference                      : {obs:+.4f}   permutation p = {p:.4f}")
    verdict = ("SIMULATOR LIKELY SAW THE CARD -> collaborative, under-detects drift"
               if p < 0.05 and obs > 0 else
               "no evidence of card access -> simulator appears card-blind")
    print(f"  --> {verdict}\n")
