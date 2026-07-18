"""
CC08_Hebrew — Hebrew-calendar arithmetic from R&D chapter 8.

**Purpose.**  R.D. ↔ Hebrew (year, month, day) conversion, leap
year / long-Marheshvan / short-Kislev tests, and the month-length
lookups they rely on.  The Hebrew calendar is arithmetically
self-contained (no astronomical input), which makes it a good
test bed for the R&D `MAX`/`MIN` search idioms this module uses.

**Public surface (re-exported via `__init__.py`).**
    `months` (enum), `is_hebrew_leap_year`, `last_hebrew_month_of_year`,
    `last_day_of_hebrew_month`, `rd_from_hebrew`, `hebrew_from_rd`.

**Private helpers (kept in-module).**
    `_is_sabbatical_year`, `_calendar_elapsed_days`,
    `_year_length_correction`, `_new_year`, `_is_long_marheshvan`,
    `_is_short_kislev`, `_days_in_year`.  The R&D `molad` function
    is commented out below — the current conversion path does not
    need it; if a future feature needs the molad it should live
    here.

**R&D references.**  Every function carries its equation number
inline (e.g. ``# (8.14)`` above `is_hebrew_leap_year`); the
citations are load-bearing and must not be removed.  Chapter 8
spans roughly pp. 87–101 in the R&D Ultimate Edition.

**Not in scope.**  Presentation / localisation
(`Moment_cPresent_Hebrew`, `Constants_Hebrew`).

**Change history.**  See `CHANGELOG.md`.
"""

from enum import Enum
from .CC00_Decimal_library import MAX, MIN
from .CC01_Calendar_Basics import Epoch_rd

class months(Enum):
    """
    Hebrew months, numbered per R&D chapter 8.

    Note the numbering: NISAN=1 through ADAR_II=13, with TISHRI=7
    (the religious year begins in Nisan; the civil year begins in
    Tishri, which is why the year-transition code in
    `hebrew_from_rd` special-cases the Tishri boundary).
    ADAR_I / ADAR_II collapse to a single Adar in common (non-leap)
    years — `last_day_of_hebrew_month` handles the mapping.
    """
    NISAN = 1
    IYYAR = 2
    SIVAN = 3
    TAMMUZ = 4
    AV = 5
    ELUL = 6
    TISHRI = 7
    MARHESHVAN = 8
    KISLEV = 9
    TEVET = 10
    SHEVAT = 11
    ADAR_I = 12
    ADAR_II = 13
    

# Calendrical Calculations pp Chapter 8
# (8.14)
def is_hebrew_leap_year(h_year: int) -> bool:
    """
    R&D (8.14): test whether `h_year` is a Hebrew leap year (embolismic).

    Leap-year rule follows the 19-year Metonic cycle: 7 of every
    19 years are leap.  R&D's compact form ``((7 * y + 1) mod 19) < 7``
    selects exactly those years.

    Args:
        h_year:  Hebrew year as `int`.

    Returns:
        `True` for leap (13-month) years, `False` for common
        (12-month) years.
    """
    return ((7 * h_year + 1) % 19) < 7

# (8.15) 
def last_hebrew_month_of_year(h_year) -> int:
    """
    R&D (8.15): last month number of `h_year` (12 or 13).

    Args:
        h_year:  Hebrew year as `int`.

    Returns:
        `months.ADAR_II.value` (13) in leap years, else
        `months.ADAR_I.value` (12).
    """
    if is_hebrew_leap_year(h_year):
        return months.ADAR_II.value
    return months.ADAR_I.value

# (8.16)
def _is_sabbatical_year(h_year: int) -> bool:
    """R&D (8.16): `True` when `h_year` is a Sabbatical (shmita) year."""
    return h_year % 7 == 0
    
# (8.19)
# def _molad(h_year : int, h_month: int, hour : int = 0) -> int:
#     """Calculate the molad (new moon) for a given Hebrew year and month"""
#     y = h_year + 1  if h_month < UnivHEBREW.months.TISHRI.value else h_year 
#     months_elapsed = h_month - UnivHEBREW.months.TISHRI.value + (235 * y - 214) // 19
#     m = super().Epoch_rd['Hebrew']
#     m -= 876 // 25920
#     m += months_elapsed * (29 + 12**hour + 793 // 25920)
#     return m

# (8.20)
def _calendar_elapsed_days(h_year : int) -> int :
    """
    R&D (8.20): days from the Hebrew epoch to the start of `h_year`,
    including the dehiyyah adjustment for a Sunday/Wednesday/Friday
    Rosh Hashanah landing.
    """
    months_elapsed = (235 * h_year - 234) // 19
    parts_elapsed = 12084 + 13753 * months_elapsed 
    days = 29 * months_elapsed + parts_elapsed // 25920
    d = days + 1 if ((3 * (days + 1)) % 7) < 3 else days
    return d

# (8.21)
def _year_length_correction(h_year : int) -> int:
    """
    R&D (8.21): 0, 1, or 2-day correction applied to `_new_year` so
    that the year length remains one of the four canonical values
    (353, 354, 355 common; 383, 384, 385 leap).
    """
    ny1 = _calendar_elapsed_days(h_year)
    ny2 = _calendar_elapsed_days(h_year+1)
    if ny2-ny1 == 356 :
        return 2
    else:
        ny0 = _calendar_elapsed_days(h_year-1)
        if ny1-ny0 == 382 :
            return 1
    return 0

