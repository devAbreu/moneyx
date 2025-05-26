"""Property-based tests for the moneyx library using Hypothesis."""

from decimal import Decimal

import pytest
from hypothesis import given
from hypothesis import strategies as st

from moneyx import Money
from moneyx.currency import Currency
from moneyx.exceptions import PrecisionError
from moneyx.rounding import RoundingMode


# Strategies for generating test data
@st.composite
def valid_money_amounts(draw, currency_code="USD"):
    """Generate valid monetary amounts for a given currency."""
    currency = Currency.get(currency_code)

    # Generate a string with valid number of decimal places
    if currency.decimals == 0:
        # For currencies with no decimal places, only generate integers
        return str(draw(st.integers(-10000, 10000)))

    # Generate amount with correct decimal precision
    whole = draw(st.integers(-10000, 10000))
    decimal_part = draw(st.integers(0, 10**currency.decimals - 1))
    decimal_str = str(decimal_part).zfill(currency.decimals)

    return f"{whole}.{decimal_str}"


# Strategy for valid ISO currency codes
currency_codes = st.sampled_from(
    [
        "USD",
        "EUR",
        "GBP",
        "JPY",
        "CAD",
        "AUD",
        "CHF",
        "CNY",
        "SEK",
        "NZD",
        "MXN",
        "SGD",
        "HKD",
        "BRL",
    ],
)


# Strategy that pairs a currency with a valid amount for that currency
@st.composite
def currency_and_amount(draw):
    """Generate a currency code and a valid amount for that currency."""
    curr = draw(currency_codes)
    amt = draw(valid_money_amounts(curr))
    return (curr, amt)


# Strategy for rounding modes
rounding_modes = st.sampled_from(
    [
        RoundingMode.HALF_UP,
        RoundingMode.HALF_DOWN,
        RoundingMode.BANKERS,
        RoundingMode.HALF_ODD,
        RoundingMode.DOWN,
        RoundingMode.UP,
        RoundingMode.CEILING,
        RoundingMode.FLOOR,
        RoundingMode.HALF_TOWARDS_ZERO,
        RoundingMode.HALF_AWAY_FROM_ZERO,
    ],
)

# Strategy for weights in allocation
allocation_weights = st.lists(
    st.integers(1, 100),  # Positive weights
    min_size=1,  # At least one weight
    max_size=10,  # Maximum of 10 weights
)


@given(
    curr_amt=currency_and_amount(),
    rounding=rounding_modes,
)
def test_money_creation(curr_amt, rounding):
    """Test Money creation with various inputs."""
    currency, amount = curr_amt

    money = Money(amount, currency, rounding=rounding)
    assert money.amount == Decimal(amount)
    assert money.currency.code == currency
    assert money.rounding_mode == rounding


@given(
    amount1=valid_money_amounts("USD"),
    amount2=valid_money_amounts("USD"),
)
def test_addition_properties(amount1, amount2):
    """Test mathematical properties of Money addition."""
    a = Money(amount1, "USD")
    b = Money(amount2, "USD")

    # Commutativity: a + b = b + a
    assert a.add(b) == b.add(a)

    # Associativity: (a + b) + c = a + (b + c)
    c = Money("1.00", "USD")
    assert a.add(b).add(c) == a.add(b.add(c))


@given(
    amount=valid_money_amounts("USD"),
    multiplier=st.integers(-100, 100),
)
def test_multiplication_properties(amount, multiplier):
    """Test mathematical properties of Money multiplication."""
    a = Money(amount, "USD")

    # Multiplicative identity: a * 1 = a
    assert a.multiply(1) == a

    # Distributive property: a * (b + c) = a * b + a * c
    b, c = 2, 3
    assert a.multiply(b + c) == a.multiply(b).add(a.multiply(c))


@given(
    amount=valid_money_amounts("USD"),
    weights=allocation_weights,
)
def test_allocation_properties(amount, weights):
    """Test properties of money allocation."""
    money = Money(amount, "USD")
    allocated = money.allocate(weights)

    # Sum of allocated amounts equals original amount
    total = sum(part.amount for part in allocated)
    assert total == money.amount

    # Number of allocations equals number of weights
    assert len(allocated) == len(weights)

    # Allocations preserve currency and rounding mode
    for part in allocated:
        assert part.currency.code == money.currency.code
        assert part.rounding_mode == money.rounding_mode


@given(
    amount=valid_money_amounts("USD"),
    n=st.integers(1, 20),  # Split between 1 and 20 ways
)
def test_split_evenly_properties(amount, n):
    """Test properties of even money splitting."""
    money = Money(amount, "USD")
    splits = money.split_evenly(n)

    # Sum of splits equals original amount
    total = sum(part.amount for part in splits)
    assert total == money.amount

    # Number of splits equals n
    assert len(splits) == n

    # Difference between any two splits is at most one cent
    if n > 1:
        amounts = [part.amount for part in splits]
        diff = max(amounts) - min(amounts)
        assert diff <= Decimal("0.01")


@given(
    amount=st.decimals(
        min_value=-10000,
        max_value=10000,
        allow_nan=False,
        allow_infinity=False,
        places=5,  # More places than USD allows
    ),
)
def test_precision_error(amount):
    """Test that precision errors are raised appropriately."""
    amount_str = str(amount)
    decimal_places = len(amount_str.split(".")[-1]) if "." in amount_str else 0

    # USD allows 2 decimal places
    if decimal_places > 2:
        with pytest.raises(PrecisionError):
            Money(amount_str, "USD")
    else:
        # This should not raise an exception
        Money(amount_str, "USD")


@given(
    amount=valid_money_amounts("USD"),
    tax_rate=st.floats(min_value=0, max_value=100, exclude_min=True),
)
def test_tax_calculations(amount, tax_rate):
    """Test properties of tax calculations."""
    money = Money(amount, "USD")

    # Test with_tax
    with_tax = money.with_tax(tax_rate)
    expected_with_tax = money.amount * (
        Decimal("1") + Decimal(str(tax_rate)) / Decimal("100")
    )
    assert abs(with_tax.amount - expected_with_tax) < Decimal("0.01")

    # Test extract_tax (inverse operation)
    result = with_tax.extract_tax(tax_rate)
    assert abs(result["base"].amount - money.amount) < Decimal("0.01")

    # Tax amount should be the difference
    tax_amount = with_tax.amount - result["base"].amount
    assert abs(tax_amount - result["tax"].amount) < Decimal("0.01")
