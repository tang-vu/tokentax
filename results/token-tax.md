# Token Tax

How many tokens a language costs relative to the **same sentence in English**. `1.00x` means parity with English; `2.00x` means every request costs twice as many tokens for identical content.

Corpus `Helsinki-NLP/opus-100` (split `test`), up to 500 aligned sentence pairs per language. Generated 2026-07-20T03:20:13+00:00.

## Token tax by tokenizer

`—` the tokenizer does not target that language. `⚠` the tokenizer emitted unknown tokens, so its count describes degraded text and is excluded from the rankings below. GPT-2 is included as a 2019 reference point, not as a live option.

| Language | GPT-2 (2019) | GPT-3.5 / GPT-4 (cl100k) | GPT-4o (o200k) | Mistral 7B v0.3 | BLOOM | Qwen2.5 | Qwen3 | Llama-SEA-LION v3 | PhoBERT v2 (Vietnamese-only) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Burmese | 13.17x | 9.28x | 2.64x | 6.61x | 8.11x | 7.20x | 7.20x | 9.28x | — |
| Kannada | 12.90x | 8.81x | 2.17x | 6.37x | 1.51x | 6.88x | 6.88x | 8.82x | — |
| Khmer | 11.88x | 7.48x | 2.90x | 5.46x | 5.50x | 5.80x | 5.80x | 7.50x | — |
| Gujarati | 11.15x | 7.48x | 1.87x | 8.51x | 1.46x | 6.60x | 6.60x | 7.48x | — |
| Punjabi | 6.42x | 6.69x | 2.42x | 8.93x | 1.47x | 6.24x | 6.24x | 6.65x | — |
| Malayalam | 12.20x | 7.28x | 1.75x | 8.77x | 1.20x | 6.05x | 6.05x | 7.19x | — |
| Sinhala | 9.12x | 6.30x | 2.11x | 5.46x | 6.02x | 5.00x | 5.00x | 6.29x | — |
| Tamil | 14.68x | 7.47x | 2.05x | 5.77x | 1.42x | 5.97x | 5.97x | 7.47x | — |
| Amharic | 6.59x | 6.56x | 5.05x | 5.78x | 4.38x | 3.76x | 3.76x | 6.56x | — |
| Telugu | 10.18x | 6.65x | 1.71x | 5.97x | 1.23x | 5.70x | 5.70x | 6.65x | — |
| Armenian | 7.28x | 7.33x | 1.63x | 4.19x | 3.42x | 4.03x | 4.03x | 6.57x | — |
| Kurdish | 7.45x | 5.24x | 3.46x | 5.58x | 3.86x | 4.31x | 4.31x | 3.86x | — |
| Georgian | 7.58x | 5.57x | 2.60x | 3.73x | 3.81x | 3.49x | 3.49x | 5.56x | — |
| Bengali | 8.58x | 5.29x | 1.63x | 4.53x | 1.17x | 4.63x | 4.63x | 5.27x | — |
| Yoruba | 5.93x | 4.25x | 3.41x | 4.08x | 2.98x | 3.30x | 3.30x | 4.00x | — |
| Nepali | 7.34x | 4.90x | 1.78x | 4.61x | 1.35x | 4.54x | 4.54x | 2.71x | — |
| Hindi | 6.54x | 4.38x | 1.55x | 4.26x | 1.29x | 4.14x | 4.14x | 2.37x | — |
| Marathi | 6.52x | 4.29x | 1.76x | 4.15x | 1.23x | 3.95x | 3.95x | 2.47x | — |
| Uzbek | 6.16x | 3.81x | 2.18x | 2.92x | 3.34x | 3.08x | 3.08x | 3.07x | — |
| Greek | 4.78x | 3.77x | 1.71x | 3.91x | 2.93x | 3.58x | 3.58x | 1.75x | — |
| Pashto | 4.49x | 3.63x | 1.82x | 4.13x | 2.71x | 2.65x | 2.65x | 2.79x | — |
| Urdu | 5.15x | 3.71x | 1.36x | 3.64x | 1.14x | 2.69x | 2.69x | 2.76x | — |
| Kazakh | 4.42x | 2.93x | 1.41x | 2.15x | 2.62x | 2.38x | 2.38x | 2.41x | — |
| Igbo | 3.52x | 2.53x | 1.88x | 2.46x | 1.91x | 2.40x | 2.40x | 2.47x | — |
| Thai | 6.04x | 2.94x | 1.47x | 2.94x | 3.24x | 1.81x | 1.81x | 1.60x | — |
| Persian | 4.18x | 2.83x | 1.53x | 3.44x | 1.58x | 2.17x | 2.17x | 1.52x | — |
| Hebrew | 3.38x | 2.83x | 1.23x | 2.77x | 2.44x | 1.17x | 1.17x | 2.83x | — |
| Zulu | 2.18x | 2.08x | 1.66x | 2.09x | 1.76x | 2.08x | 2.08x | 2.06x | — |
| Xhosa | 2.18x | 2.01x | 1.60x | 2.03x | 1.58x | 2.00x | 2.00x | 1.99x | — |
| Hausa | 2.08x | 1.95x | 1.57x | 1.90x | 1.68x | 1.85x | 1.85x | 1.89x | — |
| Arabic | 3.73x | 2.63x | 1.27x | 2.99x | 1.01x | 1.43x | 1.43x | 1.48x | — |
| Russian | 4.92x | 2.17x | 1.31x | 1.70x | 2.27x | 1.56x | 1.56x | 1.47x | — |
| Ukrainian | 4.14x | 2.08x | 1.35x | 1.56x | 2.05x | 1.69x | 1.69x | 1.34x | — |
| Korean | 3.65x | 1.81x | 1.20x | 1.91x | 2.10x | 1.25x | 1.25x | 1.16x | — |
| Afrikaans | 1.75x | 1.56x | 1.36x | 1.54x | 1.58x | 1.55x | 1.55x | 1.55x | — |
| Polish | 2.01x | 1.46x | 1.30x | 1.48x | 1.67x | 1.36x | 1.36x | 1.45x | — |
| French | 1.82x | 1.49x | 1.28x | 1.49x | 1.13x | 1.46x | 1.46x | 1.49x | — |
| Turkish | 1.88x | 1.51x | 1.21x | 1.71x | 1.57x | 1.31x | 1.31x | 1.16x | — |
| Italian | 1.67x | 1.39x | 1.27x | 1.39x | 1.41x | 1.38x | 1.38x | 1.39x | — |
| Vietnamese | 3.29x | 1.93x | 1.25x | 2.25x | 1.04x | 1.18x | 1.18x | 1.16x | 0.76x |
| Malay | 1.76x | 1.39x | 1.16x | 1.66x | 0.98x | 1.39x | 1.39x | 1.38x | — |
| German | 1.75x | 1.35x | 1.17x | 1.36x | 1.47x | 1.33x | 1.33x | 1.35x | — |
| Dutch | 1.65x | 1.34x | 1.10x | 1.36x | 1.47x | 1.33x | 1.33x | 1.33x | — |
| Japanese | 2.12x | 1.66x | 1.29x | 1.65x | 1.39x | 1.08x | 1.08x | 1.12x | — |
| Indonesian | 1.73x | 1.34x | 1.13x | 1.62x | 0.92x | 1.34x | 1.34x | 1.34x | — |
| Spanish | 1.73x | 1.34x | 1.16x | 1.41x | 1.09x | 1.33x | 1.33x | 1.34x | — |
| Portuguese | 1.65x | 1.28x | 1.08x | 1.37x | 1.01x | 1.26x | 1.26x | 1.28x | — |
| Chinese | 2.95x | 1.68x | 1.12x | 1.46x | 0.78x | 0.94x | 0.94x | 1.16x | — |

