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
- 🌟 **Astronomical Time** - Julian Day Numbers
- ⚗️ **Scientific Measurements** - High-precision timestamps with uncertainty tracking
- ⚡ **Ultra-High Precision** - From attoseconds to billion-year scales
- ⏱️ **Time Spans** - `UnivDuration` for arithmetic over time intervals at any precision level
- 🔄 **Calendar Conversions** - Seamless conversion between calendar systems
- 📖 **Type Safety** - Full type annotations for better IDE experience
- 📖 **Multi-lingual** - For some calendars there is English, French, German, Italian


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

### UnivMoment

```python
from SPK_UniversalTimestamp import (
    UnivMoment,
    UnivDuration,
    Calendar,
    UnivMomPrecision,
    MomPrecLevel,
    MomPrecAbbrev,
)
from decimal import Decimal

# Get current time (default: MICROSECOND precision)
now = UnivMoment.now()
print(f"Current time: {now.format_signature()}")

# Create a Gregorian timestamp
greg_date = UnivMoment.from_gregorian(2025, 9, 8, description="Example date")
print(f"Gregorian date: {greg_date.present(Calendar.GREGORIAN, '%A, %B %d, %Y')}")

# Create timestamp with scientific precision
scientific_ts = UnivMoment.from_gregorian(
    2035, 7, 28, 21, 47, Decimal("30.123123123123123123"),
    precision=UnivMomPrecision.ATTOSECOND,
    description="Quantum experiment measurement"
)
print(f"Scientific timestamp: {scientific_ts.format_signature()}")

# Format timestamps in different languages
print(now.present(Calendar.GREGORIAN, "%A, %B %d, %Y %H:%M:%S", language='en'))
print(now.present(Calendar.GREGORIAN, "%A %d %B %Y %H:%M:%S", language='fr'))
print(now.present(Calendar.GREGORIAN, "%A %d %B %Y %H:%M:%S", language='de'))

# Subtract two UnivMoments → produces a UnivDuration
t1 = UnivMoment.from_gregorian(2025, 1, 1, 0, 0, 0)
t2 = UnivMoment.from_gregorian(2025, 1, 2, 1, 1, 1)
gap: UnivDuration = t2 - t1
print(gap.format_for_display())     # → "1 day 1 hr 1 min 1 s"

# Add a UnivDuration to a UnivMoment
one_week = UnivDuration(Decimal("604800"), precision=3)  # 7 days
next_week = t1 + one_week
print(next_week.present(Calendar.GREGORIAN, "%Y-%m-%d"))
```

### UnivDuration

`UnivDuration` represents a time span (positive or negative) expressed in seconds with a
precision level that determines how finely the value is rounded and displayed.

