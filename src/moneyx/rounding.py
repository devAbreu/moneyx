# moneyx/rounding.py
"""
Rounding utilities for Money objects.

This module provides functionality for rounding decimal values according to
different rounding strategies.

Available rounding modes:
    - HALF_UP: Classic rounding. If the fractional part is >= 0.5, rounds up.
    - HALF_DOWN: If the fractional part is > 0.5, rounds up; if it's exactly 0.5,
      rounds down.
    - BANKERS (HALF_EVEN): Banker's rounding. Rounds to the nearest even number
      when exactly 0.5.
    - HALF_ODD: Rounds to the nearest odd number when exactly 0.5.
    - DOWN: Always truncates (towards zero).
    - UP: Always rounds away from zero.
    - CEILING: Always rounds towards positive infinity.
    - FLOOR: Always rounds towards negative infinity.
    - HALF_TOWARDS_ZERO: If exactly 0.5, rounds towards zero.
    - HALF_AWAY_FROM_ZERO: If exactly 0.5, rounds away from zero.
"""

from decimal import (
    ROUND_CEILING,
    ROUND_DOWN,
    ROUND_FLOOR,
    ROUND_HALF_DOWN,
    ROUND_HALF_EVEN,
    ROUND_HALF_UP,
    ROUND_UP,
    Decimal,
)
from typing import Literal

