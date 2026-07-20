"""Command-line entry point for tokentax."""

from __future__ import annotations

import argparse
from pathlib import Path

from . import commands, corpus, tokenizer_registry


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
        "--source",
        default="opus-100",
        choices=sorted(corpus.SOURCES),
        help="which parallel corpus to measure on (default: opus-100)",
    )
    bench.add_argument(
        "--split", default=None, help="corpus split (default: the source's own)"
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

    inspect = sub.add_parser(
        "check", help="count tokens for your own text across every tokenizer"
    )
    inspect.add_argument("text", nargs="?", help="text to measure")
    inspect.add_argument(
        "--file", type=Path, help="read the text from a file instead"
    )
    inspect.add_argument(
        "--tokenizers",
        default="all",
        help="comma-separated keys, or 'all' (default: all)",
    )

    render = sub.add_parser(
        "render",
        help="re-render the Markdown and HTML reports from an existing "
        "results JSON, without repeating the measurement pass",
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
        default=Path("results"),
        help="output directory (default: results)",
    )

    cross = sub.add_parser(
        "cross-check",
        help="compare two runs measured on different corpora, to see which "
        "conclusions survive a change of dataset",
    )
    cross.add_argument("baseline", type=Path, help="first results JSON")
    cross.add_argument("other", type=Path, help="second results JSON")
    cross.add_argument(
        "--out",
        type=Path,
        default=Path("docs/cross-check-against-wmt24pp.md"),
        help="where to write the comparison",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    handler = {
        "list": lambda _a: commands.cmd_list(),
        "bench": commands.cmd_bench,
        "check": commands.cmd_check,
        "render": commands.cmd_render,
        "cross-check": commands.cmd_cross_check,
    }[args.command]
    return handler(args)


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
