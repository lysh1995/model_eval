"""Card-awareness audit, v2 -- fixing two confounds in v1.

v1 found own-card term leak at 1.84x (en) / 1.68x (zh) over a random-other-card control,
p<0.0001. Two things could produce that WITHOUT the simulator seeing the card:

  BUG   the first user turn is `initial_user_input`, taken verbatim from the seed. It is
        card-derived BY CONSTRUCTION. v1 counted it. Exclude it.

  CONFOUND  topic. The card says "scalpel"; the AI says "knife"; the user says "scalpel"
        because they are in a hospital. The control (a RANDOM other card) is a different
        topic entirely, so v1's lift may be measuring topic-relatedness, not card access.

v2 adds the decisive test: TEMPORAL PRECEDENCE. A card-blind simulator can only learn
about the character from what the AI has already said. So count card terms the user
utters at turn t that the AI has NOT said at any turn < t. Under the topic explanation
these should still appear (topic is available from context); under card access they
appear MORE for the own card than a topic-matched control.

Topic-matched control: the other card with the highest term overlap with THIS card
(nearest neighbour), rather than a random card. That holds topic roughly fixed and
isolates card-specificity.
"""
import json, collections, random, re, statistics as st
random.seed(0)

STOP_EN = set("""a an the and or but if then than that this these those of in on at to for with by from up
about into over after is are was were be been being have has had do does did will would shall should may
might must can could i you he she it we they them his her its their my your our not no yes as so very
just also more most much many some any all each every other another such own same too who whom whose
which what when where why how there here now new old good bad man woman men women person people said say
says like know think want come came go went get got make made take took see saw look looked""".split())

def terms(text, lang):
    if lang == 'en':
        return {w for w in re.findall(r"[a-z']{4,}", text.lower()) if w not in STOP_EN}
    t = re.sub(r'[^一-鿿]', '', text)
    return {t[i:i+2] for i in range(len(t) - 1)}

for lang in ('en', 'zh'):
    seeds = {}
    with open(f'data/{lang}/seeds.jsonl') as f:
        for line in f:
            r = json.loads(line); seeds[r['id']] = r
    ids = sorted(seeds)
    card = {i: terms(seeds[i]['ai_setting'], lang) for i in ids}

    # topic-matched control: nearest-neighbour card by Jaccard overlap
    nn = {}
    for i in ids:
        best, bj = None, -1.0
        for j in ids:
            if i == j: continue
            inter = len(card[i] & card[j]); union = len(card[i] | card[j]) or 1
            jac = inter / union
            if jac > bj: bj, best = jac, j
        nn[i] = (best, bj)
    print(f"=== {lang.upper()} — card-awareness v2 ===")
    print(f"  topic-matched control: mean Jaccard(own card, nearest other card) = "
          f"{st.mean(b for _, b in nn.values()):.3f}")

    own_pre, ctl_pre = [], []
    with open(f'data/{lang}/dialogues.jsonl') as f:
        for line in f:
            r = json.loads(line)
            if r['run_id'] != 'run_1':
                continue
            d = json.loads(r['dialogue'])
            # FIX: drop the scripted first user turn (round 1 == initial_user_input)
            user_turns = [t for t in d if t['role'] == 'user' and t['round'] > 1]
            ai_turns   = [t for t in d if t['role'] == 'ai']
            if not user_turns:
                continue

            # AI vocabulary revealed strictly BEFORE each user turn
            ai_by_round = sorted(((t['round'], terms(t['text'], lang)) for t in ai_turns))
            def ai_said_before(rnd):
                acc = set()
                for ar, ts in ai_by_round:
                    if ar >= rnd: break
                    acc |= ts
                return acc

            def precedence_rate(seed_id):
                c = card[seed_id]
                if not c: return None
                hits = tot = 0
                for ut in user_turns:
                    revealed = ai_said_before(ut['round'])
                    unrevealed = c - revealed          # card terms the AI has NOT yet said
                    if not unrevealed: continue
                    hits += len(terms(ut['text'], lang) & unrevealed)
                    tot  += len(unrevealed)
                return hits / tot if tot else None

            o = precedence_rate(r['seed_id'])
            c_ = precedence_rate(nn[r['seed_id']][0])
            if o is None or c_ is None: continue
            own_pre.append(o); ctl_pre.append(c_)

    diffs = [a - b for a, b in zip(own_pre, ctl_pre)]
    obs = st.mean(diffs)
    hits = 0; TRIALS = 20000
    for _ in range(TRIALS):
        if abs(st.mean(d if random.random() < .5 else -d for d in diffs)) >= abs(obs):
            hits += 1
    p = (hits + 1) / (TRIALS + 1)
    om, cm = st.mean(own_pre), st.mean(ctl_pre)
    print(f"  n={len(diffs)} dialogues, scripted first user turn EXCLUDED")
    print(f"  user says card term the AI has not yet said:")
    print(f"     own card              : {om:.5f}")
    print(f"     topic-matched control : {cm:.5f}")
    print(f"     lift                  : {om/cm if cm else float('inf'):.2f}x")
    print(f"     paired diff {obs:+.5f}   permutation p = {p:.4f}")
    print(f"  --> {'CARD ACCESS (survives topic control + precedence)' if p<0.05 and obs>0 else 'NO evidence of card access once topic is controlled'}\n")
