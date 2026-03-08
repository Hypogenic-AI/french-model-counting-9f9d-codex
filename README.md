# French Model Counting Study

This project probes how modern LLMs represent French numeral structure, with emphasis on the irregular `70-99` forms.

## Key Findings
- French numeral transduction is near-perfect for completed runs (`digit_to_word` and `word_to_digit`).
- No significant irregular-band drop (`70-99`) in transduction under deterministic prompting.
- Pattern-classification probes show strong band effects (FDR-significant), indicating probe design strongly shapes conclusions.
- On MGSM-FR (gpt-4.1), reasoning prompt improved accuracy from `48.8%` to `57.5%`.

## Reproduce
1. Activate environment:
```bash
source .venv/bin/activate
```
2. Run data checks:
```bash
PYTHONPATH=src python src/data_profile.py
```
3. Run experiments:
```bash
PYTHONPATH=src python src/run_french_counting_experiment.py --models gpt-4.1,gpt-4.1-mini --conditions direct,reasoned --mgsm-limit 80 --output-dir results/raw
```
4. Analyze results:
```bash
PYTHONPATH=src python src/analyze_results.py --input-csv results/raw/raw_outputs_20260308_214204_partial.csv --out-dir results
```

## File Structure
- `planning.md`: phase-1 plan and preregistered stats plan
- `src/`: experiment code
- `results/`: metrics, tables, plots, and data profile outputs
- `REPORT.md`: full research report

See [REPORT.md](/workspaces/french-model-counting-9f9d-codex/REPORT.md) for full methods, statistics, and limitations.
