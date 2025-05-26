"""Benchmarks for the moneyx library."""

from decimal import Decimal

import pytest

from moneyx import Money
from moneyx.bulk import bulk_add, bulk_allocate, bulk_multiply
from moneyx.rounding import RoundingMode, apply_rounding


@pytest.fixture
def money_objects():
    """Create a list of Money objects for benchmarking."""
    return [
        Money("10.50", "USD"),
        Money("20.75", "USD"),
        Money("5.99", "USD"),
        Money("100.00", "USD"),
        Money("250.50", "USD"),
        Money("7.25", "USD"),
        Money("33.33", "USD"),
        Money("12.99", "USD"),
        Money("45.45", "USD"),
        Money("67.89", "USD"),
    ]


class TestCoreBenchmarks:
    """Benchmark core Money operations."""

    def test_money_creation(self, benchmark):
        """Benchmark creating Money objects."""
        benchmark(lambda: Money("1234.56", "USD"))

    def test_addition(self, benchmark):
        """Benchmark adding two Money objects."""
        a = Money("100.00", "USD")
        b = Money("200.00", "USD")
        benchmark(lambda: a + b)

    def test_subtraction(self, benchmark):
        """Benchmark subtracting two Money objects."""
        a = Money("200.00", "USD")
        b = Money("100.00", "USD")
        benchmark(lambda: a - b)

    def test_multiplication(self, benchmark):
        """Benchmark multiplying Money by a scalar."""
        money = Money("100.00", "USD")
        benchmark(lambda: money * 1.5)

    def test_allocation(self, benchmark):
        """Benchmark allocating Money into parts."""
        money = Money("100.00", "USD")
        benchmark(lambda: money.allocate([1, 2, 3, 4]))


class TestRoundingBenchmarks:
    """Benchmark rounding operations."""

    def test_half_up_rounding(self, benchmark):
        """Benchmark half-up rounding."""
        value = Decimal("100.555")
        benchmark(lambda: apply_rounding(value, RoundingMode.HALF_UP, 2))

    def test_bankers_rounding(self, benchmark):
        """Benchmark banker's rounding."""
        value = Decimal("100.555")
        benchmark(lambda: apply_rounding(value, RoundingMode.BANKERS, 2))

    def test_half_odd_rounding(self, benchmark):
        """Benchmark half-odd rounding."""
        value = Decimal("100.555")
        benchmark(lambda: apply_rounding(value, RoundingMode.HALF_ODD, 2))


class TestBulkOperationsBenchmarks:
    """Benchmark bulk operations."""

    def test_bulk_add(self, benchmark, money_objects):
        """Benchmark bulk addition."""
        benchmark(lambda: bulk_add(money_objects))

    def test_bulk_multiply(self, benchmark, money_objects):
        """Benchmark bulk multiplication."""
        multipliers = [1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0]
        benchmark(lambda: bulk_multiply(money_objects, multipliers))

    def test_bulk_allocate(self, benchmark):
        """Benchmark bulk allocation."""
        money = Money("1000.00", "USD")
        allocations = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        benchmark(lambda: bulk_allocate(money, allocations))


class TestFormattingBenchmarks:
    """Benchmark formatting operations."""

    def test_format(self, benchmark):
        """Benchmark string formatting."""
        money = Money("1234.56", "USD")
        benchmark(lambda: str(money))

    def test_format_locale(self, benchmark):
        """Benchmark locale-specific formatting."""
        money = Money("1234.56", "USD")
        benchmark(lambda: money.format_locale("en_US"))
