
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
class Precision(Enum):
    """Precision levels for date and time components"""
    BILLION_YEARS = "10⁹years"  # billion years
    MILLION_YEARS = "10⁶years"  # million years
    THOUSAND_YEARS = "10³years"  # 1000 years
    YEAR = "year"  # 1 year
    MONTH = "month"  # 1 month
    DAY = "day"  # 1 day
    HOUR = "hour"  # hour
    MINUTE = "minute"  # minute
    SECOND = "second"  # second
    MILLISECOND = "10⁻³second"  # ms
    MICROSECOND = "10⁻⁶second"  # μs
    NANOSECOND = "10⁻⁹second"  # ns
    PICOSECOND = "10⁻¹²second"  # ps
    FEMTOSECOND = "10⁻¹⁵second"  # fs
    ATTOSECOND = "10⁻¹⁸second"  # as

# NOTE : The prefixes for the abbrv should be SI conformant
PrecisionAtts = {
    Precision.BILLION_YEARS: {'level': 1, 'power': 9,    'abbrv' : 'G-yr'},
    Precision.MILLION_YEARS: {'level': 2, 'power': 6,    'abbrv' : 'M-yr'},
    Precision.THOUSAND_YEARS:{'level': 3, 'power': 3,    'abbrv' : 'k-yr'},
    Precision.YEAR:          {'level': 6, 'power': 0,    'abbrv' : 'yr'},
    Precision.MONTH:         {'level': 7, 'power': None, 'abbrv' : 'mo'},
    Precision.DAY:           {'level': 8, 'power': None, 'abbrv' : 'day'},
    Precision.HOUR:          {'level': 9, 'power': None, 'abbrv' : 'hr'},
    Precision.MINUTE:        {'level': 10, 'power': None,'abbrv' : 'min'},
    Precision.SECOND:        {'level': 11, 'power': 0,   'abbrv' : 's'},
    Precision.MILLISECOND:   {'level': 12, 'power': -3,  'abbrv' : 'ms'},
    Precision.MICROSECOND:   {'level': 13, 'power': -6,  'abbrv' : 'μs'},
    Precision.NANOSECOND:    {'level': 14, 'power': -9,  'abbrv' : 'ns'},
    Precision.PICOSECOND:    {'level': 15, 'power': -12, 'abbrv' : 'ps'},
    Precision.FEMTOSECOND:   {'level': 16, 'power': -15, 'abbrv' : 'fs'},
    Precision.ATTOSECOND:    {'level': 17, 'power': -18, 'abbrv' : 'as'},   
}

