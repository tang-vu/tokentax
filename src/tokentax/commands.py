"""Implementations of the CLI subcommands.

Split from :mod:`cli`, which owns argument definitions and dispatch, so each
file stays about one thing: what the commands accept, and what they do.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import check, corpus, cross_check, report, report_html, tokenizer_registry
from .benchmark import run as run_benchmark
from .results import BenchmarkRun


def cmd_list() -> int:
    print("Tokenizers:")
    for spec in tokenizer_registry.REGISTRY:
        flag = "  [gated]" if spec.gated else ""
        print(f"  {spec.key:<14} {spec.label:<28} {spec.vocab_note}{flag}")
    print(f"\nLanguages ({len(corpus.LANGUAGES)}):")
    for language in corpus.LANGUAGES:
        print(
            f"  {language.code:<4} {language.name:<12} "
            f"{language.script:<12} {language.region}"
        )
    regions = sorted({language.region for language in corpus.LANGUAGES})
    print(f"\nRegions usable with --languages: {', '.join(regions)}")
    return 0


def cmd_bench(args: argparse.Namespace) -> int:
    try:
        specs = tokenizer_registry.resolve(_split(args.tokenizers))
        languages = corpus.resolve(_split(args.languages))
    except KeyError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if args.samples < 1:
        print("error: --samples must be >= 1", file=sys.stderr)
        return 2

    progress = None if args.quiet else lambda msg: print(msg, file=sys.stderr)
    result = run_benchmark(
        specs,
        languages,
        args.samples,
        split=args.split,
        source=args.source,
        progress=progress,
    )

    if not result.measurements:
        print("error: no measurements produced", file=sys.stderr)
        for key, reason in result.skipped.items():
            print(f"  {key}: {reason}", file=sys.stderr)
        return 1

    print()
    print(report.summarize(result))
    print()
    _write_reports(result, args.out)
    return 0


def cmd_check(args: argparse.Namespace) -> int:
    try:
        text = check.resolve_text(args.text, args.file)
        specs = tokenizer_registry.resolve(_split(args.tokenizers))
    except (check.InputError, KeyError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    counts, failures = check.count_all(text, specs)
    if not counts:
        print("error: no tokenizers could be loaded", file=sys.stderr)
        return 1
    print(check.format_report(text, counts, failures))
    return 0


def cmd_cross_check(args: argparse.Namespace) -> int:
    runs = []
    for path in (args.baseline, args.other):
        if not path.exists():
            print(f"error: {path} not found", file=sys.stderr)
            return 2
        runs.append(
            BenchmarkRun.from_dict(json.loads(path.read_text(encoding="utf-8")))
        )
    rows = cross_check.compare(*runs)
    if not rows:
        print("error: the two runs share no languages", file=sys.stderr)
        return 1
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(cross_check.to_markdown(*runs, rows), encoding="utf-8")
    agree = sum(1 for r in rows if r.cheapest_agrees)
    print(f"{len(rows)} shared languages; cheapest tokenizer agrees on {agree}")
    print(f"wrote {args.out}")
    return 0


def cmd_render(args: argparse.Namespace) -> int:
    if not args.input.exists():
        print(f"error: {args.input} not found — run `tokentax bench` first",
              file=sys.stderr)
        return 2
    run = BenchmarkRun.from_dict(json.loads(args.input.read_text(encoding="utf-8")))
    if not run.measurements:
        print(f"error: {args.input} contains no measurements", file=sys.stderr)
        return 1
    _write_reports(run, args.out)
    return 0


def _write_reports(run: BenchmarkRun, out: Path) -> None:
    """Every output format is written from one run, so they never disagree."""
    out.mkdir(parents=True, exist_ok=True)
    report.to_json(run, out / "token-tax.json")
    (out / "token-tax.md").write_text(report.to_markdown(run), encoding="utf-8")
    report_html.write(run, out / "index.html")
    print(f"wrote {out / 'token-tax.md'}, {out / 'token-tax.json'}, "
          f"{out / 'index.html'}")


def _split(value: str) -> list[str]:
    return [part.strip() for part in value.split(",") if part.strip()]
