"""Tests to improve coverage for missing lines in the codebase."""

from decimal import Decimal

import pytest

from moneyx import Money
from moneyx.bulk import bulk_add, bulk_allocate, bulk_multiply, bulk_with_tax
from moneyx.exceptions import SerializationError
from moneyx.serialization import from_dict, from_json, to_json
from moneyx.rounding import RoundingMode


class TestComparisons:
    """Test suite for Money comparison operations."""

    def test_eq_with_non_money(self):
        """Test equality comparison with non-Money object."""
        money = Money("10.00", "USD")
        assert (money == "not a money") is False
        assert (money == 10) is False
        assert (money is None) is False

    def test_lt_gt_comparisons(self):
        """Test less than and greater than comparisons."""
        money1 = Money("10.00", "USD")
        money2 = Money("20.00", "USD")

        # Test less than
        assert money1 < money2
        assert not money2 < money1

        # Test greater than
        assert money2 > money1
        assert not money1 > money2

        # Test with same values
        money3 = Money("10.00", "USD")
        assert not money1 < money3
        assert not money3 < money1
        assert not money1 > money3
        assert not money3 > money1


class TestSerializationEdgeCases:
    """Test edge cases for serialization and deserialization."""

    def test_serialization_exceptions(self):
        """Test serialization error handling."""

        # Test to_json with invalid object
        class BadObject:
            def __init__(self):
                self.amount = "not serializable"
                self.currency = None

        with pytest.raises(SerializationError) as exc_info:
            to_json(BadObject())
        assert "Failed to serialize to JSON" in str(exc_info.value)

        # Test from_json with invalid JSON
        with pytest.raises(SerializationError) as exc_info:
            from_json(Money, "{invalid json")
        assert "Invalid JSON" in str(exc_info.value)

        # Test from_dict with various validation errors
        with pytest.raises(SerializationError) as exc_info:
            from_dict(Money, {"amount": "10.00", "rounding": 123})
        assert "Missing required field" in str(exc_info.value)

        with pytest.raises(SerializationError) as exc_info:
            from_dict(Money, {"amount": [], "currency": "USD"})
        assert "Amount must be numeric or string" in str(exc_info.value)

        with pytest.raises(SerializationError) as exc_info:
            from_dict(Money, {"amount": "10.00", "currency": 123})
        assert "Currency code must be string" in str(exc_info.value)

        with pytest.raises(SerializationError) as exc_info:
            from_dict(Money, {"amount": "10.00", "currency": "USD", "rounding": 123})
        assert "Rounding mode must be string" in str(exc_info.value)

        # Test general exception during Money creation
        with pytest.raises(SerializationError) as exc_info:
            from_dict(Money, {"amount": "10.00", "currency": "INVALID"})
        assert "Failed to create Money object" in str(exc_info.value)

    def test_json_serialization_full(self):
        """Test the full JSON serialization and deserialization cycle."""
        # Test with a complex Money object
        original = Money("1234.56", "EUR")

        # Serialize to JSON
        json_str = to_json(original, indent=2)

        # Verify JSON string format
        assert "amount" in json_str
        assert "1234.56" in json_str
        assert "EUR" in json_str

        # Deserialize back to Money object
        restored = from_json(Money, json_str)

        # Verify the restoration
        assert restored.amount == original.amount
        assert restored.currency.code == original.currency.code
        assert restored.rounding_mode == original.rounding_mode


class TestOperatorOverloads:
    """Test operator overloads in Money class."""

    def test_add_operator(self):
        """Test the + operator for Money objects."""
        a = Money("10.00", "USD")
        b = Money("20.00", "USD")
        result = a + b
        assert result.amount == Decimal("30.00")
        assert result.currency.code == "USD"

    def test_sub_operator(self):
        """Test the - operator for Money objects."""
        a = Money("30.00", "USD")
        b = Money("10.00", "USD")
        result = a - b
        assert result.amount == Decimal("20.00")
        assert result.currency.code == "USD"

    def test_mul_operator(self):
        """Test the * operator for Money objects."""
        money = Money("10.00", "USD")
        result = money * 3
        assert result.amount == Decimal("30.00")
        assert result.currency.code == "USD"


