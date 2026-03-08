"""Data quality profiling for French counting probes and MGSM-FR."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from french_numerals import band_for_number, french_number


def main() -> None:
    out_dir = Path("results")
    out_dir.mkdir(parents=True, exist_ok=True)

    mgsm = pd.read_csv("datasets/mgsm/mgsm_fr.tsv", sep="\t", header=None, names=["question", "answer"])
    mgsm["answer"] = pd.to_numeric(mgsm["answer"], errors="coerce")

    synth = pd.DataFrame({"number": list(range(200))})
    synth["french"] = synth["number"].apply(french_number)
    synth["band"] = synth["number"].apply(band_for_number)

    profile = {
        "mgsm_fr_rows": int(mgsm.shape[0]),
        "mgsm_missing_question_pct": float(mgsm["question"].isna().mean() * 100),
        "mgsm_missing_answer_pct": float(mgsm["answer"].isna().mean() * 100),
        "mgsm_duplicate_questions": int(mgsm["question"].duplicated().sum()),
        "mgsm_answer_min": float(mgsm["answer"].min()),
        "mgsm_answer_max": float(mgsm["answer"].max()),
        "synth_rows": int(synth.shape[0]),
        "synth_band_counts": synth["band"].value_counts().to_dict(),
        "synth_duplicate_forms": int(synth["french"].duplicated().sum()),
    }

    (out_dir / "data_profile.json").write_text(json.dumps(profile, indent=2, ensure_ascii=False), encoding="utf-8")

    samples = {
        "mgsm_examples": mgsm.head(3).to_dict(orient="records"),
        "synth_examples": synth.iloc[[0, 71, 95, 100, 199]].to_dict(orient="records"),
    }
    (out_dir / "data_samples.json").write_text(json.dumps(samples, indent=2, ensure_ascii=False), encoding="utf-8")

    print("Wrote results/data_profile.json and results/data_samples.json")


if __name__ == "__main__":
    main()
