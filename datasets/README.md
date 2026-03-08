# Downloaded Datasets

This directory contains datasets for multilingual and French-relevant numerical reasoning experiments. Data files are not intended for git commits; see `datasets/.gitignore`.

## Dataset 1: GSM8K (`openai/gsm8k`, config `main`)

### Overview
- Source: https://huggingface.co/datasets/openai/gsm8k
- Size: train 7,473 / test 1,319
- Format: HuggingFace DatasetDict (Arrow)
- Task: Grade-school math word-problem reasoning
- Splits: train, test
- License: See dataset card

### Download Instructions

Using HuggingFace:
```python
from datasets import load_dataset

# Download
dataset = load_dataset("openai/gsm8k", "main")
# Save local copy
dataset.save_to_disk("datasets/gsm8k_main")
```

### Loading
```python
from datasets import load_from_disk
dataset = load_from_disk("datasets/gsm8k_main")
```

### Sample Data
Saved at: `datasets/gsm8k_main/samples/examples.json`

### Notes
- English-only but standard baseline for arithmetic reasoning.

## Dataset 2: MGSM (official Google Research benchmark files)

### Overview
- Source: https://github.com/google-research/url-nlp/tree/main/mgsm
- Size: 250 translated problems per language x 11 files (including English)
- Format: TSV files (`mgsm_<lang>.tsv`)
- Task: Multilingual grade-school math reasoning
- Splits: benchmark-style files (no train split; commonly used as test/eval)
- Languages: en, fr, de, es, ru, zh, ja, th, sw, bn, te
- License: See upstream repository

### Download Instructions
```bash
mkdir -p datasets/mgsm
for lg in bn de en es fr ja ru sw te th zh; do
  curl -L "https://raw.githubusercontent.com/google-research/url-nlp/main/mgsm/mgsm_${lg}.tsv" \
    -o "datasets/mgsm/mgsm_${lg}.tsv"
done
```

### Loading
```python
import pandas as pd
fr = pd.read_csv("datasets/mgsm/mgsm_fr.tsv", sep="\t")
```

### Sample Data
Saved at: `datasets/mgsm/samples/examples.json`

### Notes
- This is the most directly relevant benchmark for French counting/reasoning.

## Dataset 3: SVAMP (`ChilleD/SVAMP`)

### Overview
- Source: https://huggingface.co/datasets/ChilleD/SVAMP
- Size: train 700 / test 300
- Format: HuggingFace DatasetDict (Arrow)
- Task: Math word-problem reasoning
- Splits: train, test
- License: See dataset card

### Download Instructions
```python
from datasets import load_dataset
dataset = load_dataset("ChilleD/SVAMP")
dataset.save_to_disk("datasets/svamp")
```

### Loading
```python
from datasets import load_from_disk
dataset = load_from_disk("datasets/svamp")
```

### Sample Data
Saved at: `datasets/svamp/samples/examples.json`

### Notes
- Useful for cross-dataset transfer/generalization checks.
