"""Command-line entry point for tokentax."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import corpus, report, report_html, tokenizer_registry
from .benchmark import BenchmarkRun
from .benchmark import run as run_benchmark


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="tokentax",
        description="Measure how many extra tokens a language costs versus English.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    bench = sub.add_parser("bench", help="run the benchmark")
    bench.add_argument(
        "--languages",
        default="all",
        help="comma-separated ISO 639-1 codes, region names, or 'all' "
        "(default: all)",
    )
    bench.add_argument(
        "--tokenizers",
        default="all",
        help="comma-separated keys, 'all', or 'all+gated' (default: all)",
    )
    bench.add_argument(
        "--samples",
        type=int,
        default=500,
        help="sentence pairs per language (default: 500)",
    )
    bench.add_argument(
        "--split", default="test", help="corpus split (default: test)"
    )
    bench.add_argument(
        "--out",
        type=Path,
        default=Path("results"),
        help="output directory (default: results)",
    )
    bench.add_argument(
        "--quiet", action="store_true", help="suppress progress output"
    )

    sub.add_parser("list", help="list available tokenizers and languages")

    render = sub.add_parser(
        "html", help="re-render the HTML report from an existing results JSON"
    )
    render.add_argument(
        "--input",
        type=Path,
        default=Path("results/token-tax.json"),
        help="results JSON (default: results/token-tax.json)",
    )
    render.add_argument(
        "--out",
        type=Path,
        default=Path("results/index.html"),
        help="output HTML path (default: results/index.html)",
    )
    return parser


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
        specs, languages, args.samples, split=args.split, progress=progress
    )

    if not result.measurements:
        print("error: no measurements produced", file=sys.stderr)
        for key, reason in result.skipped.items():
            print(f"  {key}: {reason}", file=sys.stderr)
        return 1

    out = args.out
    report.to_json(result, out / "token-tax.json")
    markdown_path = out / "token-tax.md"
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.write_text(report.to_markdown(result), encoding="utf-8")
    report_html.write(result, out / "index.html")

    print()
    print(report.summarize(result))
    print()
    print(f"wrote {markdown_path}, {out / 'token-tax.json'}, {out / 'index.html'}")
    return 0


def cmd_html(args: argparse.Namespace) -> int:
    if not args.input.exists():
        print(f"error: {args.input} not found — run `tokentax bench` first",
              file=sys.stderr)
        return 2
    run = BenchmarkRun.from_dict(json.loads(args.input.read_text(encoding="utf-8")))
    if not run.measurements:
        print(f"error: {args.input} contains no measurements", file=sys.stderr)
        return 1
    report_html.write(run, args.out)
    print(f"wrote {args.out}")
    return 0


def _split(value: str) -> list[str]:
    return [part.strip() for part in value.split(",") if part.strip()]


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "list":
        return cmd_list()
    if args.command == "bench":
        return cmd_bench(args)
    if args.command == "html":
        return cmd_html(args)
    return 2  # pragma: no cover - argparse enforces the choices


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
