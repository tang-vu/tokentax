"""The data model a benchmark run produces.

Separate from :mod:`benchmark` because the reporting and ranking modules need
these types but have no business depending on the measurement engine — they
render results, whether those came from a fresh run or from a JSON file written
months ago.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field


@dataclass
class Measurement:
    """Result of one (tokenizer, language) cell."""

    tokenizer: str
    tokenizer_label: str
    language: str
    language_name: str
    pairs: int
    english_tokens: int
    target_tokens: int
    tax: float  # aggregate target/english token ratio
    median_ratio: float  # per-sentence median, robustness check
    p90_ratio: float
    target_tokens_per_char: float
    unknown_rate: float = 0.0
    lossy: bool = False
    legacy: bool = False
    # Split the pairs actually came from. Differs from the requested split when
    # a low-resource language ships only a train split.
    split: str = "test"


@dataclass
class BenchmarkRun:
    """A full sweep plus the metadata needed to interpret and reproduce it."""

    measurements: list[Measurement] = field(default_factory=list)
    skipped: dict[str, str] = field(default_factory=dict)
    samples_requested: int = 0
    corpus_source: str = "opus-100"
    corpus_name: str = "Helsinki-NLP/opus-100"
    corpus_split: str = "test"
    generated_at: str = ""

    def to_dict(self) -> dict:
        return {
            "generated_at": self.generated_at,
            "corpus": {
                "source": self.corpus_source,
                "name": self.corpus_name,
                "split": self.corpus_split,
                "samples_requested": self.samples_requested,
            },
            "skipped": self.skipped,
            "measurements": [asdict(m) for m in self.measurements],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "BenchmarkRun":
        """Rebuild a run from its JSON form, so reports can be re-rendered
        without repeating the measurement pass."""
        corpus_info = data.get("corpus", {})
        return cls(
            measurements=[Measurement(**m) for m in data.get("measurements", [])],
            skipped=data.get("skipped", {}),
            samples_requested=corpus_info.get("samples_requested", 0),
            corpus_source=corpus_info.get("source", "opus-100"),
            corpus_name=corpus_info.get("name", "Helsinki-NLP/opus-100"),
            corpus_split=corpus_info.get("split", "test"),
            generated_at=data.get("generated_at", ""),
        )

    def for_tokenizer(self, key: str) -> list[Measurement]:
        return [m for m in self.measurements if m.tokenizer == key]

    def for_language(self, code: str) -> list[Measurement]:
        return [m for m in self.measurements if m.language == code]
