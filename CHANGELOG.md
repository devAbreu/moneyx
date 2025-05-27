# Changelog

All notable changes to the `moneyx` project will be documented in this file.

This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Thread-safety improvements
- Property-based testing with Hypothesis
- Performance benchmarks for high-volume operations

### Changed
- Improved package structure following modern Python best practices
- Enhanced documentation with Sphinx

### Fixed
- Precision issues in allocation and remainder handling
- Currency conversion edge cases

## [0.1.1] - 2025-07-26

### Added
- Reference to Martin Fowler's Money Pattern in documentation
- ReadTheDocs integration for comprehensive documentation
- Documentation on working with cents and smallest currency units

### Changed
- Updated documentation URLs to point to ReadTheDocs
- Improved GitHub username references across documentation
- Enhanced development and installation instructions

## [0.1.0] - 2025-05-26

### Added
- Initial release with core Money class
- Currency handling with ISO 4217 support
- Multiple rounding strategies
- Basic arithmetic operations (add, subtract, multiply)
- Tax calculation utilities
- Money allocation and distribution functions
- Formatting with locale support
- Serialization to/from JSON and dictionaries
- Type hints throughout the codebase
- Basic test suite with high coverage 