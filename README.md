# SPK Universal Timestamp

[![PyPI version](https://badge.fury.io/py/spk-universal-timestamp.svg)](https://badge.fury.io/py/spk-universal-timestamp)
[![Python versions](https://img.shields.io/pypi/pyversions/spk-universal-timestamp.svg)](https://pypi.org/project/spk-universal-timestamp/)
[![License](https://img.shields.io/pypi/l/spk-universal-timestamp.svg)](https://github.com/RoswellMiller/spk-universal-timestamp/blob/main/LICENSE)
[![Tests](https://github.com/RoswellMiller/spk-universal-timestamp/workflows/Tests/badge.svg)](https://github.com/RoswellMiller/spk-universal-timestamp/actions)

A comprehensive multi-scale timestamp system for knowledge bases that handles time from geological epochs to attosecond precision with cultural calendar support.

## Features

- 🌍 **Geological Time Scales** - Handle billions of years with appropriate precision levels
- 📅 **Cultural Calendars** - Support for Gregorian, Julian, Hebrew, and Chinese calendars
- 🔄 **Uniform sorting** - Sort time stamps across all calendars achieving order within the precision of each time stamp
- 🌟 **Astronomical Time** - Julian Day Numbers and coordinate time
- ⚗️ **Scientific Measurements** - High-precision timestamps with uncertainty tracking
- ⚡ **Ultra-High Precision** - From attoseconds to billion-year scales
- 🔄 **Calendar Conversions** - Seamless conversion between calendar systems
- 📖 **Type Safety** - Full type annotations for better IDE experience

## Installation

Install from PyPI:

```bash
pip install spk-universal-timestamp
```

Or install from source:

```bash
git clone https://github.com/RoswellMiller/spk-universal-timestamp.git
cd spk-universal-timestamp
pip install -e .
```

## Quick Start Examples

```python
from SPK_UniversalTimestamp import (
    UnivTimestampFactory,
    Calendar, 
    Precision,
    UnivGREGORIAN
)
from decimal import Decimal

# Get current time
now = UnivTimestampFactory.now()
print(f"Current time: {now.format_signature()}")

# Create timestamps for different calendar systems
greg_date = UnivGREGORIAN(2025, 9, 8, description="Example date")
print(f"Gregorian date: {greg_date.strftime('%A, %B %d, %Y')}")

# Create timestamp with scientific precision
scientific_ts = UnivTimestampFactory.for_SCIENTIFIC(
    2035, 7, 28, 21, 47, Decimal("30.123_123_123_123_123_123"),
    description="Quantum experiment measurement"
)
print(f"Scientific timestamp: {scientific_ts.format_signature()}")

# Create timestamp from Unix timestamp
unix_ts = UnivTimestampFactory.from_unix_timestamp(
    1640995200.123456789,
    description="Unix timestamp example"
)
print(f"From Unix timestamp: {unix_ts.format_signature()}")

# Format timestamps in different languages
print(now.strftime("%A, %B %d, %Y %H:%M:%S", language='en'))
print(now.strftime("%A %d %B %Y %H:%M:%S", language='fr'))
print(now.strftime("%A %d %B %Y %H:%M:%S", language='de'))

```
## API Reference
The `UnivTimestamp` is a python class intended to support a time stamp the can be universally ordered.  The underlying notion
of ordering is the rata die(rd) developed by Reingold and Dershowitz in their book "Calendrical Calculations : The Ultimate Edition".  While
the rd maps human calendars to a unique day number as does the modern Julian Day number, we have extended the notion to UTC attosecond enabling
timestamps to be accurately sorted and distinguished.  The extensions make extensive use of Python's long integer and Decimal numbers
and functional calculations with the current precision for Decimal set to 35. 

Each calendar is an subclass of `UnivTimestamp` either `UnivGEOLOGICAL` or `UnivCalendars` which is further subclassed into `UnivGREGORIAN`,
`UnivJULIAN`, `UnivHEBREW` and `UnivCHINESE`.  The components of the time stamp are added as follows: `UnivTimestamp` maintains a year.  `The UnivCalendar` maintains month, day, hour, minute, seconds and timezone. Geological time does not have a UTC time stamp as there is no current need nor perhaps method of accurately telling time of day in the time periods covered by Geological time.  It should be further noted that while the time is kept in local time in the time stamp it is converted to UTC time for sorting.  This sorting value is the field/slot sortvalue.

When specifying a timestamp the elements of the time stamp must be stated top(year) down with no intervening type None values. Specifying a precision is therefore unnecessary unless your using geological time or needing seconds to be more precise, more accurate than seconds e.g. when using `UnivTimestampFactory.from_ms_datetime(ms : DateTime)` the UnivTimestamp constructor will pick microseconds as the precision, unless you override it. 

There are known problems with some of the astronomy calculations used in the Appendix C of "Calendrical Calculations".  The test cases highlight these
known issues.  The correct fix for these errors and for errors that will appear in other astronomically based calendars is to convert them all to JPL's DE422.
This is an objective for a next release since there are historical issues in addition to scientific issues.  For example, it's not enough to convert to
the science based numbers and apply them to a period in history in which they would not have been known.  All us further complicated by the possibility of not knowing how it was done in some periods of history.

### Main Classes

#### `Calendar` (Enum)
- `GREGORIAN` - Standard Gregorian calendar
- `JULIAN` - Julian calendar (Old Style)  
- `CHINESE` - Chinese traditional calendar
- `HEBREW` - Hebrew/Jewish calendar
- `GEOLOGICAL` - Geological time scales

#### `Precision` (Enum)
**Timestamp Precision:**
- `BILLION_YEARS`, `MILLION_YEARS`, `THOUSAND_YEARS`
- `CENTURY`, `DECADE`, `YEAR`, `MONTH`, `DAY`
- `HOUR`, `MINUTE`, `SECOND`
- `MILLISECOND`, `MICROSECOND`, `NANOSECOND`
- `PICOSECOND`, `FEMTOSECOND`, `ATTOSECOND`

### Class Methods

#### UnivTimestamp
##### Constructors
UnivGEOLOGICAL(years_ago, precision, description)
UnivGREGORIAN(year, month, day, hour, minute, second, precision, description)
UnivJULIAN(year, month, day, hour, minute, second, precision, description)
UnivHEBREW(year, month, day, hour, minute, second, precision, description)
UnivCHINESE(cycle, year, (leap,term), day, hour, minute, second, precision, description)

##### Standard
strftime(format)
__str__
__repr__


#### UnivTimestampFactory
##### Utilities
UnivTimestampFactory.now()
UnivTimestampFactory.convert(to_calendar, from_timestamp)
parse(string)
parse_repr(string)
UnivTimestampFactory.from_unix_timestamp(timestamp, precision)
UnivTimestampFactory.from_ISO_timestamp(timestamp, precision)
UnivTimestampFactory.for_SCIENTIFIC(year, month, day, hour, minute, second, description)


##### Predefined Constants
- python
GEOLOGICAL_PERIODS = {
    "Hadean": ...,
    "Archean": ...,
    "Proterozoic": ...,
    # ... more geological periods
}

MEASUREMENT_HISTORY = {
    "meter_definition_1793": ...,
    "atomic_second_1967": ...,
    "si_redefinition_2019": ...,
    # ... more measurement milestones
}


## Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/RoswellMiller/spk-universal-timestamp.git
cd spk-universal-timestamp

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode with dev dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=SPK_UniversalTimestamp --cov-report=html

# Run specific test file
pytest Tests/test_timestamp.py
```

### Code Quality

```bash
# Format code
black .

# Sort imports
isort .

# Lint code
flake8

# Type checking
mypy SPK_UniversalTimestamp
```

### Building and Publishing

```bash
# Build the package
python -m build

# Check the build
twine check dist/*

# Upload to TestPyPI (optional)
twine upload --repository testpypi dist/*

# Upload to PyPI
twine upload dist/*
```

## 🚧 Active Development Branch

We are currently working on `release/v1.1.0`.  
Please submit bug fixes and enhancements to this branch until the next stable release.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and ensure they pass
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## License

This project is licensed under a **Custom Dual License**:

### 🆓 **Single Use License (Free)**
- ✅ Personal, educational, or research use
- ✅ Single-user applications
- ✅ Open source projects (with attribution)
- ✅ Academic research and publications

### 💼 **Commercial License (Paid)**
For commercial use, enterprise deployment, or integration into sold software products, a separate commercial license must be obtained. This includes:
- 🏢 Company/enterprise environments with multiple users
- 💰 Software products that are sold or commercially distributed
- 🔄 SaaS platforms and commercial services
- 📦 Commercial software packages

**Contact for Commercial Licensing:** [roswellmiller@gmail.com]

See the [LICENSE](LICENSE) file for complete terms and conditions.

## Changelog

### [1.0.0] - 2025-09-15
- Initial release
- Basic timestamp handling and conversion functionality
- Support for Unix timestamps, ISO strings, and datetime objects
