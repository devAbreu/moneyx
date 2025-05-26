"""Tests for the bulk operations module."""

from decimal import Decimal

import pytest

from moneyx import Money
from moneyx.bulk import bulk_add, bulk_allocate, bulk_multiply, bulk_with_tax


class TestBulkOperations:
    """Test suite for bulk operations on Money objects."""

    def test_bulk_multiply(self):
        """Test bulk multiplication of Money objects."""
        # Setup
        money_objects = [
            Money("10.00", "USD"),
            Money("20.00", "USD"),
            Money("30.00", "USD"),
        ]
        multipliers = [2, 3, 1]

        # Execute
        results = bulk_multiply(money_objects, multipliers)

        # Verify
        assert len(results) == len(money_objects)
        assert results[0].amount == Decimal("20.00")
        assert results[1].amount == Decimal("60.00")
        assert results[2].amount == Decimal("30.00")

        # Check currencies are preserved
        for i, result in enumerate(results):
            assert result.currency.code == money_objects[i].currency.code
            assert result.rounding_mode == money_objects[i].rounding_mode

    def test_bulk_multiply_with_different_lengths(self):
        """Test bulk multiplication with mismatched lengths raises ValueError."""
        money_objects = [Money("10.00", "USD"), Money("20.00", "USD")]
        multipliers = [2, 3, 4]

        with pytest.raises(ValueError):
            bulk_multiply(money_objects, multipliers)

    def test_bulk_add(self):
        """Test bulk addition of Money objects."""
        # Setup
        money_objects = [
            Money("10.50", "USD"),
            Money("20.75", "USD"),
            Money("5.99", "USD"),
        ]

        # Execute
        result = bulk_add(money_objects)

        # Verify
        assert result.amount == Decimal("37.24")
        assert result.currency.code == "USD"
        assert result.rounding_mode == money_objects[0].rounding_mode

    def test_bulk_add_empty_sequence(self):
        """Test bulk addition with empty sequence raises ValueError."""
        with pytest.raises(ValueError):
            bulk_add([])

    def test_bulk_add_different_currencies(self):
        """Test bulk addition with different currencies raises ValueError."""
        money_objects = [
            Money("10.00", "USD"),
            Money("20.00", "EUR"),
            Money("30.00", "USD"),
        ]

        with pytest.raises(ValueError):
            bulk_add(money_objects)

    def test_bulk_add_with_currency_code(self):
        """Test bulk addition with specified currency code."""
        # Setup
        money_objects = [
            Money("10.50", "USD"),
            Money("20.75", "USD"),
            Money("5.99", "USD"),
        ]

        # Execute
        result = bulk_add(money_objects, currency_code="USD")

        # Verify
        assert result.amount == Decimal("37.24")
        assert result.currency.code == "USD"

    def test_bulk_allocate(self):
        """Test bulk allocation of Money objects."""
        # Setup
        money = Money("100.00", "USD")
        allocations = [1, 2, 3, 4]  # Ratio 1:2:3:4

        # Execute
        results = bulk_allocate(money, allocations)

        # Verify
        assert len(results) == len(allocations)
        assert results[0].amount == Decimal("10.00")
        assert results[1].amount == Decimal("20.00")
        assert results[2].amount == Decimal("30.00")
        assert results[3].amount == Decimal("40.00")

        # Check sum equals original amount
        total = sum(result.amount for result in results)
        assert total == money.amount

    def test_bulk_allocate_empty_sequence(self):
        """Test bulk allocation with empty sequence returns empty list."""
        money = Money("100.00", "USD")
        results = bulk_allocate(money, [])
        assert results == []

    def test_bulk_allocate_zero_total(self):
        """Test bulk allocation with zero total raises ValueError."""
        money = Money("100.00", "USD")
        allocations = [0, 0, 0]

        with pytest.raises(ValueError):
            bulk_allocate(money, allocations)

    def test_bulk_allocate_negative_weights(self):
        """Test bulk allocation with negative weights raises ValueError."""
        money = Money("100.00", "USD")
        allocations = [10, -5, 5]  # One negative weight

        with pytest.raises(ValueError) as exc_info:
            bulk_allocate(money, allocations)
        assert "Allocation weights cannot be negative" in str(exc_info.value)

    def test_bulk_with_tax(self):
        """Test bulk tax addition to Money objects."""
        # Setup
        money_objects = [
            Money("10.00", "USD"),
            Money("20.00", "USD"),
            Money("30.00", "USD"),
        ]
        tax_rate = 10  # 10%

        # Execute
        results = bulk_with_tax(money_objects, tax_rate)

        # Verify
        assert len(results) == len(money_objects)
        assert results[0].amount == Decimal("11.00")
        assert results[1].amount == Decimal("22.00")
        assert results[2].amount == Decimal("33.00")

        # Check currencies are preserved
        for i, result in enumerate(results):
            assert result.currency.code == money_objects[i].currency.code
            assert result.rounding_mode == money_objects[i].rounding_mode
