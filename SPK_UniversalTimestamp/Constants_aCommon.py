
from enum import Enum


class Calendar(Enum):
    """Supported calendar systems"""
    GEOLOGICAL = "geological"   # Done
    # Arithmetic calendars
    GREGORIAN = "gregorian"     # Done
    JULIAN = "julian"           # Done
    COPTIC = "coptic"          
    ETHIOPIAN = "ethiopian"
    ISO = "iso"              
    ICELANDIC = "icelandic"
    ISLAMIC = "islamic"
    HEBREW = "hebrew"           # Done
    ECCLESIASTICAL = "ecclesiastical"
    OLD_HINDU = "old_hindu"
    MAYAN = "mayan"
    BALINESE_PAWUKON = "balinese_pawukon"
    GENERIC_CYCLICAL = "generic_cyclic"  
    
    # Astronomical calendars
    PERSIAN = "persian"
    BAHAI = "bahai"
    FRENCH_REVOLUTIONARY = "french_revolutionary"
    LUNAR = "lunar"
    CHINESE = "chinese"         # Done, Reingold & Dershowitz algorithms
    MODERN_HINDU = "modern_hindu"
    TIBETAN = "tibetan"

CalendarAtts = {
    'en' : {
        Calendar.GREGORIAN: {'abbrv': '', 'name': 'Gregorian', 'bce_suffix': 'BCE', 'ce_suffix': 'CE'},
        Calendar.JULIAN:    {'abbrv': 'JC', 'name': 'Julian',    'bce_suffix': 'bc', 'ce_suffix': 'ad'},
        
        Calendar.HEBREW:    {'abbrv': 'AM', 'name': 'Hebrew',    'bce_suffix': ''},
        Calendar.CHINESE:   {'abbrv': 'CC', 'name': 'Chinese',   'bce_suffix': ''}, 
        Calendar.ISLAMIC:   {'abbrv': 'AH', 'name': 'Islamic',   'bce_suffix': ''},
        Calendar.PERSIAN:   {'abbrv': 'AP', 'name': 'Persian',   'bce_suffix': ''},
        Calendar.ETHIOPIAN: {'abbrv': 'EE', 'name': 'Ethiopian', 'bce_suffix': ''},
        
        Calendar.GEOLOGICAL:   {'abbrv': 'Ge', 'name': 'Geological',   'bce_suffix': ''},
    },
    'fr' : {
        Calendar.GREGORIAN: {'abbrv': '', 'name': 'Gregorian', 'bce_suffix': 'BCE', 'ce_suffix': 'CE'},
        Calendar.JULIAN:    {'abbrv': 'JC', 'name': 'Julian',    'bce_suffix': 'bc', 'ce_suffix': 'ad'},
        
        Calendar.HEBREW:    {'abbrv': 'AM', 'name': 'Hebrew',    'bce_suffix': ''},
        Calendar.CHINESE:   {'abbrv': 'CC', 'name': 'Chinese',   'bce_suffix': ''}, 
        Calendar.ISLAMIC:   {'abbrv': 'AH', 'name': 'Islamic',   'bce_suffix': ''},
        Calendar.PERSIAN:   {'abbrv': 'AP', 'name': 'Persian',   'bce_suffix': ''},
        Calendar.ETHIOPIAN: {'abbrv': 'EE', 'name': 'Ethiopian', 'bce_suffix': ''},
        
        Calendar.GEOLOGICAL:   {'abbrv': 'Ge', 'name': 'Geological',   'bce_suffix': ''},
    },
    'de' : {
        Calendar.GREGORIAN: {'abbrv': '', 'name': 'Gregorian', 'bce_suffix': 'BCE', 'ce_suffix': 'CE'},
        Calendar.JULIAN:    {'abbrv': 'JC', 'name': 'Julian',    'bce_suffix': 'bc', 'ce_suffix': 'ad'},
        
        Calendar.HEBREW:    {'abbrv': 'AM', 'name': 'Hebrew',    'bce_suffix': ''},
        Calendar.CHINESE:   {'abbrv': 'CC', 'name': 'Chinese',   'bce_suffix': ''}, 
        Calendar.ISLAMIC:   {'abbrv': 'AH', 'name': 'Islamic',   'bce_suffix': ''},
        Calendar.PERSIAN:   {'abbrv': 'AP', 'name': 'Persian',   'bce_suffix': ''},
        Calendar.ETHIOPIAN: {'abbrv': 'EE', 'name': 'Ethiopian', 'bce_suffix': ''},
        
        Calendar.GEOLOGICAL:   {'abbrv': 'Ge', 'name': 'Geological',   'bce_suffix': ''},
    },
    'es' : {
        Calendar.GREGORIAN: {'abbrv': '', 'name': 'Gregorian', 'bce_suffix': 'BCE', 'ce_suffix': 'CE'},
        Calendar.JULIAN:    {'abbrv': 'JC', 'name': 'Julian',    'bce_suffix': 'bc', 'ce_suffix': 'ad'},
        
        Calendar.HEBREW:    {'abbrv': 'AM', 'name': 'Hebrew',    'bce_suffix': ''},
        Calendar.CHINESE:   {'abbrv': 'CC', 'name': 'Chinese',   'bce_suffix': ''}, 
        Calendar.ISLAMIC:   {'abbrv': 'AH', 'name': 'Islamic',   'bce_suffix': ''},
        Calendar.PERSIAN:   {'abbrv': 'AP', 'name': 'Persian',   'bce_suffix': ''},
        Calendar.ETHIOPIAN: {'abbrv': 'EE', 'name': 'Ethiopian', 'bce_suffix': ''},
        
        Calendar.GEOLOGICAL:   {'abbrv': 'Ge', 'name': 'Geological',   'bce_suffix': ''},
    },
    'it' : {
        Calendar.GREGORIAN: {'abbrv': '', 'name': 'Gregorian', 'bce_suffix': 'BCE', 'ce_suffix': 'CE'},
        Calendar.JULIAN:    {'abbrv': 'JC', 'name': 'Julian',    'bce_suffix': 'bc', 'ce_suffix': 'ad'},
        
        Calendar.HEBREW:    {'abbrv': 'AM', 'name': 'Hebrew',    'bce_suffix': ''},
        Calendar.CHINESE:   {'abbrv': 'CC', 'name': 'Chinese',   'bce_suffix': ''}, 
        Calendar.ISLAMIC:   {'abbrv': 'AH', 'name': 'Islamic',   'bce_suffix': ''},
        Calendar.PERSIAN:   {'abbrv': 'AP', 'name': 'Persian',   'bce_suffix': ''},
        Calendar.ETHIOPIAN: {'abbrv': 'EE', 'name': 'Ethiopian', 'bce_suffix': ''},
        
        Calendar.GEOLOGICAL:   {'abbrv': 'Ge', 'name': 'Geological',   'bce_suffix': ''},
    },

}
# The allowed precision levels for timestamps
# MONTH is intentionally omitted: months are calendar-specific (Gregorian, Hebrew, Chinese
# months differ in length) and therefore cannot represent a universal time quantum.
class UnivMomPrecision(Enum):
    """UnivMomPrecision levels for date and time components"""
    BILLION_YEARS  = "10⁹years"   # billion years
    MILLION_YEARS  = "10⁶years"   # million years
    THOUSAND_YEARS = "10³years"   # 1000 years
    YEAR           = "year"       # 1 year
    DAY            = "day"        # 1 day
    HOUR           = "hour"       # hour
    MINUTE         = "minute"     # minute
    SECOND         = "second"     # second
    MILLISECOND    = "10⁻³second" # ms
    MICROSECOND    = "10⁻⁶second" # μs
    NANOSECOND     = "10⁻⁹second" # ns
    PICOSECOND     = "10⁻¹²second"# ps
    FEMTOSECOND    = "10⁻¹⁵second"# fs
    ATTOSECOND     = "10⁻¹⁸second"# as

