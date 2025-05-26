"""
Module for secure serialization and deserialization of Money objects.

This module provides functions to safely convert Money objects to and from
various serialized formats (JSON, dictionaries) with appropriate validation.
"""

import json
from decimal import Decimal
from typing import Any, Dict, Optional, Type, TypeVar, cast

from moneyx.core import Money
from moneyx.exceptions import SerializationError

# Type variable for Money class
T = TypeVar("T", bound="Money")

# We need to import Money inside the functions to avoid circular imports
# The Money class will be imported only when needed


def to_dict(money: Any) -> Dict[str, str]:
    """
    Convert a Money object to a dictionary representation.

    Args:
        money: A Money object

    Returns:
        Dictionary with amount, currency, and rounding mode

    Example:
        >>> from moneyx import Money
        >>> money = Money("10.50", "USD")
        >>> to_dict(money)
        {'amount': '10.50', 'currency': 'USD', 'rounding': 'HALF_UP'}
    """
    return {
        "amount": str(money.amount),
        "currency": money.currency.code,
        "rounding": money.rounding_mode,
    }


def from_dict(cls: Type[T], data: Dict[str, Any]) -> T:
    """
    Create a Money object from a dictionary.

    Args:
        cls: The Money class
        data: Dictionary containing amount, currency, and optional rounding

    Returns:
        New Money object

    Raises:
        SerializationError: If the dictionary is missing required fields or has invalid data

    Example:
        >>> from moneyx import Money
        >>> data = {'amount': '10.50', 'currency': 'USD', 'rounding': 'HALF_UP'}
        >>> from_dict(Money, data)
        <Money 10.50 USD>
    """
    # Validate required fields
    if not isinstance(data, dict):
        raise SerializationError(f"Expected dictionary, got {type(data).__name__}")

    required_fields = ["amount", "currency"]
    for field in required_fields:
        if field not in data:
            raise SerializationError(f"Missing required field: {field}")

    # Validate field types
    amount_str = data["amount"]
    currency_code = data["currency"]

    if not isinstance(amount_str, (str, int, float, Decimal)):
        raise SerializationError(
            f"Amount must be numeric or string, got {type(amount_str).__name__}",
        )

    if not isinstance(currency_code, str):
        raise SerializationError(
            f"Currency code must be string, got {type(currency_code).__name__}",
        )

    # Get optional rounding mode
    rounding_mode = data.get("rounding", "HALF_UP")
    if not isinstance(rounding_mode, str):
        raise SerializationError(
            f"Rounding mode must be string, got {type(rounding_mode).__name__}",
        )

    # Validate rounding mode
    valid_rounding_modes = [
        "HALF_UP",
        "HALF_DOWN",
        "BANKERS",
        "DOWN",
        "UP",
        "CEILING",
        "FLOOR",
        "HALF_ODD",
        "HALF_TOWARDS_ZERO",
        "HALF_AWAY_FROM_ZERO",
    ]
    if rounding_mode not in valid_rounding_modes:
        raise SerializationError(f"Invalid rounding mode: {rounding_mode}")

    # Create Money object with validated data
    try:
        # Import here to avoid circular imports
        from moneyx.core import Money

        return cast(
            T,
            Money(
                amount=amount_str,
                currency=currency_code,
                rounding=rounding_mode,  # type: ignore
            ),
        )
    except Exception as e:
        raise SerializationError(f"Failed to create Money object: {e!s}") from e


def to_json(money: Any, indent: Optional[int] = None) -> str:
    """
    Convert a Money object to a JSON string.

    Args:
        money: A Money object
        indent: Optional indentation for pretty-printing

    Returns:
        JSON string representation

    Example:
        >>> from moneyx import Money
        >>> money = Money("10.50", "USD")
        >>> to_json(money)
        '{"amount": "10.50", "currency": "USD", "rounding": "HALF_UP"}'
    """
    try:
        return json.dumps(to_dict(money), indent=indent)
    except Exception as e:
        raise SerializationError(f"Failed to serialize to JSON: {e!s}") from e


def from_json(cls: Type[T], json_str: str) -> T:
    """
    Create a Money object from a JSON string.

    Args:
        cls: The Money class
        json_str: JSON string representation

    Returns:
        New Money object

    Raises:
        SerializationError: If the JSON is invalid or missing required fields

    Example:
        >>> from moneyx import Money
        >>> json_str = '{"amount": "10.50", "currency": "USD", "rounding": "HALF_UP"}'
        >>> from_json(Money, json_str)
        <Money 10.50 USD>
    """
    try:
        data = json.loads(json_str)
        return from_dict(cls, data)
    except json.JSONDecodeError as e:
        raise SerializationError(f"Invalid JSON: {e!s}") from e
    except Exception as e:
        raise SerializationError(f"Failed to deserialize from JSON: {e!s}") from e
