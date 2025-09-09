"""
Universal Timestamp System
Comprehensive multi-scale time system:
- Geological: Deep time scales (universal_time.py custom implementation)
- Astronomical: Julian Day Numbers, coordinate time (universal_time.py)
- Human Calendars: convertdate library for cultural/religious calendars
- Scientific: High-precision measurements with uncertainty (universal_time.py)
"""

from decimal import Decimal, getcontext, ROUND_DOWN
from typing import Optional, Union, Tuple, Callable, List
from abc import abstractmethod
from zoneinfo import ZoneInfo
from datetime import datetime, timedelta
from SPK_UniversalTimestamp import UnivTimestamp, Precision, PrecisionAtts, Calendar, CalendarAtts
from SPK_UniversalTimestamp.CC01_Calendar_Basics import Epoch_rd
getcontext().prec = 50

##################################################################################################################################################
class UnivCalendars(UnivTimestamp):
    """
    Attributes:
        calendar            : calendar system being used
        year, month, day    : date component
        hour, minute, second: time component
        precision           : precision level for this timestamp
        accuracy            : human-readable accuracy description
        description         : description of measurement/source
        confidence          : statistical confidence level (0.0-1.0)
    """
    # __slots__ ####################################################################################
    #_cnst_validated : bool = False
    month: Optional[int]
    day: Optional[int]
    hour: Optional[int]
    minute: Optional[int]
    second: Optional[Union[Decimal]]
    tz : Optional[str]
    fold: Optional[int]
    # IMMUTABLE #######################################################################################
    __slots__ = ('_cnst_validated', 'month', 'day', 'hour', 'minute', 'second', 'tz', 'fold')
    
    # CONSTANTS #########################################################################################
    Day_of_Week_Atts = {
        'en' : {
            0 : {'name': 'Monday',    'abbrv': 'Mon'},
            1 : {'name': 'Tuesday',   'abbrv': 'Tue'},
            2 : {'name': 'Wednesday', 'abbrv': 'Wed'},
            3 : {'name': 'Thursday',  'abbrv': 'Thu'},
            4 : {'name': 'Friday',    'abbrv': 'Fri'},
            5 : {'name': 'Saturday',  'abbrv': 'Sat'},
            6 : {'name': 'Sunday',    'abbrv': 'Sun'}
        },
        'fr' : {
            0 : {'name': 'Lundi',     'abbrv': 'Lun'},
            1 : {'name': 'Mardi',     'abbrv': 'Mar'},
            2 : {'name': 'Mercredi',  'abbrv': 'Mer'},
            3 : {'name': 'Jeudi',     'abbrv': 'Jeu'},
            4 : {'name': 'Vendredi',  'abbrv': 'Ven'},
            5 : {'name': 'Samedi',    'abbrv': 'Sam'},
            6 : {'name': 'Dimanche',  'abbrv': 'Dim'}
        },
        'de' : {
            0 : {'name': 'Montag',    'abbrv': 'Mo'},
            1 : {'name': 'Dienstag',  'abbrv': 'Di'},
            2 : {'name': 'Mittwoch',  'abbrv': 'Mi'},
            3 : {'name': 'Donnerstag', 'abbrv': 'Do'},
            4 : {'name': 'Freitag',   'abbrv': 'Fr'},
            5 : {'name': 'Samstag',   'abbrv': 'Sa'},
            6 : {'name': 'Sonntag',   'abbrv': 'So'}
        },
        'es' : {
            0 : {'name': 'Lunes',     'abbrv': 'Lun'},
            1 : {'name': 'Martes',    'abbrv': 'Mar'},
            2 : {'name': 'Miércoles', 'abbrv': 'Mié'},
            3 : {'name': 'Jueves',    'abbrv': 'Jue'},
            4 : {'name': 'Viernes',   'abbrv': 'Vie'},
            5 : {'name': 'Sábado',    'abbrv': 'Sáb'},
            6 : {'name': 'Domingo',   'abbrv': 'Dom'}
        },
        'it' : {
            0 : {'name': 'Lunedì',    'abbrv': 'Lun'},
            1 : {'name': 'Martedì',   'abbrv': 'Mar'},      
            2 : {'name': 'Mercoledì', 'abbrv': 'Mer'},
            3 : {'name': 'Giovedì',   'abbrv': 'Gio'},
            4 : {'name': 'Venerdì',   'abbrv': 'Ven'},
            5 : {'name': 'Sabato',    'abbrv': 'Sab'},
            6 : {'name': 'Domenica',  'abbrv': 'Dom'}
        }
    }
 
    # CONSTRUCTOR ###################################################################################
    CNST_ARGS =  []
    # Each tuple: (slot name, allowed_types, valid_function, precision_enum)
    
    # Validation method for constructor arguments
    def _init_validate_constructor_args(self, num_required, args: List, init_precision) -> Tuple[dict, Precision]:
        if len(args) < num_required:
            expected = ', '.join(self.CNST_ARGS[:num_required][0])
            raise ValueError(f"Too few arguments: expected at least {num_required} ({expected})")
        if len(args) > len(self.CNST_ARGS):
            raise ValueError(f"Too many arguments: expected at most {len(self.CNST_ARGS)}")

        arg_context = {}
        parm_precision = None
        for i, arg in enumerate(args):
            if arg is None:
                break
            name, types, is_valid_fn, parm_precision= self.CNST_ARGS[i]
            # Type check
            if not isinstance(arg, types):
                raise TypeError(f"{name} must be of type(s) {types}, got {type(arg)}")
            # Value check
            if not is_valid_fn(arg, arg_context):
                raise ValueError(f"{name}={arg} not valid for {arg_context}")
            # Add to context for subsequent arguments
            arg_context[name] = arg
        # Validate precision    
        if init_precision is None :
            precision = parm_precision
        elif init_precision == parm_precision:
            precision = init_precision
        elif PrecisionAtts[init_precision]['level'] < PrecisionAtts[parm_precision]['level']:
            raise ValueError(f"Invalid precision {init_precision}. {parm_precision} is less than the precision specified.")
        elif parm_precision == Precision.SECOND and PrecisionAtts[init_precision]['level'] >= PrecisionAtts[Precision.SECOND]['level']:
            precision = init_precision
        else:
            raise ValueError(f"Invalid precision {init_precision}. Must be at least {parm_precision}.")
        # Ensure no trailing parameters
        if len(args) < len(self.CNST_ARGS):
            for trailing in args[len(args):]:
                if trailing is not None:
                    raise ValueError("Parameters must be contiguous with no gaps")
        # Set trailing parameters to None
        if len(arg_context) < len(self.CNST_ARGS):
            for name, _, _, _ in self.CNST_ARGS[len(arg_context):]:
                arg_context[name] = None
        self._cnst_validated = True
        return arg_context, precision
        
    ##################################  
    def __init__(
        self,
        calendar: Calendar,
        year : Union[int, float, Decimal, str],
        month: Optional[int],
        day: Optional[int],
        hour: Optional[int],
        minute: Optional[int],
        second: Optional[Union[int, Decimal]],
        precision: Precision,
        timezone : Optional[str] = 'UTC',
        fold : Optional[int] = 0,
        accuracy: Decimal = None,
        description: str = ""
    ):
        """
        Initialize Universal Timestamp

        Args:
            date component: (year, month, day)
            ime component: (hour, minute, second)
            calendar: Calendar system being used
            time zone: Timezone for the timestamp, defaults to 'UTC'
            fold: 0 or 1, used for ambiguous times in daylight saving time transitions
            precision: Precision level for this timestamp
            accuracy: [0,1] plus/minus accuracy as a decimal fraction
            source_description: Description of measurement/source
        """
        # ASSUMES : Values for year, month, day, hour, minute and second HAVE BEEN VALIDATED by a call to _validate_constructor_args()
        if not hasattr(self, '_cnst_validated') or not self._cnst_validated:
            raise ValueError("Constructor arguments must be validated using _validate_constructor_args() before initializing")
        # Truncate to specified precision
        if second is not None :    
            power = PrecisionAtts[precision].get('power', 0)
            if power<0:
                second = second.quantize(Decimal('1e' + str(power)), rounding=ROUND_DOWN) 
        # Convert time components to UTC if timezone is specified and time components exist
        fold = fold if fold in (0,1) else 0
        # if timezone and timezone != 'UTC' and hour is not None:
        #     hour, minute, adj_day = self._init_convert_to_utc(hour, minute, timezone, fold, year, month, day)
        #     if adj_day != 0:
        #         rd = self._calc_rata_die(year, month, day) - adj_day
        #         year, month, day = self._calc_date_from_rd(rd)
            
        super().__init__(calendar, year, precision=precision, accuracy=accuracy, description=description)
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        self.second = second
        self.tz = timezone
        self.fold = fold
        self.sort, self.rd = super()._calc_sort_value()        
        return
    
    ################################################################################
    # Methodology from "Calendrical Calculations" by Edward M. Reingold and Nachum Dershowitz
    # r.d. (Rata Die) fixed day 1 =(def) Midnight Monday January 1, 1 Gregorian
    # fixed days are the ... -3, -2, -1, 0, 1, 2, 3 ...
    # The external routines are constructors
    # The internal routines will follow the pattern EMR and ND defined on p. 13
    #   y-from-x =(def) y-from-fixed(fixed-from-x(x-date)) where x,y are calendars
    #   'fixed' here is the Rata Die (r.d.) fixed day number, we will adopt the naming conventiion
    #   x-from-rd, rd-from-x where x is the calendar system
    #############################################################################
    # Reference "Calendrical Calculations" by Edward M. Reingold and Nachum Dershowitz"
    # UnivCalendars introduce day and time components
    # Day components are month, day of month
    # -- day components map year, month, day to a fixed day number (Rata Die)
    # Time components are hour, minute, second
    # -- time components map hour, minute, second to a fractional day or (hour, minute, second)
    # Both day and time are in the context of a timezone and folding protocol for ambiguous changes of time, e.g. daylight savings time
    # NOTE : slots of the timestamp are local according to the timezone and fold
    # NOTE : the rata die (,rd) is local
    # NOTE : the sort value (.sort) is UTC
    @staticmethod
    def convert_to_utc(hour, minute, second, from_timezone : str, fold : int, year, month, day) -> Tuple[int, int, int, Decimal]:
        """
        Convert time components from source timezone to UTC
        
        Args:
            source_timezone: Source timezone name
            
        Returns:
            Tuple of (hour, minute, second) in UTC
        """
        if hour is None:
            raise ValueError("Hour must be specified for conversion")
        minute = minute if minute is not None else 0
        # Get timezone offset in hours and minutes
        offset_hours, offset_minutes = UnivCalendars._get_timezone_offset(from_timezone, fold, year, month, day, hour, minute)
        # Calculate total minutes
        total_minutes_source = hour * 60 + minute    
        # Adjust by the timezone offset (subtract because we're converting to UTC)
        total_minutes_utc = total_minutes_source - (offset_hours * 60 + offset_minutes)    
        # Handle day boundary crossing
        day_adjustment = 0
        while total_minutes_utc < 0:
            total_minutes_utc += 24 * 60
            day_adjustment -= 1           
        while total_minutes_utc >= 24 * 60:
            total_minutes_utc -= 24 * 60
            day_adjustment += 1       
        # Convert back to hours and minutes
        utc_hour = total_minutes_utc // 60
        utc_minute = total_minutes_utc % 60 
        # Return the converted time and day adjustment
        return day_adjustment, utc_hour, utc_minute, second

    @staticmethod
    def _get_timezone_offset(timezone_name : str, fold : int, year : int, month : int, day : int, hour : int, minute : int) -> Tuple[int, int]:
        """
        Get the offset (in hours and minutes) for a timezone
        
        Args:
            timezone_name: Timezone name
            
        Returns:
            Tuple of (hours, minutes) offset from UTC
        """
        try:
            # Create timezone object
            tz = ZoneInfo(timezone_name)
            if tz is None:
                raise ValueError(f"Invalid timezone name: {timezone_name}")    
            # We need a reference datetime to get the offset
            # NOTE you should never be here is year, month and day None
            # NOTE Assumes there was no such thing as daylight savings time before year 1
            # If year is 0 or negative, set it to 1 to avoid invalid datetime
            year = max(1,year)
            # delta = timedelta(days=0)
            if isinstance(month, Tuple):
                month = month[0]
                # if month[1]:
                #     delta = timedelta(days=30)
            source_date = datetime(year, month, day, hour, minute, 0, tzinfo=tz, fold=fold) #+ delta
            # Get offset in seconds
            offset_seconds = source_date.utcoffset().total_seconds()            
            # Convert to hours and minutes
            offset_hours = int(offset_seconds // 3600)
            offset_minutes = int((offset_seconds % 3600) // 60)           
            return offset_hours, offset_minutes
        except Exception as e:
            raise ValueError(f"Invalid timezone '{timezone_name}': {e}")
    
    # TIMESTAMP/RD METHODS ######################################################################################
    @abstractmethod
    def _self_rata_die(self) -> int:  
        """
        Convert the date to Rata Die (fixed day number) for sorting and comparison.
        This method should be implemented in subclasses for specific calendar systems.
        """
        raise NotImplementedError("Subclasses must implement _self_rata_die() method") 
    
    def _self_utc(self) -> Tuple[int, int, int, Decimal]:
        """
        Convert the time to UTC components (day_adjust, hour, minute, second).
        """
        if self.hour is None or self.tz == 'UTC':
            return 0, self.hour, self.minute, self.second
        day_adjust, utc_hour, utc_minute, utc_second = UnivCalendars.convert_to_utc(self.hour, self.minute, self.second, self.tz, self.fold, self.year, self.month, self.day)
        return day_adjust, utc_hour, utc_minute, utc_second

    @abstractmethod
    def _calc_rata_die(self, year: int, month: int, day: int) -> int:
        """
        Convert date components (year, month, day) to Rata Die (fixed day number).
        This method should be implemented in subclasses for specific calendar systems.
        """
        raise NotImplementedError("Subclasses must implement _calc_rata_die() method")
    
    # CALENDARS METHODS ######################################################################################
    @abstractmethod
    def _calc_date_from_rd(self, rd: int) -> Tuple[int, int, int]:
        """
        Convert Rata Die (fixed day number) to date components (year, month, day).
        This method should be implemented in subclasses for specific calendar systems.  
        """
        raise NotImplementedError("Subclasses must implement _calc_date_from_rd() method")

    @abstractmethod
    def month_attr(self, attr : str, language : str='en') -> Union[int, str]:
        """
        Get a month attribute.
        This method should be implemented in subclasses for specific calendar systems.
        """
        raise NotImplementedError("Subclasses must implement month_attr() method")

    @abstractmethod
    def day_of_year(self) -> int:
        """
        Calculate the day of the year for this timestamp.
        This method should be implemented in subclasses for specific calendar systems.
        """
        raise NotImplementedError("Subclasses must implement day_of_year() method")
    
    
    def day_of_week_attr(self, attr : str, language : str='en') -> Union[int, str]:
        """
        Get a day of the week attribute.
        """
        return UnivCalendars.Day_of_Week_Atts[language][(self.rd - 1) % 7][attr]

    # def _get_timezone_info(self, format_tz_name: Optional[str] = None) -> dict:
    #     """
    #     Get timezone information for formatting
        
    #     Args:
    #         format_tz_name: Optional timezone name to format in. If None, uses self.timezone_name
        
    #     Returns:
    #         Dictionary with timezone details
    #     """
    #     # Use provided timezone for formatting or default to the timestamp's timezone
    #     tz_name = format_tz_name or self.timezone_name or "UTC"
        
    #     try:
    #         # Create timezone object
    #         tz = ZoneInfo(tz_name)
            
    #         # Create a datetime object in this timezone (for calculating offsets)
    #         dt_components = [
    #             self.year if self.year is not None else 2000,
    #             self.month if self.month is not None else 1,
    #             self.day if self.day is not None else 1,
    #             self.hour if self.hour is not None else 0,
    #             self.minute if self.minute is not None else 0,
    #             int(self.second) if self.second is not None else 0,
    #         ]
            
    #         # Create datetime in UTC
    #         utc_dt = datetime(*dt_components, tzinfo=timezone.utc)
            
    #         # Convert to target timezone
    #         local_dt = utc_dt.astimezone(tz)
            
    #         # Extract timezone information
    #         offset_str = local_dt.strftime("%z")
    #         offset_with_colon = f"{offset_str[:3]}:{offset_str[3:]}"
            
    #         return {
    #             "name": tz_name,
    #             "abbr": local_dt.strftime("%Z"),
    #             "offset": offset_str,
    #             "offset_colon": offset_with_colon,
    #             "tzinfo": tz
    #         }
    #     except Exception as e:
    #         # Fallback if timezone not found
    #         return {
    #             "name": "UTC",
    #             "abbr": "UTC",
    #             "offset": "+0000",
    #             "offset_colon": "+00:00",
    #             "tzinfo": timezone.utc
    #         }    

    # @staticmethod
    # def get_system_timezone() -> str:
    #     """Get the system's local timezone"""
    #     try:
    #         from zoneinfo import ZoneInfo
    #         from tzlocal import get_localzone
    #         return str(get_localzone())
    #     except ImportError:
    #         # Fallback if tzlocal is not available
    #         return "UTC"

    # def as_timezone(self, target_timezone: str) -> dict:
    #     """
    #     Convert the timestamp to the specified timezone
        
    #     Args:
    #         target_timezone: Target timezone name
        
    #     Returns:
    #         Dictionary with date/time components in the target timezone
    #     """
    #     try:
    #         # Create timezone objects
    #         target_tz = ZoneInfo(target_timezone)
    #         utc_tz = timezone.utc
            
    #         # Create a datetime object in UTC from our internal representation
    #         dt_components = [
    #             self.year if isinstance(self.year, int) else int(self.year),
    #             self.month if self.month is not None else 1,
    #             self.day if self.day is not None else 1,
    #             self.hour if self.hour is not None else 0,
    #             self.minute if self.minute is not None else 0,
    #             int(self.second) if self.second is not None else 0,
    #         ]
            
    #         # Create datetime in UTC
    #         utc_dt = datetime(*dt_components, tzinfo=utc_tz)
            
    #         # Convert to target timezone
    #         local_dt = utc_dt.astimezone(target_tz)
            
    #         # Extract components
    #         result = {
    #             "year": local_dt.year,
    #             "month": local_dt.month,
    #             "day": local_dt.day,
    #             "hour": local_dt.hour,
    #             "minute": local_dt.minute,
    #             "second": local_dt.second,
    #             "timezone": target_timezone,
    #             "offset": local_dt.strftime("%z")
    #         }
        
    #         # If original seconds had a fractional part, preserve it
    #         if self.second is not None and isinstance(self.second, (Decimal, float)) and self.second != int(self.second):
    #             frac_part = Decimal(str(self.second)) - int(self.second)
    #             result["second"] = Decimal(local_dt.second) + frac_part
                
    #         return result
    #     except Exception as e:
    #         # If conversion fails, return original values
    #         return {
    #             "year": self.year,
    #             "month": self.month,
    #             "day": self.day,
    #             "hour": self.hour,
    #             "minute": self.minute,
    #             "second": self.second,
    #             "timezone": "UTC",
    #             "offset": "+0000"
    #         }   

    # FORMATTING METHODS ######################################################################################
    def __str__(self) -> str:
        return self.format_signature()

    def __repr__(self) -> str:
        """Create a string representation that could be used to recreate the object."""
        # Safely represent string attributes by escaping quotes and special characters
        safe_accuracy = f"'{str(self.accuracy)}'" if self.accuracy is not None else "None"
        safe_description = repr(self.description)
        
        # Build the string with proper escaping
        class_name = self.__class__.__name__
        result = ("{"
                f"'class':'{class_name}',"
                f"'ca':'{self.calendar.name}',"
                f"'yr':{self.year},"
                f"'mo':{self.month},"
                f"'da':{self.day},"
                f"'hr':{self.hour},"
                f"'mi':{self.minute},"
                f"'sc':{self.second},"
                f"'pr':'{self.precision.name}',"
                f"'tz':{repr(self.tz)},"
                f"'fo':{self.fold},"
                f"'ac':{safe_accuracy},"
                f"'de':{safe_description}"
                "}"
                )
        return result   # End of class UnivTimestamp

    def _strftime_month(self, seg_type : str, language :str, eliminate_leading_zero: bool = False) -> str:
        if self.month is None:
            return ""
            #zs = '02d' if not eliminate_leading_zero else 'd'
            #return f"{0:{zs}}"  # Default to January if month is not specified
        if seg_type == 'm':
            zs = '02d' if not eliminate_leading_zero else 'd'
            return f"{self.month:{zs}}"  # Zero-padded month number
        elif seg_type == 'B':
            return self.month_attr('name', language)  # Full month name
        elif seg_type == 'b':
            return self.month_attr('abbrv', language)  # Abbreviated month name
        return ""

    def _strftime_day(self, seg_type : str, language :str, eliminate_leading_zero: bool = False) -> str:
        fmt = ""
        if self.day is None:
            return ""
            # zs = '02d' if not eliminate_leading_zero else 'd'
            # fmt += f"{0:{zs}}"  # Default to 1st if day is not specified
        elif seg_type == 'd':
            zs = '02d' if not eliminate_leading_zero else 'd'
            fmt +=  f"{self.day:{zs}}"  # Zero-padded day of the month
    
        elif seg_type == 'A':
            fmt +=  self.day_of_week_attr('name', language)  # Full weekday name
        elif seg_type == 'a':
            fmt += self.day_of_week_attr('abbrv', language)  # Abbreviated weekday name
        elif seg_type == 'j':
            zs = '03d' if not eliminate_leading_zero else 'd'
            fmt += f"{self.day_of_year():{zs}}"  # Day of the year (001-366)
        return fmt

    def _strftime_time(self, seg_type : str, language :str, eliminate_leading_zero: bool = False) -> str:
        # Hour
        fmt = ""
        if self.hour is None:
            return ""
        if seg_type == 'H':
            fmt += f"{self.hour:02d}" if self.hour is not None else ".."   
        elif seg_type == 'I':
            fmt += f"{self.hour % 12:02d}" if self.hour is not None else ".."
        elif seg_type == 'p':
            # AM/PM
            if self.hour is None:
                pass #fmt += ""
            else:
                fmt += "am" if self.hour < 12 else "pm"     
        elif seg_type == 'M':
            fmt +=  f"{self.minute:02d}" if self.minute is not None else ".."
        elif seg_type in 'S':
            if self.second is None:
                pass #return ".."
            else:
                int_part = int(self.second)
                fmt += f"{int_part:02d}"  # Format seconds intger part                   
        elif seg_type == 'f':
            if self.second is None:
                pass #fmt += "000000"
            else:
                fmt += self._format_seconds()[3:] # Format factional part
        elif seg_type == 'z':
            # UTC offset, assuming no timezone information is available
            fmt += "+0000"
        elif seg_type == 'Z':
            # Timezone name, assuming UTC
            fmt += "UTC"
        return fmt
    
    def _strftime_compound(self, seg_type : str, language :str, eliminate_leading_zero: bool = False) -> str:
        if seg_type == 'c':
            # Locale's appropriate date and time
            return self.format_signature()
        elif seg_type == 'x':
            # Locale's appropriate date
            return self.format_signature_date()
        elif seg_type == 'X':
            # Locale's appropriate time
            return self.format_signature_time()
        return ""

    def format_signature_date(self) -> str:
        """Format the date component based on calendar system and precision"""
        result = ""
        if self.year is None:
            return "????"
        result+= f"{self.year}"
        if self.calendar == Calendar.GREGORIAN:
            if self.year<0:
                if result[0] == '-':
                    result = result[1:]
                    result +=' ' + CalendarAtts['en'][self.calendar]['bce_suffix']
            else:
                pass 
        elif self.calendar == Calendar.JULIAN:
            if self.year<0:
                if result[0] == '-':
                    result = result[1:]
                    result += " " + CalendarAtts['en'][self.calendar]['bce_suffix']
            else:
                pass  
            
        if self.month is not None:
            result += f"-{self.month:02d}"
        if self.day is not None:
            result += f"-{self.day:02d}"

        cal_abbrv = CalendarAtts['en'][self.calendar]['abbrv']
        if cal_abbrv and len(cal_abbrv) > 0:
            result += f" {cal_abbrv}"
        return result

    def _format_seconds(self) -> str:
        """Format the seconds component with appropriate precision"""
        if self.second is None:
            return "00"
        fmt = ""
        int_second = int(self.second)
        frac_part = self.second - int_second
        if frac_part == 0:
            fmt += f"{int_second:02d}"
        else:
            fmt += f"{int_second:02d}{str(frac_part)[1:]}"
        return fmt
    
    def format_signature_time(self) -> str:
        """Format the time component with appropriate precision"""
        if self.hour is None and self.minute is None and self.second is None:
            return ""
        hour = self.hour if self.hour is not None else 0
        minute = self.minute if self.minute is not None else 0
        second = self.second if self.second is not None else 0
        if hour == 0 and minute == 0 and second == 0:
            result = "MIDNIGHT"
        elif hour == 12 and minute == 0 and second == 0:
            result = "NOON"
        else:
            result = f"{hour:02d}:{minute:02d}:{self._format_seconds()}"
        return result

    def format_signature(self, include_precision: bool = False) -> str:
        """Format complete timestamp for display"""
        date_part = self.format_signature_date()
        time_part = self.format_signature_time()
        result = date_part
        if time_part:
            result += f" {time_part}"
        # Add precision if requested
        if include_precision:
            result += f" {self.precision.value}"  
            if self.accuracy:
                result += f"±{self.accuracy*100:.1f}%"
        return result

    ###########################################################################################
    # Reference "Calendrical Calculations" by Edward M. Reingold and Nachum Dershowitz



## End of class UnivTimestamp #################################################################################################################


