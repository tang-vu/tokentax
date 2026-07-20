# Token Tax

How many tokens a language costs relative to the **same sentence in English**. `1.00x` means parity with English; `2.00x` means every request costs twice as many tokens for identical content.

Corpus `google/wmt24pp` (split `train`), up to 500 aligned sentence pairs per language. Generated 2026-07-20T15:20:28+00:00.

## Token tax by tokenizer

`—` the tokenizer does not target that language. `⚠` the tokenizer emitted unknown tokens, so its count describes degraded text and is excluded from the rankings below. GPT-2 is included as a 2019 reference point, not as a live option.

| Language | GPT-2 (2019) | GPT-3.5 / GPT-4 (cl100k) | GPT-4o (o200k) | Mistral 7B v0.3 | BLOOM | Llama 3 | Gemma 2 | Mistral Nemo (Tekken) | Aya 101 | Qwen2.5 | Phi-4 | DeepSeek V3 | Aya Expanse | Command A | Mistral Small 3 | Gemma 3 | Llama 4 Scout | Qwen3 | GLM-4.5 | GPT-OSS | Llama-SEA-LION v3 | PhoBERT v2 (Vietnamese-only) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Malayalam | 14.56x | 8.67x | 1.90x | 10.43x | 1.36x | 8.67x | 3.06x | 2.50x | 1.34x | 7.07x | 8.67x | 4.23x | 8.68x | 8.68x | 3.51x | 1.74x | 2.71x | 7.07x | 8.66x | 1.90x | 8.67x | — |
| Telugu | 13.44x | 8.67x | 2.02x | 7.59x | 1.43x | 8.67x | 2.99x | 2.38x | 1.50x | 7.36x | 8.67x | 3.93x | 8.20x | 8.20x | 3.26x | 1.81x | 3.02x | 7.36x | 8.67x | 2.02x | 8.67x | — |
| Punjabi | 7.54x | 7.59x | 2.52x | 10.13x | 1.42x | 7.56x | 3.08x | 2.85x | 2.10x | 7.06x | 7.59x | 4.30x | 7.53x | 7.53x | 3.28x | 2.54x | 3.06x | 7.06x | 7.59x | 2.52x | 7.56x | — |
| Kannada | 13.18x | 8.67x | 1.91x | 6.12x | 1.27x | 8.67x | 3.16x | 2.18x | 1.42x | 6.81x | 8.67x | 3.59x | 8.16x | 8.16x | 3.14x | 1.76x | 2.40x | 6.81x | 8.67x | 1.91x | 8.67x | — |
| Gujarati | 11.91x | 7.54x | 1.80x | 8.63x | 1.39x | 7.54x | 2.93x | 2.71x | 1.78x | 6.67x | 7.54x | 3.76x | 7.48x | 7.48x | 3.08x | 1.81x | 2.53x | 6.67x | 7.54x | 1.80x | 7.54x | — |
| Tamil | 15.71x | 7.85x | 2.05x | 6.02x | 1.35x | 7.85x | 2.60x | 2.27x | 1.32x | 6.29x | 7.85x | 3.10x | 6.43x | 6.43x | 3.49x | 1.51x | 3.89x | 6.29x | 7.85x | 2.05x | 7.85x | — |
| Bengali | 8.53x | 5.23x | 1.56x | 4.51x | 1.16x | 5.19x | 2.42x | 2.03x | 1.50x | 4.57x | 5.23x | 1.87x | 4.98x | 4.98x | 2.58x | 1.14x | 1.94x | 4.57x | 5.23x | 1.56x | 5.19x | — |
| Hindi | 7.66x | 5.10x | 1.72x | 4.80x | 1.44x | 2.71x | 1.96x | 1.92x | 1.80x | 4.74x | 5.10x | 3.06x | 3.31x | 3.31x | 2.96x | 1.42x | 1.80x | 4.74x | 5.10x | 1.72x | 2.71x | — |
| Marathi | 7.39x | 4.88x | 1.86x | 4.50x | 1.26x | 2.75x | 2.23x | 2.17x | 1.57x | 4.47x | 4.88x | 2.91x | 3.48x | 3.48x | 2.83x | 1.39x | 1.97x | 4.47x | 4.86x | 1.86x | 2.75x | — |
| Urdu | 6.24x | 4.48x | 1.66x | 4.30x | 1.37x | 3.28x | 1.94x | 1.78x | 1.56x | 3.25x | 4.48x | 2.43x | 3.28x | 3.28x | 1.79x | 1.49x | 1.93x | 3.25x | 3.45x | 1.66x | 3.28x | — |
| Greek | 5.79x | 4.61x | 1.97x | 4.75x | 3.45x | 2.06x | 2.05x | 1.97x | 1.54x | 4.42x | 4.61x | 2.44x | 1.53x | 1.53x | 1.97x | 1.97x | 1.90x | 4.42x | 2.19x | 1.97x | 2.06x | — |
| Thai | 7.96x | 3.89x | 1.81x | 3.82x | 4.16x | 2.04x | 1.63x | 2.18x | 0.92x | 2.36x | 3.89x | 1.64x | 4.16x | 4.16x | 2.62x | 1.43x | 1.46x | 2.36x | 3.89x | 1.81x | 2.04x | — |
| Hebrew | 3.99x | 3.35x | 1.38x | 3.19x | 2.74x | 3.35x | 1.50x | 1.56x | 1.19x | 1.35x | 3.35x | 1.64x | 1.34x | 1.34x | 1.56x | 1.59x | 1.63x | 1.35x | 3.35x | 1.38x | 3.35x | — |
| Persian | 5.17x | 3.27x | 1.56x | 3.97x | 1.80x | 1.54x | 1.40x | 1.47x | 1.36x | 2.60x | 3.27x | 1.82x | 1.53x | 1.53x | 1.48x | 1.43x | 1.51x | 2.60x | 1.83x | 1.56x | 1.54x | — |
| Zulu | 2.24x | 2.07x | 1.63x | 2.06x | 1.68x | 2.05x | 1.86x | 1.95x | 1.35x | 2.05x | 2.07x | 2.03x | 1.89x | 1.89x | 1.95x | 1.82x | 1.85x | 2.05x | 2.04x | 1.63x | 2.05x | — |
| Ukrainian | 5.34x | 2.84x | 1.71x | 1.90x | 2.62x | 1.60x | 1.58x | 1.69x | 1.32x | 2.40x | 2.84x | 2.07x | 1.42x | 1.42x | 1.69x | 1.55x | 1.52x | 2.40x | 1.77x | 1.71x | 1.60x | — |
| Polish | 2.74x | 1.96x | 1.70x | 1.98x | 2.22x | 1.94x | 1.49x | 1.67x | 1.38x | 1.82x | 1.96x | 1.74x | 1.45x | 1.45x | 1.67x | 1.53x | 1.46x | 1.82x | 1.73x | 1.70x | 1.94x | — |
| Korean | 4.85x | 2.35x | 1.47x | 2.44x | 2.72x | 1.47x | 1.62x | 1.27x | 1.28x | 1.62x | 2.35x | 1.66x | 1.30x | 1.30x | 1.27x | 1.31x | 1.28x | 1.62x | 1.94x | 1.47x | 1.47x | — |
| Vietnamese | 4.38x | 2.49x | 1.51x | 2.90x | 1.29x | 1.41x | 1.37x | 1.46x | 2.00x | 1.43x | 2.49x | 2.12x | 1.35x | 1.35x | 1.46x | 1.36x | 1.36x | 1.43x | 1.47x | 1.51x | 1.41x | 0.87x |
| Arabic | 3.73x | 2.65x | 1.32x | 3.06x | 1.10x | 1.53x | 1.37x | 1.21x | 1.20x | 1.52x | 2.65x | 1.50x | 1.40x | 1.40x | 1.21x | 1.31x | 1.50x | 1.52x | 1.62x | 1.32x | 1.53x | — |
| Turkish | 2.37x | 1.88x | 1.43x | 2.18x | 1.93x | 1.39x | 1.36x | 1.51x | 1.11x | 1.61x | 1.88x | 1.98x | 1.27x | 1.27x | 1.52x | 1.34x | 1.34x | 1.61x | 1.62x | 1.43x | 1.39x | — |
| Russian | 5.09x | 2.25x | 1.35x | 1.77x | 2.27x | 1.52x | 1.28x | 1.43x | 1.22x | 1.63x | 2.25x | 1.50x | 1.26x | 1.26x | 1.43x | 1.28x | 1.20x | 1.63x | 1.35x | 1.35x | 1.52x | — |
| Japanese | 2.88x | 2.23x | 1.67x | 2.10x | 1.82x | 1.49x | 1.13x | 1.51x | 0.88x | 1.39x | 2.23x | 1.44x | 1.24x | 1.24x | 1.51x | 1.18x | 1.33x | 1.39x | 1.51x | 1.67x | 1.49x | — |
| Dutch | 1.97x | 1.58x | 1.26x | 1.62x | 1.72x | 1.57x | 1.31x | 1.43x | 1.19x | 1.57x | 1.58x | 1.48x | 1.30x | 1.30x | 1.43x | 1.35x | 1.35x | 1.57x | 1.49x | 1.26x | 1.57x | — |
| German | 2.13x | 1.55x | 1.31x | 1.59x | 1.67x | 1.54x | 1.24x | 1.32x | 1.21x | 1.53x | 1.55x | 1.50x | 1.35x | 1.35x | 1.32x | 1.31x | 1.31x | 1.53x | 1.42x | 1.31x | 1.54x | — |
| French | 1.88x | 1.50x | 1.32x | 1.55x | 1.17x | 1.50x | 1.32x | 1.28x | 1.37x | 1.48x | 1.50x | 1.46x | 1.34x | 1.34x | 1.28x | 1.36x | 1.33x | 1.48x | 1.43x | 1.32x | 1.50x | — |
| Italian | 1.79x | 1.48x | 1.34x | 1.48x | 1.48x | 1.48x | 1.21x | 1.28x | 1.23x | 1.47x | 1.48x | 1.40x | 1.23x | 1.23x | 1.28x | 1.24x | 1.25x | 1.47x | 1.38x | 1.34x | 1.48x | — |
| Indonesian | 1.96x | 1.53x | 1.25x | 1.86x | 0.99x | 1.52x | 1.10x | 1.34x | 1.09x | 1.52x | 1.53x | 1.33x | 1.13x | 1.13x | 1.34x | 1.13x | 1.15x | 1.52x | 1.52x | 1.25x | 1.52x | — |
| Portuguese | 1.88x | 1.44x | 1.21x | 1.54x | 1.12x | 1.44x | 1.19x | 1.26x | 1.29x | 1.42x | 1.44x | 1.39x | 1.18x | 1.18x | 1.26x | 1.22x | 1.22x | 1.42x | 1.37x | 1.21x | 1.44x | — |
| Spanish | 1.83x | 1.40x | 1.22x | 1.47x | 1.13x | 1.40x | 1.16x | 1.22x | 1.21x | 1.39x | 1.40x | 1.37x | 1.20x | 1.20x | 1.22x | 1.18x | 1.22x | 1.39x | 1.32x | 1.22x | 1.40x | — |
| Chinese | 3.21x | 1.87x | 1.26x | 1.63x | 0.95x | 1.29x | 1.05x | 1.41x | 0.93x | 1.01x | 1.87x | 0.94x | 1.11x | 1.11x | 1.41x | 1.06x | 1.08x | 1.01x | 0.96x | 1.26x | 1.29x | — |

