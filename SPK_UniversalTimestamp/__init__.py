"""
SPK Universal Timestamp Package

Comprehensive multi-scale time system for knowledge bases:
- Geological: Deep time scales (billions of years)
- Astronomical: Julian Day Numbers, coordinate time
- Scientific: High-precision measurements with uncertainty
- Human Calendars: Cultural/religious calendar conversions
"""

__version__ = "1.0.0"
__author__ = "Roswell C Miller"
__email__ = "support@sarek.ai"
__description__ = "Comprehensive multi-scale timestamp system"

from .CC01_Calendar_Basics import (
    Epoch_rd,
    jd_from_rd,
    rd_from_jd,
)
from .CC02_Gregorian import (
    is_gregorian_leap_year,
    rd_from_gregorian,
    gregorian_from_rd,
    gregorian_year_from_rd,
    gregorian_new_year,
    gregorian_end_year,
    gregorian_date_difference
)
from .CC03_Julian import (
    is_julian_leap_year,
    rd_from_julian,
    julian_from_rd,
)
from .CC08_Hebrew import (
    is_hebrew_leap_year,
    last_hebrew_month_of_year,
    last_day_of_hebrew_month,
    rd_from_hebrew,
    hebrew_from_rd,
)
from .CC14_Time_and_Astronomy import (
    degrees_from_dms,
    dms_from_degrees,
    hms_from_hours,
    location,
    AST,
    direction,
    zone_from_longitude,
    universal_from_local,
    local_from_universal,
    standard_from_universal,
    universal_from_standard,
    standard_from_local,
    local_from_standard,
)
from .CC19_Chinese_1645 import (
    current_major_solar_term,
    chinese_location,
    chinese_solar_longitude_on_or_after,
    major_solar_term_on_or_after,   
    current_minor_solar_term,
    minor_solar_term_on_or_after,
    midnight_in_china,
    chinese_winter_solstice_on_or_before,
    chinese_new_moon_on_or_after,
    chinese_new_moon_before,
    is_chinese_no_major_solar_term,
    is_chinese_prior_leap_month,
    chinese_new_year_in_sui,
    chinese_new_year_on_or_before,
    chinese_from_rd,
    rd_from_chinese,
    chinese_sexagesimal_tuple,
    chinese_name_difference,
    chinese_year_tuple,
    chinese_month_epoch,
    chinese_month_tuple,
    chinese_day_epoch,
    chinese_day_tuple,
    chinese_day_tuple_on_or_before
    )

from .Constants_aCommon import *
from .Constants_Chinese import *
from .Constants_Gregorian import *
from .Constants_Julian import *
from .Constants_Hebrew import *

from .Moment_aUniversal import *
from .Moment_bPresent_Calendars import *
from .Moment_bPresent_Geological import *
from .Moment_cPresent_Chinese import *
from .Moment_cPresent_Gregorian import *
from .Moment_cPresent_Julian import *
from .Moment_cPresent_Hebrew import *

from .CC00_Decimal_library import *
from .Astro_Space import *

# Make package metadata available
__all__ = [
    # Package metadata
    "__version__",
    "__author__", 
    "__email__",
    "__description__",
    
    # Core classes
    "UnivMoment",
    
    # Enums and attributes
    "Calendar",
    "CalendarAtts",
    "Precision",
    "PrecisionAtts",
    
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