# moneyx/__init__.py
import moneyx.bulk as bulk
import moneyx.serialization as serialization
from moneyx.core import Money
from moneyx.currency import Currency
from moneyx.exceptions import (
    InvalidCurrencyError,
    MoneyError,
    PrecisionError,
    SerializationError,
)
from moneyx.rounding import RoundingMode

# Version information - automatically updated by CI/CD or release process
__version__ = "0.1.0"

__all__ = [
    "Currency",
    "InvalidCurrencyError",
    "Money",
    "MoneyError",
    "PrecisionError",
    "RoundingMode",
    "SerializationError",
    "bulk",
    "serialization",
]
