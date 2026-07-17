---
title: "promptfoo — CI/CD Integration for LLM Eval and Security"
url: https://www.promptfoo.dev/docs/integrations/ci-cd/
org: promptfoo
year: 2026
type: product-docs
accessed: 2026-07-16
topic: eval-lifecycle
---

# promptfoo in CI — "evals as CI" in its most literal form

Also: https://www.promptfoo.dev/docs/integrations/github-action/ and
https://github.com/promptfoo/promptfoo-action

## The PR gate

`promptfoo/promptfoo-action@v1` — "evaluates prompts when they change in a pull request
and runs a **before-and-after comparison**." On every PR that modifies a prompt, the action
runs a full comparison and **posts results as a PR comment**.

> **"Before-and-after on the changed prompt" is the correct default and worth copying.**
> Not "does the new prompt pass an absolute bar" but "how did it move relative to the old
> one." That is *pairwise-against-the-incumbent* — structurally the same choice note 11 §1
> forces for the judge (pairwise 73–78% vs absolute r=0.159). The CI tool and the
> measurement design agree: **the comparison is the unit, not the score.**

## GitHub Actions

```yaml
name: LLM Eval
on:
  pull_request:
    paths:
      - 'prompts/**'
      - 'promptfooconfig.yaml'
jobs:
  evaluate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '22'
      - name: Run eval
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: |
          npx promptfoo@latest eval \
            -c promptfooconfig.yaml \
            --share \
            -o results.json
```

> **`on: pull_request: paths: ['prompts/**']`** — the prompt is a **versioned file in the
> repo that triggers CI when it changes.** This is the whole "evals as CI" thesis in three
> lines of YAML: *the system prompt is source code*. For us the system prompt is one of the
> three axes of a variant, so this is directly the dry-run trigger.

## Failing the build

Error-based: `npx promptfoo@latest eval --fail-on-error`

Threshold-based:
```bash
PASS_RATE=$(jq '.results.stats.successes /
  (.results.stats.successes + .results.stats.failures) * 100' results.json)
if (( $(echo "$PASS_RATE < 95" | bc -l) )); then
  echo "Quality gate failed"
  exit 1
fi
```

> ⚠️ **This is exactly the gate we must NOT build.** A raw pass-rate threshold with no
> interval is note 10's noise floor problem in shell script form: at n=3 runs a
> (model, character) cell resolves only 19.4pp, so a `< 95` cutoff on a small eval set
> fires on run-to-run noise. **A CI gate on a point estimate with no MDE is a coin flip
> with a changelog.** The mechanism (fail the build on a computed statistic) is right; the
> statistic must be a **shrunk estimate with an interval**, and the threshold must be
> derived from the dimension's declared σ_within (note 11's gate).

## Output formats

- JSON: `-o results.json`
- HTML: `-o report.html`
- **JUnit XML: `-o results.junit.xml`** ← lets any CI system render per-test results natively
- multiple simultaneous outputs supported
- results include a **`shareableUrl`** field for PR comments / Slack

## Caching

```bash
env:
  PROMPTFOO_CACHE_PATH: ~/.cache/promptfoo
cache:
  key: promptfoo-${{ hashFiles('prompts/**', 'promptfooconfig.yaml') }}
  paths:
    - ~/.cache/promptfoo
```

> **`hashFiles('prompts/**', 'promptfooconfig.yaml')` is content-addressing the eval,
> reinvented as a cache key.** Note 06 §7 argues the evaluator identity must be
> `H(rubric_bytes, judge_model, params, code_sha)`. promptfoo's cache key is
> `H(prompt_files, config)` — the same construction, used for a cheaper purpose. Since we
> need the hash for lineage anyway, **the lineage key and the cache key are the same key.**
> Building lineage correctly makes CI faster; they are not competing priorities.

## CI context tagging

```bash
npx promptfoo@latest eval \
  --tag ci.run-id="$CI_PIPELINE_ID" \
  --tag git.sha="$CI_COMMIT_SHA"
```

## Security notes

Store API keys as encrypted secrets; use private runners for sensitive data; enable
`PROMPTFOO_STRIP_RESPONSE_OUTPUT=true` to strip outputs.

> **`PROMPTFOO_STRIP_RESPONSE_OUTPUT`** matters for us: our production traffic is intimate
> companion conversation. A CI system that echoes model outputs into PR comments on a
> shared repo is a data-exposure path. **The dry-run/CI tier must run on
> synthetic/authored characters only — never on mined production conversation** — or the
> PR comment becomes an exfiltration channel. See the anonymization note in note 11
> (characters are user-authored).
