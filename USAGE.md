# moneyx Library - Usage Guide

This guide provides comprehensive examples for using the `moneyx` library for precise money handling in Python applications.

## Table of Contents

1. [Installation](#installation)
2. [Basic Money Operations](#basic-money-operations)
3. [Working with Different Currencies](#working-with-different-currencies)
4. [Rounding Modes](#rounding-modes)
5. [Money Distribution and Allocation](#money-distribution-and-allocation)
6. [Tax Calculations](#tax-calculations)
7. [Currency Information and Lookup](#currency-information-and-lookup)
8. [Formatting and Localization](#formatting-and-localization)
9. [Serialization](#serialization)
10. [Error Handling](#error-handling)

## Installation

```bash
pip install moneyx
```

## Basic Money Operations

### Creating Money Objects

```python
from moneyx import Money

# Create money with string amount (recommended for precision)
price = Money("19.99", "USD")

# Create money with numeric amount (converted to Decimal internally)
discount = Money(5.00, "USD")

# Create money with Decimal amount
from decimal import Decimal
tax = Money(Decimal("1.40"), "USD")

# Print representation
print(price)  # <Money 19.99 USD>
```

### Arithmetic Operations

```python
from moneyx import Money

# Addition
item_price = Money("29.99", "USD")
shipping = Money("5.00", "USD")
total = item_price.add(shipping)
print(f"Total: {total.amount}")  # Total: 34.99

# Subtraction
price = Money("100.00", "USD")
discount = Money("10.00", "USD")
discounted_price = price.subtract(discount)
print(f"Discounted price: {discounted_price.amount}")  # Discounted price: 90.00

# Multiplication (with scalar)
hourly_rate = Money("25.50", "USD")
hours_worked = 8
salary = hourly_rate.multiply(hours_worked)
print(f"Daily salary: {salary.amount}")  # Daily salary: 204.00
```

## Working with Different Currencies

### Currency Conversion

```python
from moneyx import Money

# Convert USD to EUR with a conversion rate
usd = Money("100.00", "USD")
eur = usd.convert_to("EUR", rate=0.85)
print(f"USD: {usd.format()}, EUR: {eur.format_locale('de_DE')}")  # USD: $100.00, EUR: 85,00 €

# Multiple conversions
gbp = usd.convert_to("GBP", rate=0.75)
jpy = usd.convert_to("JPY", rate=110.45)
print(f"GBP: {gbp.format()}")  # GBP: £75.00
print(f"JPY: {jpy.format()}")  # JPY: ¥110
```

### Currency Validation

```python
from moneyx import Money
from moneyx.exceptions import InvalidCurrencyError

# Valid currencies
usd = Money("10.50", "USD")  # Works fine
eur = Money("15.75", "EUR")  # Works fine

# Invalid currency
try:
    invalid = Money("99.99", "XYZ")  # This will raise an exception
except InvalidCurrencyError as e:
    print(e)  # Unknown currency: XYZ
```

## Rounding Modes

moneyx supports multiple rounding strategies to handle various financial scenarios:

```python
from moneyx import Money, RoundingMode
from decimal import Decimal

# Standard rounding modes
value = Decimal("2.5")

# HALF_UP: Traditional rounding (2.5 → 3)
half_up = Money(value, "USD", rounding=RoundingMode.HALF_UP)
print(f"HALF_UP: {half_up.amount}")  # HALF_UP: 3

# HALF_DOWN: Round down if exactly half (2.5 → 2)
half_down = Money(value, "USD", rounding=RoundingMode.HALF_DOWN)
print(f"HALF_DOWN: {half_down.amount}")  # HALF_DOWN: 2

# BANKERS (HALF_EVEN): Round to nearest even number when exactly half
bankers_2_5 = Money("2.5", "USD", rounding=RoundingMode.BANKERS)
bankers_3_5 = Money("3.5", "USD", rounding=RoundingMode.BANKERS)
print(f"BANKERS (2.5): {bankers_2_5.amount}")  # BANKERS (2.5): 2
print(f"BANKERS (3.5): {bankers_3_5.amount}")  # BANKERS (3.5): 4

# Advanced rounding modes
# HALF_ODD: Round to odd when exactly half
half_odd_2_5 = Money("2.5", "USD", rounding=RoundingMode.HALF_ODD)
half_odd_3_5 = Money("3.5", "USD", rounding=RoundingMode.HALF_ODD)
print(f"HALF_ODD (2.5): {half_odd_2_5.amount}")  # HALF_ODD (2.5): 3
print(f"HALF_ODD (3.5): {half_odd_3_5.amount}")  # HALF_ODD (3.5): 3

# DOWN: Always truncate (towards zero)
down_pos = Money("7.9", "USD", rounding=RoundingMode.DOWN)
down_neg = Money("-7.9", "USD", rounding=RoundingMode.DOWN)
print(f"DOWN (7.9): {down_pos.amount}")  # DOWN (7.9): 7.9
print(f"DOWN (-7.9): {down_neg.amount}")  # DOWN (-7.9): -7.9

# UP: Always round away from zero
up_pos = Money("7.1", "USD", rounding=RoundingMode.UP)
up_neg = Money("-7.1", "USD", rounding=RoundingMode.UP)
print(f"UP (7.1): {up_pos.amount}")  # UP (7.1): 7.1
print(f"UP (-7.1): {up_neg.amount}")  # UP (-7.1): -7.1

# Directional rounding
ceiling = Money("1.01", "USD", rounding=RoundingMode.CEILING)  # Always rounds up
floor = Money("1.99", "USD", rounding=RoundingMode.FLOOR)  # Always rounds down
print(f"CEILING (1.01): {ceiling.amount}")  # CEILING (1.01): 1.01
print(f"FLOOR (1.99): {floor.amount}")  # FLOOR (1.99): 1.99

# Half-specific directional rounding
half_towards_zero = Money("2.5", "USD", rounding=RoundingMode.HALF_TOWARDS_ZERO)
half_away_from_zero = Money("2.5", "USD", rounding=RoundingMode.HALF_AWAY_FROM_ZERO)
print(f"HALF_TOWARDS_ZERO (2.5): {half_towards_zero.amount}")  # HALF_TOWARDS_ZERO (2.5): 2
print(f"HALF_AWAY_FROM_ZERO (2.5): {half_away_from_zero.amount}")  # HALF_AWAY_FROM_ZERO (2.5): 3

# Negative number examples
neg_half_towards_zero = Money("-2.5", "USD", rounding=RoundingMode.HALF_TOWARDS_ZERO)
neg_half_away_from_zero = Money("-2.5", "USD", rounding=RoundingMode.HALF_AWAY_FROM_ZERO)
print(f"HALF_TOWARDS_ZERO (-2.5): {neg_half_towards_zero.amount}")  # HALF_TOWARDS_ZERO (-2.5): -2
print(f"HALF_AWAY_FROM_ZERO (-2.5): {neg_half_away_from_zero.amount}")  # HALF_AWAY_FROM_ZERO (-2.5): -3
```

## Money Distribution and Allocation

### Even Split

```python
from moneyx import Money

# Split a bill evenly among 3 people
bill = Money("100.00", "USD")
splits = bill.split_evenly(3)

for i, split in enumerate(splits):
    print(f"Person {i+1} pays: {split.format()}")
# Person 1 pays: $33.33
# Person 2 pays: $33.33
# Person 3 pays: $33.34
```

### Proportional Allocation

```python
from moneyx import Money

# Allocate a total amount proportionally
investment = Money("1000.00", "USD")

# Allocate according to weights (3:2:1)
alice_weight = 3  # 50%
bob_weight = 2    # 33.33%
charlie_weight = 1  # 16.67%

allocations = investment.allocate([alice_weight, bob_weight, charlie_weight])

investors = ["Alice", "Bob", "Charlie"]
for investor, allocation in zip(investors, allocations):
    print(f"{investor}'s share: {allocation.format()}")
# Alice's share: $500.00
# Bob's share: $333.33
# Charlie's share: $166.67

# The allocation is guaranteed to preserve the total
total = sum(alloc.amount for alloc in allocations)
print(f"Total allocated: {total}")  # Total allocated: 1000.00
```

## Tax Calculations

### Adding Tax

```python
from moneyx import Money

# Add tax to a price
price = Money("100.00", "USD")
with_tax = price.with_tax(10)  # 10% tax

print(f"Price: {price.format()}")  # Price: $100.00
print(f"Price with tax: {with_tax.format()}")  # Price with tax: $110.00
```

### Extracting Tax from Tax-Inclusive Amount

```python
from moneyx import Money

# Extract tax from a tax-inclusive amount
inclusive_price = Money("110.00", "USD")
tax_info = inclusive_price.extract_tax(10)  # 10% tax

print(f"Base price: {tax_info['base'].format()}")  # Base price: $100.00
print(f"Tax amount: {tax_info['tax'].format()}")  # Tax amount: $10.00
```

## Currency Information and Lookup

### Currency Properties

```python
from moneyx import Money
from moneyx.currency import Currency

# Get currency information
usd = Money("100.00", "USD")
print(f"Currency code: {usd.currency.code}")  # Currency code: USD
print(f"Currency symbol: {usd.currency.symbol}")  # Currency symbol: $
print(f"Currency name: {usd.currency.name}")  # Currency name: US Dollar
print(f"Currency decimals: {usd.currency.decimals}")  # Currency decimals: 2

# Special decimal cases
bhd = Money("1.234", "BHD")  # Bahraini Dinar uses 3 decimal places
print(f"{bhd.currency.name} uses {bhd.currency.decimals} decimal places")
# Bahraini Dinar uses 3 decimal places

jpy = Money("100", "JPY")  # Japanese Yen uses 0 decimal places
print(f"{jpy.currency.name} uses {jpy.currency.decimals} decimal places")
# Yen uses 0 decimal places
```

### Finding Currencies by Country

```python
from moneyx.currency import Currency

# Get all currencies used in a specific country
swiss_currencies = Currency.get_by_country("SWITZERLAND")
print(f"Switzerland uses {len(swiss_currencies)} currencies:")
for currency in swiss_currencies:
    print(f"- {currency.code}: {currency.name}")
# Switzerland uses 3 currencies:
# - CHF: Swiss Franc
# - CHE: WIR Euro
# - CHW: WIR Franc

# Get currencies for other countries
eurozone_countries = Currency.get_by_country("GERMANY")
print(f"Germany uses: {eurozone_countries[0].code}")  # Germany uses: EUR

us_currencies = Currency.get_by_country("UNITED STATES OF AMERICA (THE)")
print(f"USA uses: {', '.join(c.code for c in us_currencies)}")
# USA uses: USD, USN
```

### Finding Currency by Numeric Code

```python
from moneyx.currency import Currency

# Get currency by ISO numeric code
eur = Currency.get_by_number("978")
print(f"Currency code 978 is {eur.code}: {eur.name}")
# Currency code 978 is EUR: Euro

# Some other examples
usd = Currency.get_by_number("840")
gbp = Currency.get_by_number("826")
print(f"Code 840: {usd.code}, Code 826: {gbp.code}")
# Code 840: USD, Code 826: GBP
```

## Formatting and Localization

### Basic Formatting

```python
from moneyx import Money

# Default formatting
price = Money("1234.56", "USD")
print(price.format())  # $1,234.56

# Different currencies
euro = Money("1234.56", "EUR")
yen = Money("1234", "JPY")
print(euro.format())  # €1,234.56
print(yen.format())  # ¥1,234
```

### Locale-Specific Formatting

```python
from moneyx import Money

amount = Money("1234.56", "USD")

# Format in different locales
print(f"US Format: {amount.format_locale('en_US')}")  # US Format: $1,234.56
print(f"UK Format: {amount.format_locale('en_GB')}")  # UK Format: $1,234.56
print(f"German Format: {amount.format_locale('de_DE')}")  # German Format: 1.234,56 $
print(f"French Format: {amount.format_locale('fr_FR')}")  # French Format: 1 234,56 $
print(f"Spanish Format: {amount.format_locale('es_ES')}")  # Spanish Format: 1.234,56 $
print(f"Japanese Format: {amount.format_locale('ja_JP')}")  # Japanese Format: $1,234.56

# Format Euro in European locales
euro = Money("1234.56", "EUR")
print(f"German Euro: {euro.format_locale('de_DE')}")  # German Euro: 1.234,56 €
print(f"French Euro: {euro.format_locale('fr_FR')}")  # French Euro: 1 234,56 €
print(f"Italian Euro: {euro.format_locale('it_IT')}")  # Italian Euro: 1.234,56 €
```

## Serialization

### To/From Dictionary

```python
from moneyx import Money

# Convert Money to dictionary
price = Money("99.95", "USD")
data = price.to_dict()
print(data)
# {'amount': '99.95', 'currency': 'USD', 'rounding': 'HALF_UP'}

# Create Money from dictionary
restored = Money.from_dict(data)
print(restored)  # <Money 99.95 USD>
```

### To/From JSON

```python
from moneyx import Money
import json

# Convert Money to JSON
price = Money("49.99", "EUR")
json_str = price.to_json()
print(json_str)
# {"amount": "49.99", "currency": "EUR", "rounding": "HALF_UP"}

# Create Money from JSON
restored = Money.from_json(json_str)
print(restored)  # <Money 49.99 EUR>

# Useful for storing in databases or sending over API
products = [
    {"id": 1, "name": "Keyboard", "price": Money("49.99", "USD").to_dict()},
    {"id": 2, "name": "Mouse", "price": Money("29.99", "USD").to_dict()},
]

# Converting back when retrieving data
for product in products:
    price = Money.from_dict(product["price"])
    print(f"{product['name']}: {price.format()}")
# Keyboard: $49.99
# Mouse: $29.99
```

## Error Handling

### Handling Precision Errors

```python
from moneyx import Money
from moneyx.exceptions import PrecisionError

# Precision validation - USD allows 2 decimal places
try:
    # This will fail
    usd_price = Money("10.123", "USD")
except PrecisionError as e:
    print(e)  # The currency USD only allows 2 decimal places. Received: 10.123
    
    # Correct approach
    usd_price = Money("10.12", "USD")
    print(f"Correct USD price: {usd_price.format()}")  # Correct USD price: $10.12

# Currencies with different decimal precision
try:
    # This works - BHD allows 3 decimal places
    bhd = Money("10.123", "BHD")
    print(f"BHD: {bhd.format()}")  # BHD: د.ب10.123
    
    # This fails - JPY allows 0 decimal places
    jpy = Money("10.5", "JPY")
except PrecisionError as e:
    print(e)  # The currency JPY only allows 0 decimal places. Received: 10.5
    
    # Correct approach
    jpy = Money("10", "JPY")
    print(f"Correct JPY amount: {jpy.format()}")  # Correct JPY amount: ¥10
```

### Handling Currency Mismatches

```python
from moneyx import Money

# Attempting operations with different currencies
usd = Money("10.00", "USD")
eur = Money("8.50", "EUR")

try:
    # This will fail
    total = usd.add(eur)
except ValueError as e:
    print(e)  # Currency mismatch
    
    # Correct approach: convert currencies first
    eur_in_usd = eur.convert_to("USD", rate=1.18)
    total = usd.add(eur_in_usd)
    print(f"Total in USD: {total.format()}")  # Total in USD: $20.03
```

### Handling Invalid Currency Codes

```python
from moneyx import Money
from moneyx.exceptions import InvalidCurrencyError

try:
    # This will fail - XYZ is not a valid currency code
    xyz_money = Money("100.00", "XYZ")
except InvalidCurrencyError as e:
    print(e)  # Unknown currency: XYZ
    
    # Suggest alternatives
    print("Did you mean one of these? XAF, XAG, XAU, XBA, XBB, XCD, XDR, XOF, XPD, XPF, XPT, XSU, XTS, XUA, XXX")
```

## Complete Application Example

Here's a complete example showing multiple features together:

```python
from moneyx import Money, RoundingMode
from moneyx.currency import Currency
from moneyx.exceptions import PrecisionError, InvalidCurrencyError
from decimal import Decimal
import json

def shopping_cart_example():
    print("=== SHOPPING CART EXAMPLE ===\n")
    
    try:
        # Create shopping cart items
        items = [
            {"name": "Laptop", "price": Money("1299.99", "USD"), "quantity": 1},
            {"name": "Mouse", "price": Money("25.99", "USD"), "quantity": 2},
            {"name": "Keyboard", "price": Money("49.99", "USD"), "quantity": 1},
        ]
        
        # Calculate subtotals for each item
        for item in items:
            item["subtotal"] = item["price"].multiply(item["quantity"])
            
        # Calculate cart total
        total = Money("0", "USD")
        for item in items:
            total = total.add(item["subtotal"])
        
        # Apply discount
        discount_percentage = 10
        discount_amount = total.multiply(discount_percentage / 100)
        discounted_total = total.subtract(discount_amount)
        
        # Calculate tax
        tax_rate = 8.25  # 8.25% tax
        final_total = discounted_total.with_tax(tax_rate)
        
        # Display cart
        print("Shopping Cart:")
        for item in items:
            print(f"  {item['name']} ({item['quantity']}x): {item['price'].format()} each = {item['subtotal'].format()}")
        
        print(f"\nSubtotal: {total.format()}")
        print(f"Discount ({discount_percentage}%): -{discount_amount.format()}")
        print(f"Discounted total: {discounted_total.format()}")
        print(f"Tax ({tax_rate}%): {final_total.subtract(discounted_total).format()}")
        print(f"Final total: {final_total.format()}")
        
        # Split payment between 3 friends
        split_payments = final_total.split_evenly(3)
        print("\nSplit payment between 3 friends:")
        for i, payment in enumerate(split_payments, 1):
            print(f"  Friend {i} pays: {payment.format()}")
        
        # Show different currency formats
        print("\nAmount in different currencies and formats:")
        eur_rate = 0.85
        eur_total = final_total.convert_to("EUR", rate=eur_rate)
        print(f"  EUR: {eur_total.format_locale('de_DE')}")
        
        gbp_rate = 0.75
        gbp_total = final_total.convert_to("GBP", rate=gbp_rate)
        print(f"  GBP: {gbp_total.format_locale('en_GB')}")
        
        jpy_rate = 110.50
        jpy_total = final_total.convert_to("JPY", rate=jpy_rate)
        print(f"  JPY: {jpy_total.format_locale('ja_JP')}")
        
        # Serialize for storage
        order = {
            "items": [{"name": item["name"], "price": item["price"].to_dict(), 
                      "quantity": item["quantity"]} for item in items],
            "total": final_total.to_dict(),
            "currency": final_total.currency.code,
        }
        
        order_json = json.dumps(order, indent=2)
        print("\nOrder JSON for storage/API:")
        print(order_json)
        
    except (InvalidCurrencyError, PrecisionError, ValueError) as e:
        print(f"Error processing shopping cart: {e}")

if __name__ == "__main__":
    shopping_cart_example()
```

Output:
```
=== SHOPPING CART EXAMPLE ===

Shopping Cart:
  Laptop (1x): $1,299.99 each = $1,299.99
  Mouse (2x): $25.99 each = $51.98
  Keyboard (1x): $49.99 each = $49.99

Subtotal: $1,401.96
Discount (10%): -$140.20
Discounted total: $1,261.76
Tax (8.25%): $104.10
Final total: $1,365.86

Split payment between 3 friends:
  Friend 1 pays: $455.29
  Friend 2 pays: $455.29
  Friend 3 pays: $455.28

Amount in different currencies and formats:
  EUR: 1.160,98 €
  GBP: £1,024.40
  JPY: ￥150,928

Order JSON for storage/API:
{
  "items": [
    {
      "name": "Laptop",
      "price": {
        "amount": "1299.99",
        "currency": "USD",
        "rounding": "HALF_UP"
      },
      "quantity": 1
    },
    {
      "name": "Mouse",
      "price": {
        "amount": "25.99",
        "currency": "USD",
        "rounding": "HALF_UP"
      },
      "quantity": 2
    },
    {
      "name": "Keyboard",
      "price": {
        "amount": "49.99",
        "currency": "USD",
        "rounding": "HALF_UP"
      },
      "quantity": 1
    }
  ],
  "total": {
    "amount": "1365.86",
    "currency": "USD",
    "rounding": "HALF_UP"
  },
  "currency": "USD"
}
``` 