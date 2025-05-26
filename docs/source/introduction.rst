=========================
Introduction to moneyx
=========================

Overview
--------

``moneyx`` is a precise and extensible library for handling money in Python. It addresses 
the common pitfalls and challenges associated with monetary calculations:

* **Precision issues**: Floating-point arithmetic can lead to rounding errors
* **Currency management**: Handling different currencies with proper symbols and formatting
* **Allocation problems**: Splitting money fairly without losing pennies
* **Tax calculations**: Calculating and extracting taxes consistently

Key Features
-----------

* **Absolute precision** using ``decimal.Decimal`` internally
* **Extensive rounding modes** with multiple strategies
* **ISO 4217 currency support** with proper symbols and decimal places
* **Currency validation and lookups** by country or numeric code
* **Currency conversion** with configurable rates
* **Money allocation** with proper remainder handling
* **Tax calculation** utilities
* **Thread-safe operations** for concurrent environments

Why not use floats for money?
-----------------------------

Using floating-point numbers (``float``) for monetary calculations can lead to unexpected
results due to the way computers represent decimal fractions in binary.

For example:

.. code-block:: python

    >>> 0.1 + 0.2
    0.30000000000000004

    >>> 19.99 * 3
    59.97000000000001

These small inaccuracies can accumulate and cause significant errors, especially in 
financial applications where precision is crucial.

``moneyx`` addresses this by using the ``decimal.Decimal`` type internally, which provides
exact decimal arithmetic as needed for monetary calculations.

Why use moneyx?
--------------

* **Precision**: Guaranteed accurate calculations without floating-point errors
* **Safety**: Type checking and validation prevent common errors
* **Convenience**: Rich API for common money operations
* **Compliance**: ISO 4217 support ensures standard currency handling
* **Performance**: Optimized for both individual and bulk operations
* **Type hints**: Full type annotation support for modern development 

The Money Pattern
----------------

``moneyx`` implements the Money Pattern as described by Martin Fowler in his book "Patterns of Enterprise Application Architecture" (2002). As Fowler notes:

    "A large proportion of the computers in this world manipulate money, so it's always puzzled me 
    that money isn't actually a first class data type in any mainstream programming language."

The Money Pattern creates a first-class representation of monetary values that handles currency, precision, and rounding issues properly. By implementing this pattern, ``moneyx`` helps you avoid common pitfalls in financial calculations.

Learn more about the pattern at `Martin Fowler's Money Pattern <https://martinfowler.com/eaaCatalog/money.html>`_. 