"""Parallel-corpus loading and alignment filtering.

Ratios are only meaningful when both sides say the same thing, so every sample
is a sentence pair from OPUS-100 (``Helsinki-NLP/opus-100``): a human-translated
corpus covering ~100 languages paired against English.

OPUS-100 is crawled data and contains misalignments and untranslated rows, so
:func:`load_pairs` applies conservative filters before any counting happens.
The language table itself lives in :mod:`languages`.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterator

from .languages import BY_CODE, LANGUAGES, Language, resolve

__all__ = [
    "BY_CODE", "LANGUAGES", "Language", "Pair", "Sample", "load_pairs", "resolve",
]

# Filter thresholds. Deliberately loose: the goal is to drop junk, not to
# curate toward a flattering result.
MIN_CHARS_EN = 25
MAX_CHARS_EN = 400
MIN_CHARS_TARGET = 5
# Character-length ratio outside this band almost always means misalignment.
MIN_CHAR_RATIO = 0.2
MAX_CHAR_RATIO = 5.0

# Leftover markup from the crawl: HTML entities, tags, escapes, bare URLs.
# These matter because they are distributed *asymmetrically* — in the Khmer
# portion of OPUS-100 they appear in 39% of target sentences and 0% of the
# English ones. Markup only on the target side adds tokens to the numerator of
# every ratio and none to the denominator, inflating that language's tax.
MARKUP = re.compile(
    r"""
    &\s*\#\s*\d+\s*;      # numeric entity, sometimes space-separated by the crawl
    | &[a-zA-Z]{2,6};     # named entity
    # Named HTML tags only. Matching any <word> would also strike prose that
    # uses angle brackets for emphasis, which is common in translated text.
    | </?(?:br|hr|p|b|i|u|a|em|strong|div|span|img|li|ul|ol|
          td|tr|table|font|h[1-6])\b[^>]{0,40}>
    | https?://           # bare URL
    | \\[nt]              # literal escape sequence
    """,
    re.VERBOSE,
)


@dataclass(frozen=True)
class Pair:
    """One aligned sentence pair."""

    english: str
    target: str


@dataclass(frozen=True)
class Sample:
    """Pairs for one language, plus the split they actually came from.

    The split is carried through to the report because a fallback to ``train``
    means the text is not held out and, for low-resource pairs, noisier.
    """

    pairs: list[Pair]
    split: str


def config_name(code: str) -> str:
    """OPUS-100 names configs as an alphabetically sorted language pair."""
    return f"en-{code}" if "en" < code else f"{code}-en"


def load_pairs(code: str, limit: int, split: str = "test") -> Sample:
    """Return up to ``limit`` filtered sentence pairs for language ``code``.

    Some OPUS-100 pairs — mostly the lowest-resource ones — ship only a train
    split. Dropping those languages would bias the benchmark toward
    well-resourced ones, which is exactly the bias it exists to measure, so the
    requested split falls back to whatever the config does provide.

    Raises ``KeyError`` for unknown languages and ``RuntimeError`` if the
    dataset cannot be fetched at all.
    """
    if code not in BY_CODE:
        raise KeyError(f"unknown language code: {code!r}")
    try:
        from datasets import get_dataset_split_names, load_dataset
    except ImportError as exc:  # pragma: no cover - dependency is declared
        raise RuntimeError("the `datasets` package is required") from exc

    config = config_name(code)
    try:
        available = list(get_dataset_split_names("Helsinki-NLP/opus-100", config))
    except Exception as exc:
        raise RuntimeError(
            f"could not inspect opus-100/{config}: {type(exc).__name__}: {exc}"
        ) from exc

    chosen = split if split in available else _fallback_split(available, config)
    try:
        dataset = load_dataset("Helsinki-NLP/opus-100", config, split=chosen)
    except Exception as exc:
        raise RuntimeError(
            f"could not load opus-100/{config}: {type(exc).__name__}: {exc}"
        ) from exc

    return Sample(pairs=list(_take(_clean(dataset, code), limit)), split=chosen)


def _fallback_split(available: list[str], config: str) -> str:
    """Prefer held-out splits; fall back to train only when nothing else exists."""
    for candidate in ("test", "validation", "train"):
        if candidate in available:
            return candidate
    raise RuntimeError(f"opus-100/{config} exposes no usable split")


def _clean(dataset, code: str) -> Iterator[Pair]:
    """Yield pairs that survive alignment and length filters, deduped."""
    seen: set[str] = set()
    for row in dataset:
        translation = row.get("translation") or {}
        english = (translation.get("en") or "").strip()
        target = (translation.get(code) or "").strip()
        if not english or not target:
            continue
        if not is_usable(english, target):
            continue
        if english in seen:
            continue
        seen.add(english)
        yield Pair(english=english, target=target)


def is_usable(english: str, target: str) -> bool:
    """Alignment heuristics, factored out so they are directly testable."""
    if not (MIN_CHARS_EN <= len(english) <= MAX_CHARS_EN):
        return False
    if len(target) < MIN_CHARS_TARGET:
        return False
    # Identical strings mean the row was never actually translated.
    if english == target:
        return False
    # Drop the pair whichever side the markup is on. Dropping only the
    # asymmetric cases would be closer to the actual bias, but "no markup
    # anywhere" is a rule a reader can check by eye.
    if MARKUP.search(english) or MARKUP.search(target):
        return False
    ratio = len(target) / len(english)
    return MIN_CHAR_RATIO <= ratio <= MAX_CHAR_RATIO


def _take(iterator: Iterator[Pair], limit: int) -> Iterator[Pair]:
    for index, item in enumerate(iterator):
        if index >= limit:
            return
        yield item
