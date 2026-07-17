---
title: "CUSUM, SPRT and EWMA control charts — formulas and parameter choices"
url: https://en.wikipedia.org/wiki/CUSUM
org: Wikipedia / Analyse-it / SPC for Excel / NIST-derived SPC literature
year: 2025
type: docs
accessed: 2026-07-16
topic: production-scale
---

# Sequential / control-chart methods

## CUSUM

Two-sided cumulative sum, detecting upward and downward shifts:

```
S_i^+ = max(0, S_{i-1}^+ + (x_i - mu_0 - k))
S_i^- = max(0, S_{i-1}^- - (x_i - mu_0 + k))
```

Alarm when `S_i^+ > h` or `S_i^- > h`.

### Parameter k (allowance / reference value)
- `k` is often set as **sigma/2**
- `k` is set to **half the shift to be detected**, in sigma units
- Default **k = 0.5** — corresponds to detecting a shift of **1 sigma**

### Parameter h (decision interval / threshold)
- `h` commonly set to **4 x sigma**
- Default **h = 5** (in sigma units)

The canonical **(k=0.5, h=5)** design gives an in-control ARL (average run length)
of roughly **465** and detects a 1-sigma shift in about **10** observations.

### Relationship to SPRT
"When the test is one-sided to detect change in one direction only, the CUSUM can be
considered as ... a sequence of SPRT tests with initial score zero, and absorbing
barriers at zero and h, with a new SPRT started each time the barrier at zero is
crossed." CUSUM is literally a repeated SPRT.

### Design tradeoff
"The sensitivity of CUSUM is adjustable by modifying the allowance k and the threshold
h, involving a trade-off between false detection (type I errors) and detection delays
or failures (type II errors)."

---

## EWMA control chart

Statistic: `z_i = lambda * x_i + (1 - lambda) * z_{i-1}`, with `z_0 = mu_0`.

### Control limits (exact, time-varying)

```
mu_0 +/- L * sigma * sqrt( (lambda / (2 - lambda)) * [1 - (1-lambda)^(2i)] )
```

### Control limits (steady state, as i -> large)

```
UCL = mu_0 + L * sigma * sqrt( lambda / (2 - lambda) )
LCL = mu_0 - L * sigma * sqrt( lambda / (2 - lambda) )
```

### Parameters
- **mu_0** — process mean (from reference period)
- **sigma** — process standard deviation
- **lambda** — smoothing constant, typically **0.05 to 0.30**
- **L** — control limit multiplier, usually **3** (3-sigma limits)
- **i** — sample number

### Choosing lambda
- A common choice is **lambda = 0.2**
- Values in the interval **0.05 <= lambda <= 0.25** work well; **0.05, 0.10, 0.20**
  are the popular choices
- Larger lambda (**0.2–0.3**): more responsive to shifts, more susceptible to false
  alarms from process noise
- Smaller lambda (**0.05–0.1**): smooths out noise, less sensitive to real changes

### Choosing L
- **L = 3** (usual 3-sigma limits) works reasonably well
- When lambda is small (**lambda <= 0.1**), there is an advantage in **reducing** the
  width of the limits by using **L between 2.6 and 2.8**

## Why these fit a 50M/day eval platform

CUSUM and EWMA operate on a *stream of aggregate statistics* (e.g. hourly mean judge
score, hourly refusal rate) rather than on raw per-generation samples. This decouples
sensitivity from the raw event volume — you tune ARL directly, in units of "how many
hours until a false alarm," which is the operationally meaningful quantity. Unlike KS,
their false-alarm rate does not degrade as daily volume grows.