```python
from SPK_UniversalTimestamp import UnivDuration
from decimal import Decimal

# --- Construction ---

# 90 061 seconds at second precision
dur_s = UnivDuration(90061)                        # precision=0 (SECOND) is the default
print(dur_s.format_for_display())                  # → "1 day 1 hr 1 min 1 s"

# Exactly 3 days at day-level precision (precision=3)
dur_d = UnivDuration(Decimal("259200"), precision=3)
print(dur_d.format_for_display())                  # → "3 days"

# 1.5 hours at minute precision (precision=1)
dur_m = UnivDuration(Decimal("5400"), precision=1)
print(dur_m.format_for_display())                  # → "1 hr 30 mins"

# Geological: 65 million years in seconds, at million-year precision (precision=6)
my_secs = Decimal("31557600000000") * Decimal("65")
dur_geo = UnivDuration(my_secs, precision=6)
print(dur_geo.format_for_display())                # → "65 M-years"

# Sub-second: 5.123 seconds at millisecond precision (precision=-3)
dur_ms = UnivDuration(Decimal("5.123"), precision=-3)
print(dur_ms.format_for_display())                 # → "5 s 123 ms"

# Nanosecond precision (precision=-9)
dur_ns = UnivDuration(Decimal("0.000000001"), precision=-9)
print(dur_ns.format_for_display())                 # → "1 ns"

# --- Arithmetic ---

d1 = UnivDuration(Decimal("3600"), precision=1)    # 1 hour at minute precision
d2 = UnivDuration(Decimal("1800"), precision=1)    # 30 minutes at minute precision
total = d1 + d2
print(total.format_for_display())                  # → "1 hr 30 mins"

diff = d1 - d2
print(diff.format_for_display())                   # → "30 mins"

# When precisions differ, the coarser precision wins
coarse = UnivDuration(Decimal("86400"), precision=3)   # 1 day (day precision)
fine   = UnivDuration(Decimal("3600"),  precision=0)   # 1 hour (second precision)
result = coarse + fine                                  # result is day-precision
print(result.precision)                                # → 3
print(result.format_for_display())                     # → "1 day"  (1 hr rounds away)

# --- Comparison ---

d3 = UnivDuration(Decimal("7200"))
d4 = UnivDuration(Decimal("3600"))
print(d3 > d4)   # True — ordered by total seconds

# --- Serialization ---

# Dictionary round-trip (suitable for JSON)
d = UnivDuration(Decimal("3661"), precision=1)
data = d.to_dict()
# {'seconds': '3661', 'precision': '1'}
restored = UnivDuration.from_dict(data)
assert restored == d

# Lexical key (sortable string)
key = d.to_StdLexicalKey()
# → "univDU000000000000003661.000000000000000000.01P"
back = UnivDuration.from_StdLexicalKey(key)
assert back == d

# --- Class constants (read-only) ---

# LEVEL_QUANTUM: seconds-per-quantum for whole-unit levels 0..7
print(UnivDuration.LEVEL_QUANTUM[3])    # → 86400  (seconds in one day)
print(UnivDuration.LEVEL_QUANTUM[0])    # → 1      (one second)

# LEVEL_ABBREV: display string for every level -18..7
print(UnivDuration.LEVEL_ABBREV[4])     # → "years"
print(UnivDuration.LEVEL_ABBREV[-3])    # → "ms"

# Both are MappingProxyType — any write raises TypeError
try:
    UnivDuration.LEVEL_QUANTUM[0] = 2
except TypeError:
    pass  # expected

# --- Parsing (from_string) ---

# Single integer pair
d = UnivDuration.from_string("5 s")
print(d.format_for_display())                  # → "5 s"

# Decimal value: each decimal digit shifts precision one level finer
d = UnivDuration.from_string("10.001 s")
assert d.precision == -3                       # 3 decimal places → ms
print(d.format_for_display())                  # → "10 s 1 ms"

# Decimal on a coarse unit subdivides it
d = UnivDuration.from_string("10.5 M-years")
assert d.precision == 5                        # 1 decimal place → k-years
print(d.format_for_display())                  # → "10 M-years 500 k-years"

# Compound string: precision = finest level across all pairs
d = UnivDuration.from_string("1 day 2 hrs 30 mins")
print(d.format_for_display())                  # → "1 day 2 hrs 30 mins"

# Round-trip with format_for_display
original = UnivDuration(90061, precision=0)    # 1 day 1 hr 1 min 1 s
restored = UnivDuration.from_string(original.format_for_display())
assert restored.seconds   == original.seconds
assert restored.precision == original.precision
```

### Precision Level Reference

`UnivDuration.precision` and `MomPrecLevel[UnivMomPrecision.*]` use the same integer scheme:

| Level | UnivMomPrecision      | Quantum           |
|------:|:----------------------|:------------------|
|     7 | `BILLION_YEARS`       | 10⁹ Julian years  |
|     6 | `MILLION_YEARS`       | 10⁶ Julian years  |
|     5 | `THOUSAND_YEARS`      | 10³ Julian years  |
|     4 | `YEAR`                | 1 Julian year     |
|     3 | `DAY`                 | 86 400 s          |
|     2 | `HOUR`                | 3 600 s           |
|     1 | `MINUTE`              | 60 s              |
|     0 | `SECOND`              | 1 s               |
|    -3 | `MILLISECOND`         | 10⁻³ s            |
|    -6 | `MICROSECOND`         | 10⁻⁶ s            |
|    -9 | `NANOSECOND`          | 10⁻⁹ s            |
|   -12 | `PICOSECOND`          | 10⁻¹² s           |
|   -15 | `FEMTOSECOND`         | 10⁻¹⁵ s           |
|   -18 | `ATTOSECOND`          | 10⁻¹⁸ s           |

