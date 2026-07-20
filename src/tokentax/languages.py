"""The language table, grouped by region.

Codes are ISO 639-1 as used by OPUS-100. Coverage is skewed deliberately
toward languages that tokenizers are most likely to handle badly — non-Latin
scripts and languages with little presence in web-scraped training data — since
that is where the token tax is largest and least documented.

Script names matter for reading results: languages sharing a script tend to
share a fate under a given tokenizer.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Language:
    """A language available for benchmarking."""

    code: str  # ISO 639-1, as used by OPUS-100
    name: str
    script: str
    region: str


LANGUAGES: tuple[Language, ...] = (
    # South Asia — large speaker populations, mostly Brahmic scripts, and
    # consistently the most heavily taxed group in results so far.
    Language("bn", "Bengali", "Bengali", "South Asia"),
    Language("hi", "Hindi", "Devanagari", "South Asia"),
    Language("mr", "Marathi", "Devanagari", "South Asia"),
    Language("ne", "Nepali", "Devanagari", "South Asia"),
    Language("gu", "Gujarati", "Gujarati", "South Asia"),
    Language("pa", "Punjabi", "Gurmukhi", "South Asia"),
    Language("ta", "Tamil", "Tamil", "South Asia"),
    Language("te", "Telugu", "Telugu", "South Asia"),
    Language("kn", "Kannada", "Kannada", "South Asia"),
    Language("ml", "Malayalam", "Malayalam", "South Asia"),
    Language("si", "Sinhala", "Sinhala", "South Asia"),
    Language("ur", "Urdu", "Arabic", "South Asia"),
    # Southeast and East Asia
    Language("vi", "Vietnamese", "Latin", "SE Asia"),
    Language("th", "Thai", "Thai", "SE Asia"),
    Language("km", "Khmer", "Khmer", "SE Asia"),
    Language("my", "Burmese", "Myanmar", "SE Asia"),
    Language("ms", "Malay", "Latin", "SE Asia"),
    Language("id", "Indonesian", "Latin", "SE Asia"),
    Language("zh", "Chinese", "Han", "East Asia"),
    Language("ja", "Japanese", "Kana/Han", "East Asia"),
    Language("ko", "Korean", "Hangul", "East Asia"),
    # Middle East and Central Asia
    Language("ar", "Arabic", "Arabic", "Middle East"),
    Language("fa", "Persian", "Arabic", "Middle East"),
    Language("ps", "Pashto", "Arabic", "Middle East"),
    Language("ku", "Kurdish", "Latin", "Middle East"),
    Language("he", "Hebrew", "Hebrew", "Middle East"),
    Language("hy", "Armenian", "Armenian", "Caucasus"),
    Language("ka", "Georgian", "Georgian", "Caucasus"),
    Language("kk", "Kazakh", "Cyrillic", "Central Asia"),
    Language("uz", "Uzbek", "Latin", "Central Asia"),
    Language("tr", "Turkish", "Latin", "Middle East"),
    # Africa — the least represented group in most tokenizer vocabularies.
    Language("am", "Amharic", "Ge'ez", "Africa"),
    Language("ha", "Hausa", "Latin", "Africa"),
    Language("ig", "Igbo", "Latin", "Africa"),
    Language("yo", "Yoruba", "Latin", "Africa"),
    Language("zu", "Zulu", "Latin", "Africa"),
    Language("xh", "Xhosa", "Latin", "Africa"),
    Language("af", "Afrikaans", "Latin", "Africa"),
    # Eastern Europe
    Language("ru", "Russian", "Cyrillic", "E Europe"),
    Language("uk", "Ukrainian", "Cyrillic", "E Europe"),
    Language("pl", "Polish", "Latin", "E Europe"),
    Language("el", "Greek", "Greek", "E Europe"),
    # Western Europe — the low-tax control group. If a tokenizer taxes these
    # heavily too, the problem is the tokenizer, not the language.
    Language("de", "German", "Latin", "W Europe"),
    Language("fr", "French", "Latin", "W Europe"),
    Language("es", "Spanish", "Latin", "W Europe"),
    Language("it", "Italian", "Latin", "W Europe"),
    Language("pt", "Portuguese", "Latin", "W Europe"),
    Language("nl", "Dutch", "Latin", "W Europe"),
)

BY_CODE: dict[str, Language] = {lang.code: lang for lang in LANGUAGES}


def resolve(codes: list[str] | None) -> list[Language]:
    """Map CLI codes to languages.

    ``None`` or ``["all"]`` selects everything; a region name selects that
    group, so ``--languages Africa`` is a valid shorthand.
    """
    if codes is None or codes == ["all"]:
        return list(LANGUAGES)

    regions = {lang.region.lower() for lang in LANGUAGES}
    selected: list[Language] = []
    unknown: list[str] = []
    for code in codes:
        if code in BY_CODE:
            selected.append(BY_CODE[code])
        elif code.lower() in regions:
            selected.extend(l for l in LANGUAGES if l.region.lower() == code.lower())
        else:
            unknown.append(code)
    if unknown:
        raise KeyError(f"unknown language codes: {', '.join(unknown)}")
    return selected