class TestAdjustRemainder:
    """Test the _adjust_for_remainder method in Money class."""

    def test_adjust_for_remainder_positive(self):
        """Test adjustment for positive remainder."""
        money = Money("100.00", "USD")
        results = [
            Money("33.33", "USD"),
            Money("33.33", "USD"),
            Money("33.33", "USD"),
        ]
        unit = Decimal("0.01")

        # Call the protected method directly
        money._adjust_for_remainder(results, 0, True, unit)

        # Check that the first element was adjusted
        assert results[0].amount == Decimal("33.34")
        assert results[1].amount == Decimal("33.33")
        assert results[2].amount == Decimal("33.33")

    def test_adjust_for_remainder_negative(self):
        """Test adjustment for negative remainder."""
        money = Money("100.00", "USD")
        results = [
            Money("33.34", "USD"),
            Money("33.33", "USD"),
            Money("33.33", "USD"),
        ]
        unit = Decimal("0.01")

        # Call the protected method directly
        money._adjust_for_remainder(results, 0, False, unit)

        # Check that the first element was adjusted
        assert results[0].amount == Decimal("33.33")
        assert results[1].amount == Decimal("33.33")
        assert results[2].amount == Decimal("33.33")


class TestCurrencyAssertions:
    """Test currency assertion methods."""

    def test_assert_same_currency(self):
        """Test the _assert_same_currency method."""
        usd = Money("10.00", "USD")
        eur = Money("10.00", "EUR")

        # Same currency should not raise
        usd._assert_same_currency(Money("20.00", "USD"))

        # Different currency should raise
        with pytest.raises(ValueError) as exc_info:
            usd._assert_same_currency(eur)
        assert "Currency mismatch" in str(exc_info.value)


class TestAdditionalMethods:
    """Test additional methods in Money class."""

    def test_with_tax(self):
        """Test the with_tax method with various tax rates."""
        money = Money("100.00", "USD")

        # Test with zero tax
        result = money.with_tax(0)
        assert result.amount == Decimal("100.00")

        # Test with standard tax
        result = money.with_tax(10)
        assert result.amount == Decimal("110.00")

        # Test with high tax
        result = money.with_tax(100)
        assert result.amount == Decimal("200.00")

        # Test with fractional tax
        result = money.with_tax(7.5)
        assert result.amount == Decimal("107.50")

    def test_extract_tax(self):
        """Test the extract_tax method."""
        with_tax = Money("110.00", "USD")

        result = with_tax.extract_tax(10)

        assert result["base"].amount == Decimal("100.00")
        assert result["tax"].amount == Decimal("10.00")
        assert result["base"].currency.code == "USD"
        assert result["tax"].currency.code == "USD"

    def test_convert_to(self):
        """Test currency conversion."""
        usd = Money("100.00", "USD")

        # Convert to EUR
        eur = usd.convert_to("EUR", 0.85)
        assert eur.amount == Decimal("85.00")
        assert eur.currency.code == "EUR"

        # Convert to JPY (0 decimal places)
        jpy = usd.convert_to("JPY", 110)
        assert jpy.amount == Decimal("11000")
        assert jpy.currency.code == "JPY"

    def test_split_evenly(self):
        """Test the split_evenly method."""
        money = Money("100.00", "USD")

        # Split among 1 person (edge case)
        result = money.split_evenly(1)
        assert len(result) == 1
        assert result[0].amount == Decimal("100.00")

        # Split among 4 people
        result = money.split_evenly(4)
        assert len(result) == 4
        assert result[0].amount == Decimal("25.00")
        assert result[1].amount == Decimal("25.00")
        assert result[2].amount == Decimal("25.00")
        assert result[3].amount == Decimal("25.00")

        # Test with validation
        with pytest.raises(ValueError) as exc_info:
            money.split_evenly(0)
        assert "There must be at least one person" in str(exc_info.value)

    def test_format_locale(self):
        """Test locale-specific formatting."""
        money = Money("1234.56", "USD")

        # Test default US formatting
        result = money.format_locale("en_US")
        assert "$" in result
        assert "1,234.56" in result

        # Test German formatting
        result = money.format_locale("de_DE")
        assert "1.234,56" in result


