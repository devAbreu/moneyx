============
Installation
============

Basic Installation
-----------------

You can install ``moneyx`` using pip:

.. code-block:: bash

    pip install moneyx

This will install the core package with all required dependencies.

Development Installation
-----------------------

For development, you can install the package with additional dependencies:

.. code-block:: bash

    # Clone the repository
    git clone https://github.com/yourusername/moneyx.git
    cd moneyx

    # Install with development dependencies
    pip install -e ".[dev,test]"

Optional Dependencies
--------------------

``moneyx`` offers several optional dependency sets:

* ``dev``: Development tools (black, isort, mypy, ruff)
* ``test``: Testing tools (pytest, pytest-cov, hypothesis)
* ``docs``: Documentation tools (sphinx, sphinx-rtd-theme)
* ``all``: All optional dependencies

.. code-block:: bash

    # Install with specific optional dependencies
    pip install moneyx[dev]    # Development tools
    pip install moneyx[test]   # Testing tools
    pip install moneyx[docs]   # Documentation tools
    pip install moneyx[all]    # All optional dependencies

Requirements
-----------

``moneyx`` requires:

* Python 3.8 or higher
* Babel 2.12.0 or higher (for localization and formatting)
* typing-extensions for Python < 3.10 (for TypedDict support)

Verifying Installation
---------------------

To verify that ``moneyx`` is correctly installed, you can run:

.. code-block:: python

    import moneyx
    print(moneyx.__version__)

    # Create a simple Money object to test functionality
    money = moneyx.Money("10.99", "USD")
    print(money.format())  # Should output: $10.99 