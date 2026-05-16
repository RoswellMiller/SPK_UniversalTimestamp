
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