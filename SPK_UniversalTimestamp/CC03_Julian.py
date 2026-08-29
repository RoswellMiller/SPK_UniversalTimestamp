"""
CC03_Julian — Julian-calendar leap-year test and R.D. ↔ (year, month, day)
conversion from R&D chapter 3.

**Purpose.**  Implement the Julian-calendar side of the R&D
calendrical-conversion pair.  Julian differs from Gregorian only
in the leap rule (Julian: every 4 years; Gregorian: with the
century correction) so the arithmetic is simpler.

**Public surface (re-exported via `__init__.py`).**
    `is_julian_leap_year`, `rd_from_julian`, `julian_from_rd`.

**R&D references.**
    Leap-year test and both converters: pp 75–77 (R&D ch. 3).

**Behavioral notes.**
    * BCE years are represented as negative `int` and internally
      shifted by +1 to close the astronomical / historical
      off-by-one (there is no year 0 in the historical convention).
    * `julian_from_rd` returns a `(year, month, day)` `tuple[int, int, int]`
      despite the `-> dict` annotation — the type hint is legacy
      and slated for repair in a future Task 1 pass (out of scope
      for PL-01's non-behavioral charter).

**Not in scope.**  Gregorian arithmetic (`CC02_Gregorian`),
presentation formatting (`Moment_cPresent_Julian`).

**Change history.**  See `CHANGELOG.md`.
"""

from .CC01_Calendar_Basics import Epoch_rd


# Calendrical Calculations Chapter 3
def is_julian_leap_year(j_year: int) -> bool:
    """
    R&D pp. 75–77: test whether `j_year` is a Julian leap year.

    Julian rule: divisible by 4, with the BCE branch subtracting 1
    (because year -1 in this codebase is 1 BCE historically and
    astronomers count 0 BCE as year 0 — the ``0 if > 0 else 3``
    residue selection is R&D's compact way to bridge the two).

    Args:
        j_year:  Julian year as `int`.  Negative values are BCE.

    Returns:
        `True` if `j_year` is a leap year, else `False`.
    """
    return j_year % 4 == (0 if j_year > 0 else 3)
    
def rd_from_julian(year: int, month: int = 1, day: int = 1) -> int:
    """
    R&D pp. 75–77: convert Julian (year, month, day) to Rata Die.

    Args:
        year:   Julian year; negative values are BCE (year -1 == 1 BCE).
        month:  1–12; defaults to January.
        day:    1–31; defaults to the 1st.

    Returns:
        R.D. fixed day number as `int`.

    Raises:
        `ValueError`:  Any of `year`, `month`, `day` is non-integer;
            `month` is outside 1–12; or `day` is outside 1–31.
            The day check is loose (does not reject e.g. February 30);
            fine-grained validation is the caller's responsibility.

    Notes:
        Internally shifts negative `year` by +1 to close the
        BCE / astronomical off-by-one before running R&D's
        arithmetic; the returned R.D. is unaffected.
    """
    day = day if day is not None else 1
    month = month if month is not None else 1
    #year = self.year if self.year is not None else 1
    # Validate input
    if not isinstance(year, int) or not isinstance(month, int) or not isinstance(day, int):
        raise ValueError("Year, month, and day must be integers")
    if month < 1 or month > 12:
        raise ValueError("Month must be between 1 and 12")
    if day < 1 or day > 31:
        raise ValueError("Day must be between 1 and 31")

    # Calculate rd from Julian date
    y = year + 1 if year < 0 else year  # Adjust for BCE
    d0 = Epoch_rd['julian'] - 1
    d0 += (y - 1) * 365 
    d0 += (y - 1) // 4 
    d0 += (367 * month - 362) // 12 
    if month <=2 :
        pass
    elif is_julian_leap_year(year):
        d0 += -1
    else:
        d0 += -2
    rd = d0 + day
    return rd
    
def julian_from_rd(rd: int) -> dict:
    """
    R&D pp. 75–77: convert Rata Die to a Julian `(year, month, day)` triple.

    Args:
        rd:  R.D. day count as `int`.

    Returns:
        `tuple[int, int, int]` — `(year, month, day)`.  The
        declared return type `dict` is legacy and does not match
        the actual return (a plain tuple); repair is deferred to a
        future Task 1 pass.

    Raises:
        `ValueError`:  Any internal `rd_from_julian` call fails
            validation (wrapped and re-raised with the `rd` value).
    """
    # Convert rd to datetime
    try:
        approx = (4 * (rd - Epoch_rd['julian']) + 1464) // 1461
        year = approx - 1 if approx <= 0 else approx
        prior_days = rd - rd_from_julian(year, 1, 1)
        if rd < rd_from_julian(year, 3, 1):
            correction = 0
        elif is_julian_leap_year(year):
            correction = 1
        else:
            correction = 2
        month = (12 * (prior_days + correction) + 373) // 367
        day = rd - rd_from_julian(year, month, 1) + 1
        # Return Julian date as dictionary
        return year, month, day
    except ValueError as e:
        raise ValueError(f"Invalid Rata Die date: {rd}: {e}")       
    

