class MoneyError(Exception):
    """General error for the moneyx library."""

    pass


class InvalidCurrencyError(MoneyError):
    """Unknown or invalid currency."""

    pass


class PrecisionError(MoneyError):
    """More decimal places than allowed for the currency."""

    pass


class SerializationError(MoneyError):
    """Error raised when serialization or deserialization fails."""

    pass
