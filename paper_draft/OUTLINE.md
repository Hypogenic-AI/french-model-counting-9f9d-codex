# Outline: How Do Large Language Models Count in French?

## Abstract
- Problem: French irregular numerals (70--99) may induce model failures
- Approach: deterministic black-box probes over 0--199 + MGSM-FR
- Results: near-ceiling transduction, strong classification band effect, MGSM prompt gains
- Significance: probe design strongly affects difficulty conclusions

## Introduction
- Motivation and practical stakes
- Gap: no French-specific numeral probe with full coverage and significance mapping
- Contributions list (pipeline, findings, statistics, implications)

## Related Work
- Numeracy probes and skill injection
- Multilingual math reasoning (MGSM)
- Tokenization effects in French
- Mechanistic arithmetic studies

## Methodology
- Tasks, models, prompt conditions
- Datasets and preprocessing
- Metrics and significance tests
- Implementation/reproducibility details

## Results
- Aggregate and task-level accuracy
- Band-wise tables
- Significance summary + logistic regression
- MGSM prompt ablation and error analysis

## Discussion
- Interpretation and probe-design sensitivity
- Limitations and scope
- Broader implications

## Conclusion
- Main findings
- Key takeaway
- Future work
