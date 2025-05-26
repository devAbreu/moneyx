"""
Bulk operations for Money objects.

This module provides functions for performing operations on multiple Money objects
at once, which can be more efficient than working with them individually.
"""

from decimal import Decimal
from typing import List, Optional, Sequence, Union

from moneyx.core import Money
from moneyx.rounding import apply_rounding


def bulk_multiply(
    money_objects: Sequence[Money],
    multipliers: Sequence[Union[int, float, Decimal]],
) -> List[Money]:
    """
    Efficiently multiply multiple Money objects by their corresponding multipliers.

    Args:
        money_objects: A sequence of Money objects
        multipliers: A sequence of multipliers (must be the same length as
            money_objects)

    Returns:
        A list of Money objects, each being the result of multiplying the
        corresponding money_object with its multiplier

    Raises:
        ValueError: If the sequences have different lengths

    Example:
        >>> from moneyx import Money
        >>> from moneyx.bulk import bulk_multiply
        >>> prices = [
        ...     Money("10.00", "USD"),
        ...     Money("20.00", "USD"),
        ...     Money("30.00", "USD")
        ... ]
        >>> quantities = [2, 3, 1]
        >>> results = bulk_multiply(prices, quantities)
        >>> [str(m.amount) for m in results]
        ['20.00', '60.00', '30.00']
    """
    if len(money_objects) != len(multipliers):
        raise ValueError(
            "The money_objects and multipliers sequences must have the same length",
        )

    results = []
    for money, multiplier in zip(money_objects, multipliers):
        results.append(money.multiply(multiplier))

    return results


def bulk_add(
    money_objects: Sequence[Money],
    currency_code: Optional[str] = None,
) -> Money:
    """
    Efficiently sum multiple Money objects.

    All Money objects must have the same currency unless a target currency_code
    is provided.

    Args:
        money_objects: A sequence of Money objects to sum
        currency_code: Optional target currency code. If provided, all amounts will be
                      assumed to be in this currency. If not provided, the currency
                      of the first Money object will be used and all objects must
                      have the same currency.

    Returns:
        A single Money object representing the sum

    Raises:
        ValueError: If the money_objects have different currencies and no
                  currency_code is provided

    Example:
        >>> from moneyx import Money
        >>> from moneyx.bulk import bulk_add
        >>> expenses = [
        ...     Money("10.50", "USD"),
        ...     Money("20.75", "USD"),
        ...     Money("5.99", "USD"),
        ... ]
        >>> total = bulk_add(expenses)
        >>> str(total.amount)
        '37.24'
    """
    if not money_objects:
        raise ValueError("Cannot sum an empty sequence")

    # Determine the currency
    if currency_code is None:
        currency_code = money_objects[0].currency.code
        # Verify all money objects have the same currency
        for money in money_objects:
            if money.currency.code != currency_code:
                raise ValueError(
                    "All Money objects must have the same currency when "
                    "currency_code is not provided",
                )

    # Use the rounding mode of the first Money object
    rounding_mode = money_objects[0].rounding_mode

    # Sum all amounts
    total = Decimal("0")
    for money in money_objects:
        total += money.amount

    return Money(str(total), currency_code, rounding_mode)


def bulk_allocate(
    money: Money,
    allocation_data: Sequence[Union[int, float, Decimal]],
) -> List[Money]:
    """
    Allocate a Money object according to a sequence of ratios.

    This function is similar to Money.allocate() but provides a more convenient
    interface for allocating money according to a sequence of ratios.

    Args:
        money: The Money object to allocate
        allocation_data: A sequence of values representing allocation ratios/weights

    Returns:
        A list of Money objects, each having a portion of the original amount

    Raises:
        ValueError: If allocation_data contains negative values or has all zero values

    Example:
        >>> from moneyx import Money
        >>> from moneyx.bulk import bulk_allocate
        >>> total = Money("100.00", "USD")
        >>> shares = [5, 3, 2]  # Allocate in 5:3:2 ratio
        >>> results = bulk_allocate(total, shares)
        >>> [str(m.amount) for m in results]
        ['50.00', '30.00', '20.00']
    """
    if not allocation_data:
        return []

    total_weight = Decimal("0")
    weights = []

    # Convert all weights to Decimal and validate
    for weight in allocation_data:
        weight_decimal = Decimal(str(weight))
        if weight_decimal < 0:
            raise ValueError("Allocation weights cannot be negative")
        weights.append(weight_decimal)
        total_weight += weight_decimal

    if total_weight == 0:
        raise ValueError("Sum of allocation weights must be greater than zero")

    # Calculate how much money each weight should get
    results = []

    # Calculate the initial allocation
    remaining = money.amount
    minimum_unit = Decimal("0.01")  # The smallest unit we'll distribute

    # First pass: allocate the integer part of each share
    for weight in weights[:-1]:  # Process all but the last weight
        share = (money.amount * weight / total_weight).quantize(minimum_unit)
        results.append(Money(share, money.currency.code, money.rounding_mode))
        remaining -= share

    # The last allocation gets the remaining amount to ensure the sum matches
    # the original
    results.append(Money(remaining, money.currency.code, money.rounding_mode))

    return results


def bulk_with_tax(
    money_objects: Sequence[Money],
    tax_rate_percent: float,
) -> List[Money]:
    """
    Add tax to multiple Money objects at once.

    Args:
        money_objects: A sequence of Money objects
        tax_rate_percent: The tax rate as a percentage (e.g., 10 for 10%)

    Returns:
        A list of Money objects with tax added

    Example:
        >>> from moneyx import Money
        >>> from moneyx.bulk import bulk_with_tax
        >>> prices = [
        ...     Money("10.00", "USD"),
        ...     Money("20.00", "USD"),
        ...     Money("30.00", "USD")
        ... ]
        >>> with_tax = bulk_with_tax(prices, 10)  # Add 10% tax
        >>> [m.amount for m in with_tax]
        [Decimal('11.00'), Decimal('22.00'), Decimal('33.00')]
    """
    results = []

    tax_multiplier = Decimal(str(tax_rate_percent)) / Decimal("100")

    for money in money_objects:
        tax_amount = money.amount * tax_multiplier
        tax_amount = apply_rounding(
            tax_amount,
            money.rounding_mode,
            money.currency.decimals,
        )
        with_tax = money.amount + tax_amount
        results.append(Money(with_tax, money.currency.code, money.rounding_mode))

    return results
