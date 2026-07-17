"""L1 comprehension, observable with no API key.

All 11 models received IDENTICAL character sheets. So: when models are given the same
character, do they converge on how to play it?

  high cross-model agreement  -> the sheet reads unambiguously
  low  cross-model agreement  -> the sheet is ambiguous, OR models genuinely differ in
                                 how they comprehend it

This is not steerability (that needs generation under perturbed prompts). It is the
closest free observable to L1, and it yields something directly useful: WHICH characters
are hard to read, and whether difficulty tracks sheet properties (L1.3 load curve).

Length-controlled from the start -- see notes/09: the naive version of this family of
metric measures verbosity (rho=+0.73).
"""
import json, collections, statistics as st, random
random.seed(0)

def toks(t, lang):
    return t.lower().split() if lang == 'en' else list(t)

def profile(units, lang):
    N = 2 if lang == 'en' else 3
    c = collections.Counter(tuple(units[i:i+N]) for i in range(len(units) - N + 1))
    tot = sum(c.values()) or 1
    return {k: v / tot for k, v in c.items()}

def cos(a, b):
    ks = set(a) & set(b)
    n = sum(a[k] * b[k] for k in ks)
    da = sum(v * v for v in a.values()) ** .5
    db = sum(v * v for v in b.values()) ** .5
    return n / (da * db) if da and db else 0.0

def spearman(a, b):
    def rank(x):
        s = sorted(range(len(x)), key=lambda i: x[i]); r = [0] * len(x)
        for p, i in enumerate(s): r[i] = p + 1
        return r
    ra, rb = rank(a), rank(b); n = len(a)
    ma, mb = st.mean(ra), st.mean(rb)
    num = sum((ra[i] - ma) * (rb[i] - mb) for i in range(n))
    den = (sum((r - ma) ** 2 for r in ra) * sum((r - mb) ** 2 for r in rb)) ** .5
    return num / den if den else 0.0

for lang, BUDGET in (('en', 900), ('zh', 3000)):
    seeds = {}
    with open(f'data/{lang}/seeds.jsonl') as f:
        for line in f:
            r = json.loads(line); seeds[r['id']] = r

    # character -> model -> concatenated ai tokens (run_1 only: one rollout per cell,
    # so cross-model divergence isn't inflated by within-model run variance)
    by = collections.defaultdict(lambda: collections.defaultdict(list))
    with open(f'data/{lang}/dialogues.jsonl') as f:
        for line in f:
            r = json.loads(line)
            if r['run_id'] != 'run_1':
                continue
            for t in json.loads(r['dialogue']):
                if t['role'] == 'ai':
                    by[r['seed_id']][r['model_name']] += toks(t['text'], lang)

    conv = {}
    for seed, models in by.items():
        P = {m: profile(u[:BUDGET], lang) for m, u in models.items() if len(u) >= BUDGET}
        if len(P) < 8:            # need most models present for a fair comparison
            continue
        ms = sorted(P)
        pairs = [(a, b) for i, a in enumerate(ms) for b in ms[i+1:]]
        conv[seed] = (st.mean(cos(P[a], P[b]) for a, b in pairs), len(P))

    if not conv:
        print(f"{lang}: no characters funded the {BUDGET}-token budget across >=8 models")
        continue

    vals = [v for v, _ in conv.values()]
    print(f"\n=== {lang.upper()} — convergent reading (cross-MODEL agreement per character) ===")
    print(f"  characters analysed: {len(conv)}  (>=8 models each, {BUDGET}-token budget)")
    print(f"  agreement: min={min(vals):.3f} median={st.median(vals):.3f} max={max(vals):.3f}")

    # Does 'hard to read' track sheet length? (L1.3 load curve, first look)
    ks = sorted(conv)
    sheet_len = [len(toks(seeds[k]['ai_setting'], lang)) for k in ks]
    agree = [conv[k][0] for k in ks]
    print(f"  Spearman(sheet length, cross-model agreement) = {spearman(sheet_len, agree):+.3f}")

    # Confound check: is agreement just tracking output length? (budget should have killed this)
    out_len = [st.mean(len(u) for u in by[k].values()) for k in ks]
    print(f"  Spearman(output length, cross-model agreement) = {spearman(out_len, agree):+.3f}   <- want ~0")

    ranked = sorted(conv.items(), key=lambda kv: kv[1][0])
    print(f"\n  HARDEST to read (models disagree most):")
    for s, (v, n) in ranked[:4]:
        print(f"    {v:.3f}  {seeds[s]['ai_name'][:34]:36s} sheet={len(toks(seeds[s]['ai_setting'],lang)):4d} tok")
    print(f"  EASIEST to read (models converge):")
    for s, (v, n) in ranked[-4:]:
        print(f"    {v:.3f}  {seeds[s]['ai_name'][:34]:36s} sheet={len(toks(seeds[s]['ai_setting'],lang)):4d} tok")