# NOTE: Level integers match UnivDuration's scheme exactly.
#   SECOND = 0; coarser (larger time span) = positive integer (max 7 = BILLION_YEARS);
#   finer (sub-second) = negative integer aligned to the SI exponent (-3, -6 … -18).
#   Higher value → coarser;  lower (more negative) value → finer.
MomPrecLevel: dict[UnivMomPrecision, int] = {
    UnivMomPrecision.BILLION_YEARS:  7,
    UnivMomPrecision.MILLION_YEARS:  6,
    UnivMomPrecision.THOUSAND_YEARS: 5,
    UnivMomPrecision.YEAR:           4,
    UnivMomPrecision.DAY:            3,
    UnivMomPrecision.HOUR:           2,
    UnivMomPrecision.MINUTE:         1,
    UnivMomPrecision.SECOND:         0,
    UnivMomPrecision.MILLISECOND:   -3,
    UnivMomPrecision.MICROSECOND:   -6,
    UnivMomPrecision.NANOSECOND:    -9,
    UnivMomPrecision.PICOSECOND:   -12,
    UnivMomPrecision.FEMTOSECOND:  -15,
    UnivMomPrecision.ATTOSECOND:   -18,
}

# Reverse lookup: level integer → UnivMomPrecision
MomLevelPrec: dict[int, UnivMomPrecision] = {v: k for k, v in MomPrecLevel.items()}

