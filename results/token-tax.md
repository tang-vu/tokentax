# Token Tax

How many tokens a language costs relative to the **same sentence in English**. `1.00x` means parity with English; `2.00x` means every request costs twice as many tokens for identical content.

Corpus `Helsinki-NLP/opus-100` (split `test`), up to 500 aligned sentence pairs per language. Generated 2026-07-20T14:47:39+00:00.

## Token tax by tokenizer

`—` the tokenizer does not target that language. `⚠` the tokenizer emitted unknown tokens, so its count describes degraded text and is excluded from the rankings below. GPT-2 is included as a 2019 reference point, not as a live option.

| Language | GPT-2 (2019) | GPT-3.5 / GPT-4 (cl100k) | GPT-4o (o200k) | Mistral 7B v0.3 | BLOOM | Llama 3 | Gemma 2 | Mistral Nemo (Tekken) | Aya 101 | Qwen2.5 | Phi-4 | DeepSeek V3 | Aya Expanse | Command A | Mistral Small 3 | Gemma 3 | Llama 4 Scout | Qwen3 | GLM-4.5 | GPT-OSS | Llama-SEA-LION v3 | PhoBERT v2 (Vietnamese-only) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Khmer | 11.57x | 7.19x | 2.79x | 5.08x | 5.24x | 7.21x | 4.58x | 11.66x | 1.38x | 5.46x | 7.19x | 5.56x | 7.46x | 7.46x | 11.66x | 2.49x | 2.89x | 5.46x | 7.22x | 2.79x | 7.21x | — |
| Burmese | 13.21x | 9.31x | 2.65x | 6.63x | 8.13x | 9.31x | 3.97x | 2.87x | 1.38x | 7.22x | 9.31x | 4.41x | 7.21x | 7.21x | 3.97x | 2.11x | 2.89x | 7.22x | 9.31x | 2.65x | 9.31x | — |
| Kannada | 12.90x | 8.81x | 2.17x | 6.37x | 1.51x | 8.82x | 3.35x | 2.40x | 1.56x | 6.88x | 8.81x | 3.63x | 8.35x | 8.35x | 3.25x | 2.08x | 2.58x | 6.88x | 8.80x | 2.17x | 8.82x | — |
| Amharic | 6.61x | 6.57x | 5.06x | 5.79x | 4.39x | 6.57x | 2.90x | 6.46x | 1.50x | 3.77x | 6.57x | 5.19x | 5.54x | 5.54x | 6.46x | 1.98x | 2.25x | 3.77x | 6.57x | 5.06x | 6.57x | — |
| Gujarati | 11.15x | 7.48x | 1.87x | 8.51x | 1.46x | 7.48x | 3.02x | 2.79x | 1.85x | 6.60x | 7.48x | 3.81x | 7.38x | 7.38x | 3.14x | 1.89x | 2.57x | 6.60x | 7.47x | 1.87x | 7.48x | — |
| Sinhala | 9.12x | 6.30x | 2.11x | 5.46x | 6.02x | 6.29x | 2.91x | 9.04x | 1.25x | 5.00x | 6.30x | 3.24x | 5.68x | 5.68x | 9.04x | 1.80x | 2.20x | 5.00x | 6.29x | 2.11x | 6.29x | — |
| Punjabi | 6.47x | 6.74x | 2.43x | 9.02x | 1.48x | 6.70x | 2.97x | 2.79x | 1.95x | 6.29x | 6.74x | 3.94x | 6.71x | 6.71x | 3.07x | 2.47x | 2.90x | 6.29x | 6.74x | 2.43x | 6.70x | — |
| Malayalam | 12.20x | 7.28x | 1.75x | 8.77x | 1.20x | 7.19x | 2.51x | 2.33x | 1.17x | 6.05x | 7.28x | 3.58x | 7.32x | 7.32x | 3.14x | 1.48x | 2.42x | 6.05x | 7.19x | 1.75x | 7.19x | — |
| Tamil | 14.68x | 7.47x | 2.05x | 5.77x | 1.42x | 7.47x | 2.56x | 2.28x | 1.34x | 5.97x | 7.47x | 2.98x | 6.10x | 6.10x | 3.38x | 1.54x | 3.66x | 5.97x | 7.47x | 2.05x | 7.47x | — |
| Telugu | 10.18x | 6.65x | 1.71x | 5.97x | 1.23x | 6.65x | 2.27x | 1.97x | 1.27x | 5.70x | 6.65x | 3.09x | 6.34x | 6.34x | 2.61x | 1.47x | 2.47x | 5.70x | 6.65x | 1.71x | 6.65x | — |
| Kurdish | 7.47x | 5.25x | 3.47x | 5.59x | 3.87x | 3.87x | 3.37x | 3.69x | 2.26x | 4.32x | 5.25x | 4.35x | 4.00x | 4.00x | 3.69x | 3.14x | 3.40x | 4.32x | 4.15x | 3.47x | 3.87x | — |
| Armenian | 7.28x | 7.33x | 1.63x | 4.19x | 3.42x | 6.57x | 2.50x | 1.79x | 1.48x | 4.03x | 7.33x | 2.52x | 4.50x | 4.50x | 1.79x | 2.34x | 3.82x | 4.03x | 7.34x | 1.63x | 6.57x | — |
| Yoruba | 5.97x | 4.27x | 3.43x | 4.10x | 3.00x | 4.02x | 3.66x | 5.24x | 2.52x | 3.32x | 4.27x | 4.04x | 3.11x | 3.11x | 5.26x | 3.60x | 3.79x | 3.32x | 4.07x | 3.43x | 4.02x | — |
| Georgian | 7.58x | 5.57x | 2.60x | 3.73x | 3.81x | 5.56x | 2.83x | 2.67x | 1.96x | 3.49x | 5.57x | 3.27x | 4.18x | 4.18x | 2.67x | 2.45x | 2.70x | 3.49x | 5.57x | 2.60x | 5.56x | — |
| Bengali | 8.58x | 5.29x | 1.63x | 4.53x | 1.17x | 5.27x | 2.49x | 2.04x | 1.56x | 4.63x | 5.29x | 1.93x | 5.11x | 5.11x | 2.65x | 1.17x | 2.00x | 4.63x | 5.31x | 1.63x | 5.27x | — |
| Nepali | 7.39x | 4.92x | 1.78x | 4.64x | 1.34x | 2.72x | 2.23x | 2.33x | 1.60x | 4.55x | 4.92x | 3.12x | 3.52x | 3.52x | 2.83x | 1.60x | 1.94x | 4.55x | 4.92x | 1.78x | 2.72x | — |
| Uzbek | 6.16x | 3.81x | 2.18x | 2.92x | 3.34x | 3.07x | 2.70x | 2.65x | 1.56x | 3.08x | 3.81x | 2.85x | 2.78x | 2.78x | 2.65x | 2.34x | 2.41x | 3.08x | 3.17x | 2.18x | 3.07x | — |
| Marathi | 6.52x | 4.29x | 1.76x | 4.15x | 1.23x | 2.47x | 2.02x | 2.01x | 1.48x | 3.95x | 4.29x | 2.64x | 3.11x | 3.11x | 2.59x | 1.30x | 1.89x | 3.95x | 4.29x | 1.76x | 2.47x | — |
| Hindi | 6.56x | 4.39x | 1.55x | 4.28x | 1.29x | 2.38x | 1.77x | 1.66x | 1.57x | 4.15x | 4.39x | 2.65x | 2.90x | 2.90x | 2.56x | 1.32x | 1.65x | 4.15x | 4.39x | 1.55x | 2.38x | — |
| Pashto | 4.51x | 3.64x | 1.83x | 4.14x | 2.71x | 2.80x | 2.24x | 2.09x | 1.61x | 2.66x | 3.64x | 2.56x | 2.77x | 2.77x | 2.09x | 2.00x | 2.12x | 2.66x | 2.89x | 1.83x | 2.80x | — |
| Igbo | 3.60x | 2.57x | 1.90x | 2.50x | 1.93x | 2.51x | 2.36x | 2.62x | 1.85x | 2.43x | 2.57x | 2.46x | 2.41x | 2.41x | 2.62x | 2.29x | 2.22x | 2.43x | 2.51x | 1.90x | 2.51x | — |
| Urdu | 5.15x | 3.71x | 1.36x | 3.64x | 1.14x | 2.76x | 1.65x | 1.48x | 1.31x | 2.69x | 3.71x | 2.04x | 2.79x | 2.79x | 1.48x | 1.28x | 1.57x | 2.69x | 2.89x | 1.36x | 2.76x | — |
| Greek | 4.78x | 3.77x | 1.71x | 3.91x | 2.93x | 1.75x | 1.72x | 1.73x | 1.35x | 3.58x | 3.77x | 2.08x | 1.35x | 1.35x | 1.73x | 1.67x | 1.66x | 3.58x | 1.85x | 1.71x | 1.75x | — |
| Kazakh | 4.42x | 2.93x | 1.41x | 2.15x | 2.62x | 2.41x | 1.83x | 1.73x | 1.06x | 2.38x | 2.93x | 2.11x | 2.08x | 2.08x | 1.73x | 1.64x | 1.58x | 2.38x | 2.45x | 1.41x | 2.41x | — |
| Thai | 6.04x | 2.94x | 1.47x | 2.94x | 3.24x | 1.60x | 1.20x | 1.73x | 0.79x | 1.81x | 2.94x | 1.31x | 3.17x | 3.17x | 2.04x | 1.09x | 1.23x | 1.81x | 2.94x | 1.47x | 1.60x | — |
| Zulu | 2.18x | 2.08x | 1.66x | 2.09x | 1.76x | 2.06x | 1.88x | 1.97x | 1.38x | 2.08x | 2.08x | 2.01x | 1.92x | 1.92x | 1.97x | 1.87x | 1.90x | 2.08x | 2.05x | 1.66x | 2.06x | — |
| Xhosa | 2.18x | 2.01x | 1.60x | 2.03x | 1.58x | 1.99x | 1.88x | 1.94x | 1.30x | 2.00x | 2.01x | 2.01x | 1.90x | 1.90x | 1.94x | 1.85x | 1.82x | 2.00x | 1.99x | 1.60x | 1.99x | — |
| Persian | 4.18x | 2.83x | 1.53x | 3.44x | 1.58x | 1.52x | 1.41x | 1.49x | 1.26x | 2.17x | 2.83x | 1.70x | 1.55x | 1.55x | 1.50x | 1.41x | 1.57x | 2.17x | 1.73x | 1.53x | 1.52x | — |
| Hebrew | 3.38x | 2.83x | 1.23x | 2.77x | 2.44x | 2.83x | 1.25x | 1.40x | 1.07x | 1.17x | 2.83x | 1.45x | 1.25x | 1.25x | 1.40x | 1.34x | 1.44x | 1.17x | 2.83x | 1.23x | 2.83x | — |
| Hausa | 2.08x | 1.94x | 1.56x | 1.90x | 1.68x | 1.89x | 1.67x | 1.82x | 1.36x | 1.85x | 1.94x | 1.88x | 1.78x | 1.78x | 1.82x | 1.69x | 1.64x | 1.85x | 1.89x | 1.56x | 1.89x | — |
| Arabic | 3.73x | 2.63x | 1.27x | 2.99x | 1.01x | 1.48x | 1.31x | 1.14x | 1.21x | 1.43x | 2.63x | 1.45x | 1.36x | 1.36x | 1.15x | 1.29x | 1.45x | 1.43x | 1.55x | 1.27x | 1.48x | — |
| Russian | 4.94x | 2.17x | 1.31x | 1.70x | 2.28x | 1.47x | 1.25x | 1.39x | 1.19x | 1.56x | 2.17x | 1.45x | 1.20x | 1.20x | 1.39x | 1.25x | 1.15x | 1.56x | 1.31x | 1.31x | 1.47x | — |
| Ukrainian | 4.14x | 2.08x | 1.35x | 1.56x | 2.05x | 1.34x | 1.21x | 1.36x | 1.13x | 1.69x | 2.08x | 1.52x | 1.21x | 1.21x | 1.36x | 1.21x | 1.23x | 1.69x | 1.34x | 1.35x | 1.34x | — |
| Afrikaans | 1.75x | 1.55x | 1.36x | 1.54x | 1.58x | 1.55x | 1.35x | 1.45x | 1.18x | 1.55x | 1.55x | 1.51x | 1.41x | 1.41x | 1.45x | 1.40x | 1.42x | 1.55x | 1.51x | 1.36x | 1.55x | — |
| French | 1.83x | 1.50x | 1.29x | 1.50x | 1.14x | 1.50x | 1.28x | 1.26x | 1.34x | 1.47x | 1.50x | 1.45x | 1.29x | 1.29x | 1.26x | 1.31x | 1.28x | 1.47x | 1.41x | 1.29x | 1.50x | — |
| Korean | 3.65x | 1.81x | 1.20x | 1.91x | 2.10x | 1.16x | 1.24x | 1.00x | 1.04x | 1.25x | 1.81x | 1.33x | 1.08x | 1.08x | 1.00x | 1.01x | 1.09x | 1.25x | 1.51x | 1.20x | 1.16x | — |
| Polish | 2.01x | 1.46x | 1.30x | 1.48x | 1.67x | 1.45x | 1.11x | 1.29x | 1.06x | 1.36x | 1.46x | 1.32x | 1.14x | 1.14x | 1.29x | 1.15x | 1.14x | 1.36x | 1.30x | 1.30x | 1.45x | — |
| Vietnamese | 3.29x | 1.93x | 1.25x | 2.25x | 1.04x | 1.16x | 1.08x | 1.22x | 1.53x | 1.18x | 1.93x | 1.67x | 1.09x | 1.09x | 1.22x | 1.08x | 1.12x | 1.18x | 1.20x | 1.25x | 1.16x | 0.76x |
| Italian | 1.67x | 1.39x | 1.27x | 1.40x | 1.41x | 1.39x | 1.13x | 1.21x | 1.17x | 1.38x | 1.39x | 1.33x | 1.16x | 1.16x | 1.21x | 1.16x | 1.19x | 1.38x | 1.30x | 1.27x | 1.39x | — |
| Turkish | 1.88x | 1.51x | 1.21x | 1.71x | 1.57x | 1.16x | 1.10x | 1.26x | 0.93x | 1.31x | 1.51x | 1.58x | 1.09x | 1.09x | 1.26x | 1.08x | 1.16x | 1.31x | 1.31x | 1.21x | 1.16x | — |
| German | 1.79x | 1.37x | 1.17x | 1.38x | 1.49x | 1.37x | 1.12x | 1.18x | 1.09x | 1.34x | 1.37x | 1.32x | 1.19x | 1.19x | 1.18x | 1.17x | 1.17x | 1.34x | 1.27x | 1.17x | 1.37x | — |
| Malay | 1.76x | 1.39x | 1.16x | 1.66x | 0.98x | 1.38x | 1.02x | 1.25x | 1.00x | 1.39x | 1.39x | 1.25x | 1.11x | 1.11x | 1.25x | 1.05x | 1.12x | 1.39x | 1.38x | 1.16x | 1.38x | — |
| Dutch | 1.65x | 1.34x | 1.10x | 1.35x | 1.47x | 1.33x | 1.11x | 1.22x | 1.03x | 1.33x | 1.34x | 1.26x | 1.12x | 1.12x | 1.22x | 1.15x | 1.16x | 1.33x | 1.27x | 1.10x | 1.33x | — |
| Spanish | 1.73x | 1.34x | 1.16x | 1.41x | 1.09x | 1.34x | 1.10x | 1.17x | 1.17x | 1.33x | 1.34x | 1.31x | 1.13x | 1.13x | 1.17x | 1.12x | 1.15x | 1.33x | 1.25x | 1.16x | 1.34x | — |
| Indonesian | 1.73x | 1.34x | 1.13x | 1.62x | 0.92x | 1.34x | 0.97x | 1.22x | 0.98x | 1.34x | 1.34x | 1.20x | 1.04x | 1.04x | 1.22x | 1.00x | 1.08x | 1.34x | 1.32x | 1.13x | 1.34x | — |
| Japanese | 2.12x | 1.66x | 1.29x | 1.65x | 1.39x | 1.12x | 0.84x | 1.13x | 0.76x | 1.08x | 1.66x | 1.13x | 0.99x | 0.99x | 1.13x | 0.92x | 1.07x | 1.08x | 1.17x | 1.29x | 1.12x | — |
| Portuguese | 1.65x | 1.28x | 1.08x | 1.37x | 1.01x | 1.28x | 1.06x | 1.12x | 1.15x | 1.26x | 1.28x | 1.24x | 1.05x | 1.05x | 1.12x | 1.08x | 1.09x | 1.26x | 1.21x | 1.08x | 1.28x | — |
| Chinese | 2.96x | 1.68x | 1.12x | 1.46x | 0.78x | 1.16x | 1.00x | 1.30x | 0.83x | 0.94x | 1.68x | 0.87x | 0.97x | 0.97x | 1.29x | 0.99x | 0.97x | 0.94x | 0.89x | 1.12x | 1.16x | — |

