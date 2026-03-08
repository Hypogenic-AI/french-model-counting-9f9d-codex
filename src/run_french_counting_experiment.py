"""Run French counting representation probes on real OpenAI API models."""

from __future__ import annotations

import argparse
import json
import os
import random
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_exponential
from tqdm import tqdm

from french_numerals import (
    band_for_number,
    french_number,
    normalize_french_number_text,
    parse_int_from_text,
)


def set_seed(seed: int = 42) -> None:
    random.seed(seed)
    np.random.seed(seed)


@dataclass
class ProbeItem:
    task: str
    number: int | None
    source_text: str
    gold_text: str | None
    gold_number: int | None
    band: str


SYSTEM_PROMPT = (
    "You are a precise French numerals evaluator. "
    "Follow formatting instructions exactly and do not add extra text."
)


def build_digit_to_word_items() -> list[ProbeItem]:
    items: list[ProbeItem] = []
    for n in range(200):
        items.append(
            ProbeItem(
                task="digit_to_word",
                number=n,
                source_text=str(n),
                gold_text=french_number(n),
                gold_number=n,
                band=band_for_number(n),
            )
        )
    return items


def build_word_to_digit_items() -> list[ProbeItem]:
    items: list[ProbeItem] = []
    for n in range(200):
        w = french_number(n)
        items.append(
            ProbeItem(
                task="word_to_digit",
                number=n,
                source_text=w,
                gold_text=w,
                gold_number=n,
                band=band_for_number(n),
            )
        )
    return items


def expected_pattern(n: int) -> str:
    if 70 <= n <= 79:
        return "soixante_plus"
    if 80 <= n <= 99:
        return "quatre_vingt"
    return "decimal"


def build_pattern_items() -> list[ProbeItem]:
    items: list[ProbeItem] = []
    for n in range(200):
        items.append(
            ProbeItem(
                task="pattern_classification",
                number=n,
                source_text=str(n),
                gold_text=expected_pattern(n),
                gold_number=None,
                band=band_for_number(n),
            )
        )
    return items


def build_mgsm_items(limit: int) -> list[ProbeItem]:
    df = pd.read_csv("datasets/mgsm/mgsm_fr.tsv", sep="\t", header=None, names=["question", "answer"])
    if limit > 0:
        df = df.head(limit)
    items: list[ProbeItem] = []
    for _, row in df.iterrows():
        ans = int(row["answer"])
        items.append(
            ProbeItem(
                task="mgsm_fr",
                number=None,
                source_text=str(row["question"]),
                gold_text=None,
                gold_number=ans,
                band="mgsm",
            )
        )
    return items


def make_user_prompt(item: ProbeItem, condition: str) -> str:
    reasoned = condition == "reasoned"

    if item.task == "digit_to_word":
        if reasoned:
            return (
                f"Convert the integer to canonical metropolitan French words. Number: {item.source_text}. "
                "Think briefly, then output exactly one line as FINAL:<answer>."
            )
        return (
            f"Convert the integer to canonical metropolitan French words. Number: {item.source_text}. "
            "Output only the French numeral text."
        )

    if item.task == "word_to_digit":
        if reasoned:
            return (
                f"Convert this French numeral to digits: {item.source_text}. "
                "Think briefly, then output exactly one line as FINAL:<integer>."
            )
        return f"Convert this French numeral to digits: {item.source_text}. Output only the integer."

    if item.task == "pattern_classification":
        labels = "decimal, soixante_plus, quatre_vingt"
        if reasoned:
            return (
                f"For the number {item.source_text}, classify the French counting pattern using one label from [{labels}]. "
                "Think briefly, then output exactly one line as FINAL:<label>."
            )
        return (
            f"For the number {item.source_text}, classify the French counting pattern using one label from [{labels}]. "
            "Output only the label."
        )

    if item.task == "mgsm_fr":
        if reasoned:
            return (
                "Résous ce problème de maths en français. Donne uniquement la réponse numérique finale. "
                f"Problème: {item.source_text} "
                "Réponds au format FINAL:<nombre entier>."
            )
        return (
            "Résous ce problème de maths en français et donne uniquement la réponse numérique finale. "
            f"Problème: {item.source_text}"
        )

    raise ValueError(f"Unknown task: {item.task}")


def extract_answer_text(raw_text: str, condition: str) -> str:
    text = raw_text.strip()
    if condition == "reasoned":
        lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
        for ln in reversed(lines):
            if ln.lower().startswith("final:"):
                return ln.split(":", 1)[1].strip()
    return text.splitlines()[0].strip() if text else ""


