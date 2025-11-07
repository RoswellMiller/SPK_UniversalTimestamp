"""
Universal Timestamp System
Comprehensive multi-scale time system:
- Geological: Deep time scales (universal_time.py custom implementation)
- Astronomical: Julian Day Numbers, coordinate time (universal_time.py)
- Human Calendars: convertdate library for cultural/religious calendars
- Scientific: High-precision measurements with uncertainty (universal_time.py)
"""

from decimal import Decimal, getcontext
from enum import Enum
from typing import Optional, Union, Tuple

from abc import abstractmethod
# Set high precision Decimal computations
getcontext().prec = 50


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
    CENTURY = "century"  # 100 years
    DECADE = "decade"  # 10 years
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
    Precision.CENTURY:       {'level': 4, 'power': 2,    'abbrv' : 'h-yr'},
    Precision.DECADE:        {'level': 5, 'power': 1,    'abbrv' : 'da-yr'},
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

##################################################################################################################################################
class UnivTimestamp:
    """
    Attributes:
        calendar            : calendar system being used
        year                : date component
        precision           : precision level for this timestamp
        accuracy            : [0,1] plus/minus accuracy as a decimal fraction
        description         : description of measurement/source
    """
    # __slots__ #######################################################################################
    calendar: Calendar
    year : Optional[Union[Decimal]]
    precision: Precision
    description: str
    accuracy: Decimal
    sort : int            # Sort value for precise ordering, set on construction
    rd : int              # Rata Die fixed day number, used internally, set when first needed, i.e. calculating sort on construction
    # IMMUTABLE #######################################################################################
    __slots__ = ( 'calendar', 'year', 'precision', 'accuracy', 'description', 'sort', 'rd' )
    def __setattr__(self, name, value):
        """Prevent modification of attributes after initialization"""
        if hasattr(self, name):
            raise AttributeError(f"Cannot modify attribute '{name}' of UnivTimestamp")
        super().__setattr__(name, value)
        return
    
    # CONSTANTS ##################################################################################################
    @staticmethod 
    def __version__():
        return "1.0.1-beta"
    @staticmethod
    def __file__():
        return "SPK_UniversalTimestamp\\UnivTimestamp.py"
    
    # CONSTRUCTOR ###################################################################################
    def __init__(
        self,
        calendar: Calendar,
        year : Union[int, Decimal] = None,
        precision: Precision = None,
        accuracy: Decimal = None,
        description: str = ""
    ):
        """
        Initialize Universal Timestamp

        Args:
            date component: year
            calendar: Calendar system being used
            precision: Precision level for this timestamp
            accuracy: Value between 0 and 1 representing plus/minus accuracy as a decimal fraction
            source_description: Description of measurement/source
        """
        # Convert year to large integer
        if year is None:
            raise ValueError("Year must be specified")
        elif not isinstance(year,  (int, Decimal)):
            raise ValueError(f"Invalid year type: {type(year)}. Expected int or Decimal.")
        if isinstance(year, int) or year.is_finite():
            if accuracy is not None and not (isinstance(accuracy, Decimal) and Decimal("0") <= accuracy <= Decimal("1")):
                raise ValueError("Accuracy must be a Decimal between 0 and 1")
        else:
            accuracy = None
        self.calendar = calendar
        self.year = year
        self.precision = precision
        self.accuracy = accuracy
        self.description = description
        return
    
    ################################################################################
    # Methodology from "Calendrical Calculations" by Edward M. Reingold and Nachum Dershowitz
    # r.d. (Rata Die) fixed day 1 =(def) Midnight Monday January 1, 1 Gregorian
    # fixed days are the ... -3, -2, -1, 0, 1, 2, 3 ...
    # The external routines are constructors
    # The internal routines will follow the pattern EMR and ND defined on p. 13
    #   y-from-x =(def) y-from-fixed(fixed-from-x(x-date)) where x,y are calendars
    #   'fixed' here is the Rata Die (r.d.) fixed day number, we will adopt the naming convention
    #   x-from-rd, rd-from-x where x is the calendar system
    #############################################################################
    # Reference "Calendrical Calculations" by Edward M. Reingold and Nachum Dershowitz"
    def _calc_sort_value(self) -> Union[int, Decimal]:
        """
        Return a large integer for precise sorting.
        If day or time is not present, fill with 0.
        """
        value = self.rd
        # Convert local time to UTC if timezone is specified and time components exist
        # Note sort value maybe modified if the day changes due to timezone conversion
        if isinstance(value, Decimal) and not value.is_finite():
            return Decimal('-Infinity')
        day_adjust, utc_hour, utc_minute, utc_second = self._get_utc()
        value += day_adjust
        # pad the sort value with the utc time.
        value *= 100 # make room for 2-digit hour
        if utc_hour is not None:
            value += utc_hour
        value *= 100 # make room for 2-digit minute
        if utc_minute is not None:
            value += utc_minute 
        
        atto_multiplier = int(1e18)  # 10^18 for attoseconds
        value *= 100 # make room for 2-digit second
        value *= atto_multiplier  # Scale to attoseconds
        if utc_second is not None:
            value += int(utc_second * atto_multiplier)
        return value
    
    # TIMESTAMP/RD METHODS ######################################################################################
    @abstractmethod
    def _self_rata_die(self) -> int:  
        """
        Convert the date to Rata Die (fixed day number) for sorting and comparison.
        This method should be implemented in subclasses for specific calendar systems.
        """
        raise NotImplementedError("Subclasses must implement _self_rata_die() method")
    @abstractmethod
    def _get_utc(self) -> Tuple[Optional[Tuple[int,int,Union[int,Decimal]]], int, int, int, Decimal]:
        """
        Convert the time to UTC components (day_adjust, hour, minute, second).
        This method should be implemented in subclasses for specific calendar systems.
        """
        raise NotImplementedError("Subclasses must implement _get_utc() method")
    @abstractmethod
    def _calc_rata_die(self, year: int, month: int, day: int) -> int:
        """
        Convert date components (year, month, day) to Rata Die (fixed day number).
        This method should be implemented in subclasses for specific calendar systems.
        """
        raise NotImplementedError("Subclasses must implement _calc_rata_die() method")

    # FORMATTING METHODS ########################################################################
    def __str__(self) -> str:
        return self.format_signature()

    @abstractmethod
    def __repr__(self) -> str:
        """
        Create a ast.literal_eval(repr_str) compatible string which can be used to construct a new instance
        of the sub-class of this Time stamp.

        Returns:
            str : ast.literal_eval(repr_str) compatible
        NOTE : UnivTimestampFactory has parse function which will return an instance.
        """
        raise NotImplementedError("Subclasses must implement __repr__ method")
    
    def strftime(self,format : str, language : str = 'en') -> str:
        """
        Format the timestamp using a custom format string.
        This is a simplified version and does not support all Python strftime features.
        
        Date Components, Geological
        Directive	Meaning	                            Example
                    YEAR
        %C          Cycle long (Chinese calendar)       
        %c          Cycle short (Chinese calendar)      1
        %Y	        Year long                   	    2025, 66.45 Gyr BCE
        %y	        Year short                          25, -66.45 Gyr
        
                    MONTH, EON
        %m	        Month as a decimal number (01-12)	08
        %B	        Full month name	                    August
        %b	        Abbreviated month name	            Aug
        
                    DAY, ERA
        %d	        Day of the month (01-31)	        02
        %A	        Full weekday name	                Saturday
        %a	        Abbreviated weekday name	        Sat
        %j	        Day of the year (001-366)	        214

        Time Components, Geological
        Directive	Meaning	                            Example
                    HOUR, PERIODS
        %H	        Hour (24-hour clock) (00-23)	    14
        %I	        Hour (12-hour clock) (01-12)	    02
        %p	        AM or PM	                        pm, am
        
                    MINUTE, EPOCHS-AGES
        %M	        Minute (00-59)	                    35
        
                    SECOND 
        %S	        Second (00-59)	                    45
        %f	        Fractional              	        345123
        
                    TIMEZONE
        %z	        UTC offset (+HHMM or -HHMM)	        +0200
        %Z	        Timezone name	                    UTC
        
        Complete Formats
        Directive	Meaning	                            Example
        %K          calender system name	            Gregorian
        %k          calender                	        JD
        %c	        Locale's appropriate date and time	Sat Aug 2 14:35:45 2025
        %x	        Locale's appropriate date	        08/02/25
        %X	        Locale's appropriate time	        14:35:45
        
        Modifiers
        %#m,%#d,%#j - eliminates leading 0s
        """
        # format string
        fmt = ""
        for i in range(len(format)):
            if format[i] == '%':
                break
            fmt += format[i]
            continue
        # split into % segments
        segments = format[i+1:].split('%')
        for segment in segments:
            # If the segment is empty, skip it
            if len(segment) == 0:
                continue
            # get segment type and any modifiers
            seg_remainder_start = 1
            seg_eliminate_leading_zero = False
            seg_type = segment[0]
            if seg_type == '#':
                seg_eliminate_leading_zero = True
                if len(segment) > 1:
                    seg_type = segment[1]
                    seg_remainder_start = 2
            # Process by segment type
            # Year
            if seg_type in 'Yy':
                fmt += self._strftime_year(seg_type, language, seg_eliminate_leading_zero)
            # Month    
            elif seg_type in 'mBb':
                fmt += self._strftime_month(seg_type, language, seg_eliminate_leading_zero)
            # Day
            elif seg_type in 'dAaj':
                fmt += self._strftime_day(seg_type, language, seg_eliminate_leading_zero)
            # Time
            elif seg_type in 'HIpMSfZz':
                fmt += self._strftime_time(seg_type, language, seg_eliminate_leading_zero)
            # Calendar
            elif seg_type == 'K':
                # Calendar system name
                fmt += CalendarAtts[language][self.calendar]['name']
            elif seg_type == 'k':
                # Calendar system abbreviation
                fmt += CalendarAtts[language][self.calendar]['abbrv']    
            # Compound segments
            elif seg_type in 'cXx':
                # Locale's appropriate date and time or date or time
                fmt += self._strftime_compound(seg_type, language, seg_eliminate_leading_zero)    
            else:
                # Unknown directive, keep it as is
                pass  # Ignore unknown directives 
            # complete the formatting till the end of the segment
            for i in range(seg_remainder_start, len(segment)):
                fmt += segment[i]    
        
        return fmt

    def _strftime_year(self, seg_type: str, language: str, eliminate_leading_zero: bool) -> str:
        """
        Format the year component based on the segment type and language.
        """
        if self.precision == Precision.BILLION_YEARS:
            year = f"{self.year / 1_000_000_000:.2f}"
        elif self.precision == Precision.MILLION_YEARS:
            year = f"{self.year / 1_000_000:.2f}" 
        elif self.precision == Precision.THOUSAND_YEARS:
            year = f"{self.year / 1_000:.2f}"
        elif self.precision == Precision.CENTURY:
            year= f"{self.year / 100:.2f}"
        elif self.precision == Precision.DECADE:
            year = f"{self.year / 10:.1f}"
        else:
            year = f"{self.year}"
        # Handle negative vales
        fmt = year
        if seg_type == 'Y':
            if PrecisionAtts[self.precision]['level'] < PrecisionAtts[Precision.YEAR]['level']:
                fmt += f" {PrecisionAtts[self.precision]['abbrv']}"
        elif seg_type == 'y':
            if (self.year < 0 ):
                fmt = year[:1]
                fmt += f" {CalendarAtts[language][self.calendar]['bce_suffix']}"
            if PrecisionAtts[self.precision]['level'] < PrecisionAtts[Precision.YEAR]['level']:
                fmt += f" {PrecisionAtts[self.precision]['abbrv']}"
        return fmt

    @abstractmethod
    def _strftime_month(self, seg_type: str, language: str, eliminate_leading_zero: bool) -> str:
        """
        Format the month component based on the segment type and language.
        This method should be implemented in subclasses for specific calendar systems.
        """
        raise NotImplementedError("Subclasses must implement _strftime_month() method")
    
    @abstractmethod
    def _strftime_day(self, seg_type : str, language :str, eliminate_leading_zero: bool = False) -> str:
        """
        Format the day component based on the segment type and language.
        This method should be implemented in subclasses for specific calendar systems.
        """
        raise NotImplementedError("Subclasses must implement _strftime_day() method")
        
    @abstractmethod
    def _strftime_time(self, seg_type : str, language :str, eliminate_leading_zero: bool = False) -> str:
        """
        Format the time component based on the segment type and language.
        This method should be implemented in subclasses for specific calendar systems.
        """
        raise NotImplementedError("Subclasses must implement _strftime_time() method")
    
    @abstractmethod
    def _strftime_compound(self, seg_type : str, language :str, eliminate_leading_zero: bool = False) -> str:
        """
        Format the compound component based on the segment type and language.
        This method should be implemented in subclasses for specific calendar systems.
        """
        raise NotImplementedError("Subclasses must implement _strftime_compound() method")

    @abstractmethod
    def format_signature(self, include_precision: bool = False, include_accuracy: bool = False, include_confidence: bool = False ) -> str:
        """
        Format the complete timestamp for display.
        This method should be implemented in subclasses for specific calendar systems.
        """
        raise NotImplementedError("Subclasses must implement format_signature() method")
    
    # COMPARISON METHODS ##########################################################################
    def __lt__(self, other) -> bool:
        """Less than comparison for sorting"""
        if not isinstance(other, UnivTimestamp):
            return NotImplemented
        return self.sort < other.sort

    def __le__(self, other) -> bool:
        """Less than or equal comparison"""
        if not isinstance(other, UnivTimestamp):
            return NotImplemented
        return self.sort <= other.sort

    def __gt__(self, other) -> bool:
        """Greater than comparison"""
        if not isinstance(other, UnivTimestamp):
            return NotImplemented
        return self.sort > other.sort

    def __ge__(self, other) -> bool:
        """Greater than or equal comparison"""
        if not isinstance(other, UnivTimestamp):
            return NotImplemented
        return self.sort_value >= other.sort

    def __eq__(self, other) -> bool:
        """Equality comparison"""
        if not isinstance(other, UnivTimestamp):
            return NotImplemented
        return self.sort == other.sort

    def __ne__(self, other) -> bool:
        """Not equal comparison"""
        return not self.__eq__(other)
    
    
    
## End of class UnivTimestamp #################################################################################################################

