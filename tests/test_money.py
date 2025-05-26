# tests/test_money.py

from decimal import Decimal

import pytest

from src.moneyx import Money

# ------------------------------------------------------------------------------
# 🧮 Basic arithmetic operations
# ------------------------------------------------------------------------------


def test_addition():
    a = Money("10.00", "USD")
    b = Money("5.00", "USD")
    assert a.add(b).amount == Decimal("15.00")


def test_subtraction():
    a = Money("10.00", "USD")
    b = Money("3.00", "USD")
    result = a.subtract(b)
    assert isinstance(result, Money)
    assert result.amount == Decimal("7.00")


def test_multiplication():
    m = Money("19.99", "USD")
    result = m.multiply(2)
    assert result.amount == Decimal("39.98")


# ------------------------------------------------------------------------------
# 💵 Distribution and allocation of amounts
# ------------------------------------------------------------------------------


def test_allocation():
    m = Money("10.00", "USD")
    parts = m.allocate([1, 1, 1])
    assert sum(p.amount for p in parts) == Decimal("10.00")


def test_allocate_precision():
    m = Money("0.05", "USD")
    parts = m.allocate([1, 1])
    assert sum(p.amount for p in parts) == Decimal("0.05")


def test_allocate_empty_list():
    m = Money("100.00", "USD")
    result = m.allocate([])
    assert isinstance(result, list)
    assert result == []


def test_allocate_with_negative_remainder():
    m = Money("10.00", "USD")
    parts = m.allocate([1, 3])
    assert sum(p.amount for p in parts) == Decimal("10.00")

    negative = Money("-10.00", "USD")
    neg_parts = negative.allocate([1, 3])
    assert sum(p.amount for p in neg_parts) == Decimal("-10.00")


def test_allocate_negative_remainder():
    """Simulates a forced negative remainder situation for coverage."""
    m = Money("-10.00", "USD")
    m._test_force_negative_remainder = True
    result = m.allocate([1, 1])
    assert isinstance(result, list)
    assert len(result) == 2


# ------------------------------------------------------------------------------
# 🌍 Currency conversion and formatting
# ------------------------------------------------------------------------------


def test_currency_conversion():
    usd = Money("100.00", "USD")
    eur = usd.convert_to("EUR", rate=0.85)
    assert eur.amount == Decimal("85.00")
    assert eur.currency.code == "EUR"


def test_format_basic():
    m = Money("123.45", "USD")
    assert m.format() == "$123.45"


def test_format_locale():
    m = Money("1999.50", "USD")
    assert m.format_locale("en_US") == "$1,999.50"
    assert m.format_locale("es_EC") == "$1.999,50"


# ------------------------------------------------------------------------------
# 💸 Taxes
# ------------------------------------------------------------------------------


def test_with_tax():
    m = Money("100.00", "USD")
    result = m.with_tax(10)
    assert result.amount == Decimal("110.00")


def test_extract_tax():
    m = Money("110.00", "USD")
    tax_info = m.extract_tax(10)
    assert tax_info["base"].amount == Decimal("100.00")
    assert tax_info["tax"].amount == Decimal("10.00")


# ------------------------------------------------------------------------------
# ✅ Currency and precision validations
# ------------------------------------------------------------------------------


def test_valid_precision():
    m = Money("100.12", "USD")
    assert m.amount == Decimal("100.12")
    bhd = Money("100.123", "BHD")
    assert bhd.amount == Decimal("100.123")


def test_invalid_precision():
    from moneyx.exceptions import PrecisionError  # Import explicitly here

    def trigger_invalid_precision():
        Money("100.1234", "USD")

    with pytest.raises(PrecisionError) as exc_info:
        trigger_invalid_precision()

    assert isinstance(exc_info.value, PrecisionError)
    assert "USD" in str(exc_info.value)
    assert "2 decimal places" in str(exc_info.value)
    assert "100.1234" in str(exc_info.value)


def test_valid_currency():
    m = Money("100.00", "USD")
    assert m.currency.code == "USD"


def test_invalid_currency_code():
    from moneyx.exceptions import InvalidCurrencyError  # Import explicitly here

    with pytest.raises(InvalidCurrencyError) as exc_info:
        Money("100.00", "XYZ")

    assert isinstance(exc_info.value, InvalidCurrencyError)
    assert "XYZ" in str(exc_info.value)
    assert "Unknown" in str(exc_info.value)


# ------------------------------------------------------------------------------
# 🔁 Special operations
# ------------------------------------------------------------------------------


def test_currency_mismatch():
    a = Money("10.00", "USD")
    b = Money("5.00", "EUR")
    with pytest.raises(ValueError, match="Currency mismatch"):
        a.add(b)
    with pytest.raises(ValueError, match="Currency mismatch"):
        a.subtract(b)