## Cheapest vs most expensive tokenizer

`Overpay` is how much more the worst tokenizer costs than the best one for the same text.

| Language | Cheapest | Tax | Most expensive | Tax | Overpay |
|---|---|---:|---|---:|---:|
| Malayalam | Aya 101 | 1.34x | Mistral 7B v0.3 | 10.43x | **7.8x** |
| Telugu | BLOOM | 1.43x | Llama 3 | 8.67x | **6.1x** |
| Punjabi | BLOOM | 1.42x | Mistral 7B v0.3 | 10.13x | **7.1x** |
| Kannada | BLOOM | 1.27x | Llama 3 | 8.67x | **6.8x** |
| Gujarati | BLOOM | 1.39x | Mistral 7B v0.3 | 8.63x | **6.2x** |
| Tamil | Aya 101 | 1.32x | Llama 3 | 7.85x | **6.0x** |
| Bengali | Gemma 3 | 1.14x | GLM-4.5 | 5.23x | **4.6x** |
| Hindi | Gemma 3 | 1.42x | GLM-4.5 | 5.10x | **3.6x** |
| Marathi | BLOOM | 1.26x | GPT-3.5 / GPT-4 (cl100k) | 4.88x | **3.9x** |
| Urdu | BLOOM | 1.37x | GPT-3.5 / GPT-4 (cl100k) | 4.48x | **3.3x** |
| Greek | Aya Expanse | 1.53x | Mistral 7B v0.3 | 4.75x | **3.1x** |
| Thai | Aya 101 | 0.92x | Aya Expanse | 4.16x | **4.5x** |
| Hebrew | Aya 101 | 1.19x | Llama 3 | 3.35x | **2.8x** |
| Persian | Aya 101 | 1.36x | Mistral 7B v0.3 | 3.97x | **2.9x** |
| Zulu | Aya 101 | 1.35x | GPT-3.5 / GPT-4 (cl100k) | 2.07x | **1.5x** |
| Ukrainian | Aya 101 | 1.32x | GPT-3.5 / GPT-4 (cl100k) | 2.84x | **2.1x** |
| Polish | Aya 101 | 1.38x | BLOOM | 2.22x | **1.6x** |
| Korean | Mistral Nemo (Tekken) | 1.27x | BLOOM | 2.72x | **2.2x** |
| Vietnamese | PhoBERT v2 (Vietnamese-only) | 0.87x | Mistral 7B v0.3 | 2.90x | **3.3x** |
| Arabic | BLOOM | 1.10x | Mistral 7B v0.3 | 3.06x | **2.8x** |
| Turkish | Aya 101 | 1.11x | Mistral 7B v0.3 | 2.18x | **2.0x** |
| Russian | Llama 4 Scout | 1.20x | BLOOM | 2.27x | **1.9x** |
| Japanese | Aya 101 | 0.88x | GPT-3.5 / GPT-4 (cl100k) | 2.23x | **2.5x** |
| Dutch | Aya 101 | 1.19x | BLOOM | 1.72x | **1.4x** |
| German | Aya 101 | 1.21x | BLOOM | 1.67x | **1.4x** |
| French | BLOOM | 1.17x | Mistral 7B v0.3 | 1.55x | **1.3x** |
| Italian | Gemma 2 | 1.21x | Mistral 7B v0.3 | 1.48x | **1.2x** |
| Indonesian | BLOOM | 0.99x | Mistral 7B v0.3 | 1.86x | **1.9x** |
| Portuguese | BLOOM | 1.12x | Mistral 7B v0.3 | 1.54x | **1.4x** |
| Spanish | BLOOM | 1.13x | Mistral 7B v0.3 | 1.47x | **1.3x** |
| Chinese | Aya 101 | 0.93x | GPT-3.5 / GPT-4 (cl100k) | 1.87x | **2.0x** |

