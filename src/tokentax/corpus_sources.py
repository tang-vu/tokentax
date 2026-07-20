"""Raw sentence-pair readers, one per corpus.

Each reader yields ``(english, target)`` before any filtering, so
:mod:`corpus` can apply one set of quality rules to every source. Keeping more
than one source matters: a quirk of a single dataset can bias a whole
benchmark, and the only way to notice is to measure somewhere else.

``opus-100`` — crawled, ~100 languages, broad coverage, noisy.
``wmt24pp``  — professionally translated from English into 55 locales, clean,
               narrower coverage.
"""

from __future__ import annotations

from typing import Iterator

SourceRows = Iterator[tuple[str, str]]


def opus_100_config(code: str) -> str:
    """OPUS-100 names configs as an alphabetically sorted language pair."""
    return f"en-{code}" if "en" < code else f"{code}-en"


def opus_100_rows(code: str, split: str) -> SourceRows:
    from datasets import load_dataset

    dataset = load_dataset("Helsinki-NLP/opus-100", opus_100_config(code), split=split)
    for row in dataset:
        translation = row.get("translation") or {}
        yield (translation.get("en") or "", translation.get(code) or "")


def opus_100_splits(code: str) -> list[str]:
    from datasets import get_dataset_split_names

    return list(
        get_dataset_split_names("Helsinki-NLP/opus-100", opus_100_config(code))
    )


# WMT24++ addresses locales, not bare language codes, and ships several
# regional variants for some languages. One variant per language is enough for
# a cross-check, so the most widely spoken is picked and pinned here rather
# than guessed at runtime.
WMT24PP_LOCALES: dict[str, str] = {
    "ar": "ar_EG", "bn": "bn_IN", "de": "de_DE", "el": "el_GR", "es": "es_MX",
    "fa": "fa_IR", "fr": "fr_FR", "gu": "gu_IN", "he": "he_IL", "hi": "hi_IN",
    "id": "id_ID", "it": "it_IT", "ja": "ja_JP", "kn": "kn_IN", "ko": "ko_KR",
    "ml": "ml_IN", "mr": "mr_IN", "nl": "nl_NL", "pa": "pa_IN", "pl": "pl_PL",
    "pt": "pt_PT", "ru": "ru_RU", "ta": "ta_IN", "te": "te_IN", "th": "th_TH",
    "tr": "tr_TR", "uk": "uk_UA", "ur": "ur_PK", "vi": "vi_VN", "zh": "zh_CN",
    "zu": "zu_ZA",
}


def wmt24pp_rows(code: str, split: str) -> SourceRows:
    from datasets import load_dataset

    locale = WMT24PP_LOCALES.get(code)
    if locale is None:
        raise KeyError(f"wmt24pp has no locale for {code!r}")

    dataset = load_dataset("google/wmt24pp", f"en-{locale}", split="train")
    for row in dataset:
        # The corpus embeds canary rows to detect training contamination; they
        # are marked as bad sources and are not real translations.
        if row.get("is_bad_source"):
            continue
        # `target` is the professionally post-edited reference, which the
        # dataset treats as its primary one. `original_target` is kept in the
        # data but not used here, so the choice stays consistent per language.
        yield (row.get("source") or "", row.get("target") or "")


def wmt24pp_splits(code: str) -> list[str]:
    if code not in WMT24PP_LOCALES:
        raise KeyError(f"wmt24pp has no locale for {code!r}")
    return ["train"]


SOURCES: dict[str, dict] = {
    "opus-100": {
        "rows": opus_100_rows,
        "splits": opus_100_splits,
        "dataset": "Helsinki-NLP/opus-100",
        "default_split": "test",
        "description": "crawled, ~100 languages",
    },
    "wmt24pp": {
        "rows": wmt24pp_rows,
        "splits": wmt24pp_splits,
        "dataset": "google/wmt24pp",
        "default_split": "train",
        "description": "professional human translation, 55 locales",
    },
}


def languages_for(source: str) -> set[str] | None:
    """Codes a source can serve, or ``None`` when it serves everything."""
    if source == "wmt24pp":
        return set(WMT24PP_LOCALES)
    return None
