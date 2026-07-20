"""Self-contained interactive HTML report.

The page is a heatmap whose cells also carry their own value, so colour is
never the only channel: it doubles as its own table. A plain-table toggle drops
the colour entirely for the WCAG-clean twin.
"""

from __future__ import annotations

import html
from pathlib import Path

from .results import BenchmarkRun, Measurement
from .html_assets import CSS, JS
from .languages import BY_CODE
from .ranking import (
    deployable,
    monolingual,
    ordered_languages,
    ordered_tokenizers,
)

# Upper bound of each bin, paired with its ramp slot. Seven bins keeps adjacent
# classes distinguishable; past that they blur together.
BINS: tuple[tuple[float, int], ...] = (
    (1.00, 1),
    (1.50, 2),
    (2.00, 3),
    (3.00, 4),
    (4.50, 5),
    (7.00, 6),
    (float("inf"), 7),
)


def to_html(run: BenchmarkRun, title: str = "Token Tax") -> str:
    tokenizers = ordered_tokenizers(run, general_only=True)
    languages = ordered_languages(run)
    lookup = {(m.tokenizer, m.language): m for m in run.measurements}

    parts = [
        "<!doctype html><html lang='en'><head><meta charset='utf-8'>",
        "<meta name='viewport' content='width=device-width,initial-scale=1'>",
        f"<title>{html.escape(title)}</title><style>{CSS}</style></head><body>",
        "<div class='wrap'>",
        f"<h1>{html.escape(title)}</h1>",
        "<p class='sub'>How many tokens a language costs relative to the "
        "<strong>same sentence in English</strong>. 1.00x is parity; 2.00x means "
        "every request spends twice as many tokens on identical content.</p>",
        _tiles(run, languages),
        _controls(languages),
        _table(run, tokenizers, languages, lookup),
        _legend(),
        _monolingual_note(run),
        _split_note(run),
        _notes(run),
        "</div><div id='tip' role='tooltip'></div>",
        f"<script>{JS}</script></body></html>",
    ]
    return "\n".join(parts)


def write(run: BenchmarkRun, path: Path, title: str = "Token Tax") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(to_html(run, title), encoding="utf-8")


def slot_for(tax: float) -> int:
    for upper, slot in BINS:
        if tax < upper:
            return slot
    return BINS[-1][1]


def _tiles(run: BenchmarkRun, languages: list[tuple[str, str]]) -> str:
    """Three headline numbers: the worst language, the widest gap, the scale."""
    worst_lang, worst_tax = "", 0.0
    widest_lang, widest_gap = "", 0.0
    for code, name in languages:
        cells = deployable(run.for_language(code))
        if not cells:
            continue
        best = min(c.tax for c in cells)
        worst = max(c.tax for c in cells)
        if worst > worst_tax:
            worst_lang, worst_tax = name, worst
        if best and worst / best > widest_gap:
            widest_lang, widest_gap = name, worst / best
    tiles = [
        (f"{worst_tax:.1f}x", f"worst tax measured ({worst_lang})"),
        (f"{widest_gap:.1f}x", f"widest spread between tokenizers ({widest_lang})"),
        (str(len(languages)), "languages measured"),
    ]
    body = "".join(
        f"<div class='tile'><div class='n'>{html.escape(n)}</div>"
        f"<div class='k'>{html.escape(k)}</div></div>"
        for n, k in tiles
    )
    return f"<div class='tiles'>{body}</div>"


def _controls(languages: list[tuple[str, str]]) -> str:
    regions = []
    for code, _ in languages:
        region = BY_CODE[code].region
        if region not in regions:
            regions.append(region)
    buttons = ["<span class='label'>Region</span>",
               "<button data-region='all' aria-pressed='true'>All</button>"]
    buttons += [
        f"<button data-region='{html.escape(r)}' aria-pressed='false'>"
        f"{html.escape(r)}</button>"
        for r in sorted(regions)
    ]
    buttons.append(
        "<button id='plain' aria-pressed='false' style='margin-left:auto'>"
        "Show table view</button>"
    )
    return f"<div class='controls'>{''.join(buttons)}</div>"