Higher value = coarser; lower (more negative) = finer.
`MONTH` is intentionally absent: month length is calendar-specific and cannot
represent a universal time quantum.

## API Reference

The `UnivMoment` is a python class intended to support a time stamp that can be universally ordered.  The underlying notion
of ordering is the rata die (rd) developed by Reingold and Dershowitz in their book "Calendrical Calculations : The Ultimate Edition".  While
the rd maps human calendars to a unique day number as does the modern Julian Day number, we have extended the notion to UTC attosecond enabling
timestamps to be accurately sorted and distinguished.  The extensions make extensive use of Python's long integer and Decimal numbers
and functional calculations with the current precision for Decimal set to 35.

When specifying a timestamp the elements of the time stamp must be stated top (year) down with no intervening `None` values. Specifying a
precision is therefore unnecessary unless you are using geological time or need finer-than-second resolution. The `UnivMoment` constructor
will pick `MICROSECOND` as the precision by default unless you override it.

`UnivDuration` represents a time span (positive or negative) as a `Decimal` number of seconds plus a plain-`int` precision level.
Arithmetic on `UnivDuration` values automatically rounds the result to the coarser of the two operands' precisions.

There are known problems with some of the astronomy calculations used in the Appendix C of "Calendrical Calculations".  The test cases highlight these
known issues.  The correct fix for these errors and for errors that will appear in other astronomically based calendars is to convert them all to JPL's DE422.
This is an objective for a next release since there are historical issues in addition to scientific issues.

### Main Classes

#### `Calendar` (Enum)

- `GREGORIAN` - Standard Gregorian calendar
- `JULIAN` - Julian calendar (Old Style)
- `CHINESE` - Chinese traditional calendar
- `HEBREW` - Hebrew/Jewish calendar
- `GEOLOGICAL` - Geological time scales

#### `UnivMomPrecision` (Enum)

Precision levels for `UnivMoment`.  `MONTH` is **not** included: month length varies
by calendar and cannot represent a universal time quantum.

- `BILLION_YEARS`
- `MILLION_YEARS`
- `THOUSAND_YEARS`
- `YEAR`
- `DAY`
- `HOUR`
- `MINUTE`
- `SECOND`
- `MILLISECOND`
- `MICROSECOND`
- `NANOSECOND`
- `PICOSECOND`
- `FEMTOSECOND`
- `ATTOSECOND`

#### Precision Attribute Dictionaries

Four module-level dicts map `UnivMomPrecision` values to their numeric properties.
They are exported from the package and share the same integer level scheme used by
`UnivDuration.precision`:

```python
MomPrecLevel  : dict[UnivMomPrecision, int]        # precision → level int (0=SECOND, 7=BILLION_YEARS, -18=ATTOSECOND)
MomLevelPrec  : dict[int, UnivMomPrecision]        # reverse of MomPrecLevel
MomPrecPower  : dict[UnivMomPrecision, int | None] # SI exponent (None for day/hour/minute)
MomPrecAbbrev : dict[UnivMomPrecision, str]        # SI-style abbreviation ('ms', 'μs', 'G-yr', …)
```

Example:

```python
from SPK_UniversalTimestamp import UnivMomPrecision, MomPrecLevel, MomPrecAbbrev

prec = UnivMomPrecision.MILLISECOND
print(MomPrecLevel[prec])    # → -3
print(MomPrecAbbrev[prec])   # → "ms"
```

### Class Methods

#### UnivMoment

##### Constructors

```
UnivMoment.from_geological(years_ago, precision, description=)
UnivMoment.from_gregorian(year, month, day, hour, minute, second, precision, description=)
UnivMoment.from_julian(year, month, day, hour, minute, second, precision, description=)
UnivMoment.from_hebrew(year, month, day, hour, minute, second, precision, description=)
UnivMoment.from_chinese(cycle, year, (leap, term), day, hour, minute, second, precision, description=)
UnivMoment.from_datetime(dt, description=)
UnivMoment.from_julian_day_number(jd, precision, description=)
UnivMoment.from_unix_timestamp(unix_ts, precision_time, description=)
UnivMoment.from_string(timestamp_str, description=)
UnivMoment.now(precision=UnivMomPrecision.MICROSECOND)
```

