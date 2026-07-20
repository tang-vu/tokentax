"""Core measurement: how many tokens does language X cost versus English?

The headline metric is the **aggregate token tax**: total target-language
tokens divided by total English tokens over the same aligned sentences. Cost
and context consumption are both proportional to totals, so the aggregate is
what actually shows up on a bill.

A per-sentence median is reported alongside it as a robustness check; a large
gap between the two means a handful of long sentences dominate the aggregate.
"""

from __future__ import annotations

import statistics
from datetime import datetime, timezone
from typing import Callable

from . import corpus, tokenizer_registry
from .corpus import Language, Pair
from .results import BenchmarkRun, Measurement
from .tokenizer_registry import TokenizerLoadError, TokenizerSpec

ProgressFn = Callable[[str], None]

# Above this share of unknown tokens the text is being destroyed rather than
# encoded, and the resulting ratio says nothing about cost.
LOSSY_UNKNOWN_RATE = 0.01


def measure(
    spec: TokenizerSpec,
    language: Language,
    pairs: list[Pair],
    encode: tokenizer_registry.EncodeFn,
    split: str = "test",
) -> Measurement:
    """Measure one tokenizer against one language's sentence pairs."""
    if not pairs:
        raise ValueError(f"no pairs supplied for {language.code}")

    english_counts: list[int] = []
    target_counts: list[int] = []
    ratios: list[float] = []
    target_chars = 0
    unknown_tokens = 0

    for pair in pairs:
        english = encode(pair.english)
        target = encode(pair.target)
        if english.tokens == 0:
            continue  # cannot form a ratio; excluded from every statistic
        english_counts.append(english.tokens)
        target_counts.append(target.tokens)
        ratios.append(target.tokens / english.tokens)
        target_chars += len(pair.target)
        unknown_tokens += target.unknown

    if not ratios:
        raise ValueError(f"{spec.key}/{language.code}: no usable pairs after encoding")

    total_english = sum(english_counts)
    total_target = sum(target_counts)
    ordered = sorted(ratios)
    unknown_rate = unknown_tokens / total_target if total_target else 0.0

    return Measurement(
        tokenizer=spec.key,
        tokenizer_label=spec.label,
        language=language.code,
        language_name=language.name,
        pairs=len(ratios),
        english_tokens=total_english,
        target_tokens=total_target,
        tax=round(total_target / total_english, 4),
        median_ratio=round(statistics.median(ordered), 4),
        p90_ratio=round(percentile(ordered, 0.90), 4),
        target_tokens_per_char=round(total_target / target_chars, 4)
        if target_chars
        else 0.0,
        unknown_rate=round(unknown_rate, 5),
        lossy=unknown_rate > LOSSY_UNKNOWN_RATE,
        legacy=spec.legacy,
        split=split,
    )


def percentile(ordered: list[float], fraction: float) -> float:
    """Nearest-rank percentile over an already-sorted list."""
    if not ordered:
        raise ValueError("percentile of empty sequence")
    index = max(0, min(len(ordered) - 1, round(fraction * len(ordered)) - 1))
    return ordered[index]


def run(
    specs: list[TokenizerSpec],
    languages: list[Language],
    samples: int,
    split: str = "test",
    progress: ProgressFn | None = None,
) -> BenchmarkRun:
    """Sweep every (tokenizer, language) cell, tolerating individual failures.

    Corpora are loaded once per language and tokenizers once per run, so the
    cost is one download per language plus one per tokenizer.
    """
    say = progress or (lambda _msg: None)
    result = BenchmarkRun(
        samples_requested=samples,
        corpus_split=split,
        generated_at=datetime.now(timezone.utc).isoformat(timespec="seconds"),
    )

    encoders: dict[str, tokenizer_registry.EncodeFn] = {}
    for spec in specs:
        say(f"loading tokenizer {spec.label}")
        try:
            encoders[spec.key] = tokenizer_registry.load(spec)
        except TokenizerLoadError as exc:
            result.skipped[spec.key] = str(exc)
            say(f"  skipped: {exc}")

    for language in languages:
        say(f"loading corpus {language.name} ({language.code})")
        try:
            sample = corpus.load_pairs(language.code, samples, split=split)
        except (RuntimeError, KeyError) as exc:
            result.skipped[f"corpus:{language.code}"] = str(exc)
            say(f"  skipped: {exc}")
            continue
        pairs = sample.pairs
        if not pairs:
            result.skipped[f"corpus:{language.code}"] = "no pairs survived filtering"
            continue
        if sample.split != split:
            say(f"  note: {language.name} has no '{split}' split, using "
                f"'{sample.split}'")

        measured = 0
        for spec in specs:
            encode = encoders.get(spec.key)
            if encode is None:
                continue
            if not tokenizer_registry.supports(spec, language.code):
                continue  # monolingual tokenizer, different language
            try:
                result.measurements.append(
                    measure(spec, language, pairs, encode, split=sample.split)
                )
                measured += 1
            except ValueError as exc:
                result.skipped[f"{spec.key}:{language.code}"] = str(exc)

        say(f"  {language.name}: {len(pairs)} pairs x {measured} tokenizers")

    return result
