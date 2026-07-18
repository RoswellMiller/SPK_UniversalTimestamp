"""
CC01_Calendar_Basics — Rata Die (R.D.) foundation table and Julian Day
Number (JDN) / Modified JDN conversion primitives from R&D chapter 1.

**Purpose.**  Define the epoch offsets that every other calendar
module depends on to convert between its own day count and R.D.
(day 1 = Monday, January 1, 1 CE Gregorian), plus the JDN and MJDN
converters that astronomy code needs.

**Public surface (re-exported via `__init__.py`).**
    `Epoch_rd`  — dict mapping calendar name -> R.D. epoch offset.
    `jd_from_rd`, `rd_from_jd`  — JDN ↔ R.D. conversion.

Also defined but not re-exported (used internally by astronomy code):
    `_moment_from_jd`, `_jd_from_moment`, `rd_from_mjd`, `mjd_from_rd`.

**R&D references.**
    Epoch table:      Table 1.2, p. 17.
    JDN converters:   p. 18 (1.4), p. 20 (1.13), p. 18 (1.5), p. 20 (1.14).
    MJDN converters:  p. 19 (1.7), p. 19 (1.8).

**Not in scope.**  Anything calendar-specific; the sibling
`CC02`–`CC19` modules import from this file, never the reverse.

**Change history.**  See `CHANGELOG.md`.  Epoch values are frozen
by R&D and must never be tweaked; if a new calendar is added, add
a new key and cite the R&D page in a trailing comment.
"""

from decimal import Decimal


# Table 1.2, p 17
Epoch_rd = {
    'julian-day-number' : Decimal(-1_721_424.5),    
    'hebrew' : -1_373_427,
    'mayan': -1_137_142,
    'hindu-kali-yuga' : -1_132_959,
    'chinese' : -963_099,
    'samaritan': -598_573,
    'egyptian': -272_787,
    'babylonian': -113_502,
    'tibetan': -46_410,
    'julian': -1,
    'gregorian': 1,         # Monday January 1, 1 Gregorian
    'ISO-8601': 1,
    'akan': 37,
    'ethiopic': 2_796,
    'coptic': 103_605,
    'armenian': 201_443,
    'persian': 226_896,
    'islamic': 227_015,
    'zoroastrian': 230_638,
    'french-revolutionary': 654_415,
    'baha-i': 673_222,
    'modified-julian-day-number': 678_576,
    'unix': 719_163
}

# Julian Day Number conversions
# p 18 (1.4)
def _moment_from_jd(jd: Decimal) -> Decimal:
    """
    R&D (1.4): map a JDN to the corresponding R&D "moment" (day + fraction).

    Args:
        jd:  Julian Day Number as `Decimal`; fractional part is
            the time-of-day past noon UTC.

    Returns:
        R&D moment as `Decimal` (day count relative to R.D. epoch;
        fractional part carries time-of-day).

    Notes:
        Private (leading underscore).  Callers that want an
        integer R.D. day should use `rd_from_jd` which floors the
        result via `int()`.
    """
    return (jd - Decimal(Epoch_rd['julian-day-number']))
# p 20 (1.13)
def rd_from_jd(jd: Decimal) -> int:
    """
    R&D (1.13): convert Julian Day Number to integer Rata Die.

    Args:
        jd:  Julian Day Number as `Decimal`.

    Returns:
        R.D. fixed day number as `int` (truncated toward zero).

    Notes:
        `int()` truncation drops any time-of-day component; if you
        need sub-day precision, use `_moment_from_jd` instead.
    """
    return int(_moment_from_jd(jd))
# p 18 (1.5)
def _jd_from_moment(rd : int) -> Decimal:
    """
    R&D (1.5): map an R.D. moment to its JDN.

    Args:
        rd:  R.D. day count (integer input; `Decimal` also works).

    Returns:
        JDN as `Decimal`.
    """
    return rd + Decimal(Epoch_rd['julian-day-number'])
# p 20 (1.14)
def jd_from_rd(rd: int) -> Decimal:
    """
    R&D (1.14): convert integer Rata Die to Julian Day Number.

    Args:
        rd:  R.D. day count.

    Returns:
        JDN as `Decimal`.
    """
    return _jd_from_moment(rd)

# Modified Julian Day Number conversions
# p 19 (1.7)
def rd_from_mjd(mjd : Decimal) -> Decimal:
    """
    R&D (1.7): convert Modified Julian Day Number to Rata Die.

    MJDN = JDN - 2_400_000.5, i.e. days since 1858-11-17 00:00 UT.
    Widely used in astronomy for its shorter, midnight-anchored form.

    Args:
        mjd:  Modified Julian Day Number as `Decimal`.

    Returns:
        R.D. moment as `Decimal` (may carry a fractional part).
    """
    return mjd + Epoch_rd['modified-julian-day-number']
# p 19 (1.8)
def mjd_from_rd(rd : Decimal) -> Decimal:
    """
    R&D (1.8): convert Rata Die to Modified Julian Day Number.

    Args:
        rd:  R.D. day count (integer or fractional `Decimal`).

    Returns:
        MJDN as `Decimal`.
    """
    return rd - Epoch_rd['modified-julian-day-number']