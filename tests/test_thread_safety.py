"""Tests for thread safety and concurrency in the moneyx library."""

import concurrent.futures
import random
from decimal import Decimal

from moneyx import Money
from moneyx.currency import Currency


def test_concurrent_money_creation():
    """Test that concurrent Money object creation is thread-safe."""

    def create_money(code_and_amount):
        code, amount = code_and_amount
        return Money(amount, code)

    def generate_valid_amount(currency_code):
        """Generate a valid amount for the given currency code."""
        currency = Currency.get(currency_code)
        if currency.decimals == 0:
            # For currencies with no decimal places (e.g., JPY)
            return str(random.randint(100, 10000))
        else:
            # For currencies with decimal places
            whole = random.randint(100, 10000)
            decimal_part = random.randint(0, 10**currency.decimals - 1)
            decimal_str = str(decimal_part).zfill(currency.decimals)
            return f"{whole}.{decimal_str}"

    # Generate a mix of currency codes and amounts
    currencies = ["USD", "EUR", "GBP", "JPY", "CAD", "AUD"]
    test_data = []

    # Generate valid amounts for each currency
    for _ in range(50):
        code = random.choice(currencies)
        amount = generate_valid_amount(code)
        test_data.append((code, amount))

    # Execute in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(create_money, test_data))

    # Verify results
    assert len(results) == len(test_data)
    for result, (code, amount) in zip(results, test_data):
        assert result.currency.code == code
        assert result.amount == Decimal(amount)


def test_concurrent_currency_lookup():
    """Test that concurrent currency lookups are thread-safe."""

    def get_currency(code):
        return Currency.get(code)

    # Generate a mix of currency codes
    codes = ["USD", "EUR", "GBP", "JPY", "CAD", "AUD", "CHF", "CNY", "HKD"]
    test_data = codes * 10  # Repeat to create more load

    # Execute in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(get_currency, test_data))

    # Verify results
    assert len(results) == len(test_data)
    for result, code in zip(results, test_data):
        assert result.code == code


def test_concurrent_arithmetic():
    """Test that concurrent arithmetic operations are thread-safe."""

    def perform_operations(seed):
        """Perform a series of arithmetic operations with a random seed."""
        random.seed(seed)
        money = Money("100.00", "USD")

        # Perform multiple operations
        for _ in range(20):
            op = random.choice(["add", "subtract", "multiply"])
            if op == "add":
                money = money.add(Money("10.00", "USD"))
            elif op == "subtract":
                money = money.subtract(Money("5.00", "USD"))
            else:  # multiply
                money = money.multiply(1.1)

        return money

    # Execute in parallel with different seeds
    seeds = list(range(50))
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(perform_operations, seeds))

    # Verify that all operations completed
    assert len(results) == len(seeds)

    # Results will differ due to different random seeds, but should all be Money objects
    for result in results:
        assert isinstance(result, Money)
        assert result.currency.code == "USD"


def test_concurrent_allocations():
    """Test that concurrent allocations are thread-safe."""

    def allocate_money(data):
        amount, weights = data
        money = Money(amount, "USD")
        return money.allocate(weights)

    # Generate test data
    test_data = [
        (
            f"{random.randint(100, 10000)}.00",
            [random.randint(1, 10) for _ in range(random.randint(2, 5))],
        )
        for _ in range(50)
    ]

    # Execute in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(allocate_money, test_data))

    # Verify results
    assert len(results) == len(test_data)
    for result, (amount, weights) in zip(results, test_data):
        # Check that the allocation has the correct number of parts
        assert len(result) == len(weights)
        # Check that the sum equals the original amount
        total = sum(part.amount for part in result)
        assert total == Decimal(amount)