# Define RoundingModeStr type for mypy
RoundingModeStr = Literal[
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


class RoundingMode:
    """
    Constants for various rounding modes.
    """

    # Standard modes
    HALF_UP: RoundingModeStr = "HALF_UP"  # Classic rounding (if fractional part >= 0.5,
    # rounds up)
    HALF_DOWN: RoundingModeStr = (
        "HALF_DOWN"  # If fractional part > 0.5, rounds up, otherwise down
    )
    BANKERS: RoundingModeStr = "BANKERS"  # Banker's rounding (round half to even)
    HALF_EVEN: RoundingModeStr = "BANKERS"  # Alias for BANKERS
    DOWN: RoundingModeStr = "DOWN"  # Always rounds towards zero (truncation)
    UP: RoundingModeStr = "UP"  # Always rounds away from zero
    CEILING: RoundingModeStr = "CEILING"  # Always rounds towards positive infinity
    FLOOR: RoundingModeStr = "FLOOR"  # Always rounds towards negative infinity

    # Extended modes
    HALF_ODD: RoundingModeStr = "HALF_ODD"  # Round half to odd
    HALF_TOWARDS_ZERO: RoundingModeStr = (
        "HALF_TOWARDS_ZERO"  # If exactly 0.5, round towards zero
    )
    HALF_AWAY_FROM_ZERO: RoundingModeStr = (
        "HALF_AWAY_FROM_ZERO"  # If exactly 0.5, round away from zero
    )


# Mapping of rounding modes to decimal module rounding constants
# Used for modes that have direct Decimal equivalents
_DECIMAL_ROUNDING_MAP = {
    RoundingMode.HALF_UP: ROUND_HALF_UP,
    RoundingMode.HALF_DOWN: ROUND_HALF_DOWN,
    RoundingMode.BANKERS: ROUND_HALF_EVEN,
    RoundingMode.DOWN: ROUND_DOWN,
    RoundingMode.UP: ROUND_UP,
    RoundingMode.CEILING: ROUND_CEILING,
    RoundingMode.FLOOR: ROUND_FLOOR,
}


def _apply_half_odd(value: Decimal, places: int) -> Decimal:
    """
    Apply half-odd rounding.

    If the value is exactly half, round to the nearest odd number.
    Otherwise, round like HALF_UP.

    Args:
        value: The Decimal to round
        places: Number of decimal places to round to

    Returns:
        Rounded Decimal value
    """
    # Shift decimal point to focus on the digit after the target place
    shifted = value * Decimal(10) ** places

    # Get the integer and fractional parts
    int_part = int(shifted)
    frac_part = shifted - int_part

    # Check if we're exactly at 0.5
    if abs(frac_part) == Decimal("0.5"):
        # Round to nearest odd number
        if int_part % 2 == 0:  # If even
            return Decimal(int_part + (1 if value >= 0 else -1)) / Decimal(10) ** places
        else:  # Already odd
            return Decimal(int_part) / Decimal(10) ** places
    else:
        # For non-half cases, use HALF_UP
        return value.quantize(Decimal("0.1") ** places, rounding=ROUND_HALF_UP)


def _apply_half_towards_zero(value: Decimal, places: int) -> Decimal:
    """
    Apply half-towards-zero rounding.

    If the value is exactly half, round towards zero.
    Otherwise, round like HALF_UP.

    Args:
        value: The Decimal to round
        places: Number of decimal places to round to

    Returns:
        Rounded Decimal value
    """
    # Shift decimal point to focus on the digit after the target place
    shifted = value * Decimal(10) ** places

    # Get the integer and fractional parts
    int_part = int(shifted)
    frac_part = shifted - int_part

    # Check if we're exactly at 0.5
    if abs(frac_part) == Decimal("0.5"):
        # Round towards zero
        return Decimal(int_part) / Decimal(10) ** places
    else:
        # For non-half cases, use HALF_UP
        return value.quantize(Decimal("0.1") ** places, rounding=ROUND_HALF_UP)


def _apply_half_away_from_zero(value: Decimal, places: int) -> Decimal:
    """
    Apply half-away-from-zero rounding.

    If the value is exactly half, round away from zero.
    Otherwise, round like HALF_UP.

    Args:
        value: The Decimal to round
        places: Number of decimal places to round to

    Returns:
        Rounded Decimal value
    """
    # Shift decimal point to focus on the digit after the target place
    shifted = value * Decimal(10) ** places

    # Get the integer and fractional parts
    int_part = int(shifted)
    frac_part = shifted - int_part

    # Check if we're exactly at 0.5
    if abs(frac_part) == Decimal("0.5"):
        # Round away from zero
        return Decimal(int_part + (1 if value >= 0 else -1)) / Decimal(10) ** places
    else:
        # For non-half cases, use HALF_UP
        return value.quantize(Decimal("0.1") ** places, rounding=ROUND_HALF_UP)


def apply_rounding(value: Decimal, mode: RoundingModeStr, places: int) -> Decimal:
    """
    Round a Decimal value according to the specified rounding mode.

    Args:
        value: The Decimal value to round
        mode: The rounding mode to use, one of the RoundingMode constants
        places: Number of decimal places to round to

    Returns:
        Rounded Decimal value

    Raises:
        ValueError: If the rounding mode is not recognized

    Examples:
        apply_rounding(Decimal('2.5'), RoundingMode.HALF_UP, 0) -> Decimal('3')
        apply_rounding(Decimal('2.5'), RoundingMode.BANKERS, 0) -> Decimal('2')
        apply_rounding(Decimal('-2.5'), RoundingMode.HALF_TOWARDS_ZERO, 0) ->
            Decimal('-2')
        apply_rounding(Decimal('1.234'), RoundingMode.UP, 2) -> Decimal('1.24')
    """
    # If the value is already correctly rounded, just return it
    exponent = value.as_tuple().exponent

    # Handle special cases with Decimal exponents
    if isinstance(exponent, int) and (
        exponent == -places or (exponent >= 0 and places == 0)
    ):
        return value

    # Handle the extended rounding modes
    if mode == RoundingMode.HALF_ODD:
        return _apply_half_odd(value, places)
    elif mode == RoundingMode.HALF_TOWARDS_ZERO:
        return _apply_half_towards_zero(value, places)
    elif mode == RoundingMode.HALF_AWAY_FROM_ZERO:
        return _apply_half_away_from_zero(value, places)

    # Handle the standard modes that map directly to Decimal rounding
    if mode in _DECIMAL_ROUNDING_MAP:
        return value.quantize(
            Decimal("0.1") ** places,
            rounding=_DECIMAL_ROUNDING_MAP[mode],
        )

    # If we get here, the mode is not recognized
    raise ValueError(f"Unknown rounding mode: {mode}")
