# Cross-check: does this replicate on a second corpus?

`Helsinki-NLP/opus-100` (opus-100) versus `google/wmt24pp` (wmt24pp), over the 31 languages both cover.

The first corpus is crawled; the second is professionally translated. They share no text, so agreement is evidence the figures describe tokenizers rather than one dataset's habits.

## Summary

- Cheapest tokenizer agrees for **27 of 31** languages.
- Most expensive agrees for **26 of 31**.
- Median tax drift across all languages: **12%**.

Absolute tax is expected to move between corpora — register and domain differ. A changed *ranking* is the finding that matters, because that is what changes the advice.

## By language

| Language | Pairs (crawled / human) | Tax drift | Cheapest agrees | Dearest agrees |
|---|---|---:|---|---|
| Polish | 500 / 500 | 33% ⚠ | yes | yes |
| Japanese | 500 / 500 | 29% ⚠ | yes | yes |
| Thai | 500 / 500 | 29% ⚠ | yes | **bloom → aya-expanse** |
| Telugu | 500 / 500 | 28% ⚠ | yes | **cl100k → llama3** |
| Korean | 500 / 500 | 27% ⚠ | **mistral-small3 → mistral-nemo** | yes |
| Ukrainian | 500 / 500 | 27% ⚠ | yes | yes |
| Vietnamese | 500 / 500 | 22% | yes | yes |
| Turkish | 500 / 500 | 21% | yes | yes |
| Urdu | 500 / 500 | 20% | yes | yes |
| Malayalam | 500 / 500 | 18% | yes | yes |
| Greek | 500 / 500 | 18% | **aya-101 → aya-expanse** | yes |
| Dutch | 500 / 500 | 17% | yes | yes |
| Hebrew | 500 / 500 | 15% | yes | **glm4.5 → llama3** |
| Hindi | 500 / 500 | 14% | **bloom → gemma3** | yes |
| German | 500 / 500 | 13% | yes | yes |
| Portuguese | 500 / 500 | 12% | yes | yes |
| Indonesian | 500 / 500 | 12% | yes | yes |
| Chinese | 500 / 500 | 11% | **bloom → aya-101** | yes |
| Punjabi | 271 / 500 | 11% | yes | yes |
| Marathi | 500 / 500 | 11% | yes | yes |
| Italian | 500 / 500 | 6% | yes | **bloom → mistral-v3** |
| Tamil | 500 / 500 | 5% | yes | yes |
| Spanish | 500 / 500 | 5% | yes | yes |
| Arabic | 500 / 500 | 4% | yes | yes |
| Russian | 500 / 500 | 3% | yes | yes |
| Kannada | 166 / 500 | 3% | yes | yes |
| Persian | 500 / 500 | 3% | yes | yes |
| Bengali | 500 / 500 | 2% | yes | yes |
| French | 500 / 500 | 2% | yes | yes |
| Zulu | 263 / 500 | 1% | yes | **mistral-v3 → cl100k** |
| Gujarati | 500 / 500 | 1% | yes | yes |
