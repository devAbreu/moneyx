# moneyx - Precise Money Handling for Python

[![Test Coverage: 100%](https://img.shields.io/badge/coverage-100%25-brightgreen.svg)](https://github.com/devAbreu/moneyx)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python Versions](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)

A lightweight, precise, and professional library for handling money in Python applications. `moneyx` solves **precision, rounding, and representation issues** that occur when using floating-point types like `float` for monetary calculations.

## 🚀 Installation

```bash
pip install moneyx
```

## 🔍 Key Features

- **Absolute precision** using `decimal.Decimal` internally
- **Extensive rounding modes** (HALF_UP, HALF_DOWN, BANKERS, HALF_ODD, DOWN, UP, CEILING, FLOOR, HALF_TOWARDS_ZERO, HALF_AWAY_FROM_ZERO)
- **Currency validation** based on [ISO 4217 standards](https://www.iso.org/iso-4217-currency-codes.html)
- **Complete ISO 4217 support** with proper symbols, decimal places, and country information
- **Currency lookup by country or numeric code**
- **Currency conversion** support
- **Proportional allocation** of amounts
- **Tax calculation** utilities
- **Formatting** with locale support
- **Serialization** to/from JSON and dictionaries
- **Type annotations** for better IDE support
- **High performance** with comprehensive benchmarks
- **Thread-safe operations** for concurrent environments
- **100% test coverage** with property-based testing

## 📚 ISO 4217 Data Sources

This library uses official ISO 4217 currency data from:
- [ISO 4217 Currency Codes](https://www.iso.org/iso-4217-currency-codes.html) - Official ISO information
- [SIX Financial Information](https://www.six-group.com/en/products-services/financial-information/data-standards.html) - Maintenance agency for ISO 4217 providing XML and XLS formats

## 📝 Usage Examples

### Basic Usage

```python
from moneyx import Money

# Create a monetary amount
price = Money("19.99", "USD")

# Basic arithmetic
tax = price.multiply(0.07)  # 7% tax
total = price.add(tax)

print(f"Price: {price.format()}")  # $19.99
print(f"Tax: {tax.format()}")      # $1.40
print(f"Total: {total.format()}")  # $21.39
```

### Different Currencies

```python
from moneyx import Money

# Create amounts in different currencies
usd = Money("100.00", "USD")
eur = Money("85.00", "EUR")

# Convert between currencies
eur_from_usd = usd.convert_to("EUR", rate=0.85)
print(f"{usd.format()} = {eur_from_usd.format_locale('de_DE')}")  # $100.00 = 85,00 €
```

### Currency Information and Lookup

```python
from moneyx import Money
from moneyx.currency import Currency

# Get information about a currency
usd = Money("100.00", "USD")
print(f"Symbol: {usd.currency.symbol}")  # $
print(f"Name: {usd.currency.name}")  # US Dollar
print(f"Decimals: {usd.currency.decimals}")  # 2
print(f"Countries: {', '.join(usd.currency.countries)}")  # Lists all countries using USD

# Find currencies by country
swiss_currencies = Currency.get_by_country("SWITZERLAND")
for currency in swiss_currencies:
    print(f"{currency.code}: {currency.name}")  # CHF, CHE, CHW

# Find currency by numeric code
eur = Currency.get_by_number("978")
print(f"{eur.code}: {eur.name}")  # EUR: Euro
```

### Rounding Modes

```python
from moneyx import Money, RoundingMode

# Classical rounding (HALF_UP)
standard = Money("2.5", "USD")  # 2.50 -> rounds to 3 when needed

# Banker's rounding (round to even)
bankers = Money("2.5", "USD", rounding=RoundingMode.BANKERS)  # 2.50 -> rounds to 2 when needed
bankers2 = Money("3.5", "USD", rounding=RoundingMode.BANKERS)  # 3.50 -> rounds to 4 when needed

# Additional rounding modes
odd = Money("2.5", "USD", rounding=RoundingMode.HALF_ODD)  # 2.50 -> rounds to 3 when needed
odd2 = Money("3.5", "USD", rounding=RoundingMode.HALF_ODD)  # 3.50 -> rounds to 3 when needed

# Directional rounding
ceiling = Money("2.1", "USD", rounding=RoundingMode.CEILING)  # Always rounds up
floor = Money("2.9", "USD", rounding=RoundingMode.FLOOR)  # Always rounds down
towards_zero = Money("2.5", "USD", rounding=RoundingMode.HALF_TOWARDS_ZERO)  # 2.5 -> 2
away_from_zero = Money("2.5", "USD", rounding=RoundingMode.HALF_AWAY_FROM_ZERO)  # 2.5 -> 3

# Negative numbers
neg = Money("-2.5", "USD", rounding=RoundingMode.HALF_TOWARDS_ZERO)  # -2.5 -> -2
neg2 = Money("-2.5", "USD", rounding=RoundingMode.HALF_AWAY_FROM_ZERO)  # -2.5 -> -3
```

### Allocation and Splitting

```python
from moneyx import Money

# Divide a bill proportionally
bill = Money("100.00", "USD")
alice_part = 2  # Alice pays 2 parts
bob_part = 1    # Bob pays 1 part

shares = bill.allocate([alice_part, bob_part])
print(f"Alice pays: {shares[0].format()}")  # $66.67
print(f"Bob pays: {shares[1].format()}")    # $33.33

# Split a bill evenly
bill = Money("100.00", "USD")
equal_shares = bill.split_evenly(3)
for i, share in enumerate(equal_shares):
    print(f"Person {i+1} pays: {share.format()}")  # $33.33, $33.33, $33.34
```

### Tax Calculations

```python
from moneyx import Money

# Add tax to a price
price = Money("100.00", "USD")
with_tax = price.with_tax(10)  # 10% tax
print(f"Price with tax: {with_tax.format()}")  # $110.00

# Extract tax from a tax-inclusive amount
inclusive = Money("110.00", "USD")
tax_info = inclusive.extract_tax(10)  # 10% tax
print(f"Base price: {tax_info['base'].format()}")  # $100.00
print(f"Tax amount: {tax_info['tax'].format()}")   # $10.00
```

### Internationalization

```python
from moneyx import Money

amount = Money("1234.56", "USD")
print(amount.format_locale("en_US"))  # $1,234.56
print(amount.format_locale("es_ES"))  # 1.234,56 $
print(amount.format_locale("de_DE"))  # 1.234,56 $
```

### Serialization

```python
from moneyx import Money
import json

price = Money("99.99", "USD")

# To/from JSON
json_str = price.to_json()
restored = Money.from_json(json_str)

# To/from dictionary
data = price.to_dict()
restored = Money.from_dict(data)
```

### Bulk Operations

```python
from moneyx import Money
from moneyx.bulk import bulk_add, bulk_multiply, bulk_allocate

# Create multiple money objects
items = [
    Money("10.50", "USD"),
    Money("20.75", "USD"),
    Money("5.99", "USD")
]

# Add all items together
total = bulk_add(items)
print(f"Total: {total}")  # $37.24

# Apply different multipliers to each item
multipliers = [1.1, 1.05, 1.2]
adjusted = bulk_multiply(items, multipliers)
for item in adjusted:
    print(item)  # $11.55, $21.79, $7.19

# Allocate money in bulk by ratio
budget = Money("1000.00", "USD")
allocations = [1, 2, 3, 4]  # Ratio 1:2:3:4
shares = bulk_allocate(budget, allocations)
for share in shares:
    print(share)  # $100.00, $200.00, $300.00, $400.00
```

## 🔒 Safe Money Handling

`moneyx` prevents common money-handling errors:

```python
from moneyx import Money
from moneyx.exceptions import PrecisionError, InvalidCurrencyError

try:
    # This will fail - USD allows max 2 decimals
    Money("100.123", "USD")
except PrecisionError as e:
    print(e)  # The currency USD only allows 2 decimal places. Received: 100.123

try:
    # This will fail - XYZ is not a valid currency
    Money("100.00", "XYZ")
except InvalidCurrencyError as e:
    print(e)  # Unknown currency: XYZ
```

## 📊 Performance Benchmarks

`moneyx` is designed for high performance. Here are some key benchmarks:

| Operation | Performance |
|-----------|-------------|
| Money creation | ~670K ops/sec |
| Addition | ~660K ops/sec |
| Subtraction | ~665K ops/sec |
| Multiplication | ~450K ops/sec |
| Allocation | ~98K ops/sec |
| HALF_UP rounding | ~1.59M ops/sec |
| BANKERS rounding | ~1.75M ops/sec |
| HALF_ODD rounding | ~1.04M ops/sec |
| Bulk addition | ~448K ops/sec |
| Bulk multiplication | ~47K ops/sec |
| String formatting | ~4.3M ops/sec |
| Locale formatting | ~87K ops/sec |

Run benchmarks yourself with:
```bash
python -m pytest tests/test_benchmark.py --no-cov --benchmark-columns=Min,Max,Mean,Median,OPS
```

## 📖 License

MIT License - see [LICENSE](LICENSE) for details.
