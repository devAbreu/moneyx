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