> These languages have no `test` split in OPUS-100 and were measured on another split: Armenian (`train`), Yoruba (`train`). Their text is not held out and, being lower-resource pairs, is likely noisier — treat those rows as indicative rather than precise.

## Cheapest vs most expensive tokenizer

`Overpay` is how much more the worst tokenizer costs than the best one for the same text.

| Language | Cheapest | Tax | Most expensive | Tax | Overpay |
|---|---|---:|---|---:|---:|
| Burmese | GPT-4o (o200k) | 2.64x | Llama-SEA-LION v3 | 9.28x | **3.5x** |
| Kannada | BLOOM | 1.51x | Llama-SEA-LION v3 | 8.82x | **5.8x** |
| Khmer | GPT-4o (o200k) | 2.90x | Llama-SEA-LION v3 | 7.50x | **2.6x** |
| Gujarati | BLOOM | 1.46x | Mistral 7B v0.3 | 8.51x | **5.8x** |
| Punjabi | BLOOM | 1.47x | Mistral 7B v0.3 | 8.93x | **6.1x** |
| Malayalam | BLOOM | 1.20x | Mistral 7B v0.3 | 8.77x | **7.3x** |
| Sinhala | GPT-4o (o200k) | 2.11x | GPT-3.5 / GPT-4 (cl100k) | 6.30x | **3.0x** |
| Tamil | BLOOM | 1.42x | Llama-SEA-LION v3 | 7.47x | **5.3x** |
| Amharic | Qwen2.5 | 3.76x | Llama-SEA-LION v3 | 6.56x | **1.7x** |
| Telugu | BLOOM | 1.23x | GPT-3.5 / GPT-4 (cl100k) | 6.65x | **5.4x** |
| Armenian | GPT-4o (o200k) | 1.63x | GPT-3.5 / GPT-4 (cl100k) | 7.33x | **4.5x** |
| Kurdish | GPT-4o (o200k) | 3.46x | Mistral 7B v0.3 | 5.58x | **1.6x** |
| Georgian | GPT-4o (o200k) | 2.60x | GPT-3.5 / GPT-4 (cl100k) | 5.57x | **2.1x** |
| Bengali | BLOOM | 1.17x | GPT-3.5 / GPT-4 (cl100k) | 5.29x | **4.5x** |
| Yoruba | BLOOM | 2.98x | GPT-3.5 / GPT-4 (cl100k) | 4.25x | **1.4x** |
| Nepali | BLOOM | 1.35x | GPT-3.5 / GPT-4 (cl100k) | 4.90x | **3.6x** |
| Hindi | BLOOM | 1.29x | GPT-3.5 / GPT-4 (cl100k) | 4.38x | **3.4x** |
| Marathi | BLOOM | 1.23x | GPT-3.5 / GPT-4 (cl100k) | 4.29x | **3.5x** |
| Uzbek | GPT-4o (o200k) | 2.18x | GPT-3.5 / GPT-4 (cl100k) | 3.81x | **1.7x** |
| Greek | GPT-4o (o200k) | 1.71x | Mistral 7B v0.3 | 3.91x | **2.3x** |
| Pashto | GPT-4o (o200k) | 1.82x | Mistral 7B v0.3 | 4.13x | **2.3x** |
| Urdu | BLOOM | 1.14x | GPT-3.5 / GPT-4 (cl100k) | 3.71x | **3.3x** |
| Kazakh | GPT-4o (o200k) | 1.41x | GPT-3.5 / GPT-4 (cl100k) | 2.93x | **2.1x** |
| Igbo | GPT-4o (o200k) | 1.88x | GPT-3.5 / GPT-4 (cl100k) | 2.53x | **1.3x** |
| Thai | GPT-4o (o200k) | 1.47x | BLOOM | 3.24x | **2.2x** |
| Persian | Llama-SEA-LION v3 | 1.52x | Mistral 7B v0.3 | 3.44x | **2.3x** |
| Hebrew | Qwen2.5 | 1.17x | Llama-SEA-LION v3 | 2.83x | **2.4x** |
| Zulu | GPT-4o (o200k) | 1.66x | Mistral 7B v0.3 | 2.09x | **1.3x** |
| Xhosa | BLOOM | 1.58x | Mistral 7B v0.3 | 2.03x | **1.3x** |
| Hausa | GPT-4o (o200k) | 1.57x | GPT-3.5 / GPT-4 (cl100k) | 1.95x | **1.2x** |
| Arabic | BLOOM | 1.01x | Mistral 7B v0.3 | 2.99x | **3.0x** |
| Russian | GPT-4o (o200k) | 1.31x | BLOOM | 2.27x | **1.7x** |
| Ukrainian | Llama-SEA-LION v3 | 1.34x | GPT-3.5 / GPT-4 (cl100k) | 2.08x | **1.5x** |
| Korean | Llama-SEA-LION v3 | 1.16x | BLOOM | 2.10x | **1.8x** |
| Afrikaans | GPT-4o (o200k) | 1.36x | BLOOM | 1.58x | **1.2x** |
| Polish | GPT-4o (o200k) | 1.30x | BLOOM | 1.67x | **1.3x** |
| French | BLOOM | 1.13x | Mistral 7B v0.3 | 1.49x | **1.3x** |
| Turkish | Llama-SEA-LION v3 | 1.16x | Mistral 7B v0.3 | 1.71x | **1.5x** |
| Italian | GPT-4o (o200k) | 1.27x | BLOOM | 1.41x | **1.1x** |
| Vietnamese | PhoBERT v2 (Vietnamese-only) | 0.76x | Mistral 7B v0.3 | 2.25x | **2.9x** |
| Malay | BLOOM | 0.98x | Mistral 7B v0.3 | 1.66x | **1.7x** |
| German | GPT-4o (o200k) | 1.17x | BLOOM | 1.47x | **1.3x** |
| Dutch | GPT-4o (o200k) | 1.10x | BLOOM | 1.47x | **1.3x** |
| Japanese | Qwen2.5 | 1.08x | GPT-3.5 / GPT-4 (cl100k) | 1.66x | **1.5x** |
| Indonesian | BLOOM | 0.92x | Mistral 7B v0.3 | 1.62x | **1.8x** |
| Spanish | BLOOM | 1.09x | Mistral 7B v0.3 | 1.41x | **1.3x** |
| Portuguese | BLOOM | 1.01x | Mistral 7B v0.3 | 1.37x | **1.4x** |
| Chinese | BLOOM | 0.78x | GPT-3.5 / GPT-4 (cl100k) | 1.68x | **2.1x** |

