"""Utilities for canonical French numeral generation and normalization (0-999)."""

from __future__ import annotations

import re

UNITS = {
    0: "zero",
    1: "un",
    2: "deux",
    3: "trois",
    4: "quatre",
    5: "cinq",
    6: "six",
    7: "sept",
    8: "huit",
    9: "neuf",
    10: "dix",
    11: "onze",
    12: "douze",
    13: "treize",
    14: "quatorze",
    15: "quinze",
    16: "seize",
}

TENS = {
    20: "vingt",
    30: "trente",
    40: "quarante",
    50: "cinquante",
    60: "soixante",
}


def normalize_french_number_text(text: str) -> str:
    """Normalize common formatting variants for French numerals."""
    t = text.strip().lower()
    t = t.replace("œ", "oe")
    t = re.sub(r"\s+", " ", t)
    t = t.replace("−", "-")
    t = t.replace("–", "-")
    t = t.replace("—", "-")
    # Keep both spaced and hyphen variants comparable by collapsing spaces around hyphens.
    t = re.sub(r"\s*-\s*", "-", t)
    # Canonicalize spelling variants frequently emitted by models.
    t = t.replace("quatre vingt", "quatre-vingt")
    t = t.replace("soixante dix", "soixante-dix")
    t = t.replace("quatre vingt dix", "quatre-vingt-dix")
    return t


def french_0_99(n: int) -> str:
    if not 0 <= n <= 99:
        raise ValueError("n must be in [0, 99]")

    if n in UNITS:
        return UNITS[n]
    if 17 <= n <= 19:
        return f"dix-{UNITS[n - 10]}"
    if 20 <= n <= 69:
        tens = (n // 10) * 10
        unit = n % 10
        if unit == 0:
            return TENS[tens]
        if unit == 1:
            return f"{TENS[tens]} et un"
        return f"{TENS[tens]}-{UNITS[unit]}"
    if 70 <= n <= 79:
        base = 60
        rem = n - base
        if rem == 11:
            return "soixante et onze"
        return f"soixante-{french_0_99(rem)}"
    # 80-99
    if n == 80:
        return "quatre-vingts"
    rem = n - 80
    prefix = "quatre-vingt"
    if rem == 1:
        return f"{prefix}-un"
    return f"{prefix}-{french_0_99(rem)}"


def french_number(n: int) -> str:
    """Canonical French numeral for n in [0, 999]."""
    if not 0 <= n <= 999:
        raise ValueError("n must be in [0, 999]")
    if n < 100:
        return french_0_99(n)
    if n == 100:
        return "cent"

    hundreds = n // 100
    rem = n % 100

    if hundreds == 1:
        head = "cent"
    else:
        head = f"{UNITS[hundreds]} cent"

    if rem == 0:
        if hundreds > 1:
            return f"{head}s"
        return head
    return f"{head} {french_0_99(rem)}"


def parse_int_from_text(text: str) -> int | None:
    """Extract first integer from model output."""
    match = re.search(r"-?\d+", text)
    if not match:
        return None
    try:
        return int(match.group(0))
    except ValueError:
        return None


def band_for_number(n: int) -> str:
    if 0 <= n <= 69:
        return "0-69"
    if 70 <= n <= 99:
        return "70-99"
    return "100-199"
