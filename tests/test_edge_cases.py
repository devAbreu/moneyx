"""Tests for edge cases to improve coverage in currency.py and rounding.py."""

from decimal import Decimal

import pytest

from moneyx.currency import Currency
from moneyx.exceptions import InvalidCurrencyError
from moneyx.rounding import RoundingMode, apply_rounding


class TestCurrencyEdgeCases:
    """Test edge cases in the Currency class."""

    def test_get_by_country(self):
        """Test getting currencies by country name."""
        # Test with a country that uses multiple currencies
        currencies = Currency.get_by_country("BHUTAN")
        assert len(currencies) >= 2

        # Verify we have both the expected currencies
        currency_codes = [c.code for c in currencies]
        assert "BTN" in currency_codes
        assert "INR" in currency_codes

        # Test with a country that doesn't exist
        empty_currencies = Currency.get_by_country("NONEXISTENT_COUNTRY")
        assert len(empty_currencies) == 0

        # Test case insensitivity
        currencies = Currency.get_by_country("bhutan")
        assert len(currencies) >= 2

    def test_get_by_number(self):
        """Test getting currency by numeric code."""
        # Get USD by its numeric code
        usd = Currency.get_by_number("840")
        assert usd.code == "USD"
        assert usd.name == "US Dollar"

        # Test with nonexistent number
        with pytest.raises(InvalidCurrencyError) as exc_info:
            Currency.get_by_number("999999")
        assert "Unknown currency numeric code" in str(exc_info.value)


class TestRoundingEdgeCases:
    """Test edge cases in the rounding module."""

    def test_unknown_rounding_mode(self):
        """Test that an unknown rounding mode raises an error."""
        with pytest.raises(ValueError) as exc_info:
            apply_rounding(Decimal("1.5"), "INVALID_MODE", 2)
        assert "Unknown rounding mode" in str(exc_info.value)

    def test_half_odd_rounding(self):
        """Test the half odd rounding mode."""
        # Test with positive numbers
        assert apply_rounding(Decimal("2.5"), RoundingMode.HALF_ODD, 0) == Decimal("3")
        assert apply_rounding(Decimal("3.5"), RoundingMode.HALF_ODD, 0) == Decimal("3")
        assert apply_rounding(Decimal("4.5"), RoundingMode.HALF_ODD, 0) == Decimal("5")

        # Test with negative numbers
        assert apply_rounding(Decimal("-2.5"), RoundingMode.HALF_ODD, 0) == Decimal(
            "-3",
        )
        assert apply_rounding(Decimal("-3.5"), RoundingMode.HALF_ODD, 0) == Decimal(
            "-3",
        )

        # Test with decimal places
        assert apply_rounding(Decimal("1.25"), RoundingMode.HALF_ODD, 1) == Decimal(
            "1.3",
        )
        assert apply_rounding(Decimal("1.35"), RoundingMode.HALF_ODD, 1) == Decimal(
            "1.3",
        )

        # Test with non-tie cases (should use HALF_UP)
        assert apply_rounding(Decimal("2.4"), RoundingMode.HALF_ODD, 0) == Decimal("2")
        assert apply_rounding(Decimal("2.6"), RoundingMode.HALF_ODD, 0) == Decimal("3")

    def test_special_decimal_cases(self):
        """Test special cases for decimal rounding."""
        # Test already correctly rounded values
        assert apply_rounding(Decimal("2.00"), RoundingMode.HALF_UP, 2) == Decimal("2.00")
        assert apply_rounding(Decimal("2"), RoundingMode.HALF_UP, 0) == Decimal("2")
        
        # Test special cases with non-int exponents (NaN, Infinity) - we just want to ensure no errors
        # and proper handling - these should fall back to 0 decimal places as a safe default
        try:
            special_decimal = Decimal("NaN")
            result = apply_rounding(special_decimal, RoundingMode.HALF_UP, 2)
            # We don't need to assert the exact result, just that it handled the case
        except Exception:
            pytest.fail("apply_rounding should handle special Decimal values")
            
    def test_half_towards_zero_rounding(self):
        """Test the HALF_TOWARDS_ZERO rounding mode."""
        # Test with exactly 0.5 - should round towards zero
        assert apply_rounding(Decimal("2.5"), RoundingMode.HALF_TOWARDS_ZERO, 0) == Decimal("2")
        assert apply_rounding(Decimal("-2.5"), RoundingMode.HALF_TOWARDS_ZERO, 0) == Decimal("-2")
        
        # Test with non-half values - should use HALF_UP
        assert apply_rounding(Decimal("2.4"), RoundingMode.HALF_TOWARDS_ZERO, 0) == Decimal("2")
        assert apply_rounding(Decimal("2.6"), RoundingMode.HALF_TOWARDS_ZERO, 0) == Decimal("3")
        
    def test_half_away_from_zero_rounding(self):
        """Test the HALF_AWAY_FROM_ZERO rounding mode."""
        # Test with exactly 0.5 - should round away from zero
        assert apply_rounding(Decimal("2.5"), RoundingMode.HALF_AWAY_FROM_ZERO, 0) == Decimal("3")
        assert apply_rounding(Decimal("-2.5"), RoundingMode.HALF_AWAY_FROM_ZERO, 0) == Decimal("-3")
        
        # Test with non-half values - should use HALF_UP
        assert apply_rounding(Decimal("2.4"), RoundingMode.HALF_AWAY_FROM_ZERO, 0) == Decimal("2")
        assert apply_rounding(Decimal("2.6"), RoundingMode.HALF_AWAY_FROM_ZERO, 0) == Decimal("3")
