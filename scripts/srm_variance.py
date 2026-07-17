"""Social Relations Model on the existing corpus -- zero new generations.

Kenny's SRM decomposes a round-robin into perceiver / target / relationship variance.
Our corpus IS a round-robin: 11 models x 95 characters x 3 runs, fully crossed, balanced.

  model    main effect      -> "some models are just better"        (the leaderboard's premise)
  character main effect     -> "some characters are just harder"
  model x character         -> CHEMISTRY. "this model suits this character"
  residual                  -> run-to-run noise (we have 3 runs, so this is IDENTIFIED
                               separately from the interaction -- most designs can't do this)

Why it matters: if the interaction term is large, "which model is best?" is the WRONG
QUESTION. The right one is "which model for which character?" Kenny predicts relationship
effects of 30-40% in human perception -- typically the largest single component.

Two-way random-effects ANOVA with replication, via expected mean squares.
Metric: repetition rate (our only fully validated, judge-free measure -- notes 09/10).
"""
import json, collections, statistics as st

def rep_rate(ai, lang):
    seen=set(); dup=0; tot=0
    for t in ai:
        if lang=='en':
            w=t.split(); g={tuple(w[i:i+5]) for i in range(max(0,len(w)-4))}
        else:
            g={t[i:i+8] for i in range(max(0,len(t)-7))}
        if g: dup+=len(g&seen); tot+=len(g); seen|=g
    return dup/tot if tot else 0.0

for lang in ('en','zh'):
    cell=collections.defaultdict(list)          # (model, seed) -> [values across runs]
    with open(f'data/{lang}/dialogues.jsonl') as f:
        for line in f:
            r=json.loads(line)
            ai=[t['text'] for t in json.loads(r['dialogue']) if t['role']=='ai']
            cell[(r['model_name'], r['seed_id'])].append(rep_rate(ai, lang))

    models=sorted({m for m,_ in cell}); seeds=sorted({s for _,s in cell})
    a, b = len(models), len(seeds)
    n = min(len(v) for v in cell.values())      # runs per cell (balanced = 3)
    if any(len(v) != n for v in cell.values()):
        cell = {k: v[:n] for k, v in cell.items()}

    allv=[x for v in cell.values() for x in v]
    grand=st.mean(allv)
    N=len(allv)

    mmean={m: st.mean(x for (mm,_),v in cell.items() if mm==m for x in v) for m in models}
    smean={s: st.mean(x for (_,ss),v in cell.items() if ss==s for x in v) for s in seeds}
    cmean={k: st.mean(v) for k,v in cell.items()}

    SS_A  = b*n*sum((mmean[m]-grand)**2 for m in models)
    SS_B  = a*n*sum((smean[s]-grand)**2 for s in seeds)
    SS_AB = n*sum((cmean[(m,s)]-mmean[m]-smean[s]+grand)**2 for m in models for s in seeds)
    SS_E  = sum((x-cmean[k])**2 for k,v in cell.items() for x in v)

    MS_A, MS_B = SS_A/(a-1), SS_B/(b-1)
    MS_AB, MS_E = SS_AB/((a-1)*(b-1)), SS_E/(a*b*(n-1))

    # EMS for a two-way random model
    v_e  = MS_E
    v_ab = max(0.0, (MS_AB - MS_E)/n)
    v_a  = max(0.0, (MS_A  - MS_AB)/(b*n))
    v_b  = max(0.0, (MS_B  - MS_AB)/(a*n))
    tot  = v_a+v_b+v_ab+v_e

    print(f"=== {lang.upper()} — SRM / variance decomposition ({a} models x {b} characters x {n} runs) ===")
    print(f"  {'component':34s} {'variance':>10s} {'% of total':>11s}")
    print(f"  {'model (some models are better)':34s} {v_a:10.5f} {100*v_a/tot:10.1f}%")
    print(f"  {'character (some are harder)':34s} {v_b:10.5f} {100*v_b/tot:10.1f}%")
    print(f"  {'model x character = CHEMISTRY':34s} {v_ab:10.5f} {100*v_ab/tot:10.1f}%")
    print(f"  {'residual (run-to-run noise)':34s} {v_e:10.5f} {100*v_e/tot:10.1f}%")
    print(f"  F(interaction) = MS_AB/MS_E = {MS_AB/MS_E:.2f}")
    print(f"  --> chemistry / model  = {v_ab/v_a if v_a else float('inf'):.2f}x")
    print(f"      Kenny predicts relationship effects 30-40% in human perception.\n")
