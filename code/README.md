# Cloned Repositories

## Repo 1: url-nlp (MGSM benchmark)
- URL: https://github.com/google-research/url-nlp
- Purpose: Official MGSM multilingual math benchmark files and exemplars
- Location: `code/url-nlp/`
- Key files:
  - `code/url-nlp/mgsm/README.md`
  - `code/url-nlp/mgsm/mgsm_fr.tsv`
  - `code/url-nlp/mgsm/exemplars.py`
- Notes: Direct source for benchmark French problems and multilingual counterparts.

## Repo 2: MathOctopus
- URL: https://github.com/microsoft/MathOctopus
- Purpose: Multilingual math-reasoning training/evaluation resources; model checkpoints and data links
- Location: `code/MathOctopus/`
- Key files:
  - `code/MathOctopus/README.md`
  - training/inference scripts referenced from README
- Notes: Reports multilingual performance including French; uses MGSM-like tasks and released datasets.

## Repo 3: arithmetic-mechanism
- URL: https://github.com/zepingyu0512/arithmetic-mechanism
- Purpose: Mechanistic interpretability for arithmetic behavior in LLMs
- Location: `code/arithmetic-mechanism/`
- Key files:
  - `code/arithmetic-mechanism/README.md`
  - `code/arithmetic-mechanism/Llama_view_arithmetic_head.ipynb`
  - `code/arithmetic-mechanism/Llama_view_arithmetic_CNA.ipynb`
- Notes: Useful for analyzing where arithmetic/counting behavior is represented internally.

## Repo 4: lm-evaluation-harness
- URL: https://github.com/EleutherAI/lm-evaluation-harness
- Purpose: Standardized evaluation framework for LLM tasks/benchmarks
- Location: `code/lm-evaluation-harness/`
- Key files:
  - `code/lm-evaluation-harness/docs/interface.md`
  - `code/lm-evaluation-harness/lm_eval/tasks/`
- Notes: Recommended for reproducible evaluation across baselines and prompt settings.
