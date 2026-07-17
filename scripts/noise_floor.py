"""Empirical noise floor from the 3 independent runs per (model, character) cell.

Answers: how large must a model-vs-model delta be before we may call it real?
Judge-free. Uses the repetition metric as the worked example.
"""
import json, collections, statistics as st, sys

def rep_rate(ai, lang):
    seen = set(); dup = 0; tot = 0
    for t in ai:
        if lang == 'en':
            w = t.split()
            g = {tuple(w[i:i+5]) for i in range(max(0, len(w) - 4))}
        else:
            g = {t[i:i+8] for i in range(max(0, len(t) - 7))}
        if g:
            dup += len(g & seen); tot += len(g); seen |= g
    return dup / tot if tot else 0.0

for lang in ('en', 'zh'):
    cells = collections.defaultdict(dict)
    with open(f'data/{lang}/dialogues.jsonl') as f:
        for line in f:
            r = json.loads(line)
            ai = [t['text'] for t in json.loads(r['dialogue']) if t['role'] == 'ai']
            cells[(r['model_name'], r['seed_id'])][r['run_id']] = rep_rate(ai, lang)

    # sigma_within: run-to-run noise, same model AND same character. Irreducible.
    within = [st.variance(list(v.values())) for v in cells.values() if len(v) >= 2]
    sigma_w = st.mean(within) ** .5

    per_model = collections.defaultdict(list)   # model -> [per-character mean]
    for (m, s), v in cells.items():
        per_model[m].append(st.mean(v.values()))
    means = {m: st.mean(vs) for m, vs in per_model.items()}

    sigma_between = st.stdev(means.values())
    char_sd = st.mean([st.stdev(vs) for vs in per_model.values()])
    n_seeds = len({s for _, s in cells})

    se = char_sd / (n_seeds ** .5)
    mde = 2.8 * se * (2 ** .5)          # ~80% power, alpha=.05, two-sample
    obs = max(means.values()) - min(means.values())

    print(f"=== {lang.upper()} — repetition metric, variance decomposition ===")
    print(f"  sigma_within  (run-to-run, same model+char) : {sigma_w:.4f}")
    print(f"  sd across CHARACTERS within a model         : {char_sd:.4f}  = {char_sd/sigma_w:5.1f}x run noise")
    print(f"  sd across MODELS (of model means)           : {sigma_between:.4f}  = {sigma_between/sigma_w:5.1f}x run noise")
    print(f"  SE of model mean over {n_seeds} chars x 3 runs   : {se:.4f}")
    print(f"  --> min detectable delta (80% power)        : {mde:.4f}  ({100*mde:.2f} pp)")
    print(f"  observed max model gap                      : {obs:.4f}  ({100*obs:.1f} pp) = {obs/mde:.0f}x MDE")
    # how many characters needed to detect a 1pp regression?
    for target in (0.01, 0.005, 0.002):
        need = (2.8 * (2 ** .5) * char_sd / target) ** 2
        print(f"      characters needed to detect a {100*target:.1f}pp regression: {need:.0f}")
    print()
