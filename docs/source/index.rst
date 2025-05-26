===========================
moneyx: Precise Money Handling
===========================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   introduction
   installation
   usage
   api/index
   development
   changelog

Introduction
===========

``moneyx`` is a precise and extensible library for handling money in Python. It follows best practices for monetary calculations and is ISO 4217 compliant, supporting all standard currencies with their correct decimal precision.

Features
--------

* Full ISO 4217 support with accurate currency data
* Precise decimal calculations using Python's Decimal type
* Multiple rounding strategies for different financial scenarios
* Money allocation and distribution functions
* Tax calculation utilities
* Comprehensive support for currency formatting and localization
* Type-hinted API for better IDE support

Quick Example
------------

.. code-block:: python

   from moneyx import Money
   
   # Create money objects
   price = Money("19.99", "USD")
   qty = 3
   
   # Perform calculations
   total = price.multiply(qty)
   with_tax = total.with_tax(8.25)  # Add 8.25% tax
   
   # Format for display
   print(f"Total: {total.format()}")  # Total: $59.97
   print(f"With tax: {with_tax.format()}")  # With tax: $64.92
   
   # Split payment between friends
   payments = with_tax.split_evenly(3)
   for i, payment in enumerate(payments, 1):
       print(f"Person {i} pays: {payment.format()}")

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search` 