# SPK Universal Timestamp Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [2.0.3] - 2026-05-18

### Changed
- **G-years replaces B-years** — display strings and parser now use `G-years` / `G-year`
  (giga-annum, Ga) for precision level 7, consistent with cosmological convention.
  `UnivDuration.LEVEL_ABBREV[7]` is now `"G-years"`.
  `UnivDuration.from_string()` accepts `"G-years"` / `"G-year"` (and the `>G-years`
  decompose prefix); `"B-years"` / `"B-year"` are **no longer accepted** by that parser.
- `UnivMoment._GEOLOGICAL_PATTERNS` BYA regex updated to `(?:GYA|BYA)` so both
  `"4.5 GYA"` and legacy `"4.5 BYA"` strings are accepted when constructing a
  geological `UnivMoment` via `from_string()`.

### Notes
- The internal enum member `UnivMomPrecision.BILLION_YEARS` is **not** renamed;
  only display/parse strings change.  `PREC_ABBREV[BILLION_YEARS]` was already `'G-yr'`.

## [2.0.2] - 2026-05-17

### Added
- **4-decimal-place display for year-scale units** — `format_for_display()` now renders
  fractional values at levels 4–7 (years, k-years, M-years, G-years) with four decimal
  places (e.g. `"1.7321 G-years"`), matching the behaviour of sub-second levels.
- **Decompose mode (`>` prefix)** — `format_for_display(">unit")` and the `"udur:>unit"`
  f-string spec decompose a coarse duration into a compound string down to the named
  unit (e.g. `"1 G-year 732.1000 M-years"`).
- **Negative-zero guard** — `format_for_display()` no longer emits `"-0 …"` for values
  that round to zero at the requested precision.

### Fixed
- `format_for_display()` with a target unit passed as an argument now preserves the
  sign of negative durations when decomposing into compound form.



### Fixed
- `UnivDuration.MAX_FINE_FOR_COARSE` for level 4 (years) relaxed from −1 to −6, allowing
  fractional-year strings with up to 6 decimal places (e.g. `"0.615187 years"`) to be parsed
  by `UnivDuration.from_string()`.

## [2.0.0] - 2026-05-15

### Added
- `UnivDuration.LEVEL_QUANTUM` — public, read-only `ClassVar[MappingProxyType]` mapping integer precision
  levels (0–7) to their second-quantum values; replaces the former module-level `_LEVEL_QUANTUM` private dict.
- `UnivDuration.LEVEL_ABBREV` — public, read-only `ClassVar[MappingProxyType]` mapping integer precision
  levels (−18 to 7) to their display abbreviations; replaces the former module-level `_LEVEL_ABBREV` private dict.
  Both constants are `MappingProxyType` instances — any mutation attempt raises `TypeError`.
- `UnivDuration.from_string(text)` classmethod — parses compound human-readable strings such as
  `"1 day 2 hrs 30 mins"`, `"10.001 s"`, and `"10.5 M-years"` into a `UnivDuration`. Precision is
  inferred from the finest unit present; decimal places on any unit subdivide precision one level per digit.
  Both singular and plural abbreviations are accepted (e.g. `"1 day"` and `"1 days"`).

### Changed
- `LEVEL_QUANTUM` and `LEVEL_ABBREV` are now public class-level constants (formerly `_LEVEL_QUANTUM`
  and `_LEVEL_ABBREV` module-level private dicts).

### Removed
- Module-level private `_LEVEL_QUANTUM` and `_LEVEL_ABBREV` dicts (superseded by class constants above).

### Tests
- Added `test_class_constants` to `Tests/test_600_UnivDuration.py` — verifies accessibility and
  read-only enforcement of the two new class constants.
- Added `test_from_string` to `Tests/test_600_UnivDuration.py` — covers single/compound pairs,
  decimal-driven precision inference, singular/plural forms, round-trip fidelity, and `ValueError` on
  invalid input.

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
- `UnivMoment` class for handling various timestamp formats
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
- a. UnivMoment - A timestamp
- b. UnivTimestampFactory - A package of support routines for cross calendar UnivMoment construction and conversion.
- Comprehensives series of test cases, which also serve as examples of how the UnivMoment is used.
