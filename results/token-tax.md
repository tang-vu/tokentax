# Token Tax

How many tokens a language costs relative to the **same sentence in English**. `1.00x` means parity with English; `2.00x` means every request costs twice as many tokens for identical content.

Corpus `Helsinki-NLP/opus-100` (split `test`), up to 500 aligned sentence pairs per language. Generated 2026-07-19T17:51:02+00:00.

## Token tax by tokenizer

`—` the tokenizer does not target that language. `⚠` the tokenizer emitted unknown tokens, so its count describes degraded text and is excluded from the rankings below. GPT-2 is included as a 2019 reference point, not as a live option.

| Language | GPT-2 (2019) | GPT-3.5 / GPT-4 (cl100k) | GPT-4o (o200k) | Mistral 7B v0.3 | BLOOM | Qwen2.5 | Qwen3 | Llama-SEA-LION v3 | PhoBERT v2 (Vietnamese-only) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Tamil | 14.68x | 7.47x | 2.05x | 5.77x | 1.42x | 5.97x | 5.97x | 7.47x | — |
| Hindi | 6.54x | 4.38x | 1.55x | 4.26x | 1.29x | 4.14x | 4.14x | 2.37x | — |
| Thai | 6.04x | 2.94x | 1.47x | 2.94x | 3.24x | 1.81x | 1.81x | 1.60x | — |
| Persian | 4.18x | 2.83x | 1.53x | 3.44x | 1.58x | 2.17x | 2.17x | 1.52x | — |
| Arabic | 3.73x | 2.63x | 1.27x | 2.99x | 1.01x | 1.43x | 1.43x | 1.48x | — |
| Russian | 4.92x | 2.17x | 1.31x | 1.70x | 2.27x | 1.56x | 1.56x | 1.47x | — |
| Korean | 3.65x | 1.81x | 1.20x | 1.91x | 2.10x | 1.25x | 1.25x | 1.16x | — |
| French | 1.82x | 1.49x | 1.28x | 1.49x | 1.13x | 1.46x | 1.46x | 1.49x | — |
| Turkish | 1.88x | 1.51x | 1.21x | 1.71x | 1.57x | 1.31x | 1.31x | 1.16x | — |
| Vietnamese | 3.29x | 1.93x | 1.25x | 2.25x | 1.04x | 1.18x | 1.18x | 1.16x | 0.76x |
| German | 1.75x | 1.35x | 1.17x | 1.36x | 1.47x | 1.33x | 1.33x | 1.35x | — |
| Japanese | 2.12x | 1.66x | 1.29x | 1.65x | 1.39x | 1.08x | 1.08x | 1.12x | — |
| Indonesian | 1.73x | 1.34x | 1.13x | 1.62x | 0.92x | 1.34x | 1.34x | 1.34x | — |
| Spanish | 1.73x | 1.34x | 1.16x | 1.41x | 1.09x | 1.33x | 1.33x | 1.34x | — |
| Chinese | 2.95x | 1.68x | 1.12x | 1.46x | 0.78x | 0.94x | 0.94x | 1.16x | — |

## Cheapest vs most expensive tokenizer

`Overpay` is how much more the worst tokenizer costs than the best one for the same text.

| Language | Cheapest | Tax | Most expensive | Tax | Overpay |
|---|---|---:|---|---:|---:|
| Tamil | BLOOM | 1.42x | Llama-SEA-LION v3 | 7.47x | **5.3x** |
| Hindi | BLOOM | 1.29x | GPT-3.5 / GPT-4 (cl100k) | 4.38x | **3.4x** |
| Thai | GPT-4o (o200k) | 1.47x | BLOOM | 3.24x | **2.2x** |
| Persian | Llama-SEA-LION v3 | 1.52x | Mistral 7B v0.3 | 3.44x | **2.3x** |
| Arabic | BLOOM | 1.01x | Mistral 7B v0.3 | 2.99x | **3.0x** |
| Russian | GPT-4o (o200k) | 1.31x | BLOOM | 2.27x | **1.7x** |
| Korean | Llama-SEA-LION v3 | 1.16x | BLOOM | 2.10x | **1.8x** |
| French | BLOOM | 1.13x | Mistral 7B v0.3 | 1.49x | **1.3x** |
| Turkish | Llama-SEA-LION v3 | 1.16x | Mistral 7B v0.3 | 1.71x | **1.5x** |
| Vietnamese | PhoBERT v2 (Vietnamese-only) | 0.76x | Mistral 7B v0.3 | 2.25x | **2.9x** |
| German | GPT-4o (o200k) | 1.17x | BLOOM | 1.47x | **1.3x** |
| Japanese | Qwen2.5 | 1.08x | GPT-3.5 / GPT-4 (cl100k) | 1.66x | **1.5x** |
| Indonesian | BLOOM | 0.92x | Mistral 7B v0.3 | 1.62x | **1.8x** |
| Spanish | BLOOM | 1.09x | Mistral 7B v0.3 | 1.41x | **1.3x** |
| Chinese | BLOOM | 0.78x | GPT-3.5 / GPT-4 (cl100k) | 1.68x | **2.1x** |

## Effective context window

English content that fits in a nominal 128,000-token window, expressed in tokens of that content's English original.

| Language | Best case | Worst case |
|---|---:|---:|
| Tamil | 90,446 tokens | 17,144 tokens |
| Hindi | 98,948 tokens | 29,239 tokens |
| Thai | 87,045 tokens | 39,518 tokens |
| Persian | 84,249 tokens | 37,195 tokens |
| Arabic | 126,883 tokens | 42,766 tokens |
| Russian | 97,874 tokens | 56,325 tokens |
| Korean | 110,506 tokens | 61,027 tokens |
| French | 113,054 tokens | 85,854 tokens |
| Turkish | 110,316 tokens | 74,831 tokens |
| Vietnamese | 167,648 tokens | 56,980 tokens |
| German | 109,645 tokens | 87,235 tokens |
| Japanese | 118,299 tokens | 77,234 tokens |
| Indonesian | 139,236 tokens | 79,232 tokens |
| Spanish | 117,560 tokens | 90,838 tokens |
| Chinese | 163,473 tokens | 76,395 tokens |

## Methodology

- Every number compares **aligned translations of the same sentence**, so differences reflect tokenizer efficiency rather than differing content.
- Tax is aggregate: total target tokens / total English tokens across all pairs. Per-sentence median and p90 are in the JSON output.
- Special tokens and chat templates are excluded; only content is counted.
- OPUS-100 is crawled data, so pairs are filtered for length, alignment plausibility, duplicates, and untranslated rows before counting.
- Cells where more than 1% of tokens are unknown are marked lossy and excluded from rankings: a tokenizer that drops characters can post a low token count while destroying the text.
- Monolingual tokenizers are only measured against the language they target.
- Historical tokenizers appear in the matrix but not in the rankings: GPT-2 is the worst option for every language, which is true and useless for choosing between tokenizers shipping today.

Full limitations: [`docs/methodology-and-limitations.md`](docs/methodology-and-limitations.md).
