"""
CC02_Gregorian — Gregorian-calendar arithmetic from R&D chapter 2.

**Purpose.**  R.D. ↔ Gregorian conversion, leap-year test, year
boundaries, and inter-date arithmetic.  These functions are the
Gregorian side of the R&D calendrical-conversion pattern and are
called by both the presentation layer (`Moment_cPresent_Gregorian`)
and by any calendar that needs to cross-reference Gregorian dates
(essentially all of them, since Gregorian is the reporting default).

**Public surface (re-exported via `__init__.py`).**
    `is_gregorian_leap_year`, `rd_from_gregorian`, `gregorian_from_rd`,
    `gregorian_year_from_rd`, `gregorian_new_year`, `gregorian_end_year`,
    `gregorian_date_difference`.

**R&D references.**
    Leap-year:            p. 59 (2.16).
    `rd_from_gregorian`:  p. 60 (2.17).
    New/end year:         p. 60 (2.18–2.19).
    `gregorian_year_from_rd`: p. 61 (2.21).
    `gregorian_from_rd`:  p. 62 (2.23).
    Date difference:      p. 62 (2.24).

**Not in scope.**  Julian arithmetic (`CC03_Julian`); presentation
formatting (`Moment_cPresent_Gregorian`); calendar constants
(`Constants_Gregorian`).

**Change history.**  See `CHANGELOG.md`.  Arithmetic formulae are
frozen by R&D — the ``# p N (X.Y)`` comments above each function
are load-bearing citations and must never be removed.
"""

from decimal import Decimal
from .CC00_Decimal_library import floor, mod
from .CC01_Calendar_Basics import Epoch_rd

# "Calendrical Calculations" by Reingold and Dershowitz
# p 59 (2.16)
def is_gregorian_leap_year(g_year: int) -> bool:
    """
    R&D (2.16): test whether `g_year` is a Gregorian leap year.

    Standard rule: divisible by 4 and NOT by 100, OR divisible by 400.
    Handles negative (BCE) years correctly under Python's mod
    convention.

    Args:
        g_year:  Gregorian year as `int`.  Negative values are BCE.

    Returns:
        `True` if `g_year` is a leap year, else `False`.
    """
    return (g_year % 4 == 0 and g_year % 100 != 0) or (g_year % 400 == 0)

# p 60 (2.17)
def rd_from_gregorian(year: int | Decimal, month: int | Decimal = 1, day: int | Decimal = 1) -> int:
    """
    R&D (2.17): convert Gregorian (year, month, day) to Rata Die.

    Args:
        year:   Gregorian year; negative = BCE.
        month:  1–12; defaults to January.
        day:    1–31; defaults to the 1st.  No end-of-month validation.

    Returns:
        R.D. fixed day number as `int` (floor of the internal
        `Decimal` result).

    Raises:
        `ValueError`:  `month` outside 1–12 or `day` outside 1–31.
    """
    day = day if day is not None else 1
    month = month if month is not None else 1
    if month < 1 or month > 12:
        raise ValueError("Month must be between 1 and 12")
    if day < 1 or day > 31:
        raise ValueError("Day must be between 1 and 31")

    # Calculate rd from Gregorian date
    d0 = Epoch_rd['gregorian'] - 1
    d0 += (year - 1) * 365 
    d0 += floor((year - 1) / 4) 
    d0 -= floor((year - 1) / 100) 
    d0 += floor((year - 1) / 400)
    d0 += floor((367 * month - 362) / 12) 
    if month <=2 :
        pass
    elif is_gregorian_leap_year(year):
        d0 -= 1
    else:
        d0 -= 2
    rd = d0 + day
    return floor(rd)

# p 60 (2.18)
def gregorian_new_year(g_year: int | Decimal) -> int:
    """R&D (2.18): R.D. of January 1 in Gregorian year `g_year`."""
    return rd_from_gregorian(g_year, 1, 1)
# p 60 (2.19)
def gregorian_end_year(g_year: int | Decimal) -> int:
    """R&D (2.19): R.D. of December 31 in Gregorian year `g_year`."""
    return rd_from_gregorian(g_year, 12, 31)
    
# p 61 (2.21)
def gregorian_year_from_rd(rd : int | Decimal) -> int:
    """
    R&D (2.21): extract the Gregorian year containing R.D. `rd`.

    Uses R&D's cascading division by the 400/100/4/1-year cycle
    lengths (146097 / 36524 / 1461 / 365).  The trailing +1
    correction handles the boundary where `n100 == 4` or `n1 == 4`
    would otherwise misattribute the last day of a 400-year or
    4-year cycle.

    Args:
        rd:  R.D. day count (`int` or `Decimal`).

    Returns:
        Gregorian year containing that R.D. as `int`.

    Raises:
        `ValueError`:  Any arithmetic error is wrapped with the `rd`
            value in the message.
    """
    # Calculate year from rd
    try:
        d0 = rd - Epoch_rd['gregorian']
        n400 = floor(d0 / 146097)
        d1 = mod(d0, 146097)
        n100 = floor(d1 / 36524)  
        d2 = mod(d1, 36524)
        n4 = floor(d2 / 1461)
        d3 = mod(d2, 1461)
        n1 = floor(d3 / 365)
        year = 400 * n400 + 100 * n100 + 4 * n4 + n1
        if n100 != 4 and n1 != 4:
            year += 1
        return floor(year)
    except Exception as e:
        raise ValueError(f"Invalid Rata Die date: {rd}: {e}")

# p 62 (2.23)    
def gregorian_from_rd(rd: int | Decimal) -> tuple[int,int,int]:
    """
    R&D (2.23): convert Rata Die to Gregorian `(year, month, day)`.

    Args:
        rd:  R.D. day count.  `Decimal` inputs are floored to `int`
            before use — fractional R.D. moments discard time-of-day
            here (the presentation layer preserves precision separately).

    Returns:
        `tuple[int, int, int]` — `(year, month, day)` in the Gregorian
        calendar.

    Raises:
        `ValueError`:  Any internal `rd_from_gregorian` call fails
            (wrapped with `rd`).
    """
    # Convert rd to date
    try:
        if isinstance(rd, Decimal):
            rd = floor(rd)
        year = gregorian_year_from_rd(rd)
        prior_days = rd -  rd_from_gregorian(year, 1, 1)
        if rd < rd_from_gregorian(year, 3, 1):
            correction = 0
        elif is_gregorian_leap_year(year):
            correction = 1
        else:
            correction = 2
        month = (12 * (prior_days + correction) + 373) // 367   
        day = rd - rd_from_gregorian(year, month, 1) + 1
        return year, month, day
    except ValueError as e:
        raise ValueError(f"Invalid Rata Die date: {rd}: {e}")
    
# p 62 (2.24)
def gregorian_date_difference(g_date_1 : tuple, g_date_2 : tuple) -> int:
    """
    R&D (2.24): signed day-count difference `g_date_2 - g_date_1`.

    Args:
        g_date_1:  `(year, month, day)` tuple for the earlier date.
        g_date_2:  `(year, month, day)` tuple for the later date.
            The naming does not enforce order; the result is signed.

    Returns:
        `int` day count.  Positive when `g_date_2` is after
        `g_date_1`, zero when identical, negative when reversed.
    """
    rd1 = rd_from_gregorian(g_date_1[0], g_date_1[1], g_date_1[2])
    rd2 = rd_from_gregorian(g_date_2[0], g_date_2[1], g_date_2[2])
    return rd2 - rd1
