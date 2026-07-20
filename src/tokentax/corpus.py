"""Parallel-corpus loading for token-tax measurement.

Ratios are only meaningful when both sides say the same thing, so every sample
is a sentence pair from OPUS-100 (``Helsinki-NLP/opus-100``): a human-translated
corpus covering ~100 languages paired against English.

OPUS-100 is crawled data and contains misalignments and untranslated rows, so
:func:`load_pairs` applies conservative filters before any counting happens.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterator


@dataclass(frozen=True)
class Language:
    """A language available for benchmarking."""

    code: str  # ISO 639-1, as used by OPUS-100
    name: str
    script: str


LANGUAGES: tuple[Language, ...] = (
    Language("vi", "Vietnamese", "Latin"),
    Language("th", "Thai", "Thai"),
    Language("zh", "Chinese", "Han"),
    Language("ja", "Japanese", "Kana/Han"),
    Language("ko", "Korean", "Hangul"),
    Language("hi", "Hindi", "Devanagari"),
    Language("ta", "Tamil", "Tamil"),
    Language("ar", "Arabic", "Arabic"),
    Language("fa", "Persian", "Arabic"),
    Language("ru", "Russian", "Cyrillic"),
    Language("tr", "Turkish", "Latin"),
    Language("id", "Indonesian", "Latin"),
    Language("de", "German", "Latin"),
    Language("fr", "French", "Latin"),
    Language("es", "Spanish", "Latin"),
)

BY_CODE: dict[str, Language] = {lang.code: lang for lang in LANGUAGES}

# Filter thresholds. Deliberately loose: the goal is to drop junk, not to
# curate toward a flattering result.
MIN_CHARS_EN = 25
MAX_CHARS_EN = 400
MIN_CHARS_TARGET = 5
# Character-length ratio outside this band almost always means misalignment.
MIN_CHAR_RATIO = 0.2
MAX_CHAR_RATIO = 5.0


@dataclass(frozen=True)
class Pair:
    """One aligned sentence pair."""

    english: str
    target: str


def config_name(code: str) -> str:
    """OPUS-100 names configs as an alphabetically sorted language pair."""
    return f"en-{code}" if "en" < code else f"{code}-en"


def load_pairs(code: str, limit: int, split: str = "test") -> list[Pair]:
    """Return up to ``limit`` filtered sentence pairs for language ``code``.

    Raises ``KeyError`` for unknown languages and ``RuntimeError`` if the
    dataset cannot be fetched.
    """
    if code not in BY_CODE:
        raise KeyError(f"unknown language code: {code!r}")
    try:
        from datasets import load_dataset
    except ImportError as exc:  # pragma: no cover - dependency is declared
        raise RuntimeError("the `datasets` package is required") from exc

    try:
        dataset = load_dataset(
            "Helsinki-NLP/opus-100", config_name(code), split=split
        )
    except Exception as exc:
        raise RuntimeError(
            f"could not load opus-100/{config_name(code)}: {type(exc).__name__}: {exc}"
        ) from exc

    return list(_take(_clean(dataset, code), limit))


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
    ratio = len(target) / len(english)
    return MIN_CHAR_RATIO <= ratio <= MAX_CHAR_RATIO


def _take(iterator: Iterator[Pair], limit: int) -> Iterator[Pair]:
    for index, item in enumerate(iterator):
        if index >= limit:
            return
        yield item


def resolve(codes: list[str] | None) -> list[Language]:
    """Map CLI codes to languages. ``None`` or ``["all"]`` selects everything."""
    if codes is None or codes == ["all"]:
        return list(LANGUAGES)
    unknown = [c for c in codes if c not in BY_CODE]
    if unknown:
        raise KeyError(f"unknown language codes: {', '.join(unknown)}")
    return [BY_CODE[c] for c in codes]
