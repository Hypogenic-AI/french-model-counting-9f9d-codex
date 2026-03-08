"""Analyze French counting probe results with statistical tests and plots."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats
from statsmodels.formula.api import logit
from statsmodels.stats.multitest import multipletests
from statsmodels.stats.proportion import proportions_ztest, proportion_confint

sns.set_theme(style="whitegrid")


def latest_csv(raw_dir: Path) -> Path:
    files = sorted(raw_dir.glob("raw_outputs_*.csv"))
    if not files:
        raise FileNotFoundError(f"No raw output CSV found in {raw_dir}")
    return files[-1]


def compute_summary(df: pd.DataFrame) -> pd.DataFrame:
    g = (
        df.groupby(["model", "condition", "task", "band"], dropna=False)["correct"]
        .agg(["mean", "std", "count", "sum"])
        .reset_index()
    )
    g = g.rename(columns={"mean": "accuracy", "std": "accuracy_std", "sum": "num_correct", "count": "n"})
    return g


def run_band_tests(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    subset = df[df["task"].isin(["digit_to_word", "word_to_digit", "pattern_classification"])].copy()

    for (model, condition, task), g in subset.groupby(["model", "condition", "task"]):
        ir = g[g["band"] == "70-99"]["correct"]
        rg = g[g["band"].isin(["0-69", "100-199"])]["correct"]
        if len(ir) == 0 or len(rg) == 0:
            continue

        count = [int(ir.sum()), int(rg.sum())]
        nobs = [int(len(ir)), int(len(rg))]
        stat, pval = proportions_ztest(count, nobs)

        ir_acc = count[0] / nobs[0]
        rg_acc = count[1] / nobs[1]
        diff = ir_acc - rg_acc
        ir_ci = proportion_confint(count[0], nobs[0], alpha=0.05, method="wilson")
        rg_ci = proportion_confint(count[1], nobs[1], alpha=0.05, method="wilson")

        rows.append(
            {
                "model": model,
                "condition": condition,
                "task": task,
                "irregular_acc": ir_acc,
                "regular_acc": rg_acc,
                "risk_difference": diff,
                "z_stat": float(stat),
                "p_value": float(pval),
                "irregular_ci_low": float(ir_ci[0]),
                "irregular_ci_high": float(ir_ci[1]),
                "regular_ci_low": float(rg_ci[0]),
                "regular_ci_high": float(rg_ci[1]),
            }
        )

    out = pd.DataFrame(rows)
    if not out.empty:
        out["p_value_fdr"] = np.nan
        out["significant_fdr_0_05"] = False
        valid = out["p_value"].notna()
        if valid.any():
            reject, p_adj, _, _ = multipletests(out.loc[valid, "p_value"].to_numpy(), method="fdr_bh", alpha=0.05)
            out.loc[valid, "p_value_fdr"] = p_adj
            out.loc[valid, "significant_fdr_0_05"] = reject
    return out


def fit_logistic(df: pd.DataFrame) -> dict:
    mdf = df[df["task"].isin(["digit_to_word", "word_to_digit", "pattern_classification"])].copy()
    mdf = mdf[mdf["error"].isna()].copy()

    # Binary indicator for the irregular band.
    mdf["irregular"] = (mdf["band"] == "70-99").astype(int)

    full_formula = "correct ~ irregular + C(model) + C(condition) + C(task) + irregular:C(model) + irregular:C(condition)"
    fallback_formula = "correct ~ irregular + C(model) + C(condition) + C(task)"
    chosen_formula = full_formula
    try:
        try:
            result = logit(full_formula, data=mdf).fit(disp=False)
        except Exception:
            try:
                chosen_formula = fallback_formula
                result = logit(fallback_formula, data=mdf).fit(disp=False)
            except Exception:
                chosen_formula = fallback_formula + " [regularized]"
                result = logit(fallback_formula, data=mdf).fit_regularized(disp=False)
    except Exception as exc:  # noqa: BLE001
        return {
            "n": int(mdf.shape[0]),
            "formula": chosen_formula,
            "error": str(exc),
        }

    params = result.params.to_dict()
    conf = result.conf_int().rename(columns={0: "low", 1: "high"}).to_dict(orient="index")
    pvals = result.pvalues.to_dict()

    return {
        "n": int(mdf.shape[0]),
        "formula": chosen_formula,
        "params": params,
        "conf_int": conf,
        "p_values": pvals,
        "pseudo_r2": float(result.prsquared),
        "aic": float(result.aic),
    }


def effect_size_cohens_h(p1: float, p2: float) -> float:
    return 2 * (np.arcsin(p1**0.5) - np.arcsin(p2**0.5))


def create_plots(df: pd.DataFrame, summary: pd.DataFrame, out_dir: Path) -> list[str]:
    paths: list[str] = []

    plt.figure(figsize=(12, 6))
    p = summary[summary["task"].isin(["digit_to_word", "word_to_digit", "pattern_classification"])].copy()
    sns.barplot(data=p, x="band", y="accuracy", hue="model", errorbar=None)
    plt.title("Accuracy by Number Band")
    plt.xlabel("Number band")
    plt.ylabel("Accuracy")
    plt.ylim(0, 1.0)
    plt.tight_layout()
    p1 = out_dir / "accuracy_by_band.png"
    plt.savefig(p1, dpi=200)
    plt.close()
    paths.append(str(p1))

    plt.figure(figsize=(12, 6))
    q = summary[summary["task"].isin(["digit_to_word", "word_to_digit"])].copy()
    sns.barplot(data=q, x="task", y="accuracy", hue="condition", errorbar=None)
    plt.title("Prompt Condition Effect on Core Tasks")
    plt.xlabel("Task")
    plt.ylabel("Accuracy")
    plt.ylim(0, 1.0)
    plt.tight_layout()
    p2 = out_dir / "condition_effect_core_tasks.png"
    plt.savefig(p2, dpi=200)
    plt.close()
    paths.append(str(p2))

    # Error concentration around irregular zone for generation task.
    d = df[(df["task"] == "digit_to_word") & (df["error"].isna()) & (df["number"].notna())].copy()
    if not d.empty:
        d["number"] = d["number"].astype(int)
        per_num = d.groupby(["model", "condition", "number"]) ["correct"].mean().reset_index()

        plt.figure(figsize=(14, 5))
        sns.lineplot(data=per_num, x="number", y="correct", hue="model", style="condition")
        plt.axvspan(70, 99, color="red", alpha=0.12, label="Irregular zone 70-99")
        plt.title("Per-Number Accuracy for Digit -> French Word")
        plt.xlabel("Number")
        plt.ylabel("Accuracy")
        plt.ylim(-0.02, 1.02)
        plt.tight_layout()
        p3 = out_dir / "per_number_accuracy_digit_to_word.png"
        plt.savefig(p3, dpi=200)
        plt.close()
        paths.append(str(p3))

    return paths


def main(args: argparse.Namespace) -> None:
    raw_dir = Path(args.raw_dir)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    csv_path = Path(args.input_csv) if args.input_csv else latest_csv(raw_dir)
    df = pd.read_csv(csv_path)

    summary = compute_summary(df)
    tests = run_band_tests(df)
    logistic = fit_logistic(df)

    # Compute Cohen's h for each band test row.
    if not tests.empty:
        tests["cohens_h"] = tests.apply(
            lambda r: effect_size_cohens_h(float(r["irregular_acc"]), float(r["regular_acc"])), axis=1
        )

    plot_paths = create_plots(df, summary, out_dir)

    summary_path = out_dir / "summary_metrics.csv"
    tests_path = out_dir / "band_significance_tests.csv"
    summary.to_csv(summary_path, index=False)
    tests.to_csv(tests_path, index=False)

    metrics = {
        "input_csv": str(csv_path),
        "summary_csv": str(summary_path),
        "tests_csv": str(tests_path),
        "plots": plot_paths,
        "logistic_regression": logistic,
        "overall_accuracy": float(df["correct"].mean()),
        "total_rows": int(df.shape[0]),
        "rows_with_errors": int(df["error"].notna().sum()),
    }
    metrics_path = out_dir / "metrics.json"
    metrics_path.write_text(json.dumps(metrics, indent=2), encoding="utf-8")

    print(f"Analyzed: {csv_path}")
    print(f"Wrote: {metrics_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw-dir", type=str, default="results/raw")
    parser.add_argument("--input-csv", type=str, default="")
    parser.add_argument("--out-dir", type=str, default="results")
    main(parser.parse_args())
