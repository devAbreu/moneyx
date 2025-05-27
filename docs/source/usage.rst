=====
Usage
=====

Basic Usage
----------

Creating Money Objects
^^^^^^^^^^^^^^^^^^^^^

The core of the library is the ``Money`` class, which represents a monetary amount in a specific currency:

.. code-block:: python

    from moneyx import Money

    # Create money objects
    amount1 = Money("19.99", "USD")  # From string
    amount2 = Money(19.99, "USD")    # From float (will be converted to Decimal)
    amount3 = Money(1999, "JPY")     # JPY has 0 decimal places

Currency Formatting
^^^^^^^^^^^^^^^^^^

Format money with currency symbols and locale-specific formatting:

.. code-block:: python

    from moneyx import Money

    price = Money("1234.56", "USD")
    
    # Default formatting
    print(price.format())                 # $1,234.56
    
    # Locale-specific formatting
    print(price.format_locale("en_US"))   # $1,234.56
    print(price.format_locale("de_DE"))   # 1.234,56 $
    print(price.format_locale("fr_FR"))   # 1 234,56 $
    print(price.format_locale("ja_JP"))   # $1,234.56

Arithmetic Operations
--------------------

Addition and Subtraction
^^^^^^^^^^^^^^^^^^^^^^^

Add and subtract Money objects with the same currency:

.. code-block:: python

    from moneyx import Money

    price = Money("19.99", "USD")
    tax = Money("1.60", "USD")
    
    # Using methods
    total = price.add(tax)                # $21.59
    change = Money("50.00", "USD").subtract(total)  # $28.41
    
    # Using operators
    total = price + tax                   # $21.59
    change = Money("50.00", "USD") - total  # $28.41
    
    # Error if currencies don't match
    try:
        usd = Money("10.00", "USD")
        eur = Money("10.00", "EUR")
        usd.add(eur)  # Raises ValueError: Currency mismatch
    except ValueError as e:
        print(e)

Multiplication
^^^^^^^^^^^^^

Multiply a Money object by a number:

.. code-block:: python

    from moneyx import Money

    price = Money("19.99", "USD")
    
    # Calculate total for 3 items
    total = price.multiply(3)             # $59.97
    
    # Using operators
    total = price * 3                     # $59.97
    
    # Apply a discount
    discount = price.multiply(0.20)       # $4.00 (20% of price)
    discounted = price.subtract(discount)  # $15.99

Working with Cents
-----------------

Many financial applications store monetary values in the smallest currency unit (cents, pence, etc.). Here's how to work with cents in moneyx:

.. code-block:: python

    from decimal import Decimal
    from moneyx import Money

    # Converting from cents to dollars
    cents_amount = 1299  # $12.99 in cents
    price = Money(cents_amount / 100, "USD")
    print(price.format())  # $12.99

    # For more precision, use Decimal
    cents_amount = 1299
    price = Money(Decimal(cents_amount) / Decimal("100"), "USD")
    print(price.format())  # $12.99

    # Converting a Money object to cents
    dollars = Money("45.67", "USD")
    cents = int(dollars.amount * 100)  # 4567
    print(f"Amount in cents: {cents}")

    # Working with currencies that have 0 decimal places
    yen_amount = 1000  # ¥1000 (JPY has 0 decimal places)
    jpy = Money(yen_amount, "JPY")
    print(jpy.format())  # ¥1,000

Note that moneyx handles the smallest currency unit internally, but converting to/from cents may be necessary when interfacing with other systems or databases that store monetary values as integers.

Rounding Strategies
------------------

Moneyx provides multiple rounding strategies for different financial scenarios:

.. code-block:: python

    from moneyx import Money, RoundingMode

    # Default rounding (HALF_UP)
    m1 = Money("2.5", "USD")              # Rounds to 3 when needed
    
    # Banker's rounding (HALF_EVEN)
    m2 = Money("2.5", "USD", rounding=RoundingMode.BANKERS)  # Rounds to 2 when needed
    m3 = Money("3.5", "USD", rounding=RoundingMode.BANKERS)  # Rounds to 4 when needed
    
    # Other rounding modes
    m4 = Money("2.5", "USD", rounding=RoundingMode.HALF_ODD)         # Rounds to 3
    m5 = Money("2.5", "USD", rounding=RoundingMode.HALF_TOWARDS_ZERO)  # Rounds to 2
    m6 = Money("2.5", "USD", rounding=RoundingMode.HALF_AWAY_FROM_ZERO)  # Rounds to 3
    m7 = Money("2.5", "USD", rounding=RoundingMode.DOWN)             # Rounds to 2
    m8 = Money("2.5", "USD", rounding=RoundingMode.UP)               # Rounds to 3
    m9 = Money("2.5", "USD", rounding=RoundingMode.CEILING)          # Rounds to 3
    m10 = Money("2.5", "USD", rounding=RoundingMode.FLOOR)           # Rounds to 2