> These languages have no `test` split in OPUS-100 and were measured on another split: Armenian (`train`), Yoruba (`train`). Their text is not held out and, being lower-resource pairs, is likely noisier — treat those rows as indicative rather than precise.

> Fewer than 500 pairs survived filtering for: Igbo (177), Kannada (166), Khmer (308), Pashto (176), Punjabi (271), Zulu (263). Their figures rest on a smaller sample than the rest.

## Cheapest vs most expensive tokenizer

`Overpay` is how much more the worst tokenizer costs than the best one for the same text.

| Language | Cheapest | Tax | Most expensive | Tax | Overpay |
|---|---|---:|---|---:|---:|
| Khmer | Aya 101 | 1.38x | Mistral Nemo (Tekken) | 11.66x | **8.4x** |
| Burmese | Aya 101 | 1.38x | GLM-4.5 | 9.31x | **6.8x** |
| Kannada | BLOOM | 1.51x | Llama 3 | 8.82x | **5.8x** |
| Amharic | Aya 101 | 1.50x | Llama 3 | 6.57x | **4.4x** |
| Gujarati | BLOOM | 1.46x | Mistral 7B v0.3 | 8.51x | **5.8x** |
| Sinhala | Aya 101 | 1.25x | Mistral Nemo (Tekken) | 9.04x | **7.2x** |
| Punjabi | BLOOM | 1.48x | Mistral 7B v0.3 | 9.02x | **6.1x** |
| Malayalam | Aya 101 | 1.17x | Mistral 7B v0.3 | 8.77x | **7.5x** |
| Tamil | Aya 101 | 1.34x | Llama 3 | 7.47x | **5.6x** |
| Telugu | BLOOM | 1.23x | GPT-3.5 / GPT-4 (cl100k) | 6.65x | **5.4x** |
| Kurdish | Aya 101 | 2.26x | Mistral 7B v0.3 | 5.59x | **2.5x** |
| Armenian | Aya 101 | 1.48x | GLM-4.5 | 7.34x | **5.0x** |
| Yoruba | Aya 101 | 2.52x | Mistral Small 3 | 5.26x | **2.1x** |
| Georgian | Aya 101 | 1.96x | GLM-4.5 | 5.57x | **2.8x** |
| Bengali | Gemma 3 | 1.17x | GLM-4.5 | 5.31x | **4.5x** |
| Nepali | BLOOM | 1.34x | GPT-3.5 / GPT-4 (cl100k) | 4.92x | **3.7x** |
| Uzbek | Aya 101 | 1.56x | GPT-3.5 / GPT-4 (cl100k) | 3.81x | **2.4x** |
| Marathi | BLOOM | 1.23x | GPT-3.5 / GPT-4 (cl100k) | 4.29x | **3.5x** |
| Hindi | BLOOM | 1.29x | GLM-4.5 | 4.39x | **3.4x** |
| Pashto | Aya 101 | 1.61x | Mistral 7B v0.3 | 4.14x | **2.6x** |
| Igbo | Aya 101 | 1.85x | Mistral Small 3 | 2.62x | **1.4x** |
| Urdu | BLOOM | 1.14x | GPT-3.5 / GPT-4 (cl100k) | 3.71x | **3.3x** |
| Greek | Aya 101 | 1.35x | Mistral 7B v0.3 | 3.91x | **2.9x** |
| Kazakh | Aya 101 | 1.06x | GPT-3.5 / GPT-4 (cl100k) | 2.93x | **2.8x** |
| Thai | Aya 101 | 0.79x | BLOOM | 3.24x | **4.1x** |
| Zulu | Aya 101 | 1.38x | Mistral 7B v0.3 | 2.09x | **1.5x** |
| Xhosa | Aya 101 | 1.30x | Mistral 7B v0.3 | 2.03x | **1.6x** |
| Persian | Aya 101 | 1.26x | Mistral 7B v0.3 | 3.44x | **2.7x** |
| Hebrew | Aya 101 | 1.07x | GLM-4.5 | 2.83x | **2.6x** |
| Hausa | Aya 101 | 1.36x | GPT-3.5 / GPT-4 (cl100k) | 1.94x | **1.4x** |
| Arabic | BLOOM | 1.01x | Mistral 7B v0.3 | 2.99x | **3.0x** |
| Russian | Llama 4 Scout | 1.15x | BLOOM | 2.28x | **2.0x** |
| Ukrainian | Aya 101 | 1.13x | GPT-3.5 / GPT-4 (cl100k) | 2.08x | **1.8x** |
| Afrikaans | Aya 101 | 1.18x | BLOOM | 1.58x | **1.3x** |
| French | BLOOM | 1.14x | Mistral 7B v0.3 | 1.50x | **1.3x** |
| Korean | Mistral Small 3 | 1.00x | BLOOM | 2.10x | **2.1x** |
| Polish | Aya 101 | 1.06x | BLOOM | 1.67x | **1.6x** |
| Vietnamese | PhoBERT v2 (Vietnamese-only) | 0.76x | Mistral 7B v0.3 | 2.25x | **2.9x** |
| Italian | Gemma 2 | 1.13x | BLOOM | 1.41x | **1.2x** |
| Turkish | Aya 101 | 0.93x | Mistral 7B v0.3 | 1.71x | **1.8x** |
| German | Aya 101 | 1.09x | BLOOM | 1.49x | **1.4x** |
| Malay | BLOOM | 0.98x | Mistral 7B v0.3 | 1.66x | **1.7x** |
| Dutch | Aya 101 | 1.03x | BLOOM | 1.47x | **1.4x** |
| Spanish | BLOOM | 1.09x | Mistral 7B v0.3 | 1.41x | **1.3x** |
| Indonesian | BLOOM | 0.92x | Mistral 7B v0.3 | 1.62x | **1.8x** |
| Japanese | Aya 101 | 0.76x | GPT-3.5 / GPT-4 (cl100k) | 1.66x | **2.2x** |
| Portuguese | BLOOM | 1.01x | Mistral 7B v0.3 | 1.37x | **1.4x** |
| Chinese | BLOOM | 0.78x | GPT-3.5 / GPT-4 (cl100k) | 1.68x | **2.2x** |