# (8.22)
def _new_year(h_year : int):
    """R&D (8.22): R.D. of 1 Tishri in `h_year` (Rosh Hashanah)."""
    v = Epoch_rd['hebrew'] 
    v += _calendar_elapsed_days(h_year) 
    v += _year_length_correction(h_year) 
    return v

# (8.23)
def last_day_of_hebrew_month(h_year : int, h_month : int) -> int:
    """
    R&D (8.23): last day (29 or 30) of `h_month` in `h_year`.

    Handles the three variable-length cases:
      * ADAR_I in a common year is 29 (there is no Adar II).
      * MARHESHVAN is 30 in a long year, 29 otherwise.
      * KISLEV is 29 in a short year, 30 otherwise.
    All other months have their canonical fixed length.

    Args:
        h_year:   Hebrew year.
        h_month:  Value from `months` enum (1–13).

    Returns:
        Number of days in that month (29 or 30).
    """
    if h_month in [months.IYYAR.value, months.TAMMUZ.value, months.ELUL.value,months.TEVET.value, months.ADAR_II.value]:
        day = 29
    elif h_month == months.ADAR_I.value and not is_hebrew_leap_year(h_year):
        day = 29
    elif h_month == months.MARHESHVAN.value and not _is_long_marheshvan(h_year):
        day = 29
    elif h_month == months.KISLEV.value and _is_short_kislev(h_year):
        day = 29
    else:
        day = 30
    return day

# (8.24)
def _is_long_marheshvan(h_year : int) -> bool:
    """R&D (8.24): Marheshvan is 30 days in abundant years (355 or 385)."""
    b = _days_in_year(h_year) in [355, 385 ]
    return b

# (8.25)
def _is_short_kislev(h_year : int) -> bool:
    """R&D (8.25): Kislev is 29 days in deficient years (353 or 383)."""
    b = _days_in_year(h_year) in [353, 383 ]
    return b

# (8,26)
def _days_in_year(h_year: int) -> int: 
    """R&D (8.26): total days in Hebrew year `h_year`."""
    d = _new_year(h_year + 1) - _new_year(h_year)
    return d

# (8.27)
def rd_from_hebrew(year: int, month: int = 1, day: int = 1) -> int:
    """
    R&D (8.27): convert Hebrew `(year, month, day)` to Rata Die.

    The month-accumulation splits on the Nisan / Tishri boundary
    because months < TISHRI belong to the second half of the
    religious year and therefore lie AFTER the Rosh-Hashanah
    anchor day; the code sums Tishri..end plus Nisan..month−1 in
    that case, else Tishri..month−1.

    Args:
        year:   Hebrew year as `int`.
        month:  Value from `months` enum (default NISAN = 1).
        day:    1..30 (default 1).  No bounds check on `day`
            — out-of-range values produce out-of-range R.D.s.

    Returns:
        R.D. fixed day number as `int`.
    """
    day = day if day is not None else 1
    month = month if month is not None else 1
    # Fixed start date
    rd = _new_year(year) + day - 1
    if month < months.TISHRI.value:
        for m in range(months.TISHRI.value, last_hebrew_month_of_year(year) + 1):
            rd += last_day_of_hebrew_month(year, m)
        for m in range(months.NISAN.value, month):    
            rd += last_day_of_hebrew_month(year, m)
    else:
        for m in range(months.TISHRI.value, month):
            rd += last_day_of_hebrew_month(year, m)        
    return rd

# (8.28)
def hebrew_from_rd(date: int) -> tuple[int, int, int]:
    """
    R&D (8.28): convert Rata Die to Hebrew `(year, month, day)`.

    Uses R&D's two-stage `MAX`/`MIN` search idiom: an approximate
    year is derived from the R.D. offset scaled by the mean tropical
    year, then `MAX` walks forward to the exact Hebrew year, and
    `MIN` walks forward to the exact month.

    Args:
        date:  R.D. fixed day number.

    Returns:
        `(year, month, day)` triple.
    """
    approx = (98496 * (date - Epoch_rd['hebrew']) // 35975351) + 1
    
    year = MAX(approx, lambda y: _new_year(y) <= date)
    # for y in range(approx - 1, approx + 2):
    #     y_rd = _new_year(y)
    #     if y_rd >= date:
    #         year = y - 1
    #         break
    #     continue
    
    if date < rd_from_hebrew(year, months.NISAN.value, 1):  
        start = months.TISHRI.value
    else:
        start = months.NISAN.value
        
    month = MIN(start, lambda m: date<= rd_from_hebrew(year, m, last_day_of_hebrew_month(year, m)))
    # for m in range(start, last_hebrew_month_of_year(year) + 1):
    #     m_rd = rd_from_hebrew(year, m, last_day_of_hebrew_month(year, m))
    #     if date <= m_rd:
    #         break
    # month = m
        
    day = date - rd_from_hebrew(year, month, 1) + 1
    return year, month, day