def _table(run, tokenizers, languages, lookup) -> str:
    head = "".join(f"<th scope='col'>{html.escape(l)}</th>" for _, l in tokenizers)
    rows = []
    for code, name in languages:
        language = BY_CODE[code]
        cells = "".join(
            _cell(lookup.get((key, code)), name, label)
            for key, label in tokenizers
        )
        rows.append(
            f"<tr data-region='{html.escape(language.region)}'>"
            f"<th scope='row'>{html.escape(name)}"
            f"<span class='scr'> · {html.escape(language.script)}</span></th>"
            f"{cells}</tr>"
        )
    return (
        "<div class='scroll'><table><thead><tr>"
        f"<th class='corner' scope='col'>Language</th>{head}</tr></thead>"
        f"<tbody>{''.join(rows)}</tbody></table></div>"
    )


def _cell(measurement: Measurement | None, language: str, tokenizer: str) -> str:
    if measurement is None:
        return "<td class='na' title='not measured for this language'>—</td>"
    slot = slot_for(measurement.tax)
    tip = (
        f"<b>{html.escape(language)} · {html.escape(tokenizer)}</b>"
        f"<div class='row'>tax {measurement.tax:.2f}x aggregate</div>"
        f"<div class='row'>median {measurement.median_ratio:.2f}x · "
        f"p90 {measurement.p90_ratio:.2f}x</div>"
        f"<div class='row'>{measurement.pairs} sentence pairs</div>"
    )
    classes = "cell lossy" if measurement.lossy else "cell"
    if measurement.lossy:
        tip += (
            f"<div class='row'>⚠ {measurement.unknown_rate:.1%} unknown tokens — "
            "this text is being degraded, not just encoded</div>"
        )
    return (
        f"<td class='{classes}' "
        f"style='background:var(--s{slot});color:var(--i{slot})' "
        f"data-tip=\"{html.escape(tip, quote=True)}\">{measurement.tax:.2f}</td>"
    )


def _legend() -> str:
    # Bin edges as ranges, not bare numbers: a lone "1.5" beside a swatch reads
    # as "this colour means 1.5x" rather than "up to 1.5x".
    labels = [
        "under 1.0x", "1.0–1.5x", "1.5–2.0x", "2.0–3.0x",
        "3.0–4.5x", "4.5–7.0x", "7.0x and up",
    ]
    swatches = "".join(
        f"<span class='sw' style='background:var(--s{i + 1})'></span>"
        f"<span>{html.escape(l)}</span>"
        for i, l in enumerate(labels)
    )
    return f"<div class='legend'><span>Tokens vs English</span>{swatches}</div>"


def _monolingual_note(run: BenchmarkRun) -> str:
    """One line per single-language tokenizer, instead of a mostly-empty column."""
    entries = sorted(monolingual(run), key=lambda m: m.tax)
    if not entries:
        return ""
    items = ", ".join(
        f"<strong>{html.escape(m.tokenizer_label)}</strong> on "
        f"{html.escape(m.language_name)} {m.tax:.2f}x"
        for m in entries
    )
    return (
        f"<p class='note'>Monolingual baselines (not usable with a general "
        f"model, but they show the floor): {items}.</p>"
    )


def _split_note(run: BenchmarkRun) -> str:
    fallbacks = sorted(
        {
            (m.language_name, m.split)
            for m in run.measurements
            if m.split != run.corpus_split
        }
    )
    if not fallbacks:
        return ""
    listed = ", ".join(
        f"{html.escape(name)} ({html.escape(split)})" for name, split in fallbacks
    )
    return (
        f"<p class='note'>No <code>{html.escape(run.corpus_split)}</code> split "
        f"exists in OPUS-100 for {listed}, so those rows use another split: not "
        "held out, and likely noisier.</p>"
    )


def _notes(run: BenchmarkRun) -> str:
    return (
        "<p class='note'>Outlined cells emitted unknown tokens above 1%: the "
        "tokenizer cannot represent that script, so its count describes degraded "
        "text and is excluded from the headline figures. Dashes mark tokenizers "
        "that do not target a language. Hover or focus any cell for detail.</p>"
        f"<p class='meta'>Corpus {html.escape(run.corpus_name)} "
        f"(split {html.escape(run.corpus_split)}), up to "
        f"{run.samples_requested} aligned sentence pairs per language. "
        f"Generated {html.escape(run.generated_at)}.</p>"
    )
