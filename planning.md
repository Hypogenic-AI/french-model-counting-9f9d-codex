# Research Plan: How does the model count in French?

## Motivation & Novelty Assessment

### Why This Research Matters
French numeral composition (especially 70-99) is linguistically systematic but cognitively atypical compared with base-10 forms. If LLMs fail disproportionately on these forms, multilingual safety, education, and translation systems can produce subtle but high-impact numeric errors. A precise map of these failures helps both prompt design and model evaluation.

### Gap in Existing Work
Prior numeracy work focuses on arithmetic and magnitude in general, and multilingual work (e.g., MGSM) reports aggregate French performance but does not isolate French-specific numeral morphology (e.g., `soixante-dix`, `quatre-vingt-dix`). Mechanistic papers identify arithmetic circuits broadly, but not language-specific counting idiosyncrasies.

### Our Novel Contribution
We introduce a targeted French numeral probe suite that isolates representation sub-skills: digit<->word transduction, decomposition/composition consistency, and robustness near irregular ranges. We also compare prompt conditions (direct vs reasoning) and multiple modern API models, then map error concentrations by number bands.

### Experiment Justification
- Experiment 1: Digit -> French numeral generation across 0-199. Why needed: directly tests productive mapping from abstract number to French lexical form.
- Experiment 2: French numeral -> digit parsing across 0-199. Why needed: tests inverse mapping and whether representation is bidirectionally coherent.
- Experiment 3: Decomposition/composition probes around 60-99. Why needed: isolates the irregular French structure (60+10, 4*20+x) to detect localized representational weakness.
- Experiment 4: Prompt ablation (direct answer vs structured reasoning). Why needed: determines whether errors are retrieval/formatting vs deeper representational failure.
- Experiment 5: Cross-model comparison (GPT-4.1 vs GPT-5-mini). Why needed: tests whether improvements come from scale/instruction-following rather than task design artifacts.

## Research Question
How accurately and consistently do state-of-the-art LLMs represent French counting forms, especially the irregular 70-99 range, and can this representation be mapped via controlled probes?

## Background and Motivation
French number words combine decimal and vigesimal-like constructions, creating transparent but nontrivial lexical mappings. Existing literature shows tokenization and numeracy are major contributors to model performance, but no focused benchmark quantifies French counting representation itself. This project fills that gap using controlled probes plus multilingual benchmark checks.

## Hypothesis Decomposition
1. H1 (core): Models achieve lower exact-match performance on irregular forms (70-99) than regular forms (0-69, 100-199) in digit->word generation.
2. H2 (inverse consistency): Word->digit accuracy exceeds digit->word accuracy, indicating stronger parsing than generation.
3. H3 (reasoning aid): Structured reasoning prompts reduce errors in irregular ranges.
4. H4 (model effect): Newer/stronger models show smaller irregular-range degradation.

Independent variables:
- Model (`gpt-4.1`, `gpt-5-mini` if available)
- Prompt condition (`direct`, `reasoned`)
- Task type (`digit_to_word`, `word_to_digit`, `decompose`, `compose`)
- Number band (`0-69`, `70-99`, `100-199`)

Dependent variables:
- Exact match accuracy
- Canonical-form accuracy (after normalization)
- Latency and token usage (secondary)
- Error category frequencies

Success criteria:
- Detect statistically significant band effect (irregular vs regular) with effect size.
- Produce reproducible error map and representative failure taxonomy.

Alternative explanations:
- Output formatting artifacts rather than conceptual errors.
- Canonicalization mismatch (hyphenation/`et` variants).
- Prompt language mismatch.

## Proposed Methodology

### Approach
Use API-based black-box probing with deterministic generation (`temperature=0`) and strict output formats to isolate representational behavior. Build a synthetic French numeral gold set for 0-199 plus targeted irregular probes. Run both forward and inverse tasks under controlled prompts and compare models/conditions.

### Experimental Steps
1. Build canonical French numeral generator and validator for 0-199 with normalization rules.
   Rationale: ensures objective scoring despite orthographic variants.
2. Construct probe datasets: full range 0-199 plus focused irregular stress set (60-99 with near-neighbors).
   Rationale: broad coverage plus targeted stress testing.
3. Implement robust API runner with retries, caching, logging, and fixed seeds.
   Rationale: reproducibility and cost control.
4. Run experiments for each model x prompt x task.
   Rationale: controlled factorial comparison.
5. Compute metrics and perform statistical tests.
   Rationale: quantify significance and effect size.
6. Generate plots and error analyses.
   Rationale: map representation structure visually.

### Baselines
- Baseline A: `direct` prompt, strict answer-only format.
- Baseline B: `reasoned` prompt requiring short decomposition then final answer.
- Baseline C: simple rule-based parser/generator (upper bound sanity check for evaluation pipeline, not an LLM baseline).

### Evaluation Metrics
- Exact Match (EM): strict string equality to canonical French form.
- Normalized EM: equality after normalization (hyphen variants, spacing).
- Numeric EM: exact integer match for parse tasks.
- Consistency score: agreement between forward and inverse predictions.
- Band gap: performance difference irregular band minus regular bands.

### Statistical Analysis Plan
Preregistered tests:
- Primary: two-proportion z-test for irregular vs regular accuracy per model/task.
- Secondary: logistic regression (`correct ~ band + model + prompt + interactions`).
- Effect size: risk difference and odds ratios with 95% CIs.
- Multiple comparisons: Benjamini-Hochberg FDR at q=0.05.
- Alpha: 0.05 (two-sided).

## Expected Outcomes
Evidence supporting hypothesis:
- Significant accuracy drop in 70-99 vs 0-69 and 100-199.
- Error categories concentrated in vigesimal-compositional forms.
- Reasoned prompting partially mitigates, but does not eliminate, the gap.

Evidence refuting hypothesis:
- No irregular-range degradation after normalization and strict formatting controls.
- Equivalent performance across bands and task directions.

## Timeline and Milestones
- M1 (30 min): finalize planning and environment checks.
- M2 (45 min): implement dataset generator, API harness, scoring.
- M3 (45 min): run core experiments and cache raw outputs.
- M4 (30 min): statistical analysis and visualizations.
- M5 (30 min): documentation (`REPORT.md`, `README.md`) and validation rerun.

## Potential Challenges
- API rate limits/timeouts: mitigate with retries, exponential backoff, and caching.
- Model availability mismatch (e.g., `gpt-5-mini` unavailable): fallback to `gpt-4.1-mini` and document.
- Orthographic ambiguity in French variants: use canonical + normalized scoring.
- Cost growth: cap sample size for pilot, then scale to full 0-199 once pipeline validated.

## Success Criteria
- Reproducible pipeline producing raw outputs, metrics JSON, and plots.
- At least one statistically supported conclusion about irregular French numeral representation.
- Complete documentation with limitations and concrete next-step experiments.