def test_even_split():
    m = Money("100.00", "USD")
    parts = m.split_evenly(3)
    assert len(parts) == 3
    assert sum(p.amount for p in parts) == Decimal("100.00")


def test_split_evenly_validation():
    m = Money("100.00", "USD")
    with pytest.raises(ValueError):
        m.split_evenly(0)


# ------------------------------------------------------------------------------
# 🧪 Serialization
# ------------------------------------------------------------------------------


def test_dict_serialization():
    m = Money("88.88", "USD")
    data = m.to_dict()
    m2 = Money.from_dict(data)
    assert m2.amount == m.amount
    assert m2.currency.code == "USD"


def test_serialization():
    m = Money("99.99", "USD")
    json_str = m.to_json()
    m2 = Money.from_json(json_str)
    assert m2.amount == m.amount
    assert m2.currency.code == "USD"


# ------------------------------------------------------------------------------
# 🧾 Representation and metadata
# ------------------------------------------------------------------------------


def test_repr():
    assert repr(Money("100.00", "USD")) == "<Money 100.00 USD>"
    assert repr(Money("-50.00", "EUR")) == "<Money -50.00 EUR>"
    assert repr(Money("0", "JPY")) == "<Money 0 JPY>"


def test_currency_properties():
    usd = Money("100.00", "USD")
    assert usd.currency.symbol == "$"
    assert usd.currency.decimals == 2
    assert usd.currency.name == "US Dollar"

    bhd = Money("100.123", "BHD")
    assert bhd.currency.decimals == 3
    assert bhd.currency.name == "Bahraini Dinar"

    jpy = Money("100", "JPY")
    assert jpy.currency.decimals == 0
    assert jpy.currency.name == "Yen"


# ------------------------------------------------------------------------------
# ➕ Negative cases and edge cases
# ------------------------------------------------------------------------------


def test_negative_values():
    m = Money("-50.00", "USD")
    assert m.amount == Decimal("-50.00")
    assert m.multiply(2).amount == Decimal("-100.00")
    assert m.add(Money("60.00", "USD")).amount == Decimal("10.00")


def test_rounding_precision():
    m = Money("0.33", "USD")
    r = m.multiply(3)
    assert r.amount == Decimal("0.99")


# ------------------------------------------------------------------------------
# 🔄 Rounding modes
# ------------------------------------------------------------------------------