# SI exponent (power of 10):
#   For geological / coarse: exponent of years (G-yr = 10^9 yr, ..., yr = 10^0 yr).
#   For sub-second: exponent of seconds (ms = 10^-3 s, ...).
#   None for calendar-derived units (day, hour, minute) that are not a power of 10.
MomPrecPower: dict[UnivMomPrecision, int | None] = {
    UnivMomPrecision.BILLION_YEARS:  9,
    UnivMomPrecision.MILLION_YEARS:  6,
    UnivMomPrecision.THOUSAND_YEARS: 3,
    UnivMomPrecision.YEAR:           0,
    UnivMomPrecision.DAY:            None,
    UnivMomPrecision.HOUR:           None,
    UnivMomPrecision.MINUTE:         None,
    UnivMomPrecision.SECOND:         0,
    UnivMomPrecision.MILLISECOND:   -3,
    UnivMomPrecision.MICROSECOND:   -6,
    UnivMomPrecision.NANOSECOND:    -9,
    UnivMomPrecision.PICOSECOND:   -12,
    UnivMomPrecision.FEMTOSECOND:  -15,
    UnivMomPrecision.ATTOSECOND:   -18,
}

# NOTE: SI-conformant abbreviations
MomPrecAbbrev: dict[UnivMomPrecision, str] = {
    UnivMomPrecision.BILLION_YEARS:  'G-yr',
    UnivMomPrecision.MILLION_YEARS:  'M-yr',
    UnivMomPrecision.THOUSAND_YEARS: 'k-yr',
    UnivMomPrecision.YEAR:           'yr',
    UnivMomPrecision.DAY:            'day',
    UnivMomPrecision.HOUR:           'hr',
    UnivMomPrecision.MINUTE:         'min',
    UnivMomPrecision.SECOND:         's',
    UnivMomPrecision.MILLISECOND:    'ms',
    UnivMomPrecision.MICROSECOND:    'μs',
    UnivMomPrecision.NANOSECOND:     'ns',
    UnivMomPrecision.PICOSECOND:     'ps',
    UnivMomPrecision.FEMTOSECOND:    'fs',
    UnivMomPrecision.ATTOSECOND:     'as',
}

# ---------------------------------------------------------------------------
# UnivDuration precision is represented as a plain int using the same scheme:
#   0 = SECOND, 1 = MINUTE, 2 = HOUR, 3 = DAY, 4 = YEAR,
#   5 = THOUSAND_YEAR, 6 = MILLION_YEAR, 7 = BILLION_YEAR,
#   negative = sub-second (SI exponent, e.g. -3 = ms, -6 = µs … -18 = as)
# UnivDurPrecision enum has been removed in favour of plain int.
# ---------------------------------------------------------------------------


