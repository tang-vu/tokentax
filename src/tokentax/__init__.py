"""tokentax — measure the token cost of writing in a language other than English."""

__version__ = "0.1.0"

from .benchmark import BenchmarkRun, Measurement, measure, run
from .corpus import Pair
from .languages import LANGUAGES, Language
from .tokenizer_registry import REGISTRY, TokenizerSpec

__all__ = [
    "BenchmarkRun",
    "LANGUAGES",
    "Language",
    "Measurement",
    "Pair",
    "REGISTRY",
    "TokenizerSpec",
    "measure",
    "run",
]
