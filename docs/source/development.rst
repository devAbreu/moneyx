=================
Development Guide
=================

This guide explains how to set up the development environment for contributing to ``moneyx``.

Setting Up the Development Environment
-------------------------------------

1. Clone the repository:

   .. code-block:: bash

       git clone https://github.com/yourusername/moneyx.git
       cd moneyx

2. Create a virtual environment (optional but recommended):

   .. code-block:: bash

       python -m venv venv
       source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install development dependencies:

   .. code-block:: bash

       pip install -e ".[dev,test]"

4. Set up pre-commit hooks:

   .. code-block:: bash

       pre-commit install

Running Tests
------------

Run the test suite with pytest:

.. code-block:: bash

    # Run all tests
    pytest

    # Run tests with coverage
    pytest --cov=moneyx

    # Run tests with specific marks
    pytest -m "not slow"

    # Run specific test file
    pytest tests/test_money.py

Code Style and Quality
---------------------

``moneyx`` uses several tools to ensure code quality:

* **Black**: Code formatting
* **isort**: Import sorting
* **mypy**: Static type checking
* **ruff**: Linting and code quality checks
* **bandit**: Security checks

You can run these tools individually:

.. code-block:: bash

    # Format code with Black
    black .

    # Sort imports with isort
    isort .

    # Type-check with mypy
    mypy src

    # Lint with ruff
    ruff .

    # Security check with bandit
    bandit -r src

Or run all checks at once using pre-commit:

.. code-block:: bash

    pre-commit run --all-files

Building Documentation
---------------------

To build the documentation:

1. Install documentation dependencies:

   .. code-block:: bash

       pip install -e ".[docs]"

2. Build the documentation:

   .. code-block:: bash

       cd docs
       make html

3. View the documentation:

   Open ``docs/build/html/index.html`` in your browser.

Versioning and Releases
----------------------

``moneyx`` follows `Semantic Versioning <https://semver.org/>`_.

To create a new release:

1. Update the version using the version script:

   .. code-block:: bash

       python scripts/bump_version.py [major|minor|patch]

2. Review and commit the changes:

   .. code-block:: bash

       git commit -am "Bump version to x.y.z"

3. Tag the release:

   .. code-block:: bash

       git tag -a vx.y.z -m "Version x.y.z"

4. Push the changes:

   .. code-block:: bash

       git push && git push --tags

The CI/CD pipeline will automatically publish the package to PyPI when a new tag is pushed.

Pull Request Guidelines
----------------------

When submitting a pull request:

1. Ensure all tests pass and code quality checks succeed.
2. Add tests for new features or bug fixes.
3. Update documentation if necessary.
4. Follow the code style of the project.
5. Include a clear description of the changes.
6. Reference any relevant issues in your PR description.

Reporting Issues
---------------

If you find a bug or want to request a feature:

1. Check the existing issues on GitHub to avoid duplicates.
2. Create a new issue with a clear title and description.
3. For bug reports, include steps to reproduce, expected behavior, and actual behavior.
4. For feature requests, explain the use case and benefits.

License
-------

By contributing to ``moneyx``, you agree that your contributions will be licensed under the project's MIT License. 