## Effective context window

English content that fits in a nominal 128,000-token window, expressed in tokens of that content's English original.

| Language | Best case | Worst case |
|---|---:|---:|
| Khmer | 92,626 tokens | 10,976 tokens |
| Burmese | 92,847 tokens | 13,745 tokens |
| Kannada | 84,521 tokens | 14,512 tokens |
| Amharic | 85,350 tokens | 19,482 tokens |
| Gujarati | 87,815 tokens | 15,038 tokens |
| Sinhala | 102,040 tokens | 14,161 tokens |
| Punjabi | 86,433 tokens | 14,192 tokens |
| Malayalam | 109,457 tokens | 14,603 tokens |
| Tamil | 95,408 tokens | 17,144 tokens |
| Telugu | 103,685 tokens | 19,255 tokens |
| Kurdish | 56,519 tokens | 22,890 tokens |
| Armenian | 86,767 tokens | 17,438 tokens |
| Yoruba | 50,695 tokens | 24,323 tokens |
| Georgian | 65,242 tokens | 22,977 tokens |
| Bengali | 109,121 tokens | 24,104 tokens |
| Nepali | 95,216 tokens | 26,021 tokens |
| Uzbek | 81,940 tokens | 33,626 tokens |
| Marathi | 104,327 tokens | 29,825 tokens |
| Hindi | 98,879 tokens | 29,129 tokens |
| Pashto | 79,577 tokens | 30,915 tokens |
| Igbo | 69,177 tokens | 48,873 tokens |
| Urdu | 112,646 tokens | 34,493 tokens |
| Greek | 94,941 tokens | 32,739 tokens |
| Kazakh | 120,493 tokens | 43,635 tokens |
| Thai | 161,922 tokens | 39,518 tokens |
| Zulu | 93,070 tokens | 61,384 tokens |
| Xhosa | 98,310 tokens | 63,144 tokens |
| Persian | 101,756 tokens | 37,195 tokens |
| Hebrew | 119,670 tokens | 45,220 tokens |
| Hausa | 94,263 tokens | 65,847 tokens |
| Arabic | 126,883 tokens | 42,766 tokens |
| Russian | 111,546 tokens | 56,194 tokens |
| Ukrainian | 112,904 tokens | 61,579 tokens |
| Afrikaans | 108,649 tokens | 81,058 tokens |
| French | 112,775 tokens | 85,447 tokens |
| Korean | 128,475 tokens | 61,027 tokens |
| Polish | 120,880 tokens | 76,867 tokens |
| Vietnamese | 167,648 tokens | 56,980 tokens |
| Italian | 113,274 tokens | 90,941 tokens |
| Turkish | 137,427 tokens | 74,858 tokens |
| German | 117,463 tokens | 86,015 tokens |
| Malay | 130,372 tokens | 76,978 tokens |
| Dutch | 124,223 tokens | 87,169 tokens |
| Spanish | 117,636 tokens | 90,805 tokens |
| Indonesian | 139,236 tokens | 79,232 tokens |
| Japanese | 169,289 tokens | 77,234 tokens |
| Portuguese | 127,198 tokens | 93,731 tokens |
| Chinese | 164,228 tokens | 76,258 tokens |

## Methodology

- Every number compares **aligned translations of the same sentence**, so differences reflect tokenizer efficiency rather than differing content.
- Tax is aggregate: total target tokens / total English tokens across all pairs. Per-sentence median and p90 are in the JSON output.
- Special tokens and chat templates are excluded; only content is counted.
- OPUS-100 is crawled data, so pairs are filtered for length, alignment plausibility, duplicates, and untranslated rows before counting.
- Cells where more than 1% of tokens are unknown are marked lossy and excluded from rankings: a tokenizer that drops characters can post a low token count while destroying the text.
- Monolingual tokenizers are only measured against the language they target.
- Historical tokenizers appear in the matrix but not in the rankings: GPT-2 is the worst option for every language, which is true and useless for choosing between tokenizers shipping today.

Full limitations: [`docs/methodology-and-limitations.md`](docs/methodology-and-limitations.md).
