# Resources Catalog

## Summary
This document catalogs all resources gathered for the project "How does the model count in French?" including papers, datasets, and code repositories.

### Papers
Total papers downloaded: 8

| Title | Authors | Year | File | Key Info |
|---|---|---:|---|---|
| Do NLP Models Know Numbers? | Wallace et al. | 2019 | papers/wallace_2019_do_nlp_models_know_numbers.pdf | Foundational numeracy probing |
| Injecting Numerical Reasoning Skills into LMs | Geva et al. | 2020 | papers/geva_2020_injecting_numerical_reasoning_skills.pdf | Synthetic skill injection |
| NumGPT | Jin et al. | 2021 | papers/yang_2021_numgpt.pdf | Numeral-aware GPT |
| Language Models Are Multilingual CoT Reasoners | Shi et al. | 2022 | papers/shi_2022_multilingual_cot_reasoners_mgsm.pdf | MGSM benchmark |
| Breaking Language Barriers in xMR | Chen et al. | 2023/24 | papers/chen_2023_breaking_language_barriers_xmr.pdf | MathOctopus multilingual training |
| Tokenization in French Medical MLMs | Labrak et al. | 2024 | papers/denoyelle_2024_tokenization_french_medical_mlm.pdf | French tokenization evidence |
| Interpreting Arithmetic Mechanism in LLMs | Yu & Ananiadou | 2024 | papers/xu_2024_interpreting_arithmetic_mechanism_llm.pdf | Arithmetic heads/neurons |
| Unraveling Arithmetic: Algebraic Structures | Chang et al. | 2024/25 | papers/lu_2024_unraveling_arithmetic_algebraic_structures.pdf | Structural arithmetic view |

See `papers/README.md` for descriptions.

### Datasets
Total datasets downloaded: 3

| Name | Source | Size | Task | Location | Notes |
|---|---|---|---|---|---|
| GSM8K main | HF `openai/gsm8k` | 7,473 train / 1,319 test | Math reasoning | datasets/gsm8k_main/ | Standard benchmark |
| MGSM TSV bundle | Google Research url-nlp | 250 rows x 11 language files | Multilingual math reasoning | datasets/mgsm/ | Includes French (`mgsm_fr.tsv`) |
| SVAMP | HF `ChilleD/SVAMP` | 700 train / 300 test | Math reasoning robustness | datasets/svamp/ | Transfer/generalization |

See `datasets/README.md` for download and loading instructions.

### Code Repositories
Total repositories cloned: 4

| Name | URL | Purpose | Location | Notes |
|---|---|---|---|---|
| url-nlp | https://github.com/google-research/url-nlp | Official MGSM resources | code/url-nlp/ | Benchmark files + exemplars |
| MathOctopus | https://github.com/microsoft/MathOctopus | Multilingual math model resources | code/MathOctopus/ | Includes French performance reporting |
| arithmetic-mechanism | https://github.com/zepingyu0512/arithmetic-mechanism | Mechanistic arithmetic analysis | code/arithmetic-mechanism/ | CNA notebooks |
| lm-evaluation-harness | https://github.com/EleutherAI/lm-evaluation-harness | Standardized LLM evaluation | code/lm-evaluation-harness/ | Reproducible benchmark runner |

See `code/README.md` for details.

## Resource Gathering Notes

### Search Strategy
- Attempted paper-finder first (required), then manual curation from ACL/arXiv due sparse direct hits.
- Focused on three themes: numeracy mechanisms, multilingual/French math reasoning, and arithmetic interpretability.

### Selection Criteria
- Direct relevance to counting/numeracy.
- Presence of French or multilingual evaluation including French.
- Availability of code/dataset for reproducible experiments.

### Challenges Encountered
- Semantic Scholar API rate limiting during automated retrieval.
- HF package changes prevented direct loading of some script-based datasets (MGSM); resolved using official raw TSV files.

### Gaps and Workarounds
- No large established dataset dedicated specifically to French counting idiosyncrasies.
- Workaround: combine MGSM French with targeted synthetic probes for French numeral composition.

## Recommendations for Experiment Design

1. **Primary dataset(s)**: MGSM French (`datasets/mgsm/mgsm_fr.tsv`) + GSM8K for pre-calibration.
2. **Baseline methods**: direct prompting, French CoT, English-intermediate CoT, multilingual-instruction tuned baselines (MathOctopus-style).
3. **Evaluation metrics**: exact-match accuracy, per-pattern error rates for French forms (`soixante-dix`, `quatre-vingt-dix`).
4. **Code to adapt/reuse**: `lm-evaluation-harness` for evaluation scaffolding, `url-nlp` data format, `arithmetic-mechanism` for interpretation probes.