@retry(wait=wait_exponential(multiplier=1, min=1, max=30), stop=stop_after_attempt(6))
def call_model(client: OpenAI, model: str, system_prompt: str, user_prompt: str) -> Any:
    return client.responses.create(
        model=model,
        temperature=0,
        max_output_tokens=180,
        input=[
            {"role": "system", "content": [{"type": "input_text", "text": system_prompt}]},
            {"role": "user", "content": [{"type": "input_text", "text": user_prompt}]},
        ],
    )


def score_prediction(item: ProbeItem, pred_text: str) -> tuple[int, str | None, int | None]:
    if item.task == "digit_to_word":
        pred_norm = normalize_french_number_text(pred_text)
        gold_norm = normalize_french_number_text(item.gold_text or "")
        return int(pred_norm == gold_norm), pred_norm, None

    if item.task in {"word_to_digit", "mgsm_fr"}:
        parsed = parse_int_from_text(pred_text)
        return int(parsed == item.gold_number), None, parsed

    if item.task == "pattern_classification":
        cleaned = pred_text.strip().lower().replace(" ", "_").replace("-", "_")
        return int(cleaned == (item.gold_text or "")), cleaned, None

    raise ValueError(item.task)


def run(args: argparse.Namespace) -> None:
    set_seed(args.seed)
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    probe_items: list[ProbeItem] = []
    probe_items.extend(build_digit_to_word_items())
    probe_items.extend(build_word_to_digit_items())
    probe_items.extend(build_pattern_items())
    probe_items.extend(build_mgsm_items(args.mgsm_limit))

    if args.limit > 0:
        probe_items = probe_items[: args.limit]

    combos = [(m.strip(), c.strip()) for m in args.models.split(",") for c in args.conditions.split(",")]

    stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    jsonl_path = out_dir / f"raw_outputs_{stamp}.jsonl"

    with jsonl_path.open("w", encoding="utf-8") as wf:
        for model, condition in combos:
            for item in tqdm(probe_items, desc=f"{model} | {condition}"):
                user_prompt = make_user_prompt(item, condition)
                started = time.time()
                error_msg = None
                raw_text = ""
                usage_in = None
                usage_out = None
                try:
                    resp = call_model(client, model, SYSTEM_PROMPT, user_prompt)
                    raw_text = resp.output_text or ""
                    if getattr(resp, "usage", None):
                        usage_in = getattr(resp.usage, "input_tokens", None)
                        usage_out = getattr(resp.usage, "output_tokens", None)
                except Exception as exc:  # noqa: BLE001
                    error_msg = str(exc)

                pred_text = extract_answer_text(raw_text, condition) if raw_text else ""
                is_correct, pred_norm, pred_num = score_prediction(item, pred_text) if not error_msg else (0, None, None)

                record = {
                    "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                    "model": model,
                    "condition": condition,
                    "task": item.task,
                    "number": item.number,
                    "band": item.band,
                    "source_text": item.source_text,
                    "gold_text": item.gold_text,
                    "gold_number": item.gold_number,
                    "raw_output": raw_text,
                    "pred_text": pred_text,
                    "pred_norm": pred_norm,
                    "pred_number": pred_num,
                    "correct": is_correct,
                    "latency_sec": round(time.time() - started, 3),
                    "usage_input_tokens": usage_in,
                    "usage_output_tokens": usage_out,
                    "error": error_msg,
                }
                wf.write(json.dumps(record, ensure_ascii=False) + "\n")

    df = pd.read_json(jsonl_path, lines=True)
    csv_path = out_dir / f"raw_outputs_{stamp}.csv"
    df.to_csv(csv_path, index=False)

    metadata = {
        "seed": args.seed,
        "models": [m.strip() for m in args.models.split(",")],
        "conditions": [c.strip() for c in args.conditions.split(",")],
        "mgsm_limit": args.mgsm_limit,
        "num_items_per_combo": len(probe_items),
        "total_calls_attempted": len(probe_items) * len(combos),
        "jsonl_path": str(jsonl_path),
        "csv_path": str(csv_path),
        "created_utc": datetime.now(timezone.utc).isoformat(),
    }
    (out_dir / f"run_metadata_{stamp}.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")

    print(f"Wrote: {jsonl_path}")
    print(f"Wrote: {csv_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--models", type=str, default="gpt-4.1,gpt-4.1-mini")
    parser.add_argument("--conditions", type=str, default="direct,reasoned")
    parser.add_argument("--mgsm-limit", type=int, default=80)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--output-dir", type=str, default="results/raw")
    run(parser.parse_args())