##### Instance Methods

```
moment.present(calendar, format, tz='UTC', language='en') → str
moment.format_signature() → str
moment.format_for_display() → str
moment.to_dict() → dict
moment.to_StdLexicalKey() → str
moment - moment → UnivDuration
moment - duration → UnivMoment
moment + duration → UnivMoment
```

##### Class / Static Methods

```
UnivMoment.from_dict(data) → UnivMoment
UnivMoment.from_StdLexicalKey(lex_key) → UnivMoment
```

#### UnivDuration

##### Construction

```
UnivDuration(seconds: Decimal | int, precision: int = 0)
```

`precision` is a plain `int` using the same level scheme as `MomPrecLevel`:
`0` = second, `3` = day, `7` = billion-year, `-3` = millisecond, `-18` = attosecond.

##### Instance Methods / Operators

```
duration.format_for_display() → str
duration.to_dict() → dict
duration.to_StdLexicalKey() → str
duration + duration → UnivDuration   # result precision = coarser of the two
duration - duration → UnivDuration
duration == duration, <, <=, >, >=   # ordered by total seconds
```

##### Class Constants

```
UnivDuration.LEVEL_QUANTUM  : MappingProxyType   # level → seconds-per-quantum (levels 0..7)
UnivDuration.LEVEL_ABBREV   : MappingProxyType   # level → display abbreviation (levels -18..7)
```

Both are read-only (`MappingProxyType`); any mutation attempt raises `TypeError`.

##### Static / Class Methods

```
UnivDuration.from_dict(data) → UnivDuration
UnivDuration.from_StdLexicalKey(lex_key) → UnivDuration
UnivDuration.from_string(text) → UnivDuration
```

`from_string` parses a compound string of `<number> <unit>` pairs and infers precision
from the finest level present, with decimal places subdividing each unit one level per digit
(e.g. `"10.5 M-years"` → k-year precision, `"10.001 s"` → millisecond precision).

#### Predefined Constants

```
GEOLOGICAL_EONS      # dict of geological eon boundaries
GEOLOGICAL_ERAS      # dict of geological era boundaries
GEOLOGICAL_PERIODS   # dict of geological period boundaries (e.g. "Cambrian", "Jurassic", …)
GEOLOGICAL_EPOCHSandAGES
```

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

**Contact for Commercial Licensing:** [roswellmiller@sarek.ai]

See the [LICENSE](LICENSE) file for complete terms and conditions.

## Changelog

### [1.1.0] - 2026-05-13

#### Added
- `UnivDuration` class — immutable, frozen dataclass representing a time span as a `Decimal` number of seconds with a plain-`int` precision level.  Supports arithmetic (`+`, `-`), comparison, `format_for_display()`, dict/lexical-key serialization.
- `MomPrecLevel`, `MomLevelPrec`, `MomPrecPower`, `MomPrecAbbrev` — four precision attribute dicts exported from the package, replacing the old `PrecisionAtts` dict-of-dicts.
- `UnivMoment.__sub__(UnivMoment)` now returns a `UnivDuration`.
- `UnivMoment.__add__(UnivDuration)` and `UnivMoment.__sub__(UnivDuration)` now return a `UnivMoment`.

#### Changed
- `UnivMomPrecision.MONTH` has been **removed**. Month length is calendar-specific (Gregorian, Hebrew, and Chinese months differ) and cannot represent a universal time quantum. Constructors that accept a `month` argument continue to work; precision defaults to `DAY`.
- `UnivDuration.precision` is now a plain `int` instead of a `UnivDurPrecision` enum value. The integer values match `MomPrecLevel` exactly (0 = second, 3 = day, 7 = billion-year, -3 = ms, -18 = as).
- `UnivDurPrecision` enum has been **removed**; use plain `int` literals or `MomPrecLevel[prec]` instead.

### [1.0.0] - 2025-09-15
- Initial release
- Basic timestamp handling and conversion functionality
- Support for Unix timestamps, ISO strings, and datetime objects
