"""Tests for the serialization module."""

import json
from decimal import Decimal

import pytest

from moneyx import Money
from moneyx.exceptions import SerializationError
from moneyx.serialization import from_dict, from_json, to_dict, to_json


class TestSerialization:
    """Test suite for serialization and deserialization of Money objects."""

    def test_to_dict(self):
        """Test converting Money object to dictionary."""
        money = Money("10.50", "USD")
        result = to_dict(money)

        assert isinstance(result, dict)
        assert result["amount"] == "10.50"
        assert result["currency"] == "USD"
        assert result["rounding"] == "HALF_UP"

    def test_from_dict_valid(self):
        """Test creating Money object from valid dictionary."""
        data = {
            "amount": "10.50",
            "currency": "USD",
            "rounding": "HALF_UP",
        }

        money = from_dict(Money, data)

        assert isinstance(money, Money)
        assert money.amount == Decimal("10.50")
        assert money.currency.code == "USD"
        assert money.rounding_mode == "HALF_UP"

    @pytest.mark.xfail(raises=SerializationError, strict=True)
    def test_from_dict_missing_fields(self):
        """Test creating Money object from dictionary with missing fields raises SerializationError."""
        data = {
            "amount": "10.50",
            # Missing currency
        }

        # This test intentionally raises an exception
        from_dict(Money, data)
        # The test should fail with SerializationError

    def test_from_dict_invalid_types(self):
        """Test from_dict with invalid data types."""
        from moneyx.exceptions import SerializationError

        # Test with invalid amount type
        with pytest.raises(SerializationError) as exc_info:
            data = {"amount": [], "currency": "USD"}  # List is not a valid amount type
            from_dict(Money, data)
        assert "Amount must be numeric or string" in str(exc_info.value)

        # Test with invalid currency type
        with pytest.raises(SerializationError) as exc_info:
            data = {"amount": "10.00", "currency": 123}  # Integer is not a valid currency
            from_dict(Money, data)
        assert "Currency code must be string" in str(exc_info.value)

        # Test with invalid rounding type
        with pytest.raises(SerializationError) as exc_info:
            data = {"amount": "10.00", "currency": "USD", "rounding": 123}  # Integer is not valid rounding
            from_dict(Money, data)
        assert "Rounding mode must be string" in str(exc_info.value)

    @pytest.mark.xfail(raises=SerializationError, strict=True)
    def test_from_dict_not_a_dict(self):
        """Test creating Money object from non-dictionary raises SerializationError."""
        # This test intentionally raises an exception
        from_dict(Money, "not a dict")
        # The test should fail with SerializationError

    def test_to_json(self):
        """Test converting Money object to JSON string."""
        money = Money("10.50", "USD")
        json_str = to_json(money)

        # Parse the JSON string back to verify
        data = json.loads(json_str)

        assert isinstance(data, dict)
        assert data["amount"] == "10.50"
        assert data["currency"] == "USD"
        assert data["rounding"] == "HALF_UP"

    def test_to_json_with_indent(self):
        """Test converting Money object to JSON string with indentation."""
        money = Money("10.50", "USD")
        json_str = to_json(money, indent=2)

        # Verify indentation is applied
        assert '\n  "' in json_str

        # Parse the JSON string back to verify
        data = json.loads(json_str)

        assert isinstance(data, dict)
        assert data["amount"] == "10.50"
        assert data["currency"] == "USD"
        assert data["rounding"] == "HALF_UP"

    def test_from_json_valid(self):
        """Test creating Money object from valid JSON string."""
        json_str = '{"amount": "10.50", "currency": "USD", "rounding": "HALF_UP"}'

        money = from_json(Money, json_str)

        assert isinstance(money, Money)
        assert money.amount == Decimal("10.50")
        assert money.currency.code == "USD"
        assert money.rounding_mode == "HALF_UP"

    @pytest.mark.xfail(raises=SerializationError, strict=True)
    def test_from_json_invalid_json(self):
        """Test creating Money object from invalid JSON string raises SerializationError."""
        json_str = '{"amount": "10.50", "currency": "USD", "rounding": HALF_UP}'  # Missing quotes

        # This test intentionally raises an exception
        from_json(Money, json_str)
        # The test should fail with SerializationError

    @pytest.mark.xfail(raises=SerializationError, strict=True)
    def test_from_json_missing_fields(self):
        """Test creating Money object from JSON with missing fields raises SerializationError."""
        json_str = '{"amount": "10.50"}'  # Missing currency

        # This test intentionally raises an exception
        from_json(Money, json_str)
        # The test should fail with SerializationError

    def test_money_to_dict_method(self):
        """Test Money.to_dict() method uses serialization module."""
        money = Money("10.50", "USD")
        result = money.to_dict()

        assert isinstance(result, dict)
        assert result["amount"] == "10.50"
        assert result["currency"] == "USD"
        assert result["rounding"] == "HALF_UP"

    def test_money_from_dict_method(self):
        """Test Money.from_dict() method uses serialization module."""
        data = {
            "amount": "10.50",
            "currency": "USD",
            "rounding": "HALF_UP",
        }

        money = Money.from_dict(data)

        assert isinstance(money, Money)
        assert money.amount == Decimal("10.50")
        assert money.currency.code == "USD"
        assert money.rounding_mode == "HALF_UP"

    def test_money_to_json_method(self):
        """Test Money.to_json() method uses serialization module."""
        money = Money("10.50", "USD")
        json_str = money.to_json()

        # Parse the JSON string back to verify
        data = json.loads(json_str)

        assert isinstance(data, dict)
        assert data["amount"] == "10.50"
        assert data["currency"] == "USD"
        assert data["rounding"] == "HALF_UP"

    def test_money_from_json_method(self):
        """Test Money.from_json() method uses serialization module."""
        json_str = '{"amount": "10.50", "currency": "USD", "rounding": "HALF_UP"}'

        money = Money.from_json(json_str)

        assert isinstance(money, Money)
        assert money.amount == Decimal("10.50")
        assert money.currency.code == "USD"
        assert money.rounding_mode == "HALF_UP"

    def test_from_dict_money_creation_error(self):
        """Test from_dict error handling for Money creation failure."""
        from moneyx.exceptions import SerializationError
        
        # This will fail when creating the Money object because "XYZ" is not a valid currency
        with pytest.raises(SerializationError) as exc_info:
            data = {"amount": "10.00", "currency": "XYZ", "rounding": "HALF_UP"}
            from_dict(Money, data)
        assert "Failed to create Money object" in str(exc_info.value)
        
    def test_invalid_rounding_mode(self):
        """Test from_dict with invalid rounding mode."""
        from moneyx.exceptions import SerializationError
        
        with pytest.raises(SerializationError) as exc_info:
            data = {"amount": "10.00", "currency": "USD", "rounding": "INVALID_MODE"}
            from_dict(Money, data)
        assert "Invalid rounding mode" in str(exc_info.value)