def test_rounding_modes():
    from decimal import Decimal

    from src.moneyx import Money, RoundingMode
    from src.moneyx.rounding import apply_rounding

    # Direct test of rounding function for integer values
    assert str(apply_rounding(Decimal("2.5"), RoundingMode.HALF_UP, 0)) == "3"
    assert str(apply_rounding(Decimal("2.5"), RoundingMode.HALF_DOWN, 0)) == "2"
    assert str(apply_rounding(Decimal("2.5"), RoundingMode.BANKERS, 0)) == "2"

    # Test cases for decimal values
    test_decimal_values = [
        {
            "input": "1.23",
            "expected": {
                RoundingMode.HALF_UP: "1.23",
                RoundingMode.HALF_DOWN: "1.23",
                RoundingMode.BANKERS: "1.23",
                RoundingMode.DOWN: "1.23",
                RoundingMode.UP: "1.23",
                RoundingMode.CEILING: "1.23",
                RoundingMode.FLOOR: "1.23",
            },
        },
        {
            "input": "-1.23",
            "expected": {
                RoundingMode.HALF_UP: "-1.23",
                RoundingMode.HALF_DOWN: "-1.23",
                RoundingMode.BANKERS: "-1.23",
                RoundingMode.DOWN: "-1.23",
                RoundingMode.UP: "-1.23",
                RoundingMode.CEILING: "-1.23",
                RoundingMode.FLOOR: "-1.23",
            },
        },
        {
            "input": "1.25",
            "expected": {
                RoundingMode.HALF_UP: "1.25",
                RoundingMode.HALF_DOWN: "1.25",
                RoundingMode.BANKERS: "1.25",
                RoundingMode.DOWN: "1.25",
                RoundingMode.UP: "1.25",
                RoundingMode.CEILING: "1.25",
                RoundingMode.FLOOR: "1.25",
            },
        },
    ]

    # Direct tests with apply_rounding for cases with more decimals
    test_more_decimals = [
        {
            "input": "1.234",
            "places": 2,
            "expected": {
                RoundingMode.HALF_UP: "1.23",
                RoundingMode.HALF_DOWN: "1.23",
                RoundingMode.BANKERS: "1.23",
                RoundingMode.DOWN: "1.23",
                RoundingMode.UP: "1.24",
                RoundingMode.CEILING: "1.24",
                RoundingMode.FLOOR: "1.23",
            },
        },
        {
            "input": "-1.234",
            "places": 2,
            "expected": {
                RoundingMode.HALF_UP: "-1.23",
                RoundingMode.HALF_DOWN: "-1.23",
                RoundingMode.BANKERS: "-1.23",
                RoundingMode.DOWN: "-1.23",
                RoundingMode.UP: "-1.24",
                RoundingMode.CEILING: "-1.23",
                RoundingMode.FLOOR: "-1.24",
            },
        },
    ]

    # Tests with integer cases using apply_rounding directly
    test_integer_values = [
        {
            "input": "2.5",
            "expected": {
                RoundingMode.HALF_UP: "3",
                RoundingMode.HALF_DOWN: "2",
                RoundingMode.BANKERS: "2",
                RoundingMode.HALF_ODD: "3",
                RoundingMode.DOWN: "2",
                RoundingMode.UP: "3",
                RoundingMode.CEILING: "3",
                RoundingMode.FLOOR: "2",
                RoundingMode.HALF_TOWARDS_ZERO: "2",
                RoundingMode.HALF_AWAY_FROM_ZERO: "3",
            },
        },
        {
            "input": "3.5",
            "expected": {
                RoundingMode.HALF_UP: "4",
                RoundingMode.HALF_DOWN: "3",
                RoundingMode.BANKERS: "4",
                RoundingMode.HALF_ODD: "3",
                RoundingMode.DOWN: "3",
                RoundingMode.UP: "4",
                RoundingMode.CEILING: "4",
                RoundingMode.FLOOR: "3",
                RoundingMode.HALF_TOWARDS_ZERO: "3",
                RoundingMode.HALF_AWAY_FROM_ZERO: "4",
            },
        },
        {
            "input": "-2.5",
            "expected": {
                RoundingMode.HALF_UP: "-3",
                RoundingMode.HALF_DOWN: "-2",
                RoundingMode.BANKERS: "-2",
                RoundingMode.HALF_ODD: "-3",
                RoundingMode.DOWN: "-2",
                RoundingMode.UP: "-3",
                RoundingMode.CEILING: "-2",
                RoundingMode.FLOOR: "-3",
                RoundingMode.HALF_TOWARDS_ZERO: "-2",
                RoundingMode.HALF_AWAY_FROM_ZERO: "-3",
            },
        },
        {
            "input": "-3.5",
            "expected": {
                RoundingMode.HALF_UP: "-4",
                RoundingMode.HALF_DOWN: "-3",
                RoundingMode.BANKERS: "-4",
                RoundingMode.HALF_ODD: "-3",
                RoundingMode.DOWN: "-3",
                RoundingMode.UP: "-4",
                RoundingMode.CEILING: "-3",
                RoundingMode.FLOOR: "-4",
                RoundingMode.HALF_TOWARDS_ZERO: "-3",
                RoundingMode.HALF_AWAY_FROM_ZERO: "-4",
            },
        },
    ]

    # Test each decimal value using Money
    for test_case in test_decimal_values:
        input_value = test_case["input"]
        for mode, expected in test_case["expected"].items():
            money = Money(input_value, "USD", rounding=mode)
            assert (
                str(money.amount) == expected
            ), f"Failed {mode} for {input_value}, expected: {expected}, got: {money.amount}"

    # Test cases with more decimals using apply_rounding directly
    for test_case in test_more_decimals:
        input_value = test_case["input"]
        places = test_case["places"]
        for mode, expected in test_case["expected"].items():
            rounded = apply_rounding(Decimal(input_value), mode, places)
            assert (
                str(rounded) == expected
            ), f"Failed {mode} for {input_value}, expected: {expected}, got: {rounded}"

    # Test each integer value using apply_rounding directly
    for test_case in test_integer_values:
        input_value = test_case["input"]
        for mode, expected in test_case["expected"].items():
            rounded = apply_rounding(Decimal(input_value), mode, 0)
            assert (
                str(rounded) == expected
            ), f"Failed {mode} for {input_value}, expected: {expected}, got: {rounded}"


# ------------------------------------------------------------------------------
# 🌍 Currencies and ISO 4217
# ------------------------------------------------------------------------------


def test_currency_by_country():
    from src.moneyx.currency import Currency

    # Get currencies for a specific country
    currencies = Currency.get_by_country("SWITZERLAND")

    # Verify we found the correct currencies
    codes = [c.code for c in currencies]
    assert "CHF" in codes
    assert "CHE" in codes
    assert "CHW" in codes

    # Test another country
    japan_currencies = Currency.get_by_country("JAPAN")
    assert len(japan_currencies) == 1
    assert japan_currencies[0].code == "JPY"
    assert japan_currencies[0].decimals == 0


def test_currency_by_number():
    from src.moneyx.currency import Currency

    # Get currency by numeric code
    currency = Currency.get_by_number("840")
    assert currency.code == "USD"

    # Test a currency with special decimals
    bhd = Currency.get_by_number("048")
    assert bhd.code == "BHD"
    assert bhd.decimals == 3
