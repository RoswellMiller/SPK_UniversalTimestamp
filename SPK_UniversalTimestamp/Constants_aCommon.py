
"""
Constants_aCommon — cross-calendar enumerations and localisation tables.

**Purpose.**  Give every calendar module a single import point for
(a) the `Calendar` enum that names each supported system and
(b) the multilingual attribute dictionary (`CalendarAtts`) that
presentation layers consult for names, abbreviations, and era suffixes.

**Public surface (star-exported via `__init__.py`).**
    `Calendar` (enum), `CalendarAtts` (dict keyed `[language][Calendar]`).

**R&D references.**  The calendar list mirrors R&D's table of
covered systems (see book table of contents); the arithmetic vs
astronomical grouping in this file matches R&D Part I / Part II.

**Not in scope.**  Calendar-specific constants (month names, day
counts) belong in the sibling `Constants_<Calendar>.py` files.

**Change history.**  See `CHANGELOG.md`.  Additions to `Calendar`
are additive and safe; renaming an enum member is a breaking API
change and needs a version bump.
"""

from enum import Enum


class Calendar(Enum):
    """
    Enumeration of every calendar system this package knows about.

    Members marked ``# Done`` in the source are implemented and
    covered by tests; the rest are placeholder identifiers reserved
    for future work.  Values are lowercase strings suitable for
    on-disk serialization.
    """
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