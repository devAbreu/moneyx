"""Benchmark tests for the moneyx library."""

import random
from decimal import Decimal

import pytest

from moneyx import Money
from moneyx.rounding import RoundingMode


@pytest.fixture
def random_usd_amounts():
    """Generate a list of random USD amounts."""
    return [str(Decimal(random.randint(1, 10000)) / 100) for _ in range(1000)]


def test_money_creation(benchmark, random_usd_amounts):
    """Benchmark Money object creation."""

    def create_money():
        return [Money(amount, "USD") for amount in random_usd_amounts[:100]]

    result = benchmark(create_money)
    assert len(result) == 100


def test_money_addition(benchmark):
    """Benchmark Money addition operations."""
    money_objects = [Money(str(i), "USD") for i in range(1, 101)]

    def add_money():
        result = Money("0", "USD")
        for m in money_objects:
            result = result.add(m)
        return result

    result = benchmark(add_money)
    assert result.amount == Decimal("5050")  # Sum of 1 to 100


def test_money_formatting(benchmark):
    """Benchmark Money formatting."""
    money = Money("1234.56", "USD")

    def format_money():
        return [money.format() for _ in range(1000)]

    result = benchmark(format_money)
    assert len(result) == 1000
    assert all(r == "$1,234.56" for r in result)


def test_allocation(benchmark):
    """Benchmark Money allocation."""
    money = Money("1000.00", "USD")
    weights = [3, 7, 5, 1, 4]

    def allocate_money():
        return money.allocate(weights)

    result = benchmark(allocate_money)
    assert len(result) == 5
    assert sum(item.amount for item in result) == Decimal("1000.00")


def test_currency_lookups(benchmark):
    """Benchmark currency lookups."""
    currency_codes = [
        "USD",
        "EUR",
        "GBP",
        "JPY",
        "CHF",
        "CAD",
        "AUD",
        "CNY",
        "HKD",
        "NZD",
    ]

    def lookup_currencies():
        return [Money("10", code) for code in currency_codes]

    result = benchmark(lookup_currencies)
    assert len(result) == 10


def test_rounding_performance(benchmark):
    """Benchmark various rounding modes."""
    amount = "123.456789"
    modes = list(RoundingMode)

    def apply_rounding():
        return [Money(amount, "USD", rounding=mode) for mode in modes]

    result = benchmark(apply_rounding)
    assert len(result) == len(modes)