## Effective context window

English content that fits in a nominal 128,000-token window, expressed in tokens of that content's English original.

| Language | Best case | Worst case |
|---|---:|---:|
| Burmese | 48,506 tokens | 13,793 tokens |
| Kannada | 84,521 tokens | 14,512 tokens |
| Khmer | 44,093 tokens | 17,059 tokens |
| Gujarati | 87,815 tokens | 15,038 tokens |
| Punjabi | 87,021 tokens | 14,331 tokens |
| Malayalam | 106,560 tokens | 14,603 tokens |
| Sinhala | 60,700 tokens | 20,311 tokens |
| Tamil | 90,446 tokens | 17,144 tokens |
| Amharic | 34,009 tokens | 19,517 tokens |
| Telugu | 103,685 tokens | 19,255 tokens |
| Armenian | 78,701 tokens | 17,471 tokens |
| Kurdish | 36,960 tokens | 22,956 tokens |
| Georgian | 49,158 tokens | 22,986 tokens |
| Bengali | 109,075 tokens | 24,196 tokens |
| Yoruba | 42,888 tokens | 30,134 tokens |
| Nepali | 95,075 tokens | 26,130 tokens |
| Hindi | 98,948 tokens | 29,239 tokens |
| Marathi | 104,327 tokens | 29,825 tokens |
| Uzbek | 58,726 tokens | 33,626 tokens |
| Greek | 74,823 tokens | 32,739 tokens |
| Pashto | 70,156 tokens | 31,017 tokens |
| Urdu | 112,646 tokens | 34,493 tokens |
| Kazakh | 90,754 tokens | 43,635 tokens |
| Igbo | 68,233 tokens | 50,644 tokens |
| Thai | 87,045 tokens | 39,518 tokens |
| Persian | 84,249 tokens | 37,195 tokens |
| Hebrew | 109,542 tokens | 45,228 tokens |
| Zulu | 77,080 tokens | 61,384 tokens |
| Xhosa | 80,910 tokens | 63,153 tokens |
| Hausa | 81,778 tokens | 65,786 tokens |
| Arabic | 126,883 tokens | 42,766 tokens |
| Russian | 97,874 tokens | 56,325 tokens |
| Ukrainian | 95,444 tokens | 61,579 tokens |
| Korean | 110,506 tokens | 61,027 tokens |
| Afrikaans | 94,249 tokens | 81,053 tokens |
| Polish | 98,476 tokens | 76,867 tokens |
| French | 113,054 tokens | 85,854 tokens |
| Turkish | 110,316 tokens | 74,831 tokens |
| Italian | 101,129 tokens | 91,096 tokens |
| Vietnamese | 167,648 tokens | 56,980 tokens |
| Malay | 130,372 tokens | 76,978 tokens |
| German | 109,645 tokens | 87,235 tokens |
| Dutch | 116,057 tokens | 87,080 tokens |
| Japanese | 118,299 tokens | 77,234 tokens |
| Indonesian | 139,236 tokens | 79,232 tokens |
| Spanish | 117,560 tokens | 90,838 tokens |
| Portuguese | 127,198 tokens | 93,731 tokens |
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
