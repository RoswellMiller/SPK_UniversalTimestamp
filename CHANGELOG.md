# SPK Universal Timestamp Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial project structure
- Basic timestamp handling functionality
- Gregorian Calendar
- Julian Calendar
- Hebrew Calendar
- Chinese Calendar - Note this first version is based purely on the astronomical calculations
    taken from "Calendrical Calculation" by Reingold and Dershowitz.  This implementation has known
    problems with some of the astronomical calculations. A version 2 is planned which will be consistent
    with the JPL De422 standard.

## [1.0.0] - 2025-09-15

### Added
- Initial release of SPK Universal Timestamp
- `UnivTimestamp` class for handling various timestamp formats
- `UnivTimestampFactory` class for conversion from Unix timestamps, ISO format strings, and datetime objects
- Conversion methods between different timestamp formats
- UTC-first approach for consistency
- Comprehensive test suite, designed for being run under pytest
- Type hints for better IDE support
- Documentation and examples

### Features
- Create timestamps from current time, Unix timestamps, ISO strings, or datetime objects
- Convert between supported calendars, Gregorian, Julian, Hebrew and Chinese
- Timezone handling and UTC normalization
- Two classes are provided : 
- a. UnivTimestamp - A timestamp
- b. UnivTimestampFactory - A package of support routines for cross calendar UnivTimestamp construction and conversion.
- Comprehensives series of test cases, which also serve as examples of how the UnivTimestamp is used.
