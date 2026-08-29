"""
SPK Universal Timestamp Package — comprehensive multi-scale time system.

**Purpose.**  Represent, convert, and format instants and durations
across the full range from cosmological deep time (billion years)
down to attoseconds (10⁻¹⁸ s), across Gregorian, Julian, Hebrew,
Chinese, and geological time-scale conventions, on an R&D
(Reingold & Dershowitz) Rata Die foundation.

**Domains covered.**
    * Geological: deep time scales (Ma / Ga).
    * Astronomical: Julian Day Numbers, dynamical / universal time,
      Beijing-meridian lunisolar calculations for the Chinese calendar.
    * Scientific: 30-decimal `Decimal` precision, immutable
      value-typed moments and durations.
    * Human calendars: Gregorian, Julian, Hebrew, Chinese (1645-onwards).

**Public surface (re-exported at package level).**
    Core types:  `UnivMoment`, `UnivMomPrecision`, `UnivDuration`.
    Calendars:   `Calendar` (enum), `Present_Gregorian`, `Present_Julian`,
        `Present_Hebrew`, `Present_Chinese`, `Present_Geological`,
        `Present_Calendars`.
    R&D primitives: everything under `CC00`–`CC19` (see individual
        module docstrings), astronomy helpers from
        `CC14_Time_and_Astronomy`, spatial primitives from `Astro_Space`.
    Constants:   `Constants_aCommon`, `Constants_Gregorian`,
        `Constants_Julian`, `Constants_Hebrew`, `Constants_Chinese`.

**Documentation.**
    * `docs/USERS_MANUAL.md`  — runnable examples per calendar.
    * `docs/Coding and Documenting Standards.md` — conventions this
      codebase follows (module headers, R&D citations, docstring
      contracts, git hygiene).
    * `CHANGELOG.md`  — versioned change log.
    * `docs/TODO_BACKLOG.md` — known issues (B-01 Chinese Appendix-C
      off-by-one, B-02 `psoEarth.__ne__` bug).
"""

__version__ = "2.0.3"
__author__ = "Roswell C Miller"
__email__ = "support@sarek.ai"
__description__ = "Comprehensive multi-scale timestamp system"

from .Astro_Space import *
from .CC00_Decimal_library import *
from .CC01_Calendar_Basics import (
    Epoch_rd,
    jd_from_rd,
    rd_from_jd,
)
from .CC02_Gregorian import (
    gregorian_date_difference,
    gregorian_end_year,
    gregorian_from_rd,
    gregorian_new_year,
    gregorian_year_from_rd,
    is_gregorian_leap_year,
    rd_from_gregorian,
)
from .CC03_Julian import (
    is_julian_leap_year,
    julian_from_rd,
    rd_from_julian,
)
from .CC08_Hebrew import (
    hebrew_from_rd,
    is_hebrew_leap_year,
    last_day_of_hebrew_month,
    last_hebrew_month_of_year,
    rd_from_hebrew,
)
from .CC14_Time_and_Astronomy import (
    AST,
    degrees_from_dms,
    direction,
    dms_from_degrees,
    hms_from_hours,
    local_from_standard,
    local_from_universal,
    location,
    standard_from_local,
    standard_from_universal,
    universal_from_local,
    universal_from_standard,
    zone_from_longitude,
)
from .CC19_Chinese_1645 import (
    chinese_day_epoch,
    chinese_day_tuple,
    chinese_day_tuple_on_or_before,
    chinese_from_rd,
    chinese_location,
    chinese_month_epoch,
    chinese_month_tuple,
    chinese_name_difference,
    chinese_new_moon_before,
    chinese_new_moon_on_or_after,
    chinese_new_year_in_sui,
    chinese_new_year_on_or_before,
    chinese_sexagesimal_tuple,
    chinese_solar_longitude_on_or_after,
    chinese_winter_solstice_on_or_before,
    chinese_year_tuple,
    current_major_solar_term,
    current_minor_solar_term,
    is_chinese_no_major_solar_term,
    is_chinese_prior_leap_month,
    major_solar_term_on_or_after,
    midnight_in_china,
    minor_solar_term_on_or_after,
    rd_from_chinese,
)
from .Constants_aCommon import *
from .Constants_Chinese import *
from .Constants_Gregorian import *
from .Constants_Hebrew import *
from .Constants_Julian import *
from .Moment_bPresent_Calendars import *
from .Moment_bPresent_Geological import *
from .Moment_cPresent_Chinese import *
from .Moment_cPresent_Gregorian import *
from .Moment_cPresent_Hebrew import *
from .Moment_cPresent_Julian import *
from .UnivDuration import *
from .UnivMoment import *

# Make package metadata available
__all__ = [
    # Package metadata
    "__version__",
    "__author__", 
    "__email__",
    "__description__",
    
    # Core classes
    "UnivMoment",
    "UnivDuration",
    
    # Enums and attributes
    "Calendar",
    "CalendarAtts",
    "UnivMomPrecision",
    
    # Calendar-specific implementations
    "Present_GEOLOGICAL",
    "Present_Calendars",
    "Present_GREGORIAN",
    "Present_JULIAN",
    "Present_HEBREW",
    "Present_CHINESE",
    
    # Constants and data
    "GEOLOGICAL_EONS",
    "GEOLOGICAL_ERAS",
    "GEOLOGICAL_PERIODS",
    "GEOLOGICAL_EPOCHSandAGES",
    "Epoch_rd",
    
    # Base calendar functions
    "jd_from_rd",
    "rd_from_jd",
    
    # Gregorian calendar functions
    "is_gregorian_leap_year",
    "rd_from_gregorian",
    "gregorian_from_rd",
    "gregorian_year_from_rd",
    "gregorian_new_year",
    "gregorian_end_year",
    "gregorian_date_difference",
    
    # Julian calendar functions
    "is_julian_leap_year",
    "rd_from_julian",
    "julian_from_rd",
    
    # Hebrew calendar functions
    "is_hebrew_leap_year",
    "last_hebrew_month_of_year",
    "last_day_of_hebrew_month",
    "rd_from_hebrew",
    "hebrew_from_rd",
    
    # Chinese calendar functions
    "rd_from_chinese",
    "chinese_from_rd"
]