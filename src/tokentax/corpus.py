"""Sentence-pair loading and alignment filtering.

Ratios are only meaningful when both sides say the same thing, so every sample
is an aligned pair from a parallel corpus. Readers live in
:mod:`corpus_sources`; the filtering below is applied identically to all of
them, so figures from different corpora stay comparable.

The language table lives in :mod:`languages`.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterator

from .corpus_sources import SOURCES, languages_for
from .languages import BY_CODE, LANGUAGES, Language, resolve

__all__ = [
    "BY_CODE", "LANGUAGES", "Language", "Pair", "Sample", "SOURCES",
    "load_pairs", "resolve", "supports",
]

# Filter thresholds. Deliberately loose: the goal is to drop junk, not to
# curate toward a flattering result.
MIN_CHARS_EN = 25
MAX_CHARS_EN = 400
MIN_CHARS_TARGET = 5
# Character-length ratio outside this band almost always means misalignment.
MIN_CHAR_RATIO = 0.2
MAX_CHAR_RATIO = 5.0

# Leftover markup from a crawl: HTML entities, tags, escapes, bare URLs.
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
    """Pairs for one language, plus where they came from.

    The split is carried through to the report because a fallback to ``train``
    means the text is not held out and, for low-resource pairs, noisier.
    """

    pairs: list[Pair]
    split: str
    source: str = "opus-100"


def supports(source: str, code: str) -> bool:
    """Whether ``source`` can serve language ``code``."""
    served = languages_for(source)
    return served is None or code in served


def load_pairs(
    code: str,
    limit: int,
    split: str | None = None,
    source: str = "opus-100",
) -> Sample:
    """Return up to ``limit`` filtered sentence pairs for language ``code``.

    Some corpora — mostly for the lowest-resource pairs — ship only a train
    split. Dropping those languages would bias the benchmark toward
    well-resourced ones, which is exactly the bias it exists to measure, so the
    requested split falls back to whatever the corpus does provide.

    Raises ``KeyError`` for unknown languages or sources, and ``RuntimeError``
    if the data cannot be fetched.
    """
    if code not in BY_CODE:
        raise KeyError(f"unknown language code: {code!r}")
    if source not in SOURCES:
        raise KeyError(f"unknown corpus source: {source!r}")

    spec = SOURCES[source]
    wanted = split or spec["default_split"]

    try:
        available = spec["splits"](code)
    except KeyError:
        raise
    except Exception as exc:
        raise RuntimeError(
            f"could not inspect {source}/{code}: {type(exc).__name__}: {exc}"
        ) from exc

    chosen = wanted if wanted in available else _fallback_split(available, code)
    try:
        rows = spec["rows"](code, chosen)
        pairs = list(_take(_clean(rows), limit))
    except Exception as exc:
        raise RuntimeError(
            f"could not load {source}/{code}: {type(exc).__name__}: {exc}"
        ) from exc

    return Sample(pairs=pairs, split=chosen, source=source)


def _fallback_split(available: list[str], code: str) -> str:
    """Prefer held-out splits; fall back to train only when nothing else exists."""
    for candidate in ("test", "validation", "train"):
        if candidate in available:
            return candidate
    raise RuntimeError(f"no usable split for {code}")


def _clean(rows) -> Iterator[Pair]:
    """Yield pairs that survive alignment and length filters, deduped."""
    seen: set[str] = set()
    for english, target in rows:
        english, target = english.strip(), target.strip()
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
