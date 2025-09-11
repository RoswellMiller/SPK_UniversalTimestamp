"""
SPK Universal Timestamp Package

Comprehensive multi-scale time system for knowledge bases:
- Geological: Deep time scales (billions of years)
- Astronomical: Julian Day Numbers, coordinate time
- Scientific: High-precision measurements with uncertainty
- Human Calendars: Cultural/religious calendar conversions
"""

__version__ = "0.1.0"
__author__ = "Roswell C Miller"
__email__ = "support@sarek.ai"
__description__ = "Comprehensive multi-scale timestamp system"

from .UnivDecimalLibrary import *
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
from .CC19_Chinese_1645 import *

from .UnivTimestamp import (
    UnivTimestamp,
    Calendar,
    CalendarAtts,
    Precision, 
    PrecisionAtts, 
)
from .UnivCalendars import (
    UnivCalendars,
)
from .UnivTimestampFactory import (
    UnivTimestampFactory,
)
from .UnivGREGORIAN import (
    UnivGREGORIAN,
    MEASUREMENT_HISTORY,
)
from .UnivJULIAN import (
    UnivJULIAN,
)
from .UnivHEBREW import (
    UnivHEBREW,
)
from .UnivCHINESE import (
    UnivCHINESE,
)
from .UnivGEOLOGICAL import (
    UnivGEOLOGICAL,
    GEOLOGICAL_EONS,
)

# Make package metadata available
__all__ = [
    # Package metadata
    "__version__",
    "__author__", 
    "__email__",
    "__description__",
    
    # Core classes
    "UnivTimestamp",
    "UnivCalendars",
    "UnivTimestampFactory",
    
    # Enums and attributes
    "Calendar",
    "CalendarAtts",
    "Precision",
    "PrecisionAtts",
    
    # Calendar-specific implementations
    "UnivGREGORIAN",
    "UnivJULIAN",
    "UnivHEBREW",
    "UnivCHINESE",
    "UnivGEOLOGICAL",
    
    # Constants and data
    "GEOLOGICAL_EONS",
    "MEASUREMENT_HISTORY",
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
]