Currency Operations
------------------

Working with Currencies
^^^^^^^^^^^^^^^^^^^^^^

Access and manage currency information:

.. code-block:: python

    from moneyx import Money
    from moneyx.currency import Currency

    # Currency information
    usd = Money("100.00", "USD")
    print(f"Symbol: {usd.currency.symbol}")              # $
    print(f"Name: {usd.currency.name}")                  # US Dollar
    print(f"Decimals: {usd.currency.decimals}")          # 2
    print(f"Countries: {usd.currency.countries}")         # List of countries

    # Find currencies by country
    swiss_currencies = Currency.get_by_country("SWITZERLAND")
    for curr in swiss_currencies:
        print(f"{curr.code}: {curr.name}")               # CHF, CHE, CHW

    # Find currency by numeric code
    eur = Currency.get_by_number("978")
    print(f"{eur.code}: {eur.name}")                     # EUR: Euro

Currency Conversion
^^^^^^^^^^^^^^^^^^

Convert between currencies with specified rates:

.. code-block:: python

    from moneyx import Money

    # Convert USD to EUR
    usd = Money("100.00", "USD")
    eur = usd.convert_to("EUR", rate=0.85)               # €85.00
    
    # Convert back
    usd_again = eur.convert_to("USD", rate=1.18)         # $100.30 (may differ due to rounding)

Advanced Features
----------------

Allocation
^^^^^^^^^

Allocate a money amount according to specified ratios:

.. code-block:: python

    from moneyx import Money

    total = Money("100.00", "USD")
    
    # Allocate by ratio
    allocated = total.allocate([1, 2, 3, 4])  # Divide in ratio 1:2:3:4
    for i, amount in enumerate(allocated):
        print(f"Person {i+1} gets: {amount.format()}")
    
    # Outputs:
    # Person 1 gets: $10.00
    # Person 2 gets: $20.00
    # Person 3 gets: $30.00
    # Person 4 gets: $40.00
    
    # Split evenly
    shared = total.split_evenly(3)  # Divide equally among 3 people
    for i, amount in enumerate(shared):
        print(f"Person {i+1} pays: {amount.format()}")
    
    # Outputs:
    # Person 1 pays: $33.34
    # Person 2 pays: $33.33
    # Person 3 pays: $33.33

Tax Calculations
^^^^^^^^^^^^^^

Calculate tax or extract tax from inclusive amounts:

.. code-block:: python

    from moneyx import Money

    price = Money("100.00", "USD")
    
    # Add 7% tax
    with_tax = price.with_tax(7)
    print(f"Price with tax: {with_tax.format()}")        # $107.00
    
    # Extract tax from inclusive amount
    tax_info = with_tax.extract_tax(7)
    print(f"Base amount: {tax_info['base'].format()}")  # $100.00
    print(f"Tax amount: {tax_info['tax'].format()}")    # $7.00

Serialization
^^^^^^^^^^^^

Serialize and deserialize money objects:

.. code-block:: python

    from moneyx import Money
    import json

    price = Money("99.99", "USD")
    
    # To/from JSON
    json_str = price.to_json()
    print(json_str)                                      # {"amount": "99.99", "currency": "USD", ...}
    
    # Recreate from JSON
    restored = Money.from_json(json_str)
    print(restored.format())                             # $99.99
    
    # To/from dictionary
    data = price.to_dict()
    print(data)                                          # {'amount': '99.99', 'currency': 'USD', ...}
    
    # Recreate from dictionary
    restored = Money.from_dict(data)
    print(restored.format())                             # $99.99

Best Practices
-------------

1. **Always use strings for input**: When creating Money objects, prefer using strings for the amount to avoid floating-point precision issues.

   .. code-block:: python

       # Good
       Money("19.99", "USD")
       
       # Avoid
       Money(19.99, "USD")

2. **Check currencies before operations**: Ensure that operations are performed between Money objects of the same currency.

3. **Use appropriate rounding modes**: Choose the correct rounding mode for your financial context.

4. **Be aware of currency precision**: Different currencies have different decimal precisions.

   .. code-block:: python

       Money("100", "JPY")        # JPY has 0 decimal places
       Money("100.00", "USD")     # USD has 2 decimal places
       Money("100.000", "BHD")    # BHD has 3 decimal places

5. **Validate inputs**: Catch potential exceptions from invalid inputs.

   .. code-block:: python

       try:
           amount = Money(user_input, currency_code)
       except (ValueError, PrecisionError, InvalidCurrencyError) as e:
           print(f"Invalid input: {e}") 