class TestBulkOperations:
    """Test bulk operations module."""

    def test_bulk_multiply(self):
        """Test bulk multiplication of Money objects."""
        money_objects = [
            Money("10.00", "USD"),
            Money("20.00", "USD"),
            Money("30.00", "USD"),
        ]
        multipliers = [2, 3, 1]

        results = bulk_multiply(money_objects, multipliers)

        assert len(results) == 3
        assert results[0].amount == Decimal("20.00")
        assert results[1].amount == Decimal("60.00")
        assert results[2].amount == Decimal("30.00")

    def test_bulk_add(self):
        """Test bulk addition of Money objects."""
        money_objects = [
            Money("10.50", "USD"),
            Money("20.75", "USD"),
            Money("5.99", "USD"),
        ]

        result = bulk_add(money_objects)

        assert result.amount == Decimal("37.24")
        assert result.currency.code == "USD"

        # Test with currency_code parameter
        result = bulk_add(money_objects, currency_code="USD")
        assert result.amount == Decimal("37.24")
        assert result.currency.code == "USD"

    def test_bulk_allocate(self):
        """Test bulk allocation of money."""
        money = Money("100.00", "USD")
        allocations = [1, 2, 3, 4]  # Ratio 1:2:3:4

        results = bulk_allocate(money, allocations)

        assert len(results) == 4
        assert results[0].amount == Decimal("10.00")
        assert results[1].amount == Decimal("20.00")
        assert results[2].amount == Decimal("30.00")
        assert results[3].amount == Decimal("40.00")

        # Test empty allocations
        results = bulk_allocate(money, [])
        assert results == []

        # Test zero total allocation
        with pytest.raises(ValueError):
            bulk_allocate(money, [0, 0, 0])

    def test_bulk_with_tax(self):
        """Test bulk tax application."""
        money_objects = [
            Money("10.00", "USD"),
            Money("20.00", "USD"),
            Money("30.00", "USD"),
        ]

        results = bulk_with_tax(money_objects, 10)  # 10% tax

        assert len(results) == 3
        assert results[0].amount == Decimal("11.00")
        assert results[1].amount == Decimal("22.00")
        assert results[2].amount == Decimal("33.00")


class TestDistributeRemainder:
    """Test the _distribute_remainder method directly for better coverage."""

    def test_distribute_remainder_negative(self):
        """Test distributing negative remainders to amounts."""
        m = Money("10.00", "USD")
        amounts = [Decimal("3.33"), Decimal("3.33"), Decimal("3.34")]
        unit = Decimal("0.01")
        
        # Call the internal method directly with is_positive=False
        m._distribute_remainder(amounts, 0, False, unit)
        
        # Check that the amount was decreased by the unit
        assert amounts[0] == Decimal("3.32")
        assert amounts[1] == Decimal("3.33")
        assert amounts[2] == Decimal("3.34")
        
    def test_distribute_remainder_positive(self):
        """Test distributing positive remainders to amounts."""
        m = Money("10.00", "USD")
        amounts = [Decimal("3.33"), Decimal("3.33"), Decimal("3.33")]
        unit = Decimal("0.01")
        
        # Call the internal method directly with is_positive=True
        m._distribute_remainder(amounts, 0, True, unit)
        
        # Check that the amount was increased by the unit
        assert amounts[0] == Decimal("3.34")
        assert amounts[1] == Decimal("3.33")
        assert amounts[2] == Decimal("3.33")


class TestValidatePrecision:
    """Test the _validate_precision method directly to increase coverage."""
    
    def test_non_int_exponent_handling(self):
        """Test _validate_precision with non-integer exponents."""
        from decimal import Decimal
        from moneyx.core import Money
        from moneyx.rounding import RoundingMode
        
        m = Money("10.00", "USD")
        
        # Create a Decimal with a non-int exponent
        # We'll mock a non-int exponent by adding a patch
        class MockDecimal(Decimal):
            def as_tuple(self):
                result = super().as_tuple()
                # Return an object with a non-int exponent attribute
                class Tuple:
                    def __init__(self, sign, digits, exponent):
                        self.sign = sign
                        self.digits = digits
                        self.exponent = "n"  # Non-int exponent
                return Tuple(result.sign, result.digits, "n")
        
        # Test the method directly
        amount = MockDecimal("123.456")
        m._validate_precision(amount, m.currency, RoundingMode.HALF_UP)
        # No assertion needed, we just want to make sure it doesn't raise an exception
