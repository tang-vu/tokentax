"""Selection and ordering rules shared by every rendered view.

Kept separate from rendering because these decisions are substantive: which
measurements count as trustworthy, and what order tells the clearest story.
"""

from __future__ import annotations

from .benchmark import BenchmarkRun, Measurement


def reliable(measurements: list[Measurement]) -> list[Measurement]:
    """Drop cells where the tokenizer could not represent the text.

    A lossy encoding produces a token count for something that is no longer the
    original text, so including it would silently reward information loss. If
    every cell is lossy there is nothing better to fall back to, so the inputs
    are returned unchanged rather than dropping the language entirely.
    """
    kept = [m for m in measurements if not m.lossy]
    return kept or measurements


def deployable(measurements: list[Measurement]) -> list[Measurement]:
    """Reliable cells, minus historical baselines nobody ships today.

    Used for "which tokenizer should I pick" tables. A 2019 tokenizer is the
    worst choice for every language, so leaving it in would make the ranking
    technically true and practically useless.
    """
    candidates = reliable(measurements)
    kept = [m for m in candidates if not m.legacy]
    return kept or candidates


def ordered_tokenizers(run: BenchmarkRun) -> list[tuple[str, str]]:
    """Registry order, restricted to tokenizers that produced data.

    Registry order runs oldest to newest, so columns read as a timeline.
    """
    from .tokenizer_registry import REGISTRY

    present = {m.tokenizer for m in run.measurements}
    labels = {m.tokenizer: m.tokenizer_label for m in run.measurements}
    return [(s.key, labels[s.key]) for s in REGISTRY if s.key in present]


def ordered_languages(run: BenchmarkRun) -> list[tuple[str, str]]:
    """Languages sorted by mean tax on currently deployed tokenizers, worst first."""
    names = {m.language: m.language_name for m in run.measurements}
    ranked = sorted(
        names,
        key=lambda code: -mean(m.tax for m in deployable(run.for_language(code))),
    )
    return [(code, names[code]) for code in ranked]


def mean(values) -> float:
    collected = list(values)
    return sum(collected) / len(collected) if collected else 0.0