## Effective context window

English content that fits in a nominal 128,000-token window, expressed in tokens of that content's English original.

| Language | Best case | Worst case |
|---|---:|---:|
| Malayalam | 95,801 tokens | 12,277 tokens |
| Telugu | 89,692 tokens | 14,763 tokens |
| Punjabi | 90,166 tokens | 12,632 tokens |
| Kannada | 100,946 tokens | 14,762 tokens |
| Gujarati | 92,212 tokens | 14,823 tokens |
| Tamil | 97,205 tokens | 16,300 tokens |
| Bengali | 112,389 tokens | 24,485 tokens |
| Hindi | 90,058 tokens | 25,112 tokens |
| Marathi | 101,329 tokens | 26,252 tokens |
| Urdu | 93,355 tokens | 28,547 tokens |
| Greek | 83,780 tokens | 26,935 tokens |
| Thai | 138,964 tokens | 30,736 tokens |
| Hebrew | 107,907 tokens | 38,219 tokens |
| Persian | 94,297 tokens | 32,281 tokens |
| Zulu | 94,913 tokens | 61,880 tokens |
| Ukrainian | 96,676 tokens | 45,091 tokens |
| Polish | 93,030 tokens | 57,592 tokens |
| Korean | 101,097 tokens | 47,005 tokens |
| Vietnamese | 146,587 tokens | 44,125 tokens |
| Arabic | 116,713 tokens | 41,862 tokens |
| Turkish | 115,242 tokens | 58,696 tokens |
| Russian | 106,462 tokens | 56,427 tokens |
| Japanese | 144,927 tokens | 57,455 tokens |
| Dutch | 107,617 tokens | 74,336 tokens |
| German | 105,558 tokens | 76,527 tokens |
| French | 109,196 tokens | 82,516 tokens |
| Italian | 106,012 tokens | 86,247 tokens |
| Indonesian | 129,554 tokens | 68,913 tokens |
| Portuguese | 114,346 tokens | 83,355 tokens |
| Spanish | 112,825 tokens | 87,140 tokens |
| Chinese | 138,124 tokens | 68,419 tokens |

