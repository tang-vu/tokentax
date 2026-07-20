"""Tokenize one piece of text across every tokenizer.

The benchmark answers "what does this language cost in general". This answers
"what does *my* prompt cost", which is the question someone actually has after
reading the results.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .tokenizer_registry import (
    EncodeFn,
    TokenizerLoadError,
    TokenizerSpec,
    load,
)


@dataclass(frozen=True)
class Count:
    """One tokenizer's verdict on a piece of text."""

    key: str
    label: str
    tokens: int
    unknown: int

    @property
    def lossy(self) -> bool:
        """Any unknown token means characters were dropped, not just encoded."""
        return self.unknown > 0


class InputError(ValueError):
    """The caller supplied no usable text."""


def resolve_text(text: str | None, file: Path | None) -> str:
    """Take the text from an argument or a file, rejecting ambiguous input."""
    if text and file:
        raise InputError("pass either text or --file, not both")
    if file:
        if not file.exists():
            raise InputError(f"{file} not found")
        text = file.read_text(encoding="utf-8")
    if not text:
        raise InputError("pass some text, or --file")
    if not text.strip():
        raise InputError("the text is empty")
    return text


def count_all(
    text: str, specs: list[TokenizerSpec]
) -> tuple[list[Count], dict[str, str]]:
    """Return counts sorted cheapest first, plus any load failures."""
    counts: list[Count] = []
    failures: dict[str, str] = {}
    for spec in specs:
        try:
            encode: EncodeFn = load(spec)
        except TokenizerLoadError as exc:
            failures[spec.key] = str(exc)
            continue
        encoding = encode(text)
        counts.append(
            Count(
                key=spec.key,
                label=spec.label,
                tokens=encoding.tokens,
                unknown=encoding.unknown,
            )
        )
    counts.sort(key=lambda c: c.tokens)
    return counts, failures


def format_report(text: str, counts: list[Count], failures: dict[str, str]) -> str:
    """Human-readable table, cheapest first, with cost relative to the best."""
    if not counts:
        return "no tokenizers could be loaded"

    lines = [
        f"{len(text):,} characters, {len(text.split()):,} whitespace-separated words",
        "",
    ]
    # Ratios are against the cheapest *usable* result: a tokenizer that dropped
    # characters would otherwise set a baseline nothing else can honestly match.
    usable = [c for c in counts if not c.lossy] or counts
    baseline = min(c.tokens for c in usable) or 1
    width = max(len(c.label) for c in counts)

    for count in counts:
        ratio = count.tokens / baseline
        flag = f"  ⚠ {count.unknown} unknown" if count.lossy else ""
        lines.append(
            f"  {count.label:<{width}}  {count.tokens:>6,} tokens"
            f"   {ratio:>5.2f}x{flag}"
        )

    cheapest = min(usable, key=lambda c: c.tokens)
    dearest = max(usable, key=lambda c: c.tokens)
    if cheapest.tokens != dearest.tokens:
        lines += [
            "",
            f"{dearest.label} costs {dearest.tokens / cheapest.tokens:.1f}x more "
            f"than {cheapest.label} for this text.",
        ]

    if failures:
        lines += ["", "Could not load:"]
        lines += [f"  {key}: {reason}" for key, reason in sorted(failures.items())]

    return "\n".join(lines)
