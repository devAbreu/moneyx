import json

from moneyx import Money
from moneyx.exceptions import InvalidCurrencyError, PrecisionError


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
            print(
                f"  {item['name']} ({item['quantity']}x): "
                f"{item['price'].format()} each = {item['subtotal'].format()}",
            )

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
            "items": [
                {
                    "name": item["name"],
                    "price": item["price"].to_dict(),
                    "quantity": item["quantity"],
                }
                for item in items
            ],
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