## Skipped

- `corpus:af`: wmt24pp does not cover this language
- `corpus:am`: wmt24pp does not cover this language
- `corpus:ha`: wmt24pp does not cover this language
- `corpus:hy`: wmt24pp does not cover this language
- `corpus:ig`: wmt24pp does not cover this language
- `corpus:ka`: wmt24pp does not cover this language
- `corpus:kk`: wmt24pp does not cover this language
- `corpus:km`: wmt24pp does not cover this language
- `corpus:ku`: wmt24pp does not cover this language
- `corpus:ms`: wmt24pp does not cover this language
- `corpus:my`: wmt24pp does not cover this language
- `corpus:ne`: wmt24pp does not cover this language
- `corpus:ps`: wmt24pp does not cover this language
- `corpus:si`: wmt24pp does not cover this language
- `corpus:uz`: wmt24pp does not cover this language
- `corpus:xh`: wmt24pp does not cover this language
- `corpus:yo`: wmt24pp does not cover this language

## Methodology

- Every number compares **aligned translations of the same sentence**, so differences reflect tokenizer efficiency rather than differing content.
- Tax is aggregate: total target tokens / total English tokens across all pairs. Per-sentence median and p90 are in the JSON output.
- Special tokens and chat templates are excluded; only content is counted.
- OPUS-100 is crawled data, so pairs are filtered for length, alignment plausibility, duplicates, and untranslated rows before counting.
- Cells where more than 1% of tokens are unknown are marked lossy and excluded from rankings: a tokenizer that drops characters can post a low token count while destroying the text.
- Monolingual tokenizers are only measured against the language they target.
- Historical tokenizers appear in the matrix but not in the rankings: GPT-2 is the worst option for every language, which is true and useless for choosing between tokenizers shipping today.

Full limitations: [`docs/methodology-and-limitations.md`](docs/methodology-and-limitations.md).
