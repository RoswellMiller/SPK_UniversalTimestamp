"""
Universal Moment
Comprehensive multi-scale time system:
- A rata die system based on the work of Reingold and Dershowitz
- Supports multiple calendar systems
- High precision date representation using Decimal
- Immutable timestamp objects for data integrity
- Range from the beginning of time Decimal('-inf')
- The Moment is composed of two factor a rd_day and an rd_time.
    1. rd_day is the rata die, from Reingold and Dershowitz, is a decimal number 
    where the integer part represents days (plus or minus)
    since Midnight Monday January 1, 1 Midnight Gregorian.
    2. rd_time is a tuple of (hour : int, minute : int, second : Decimal). The second
    here is the 1/24*60*60 fraction of a single rotation of the earth on its axis.
    It is NOT a second as measured by the radioactive decay of Cesium 133 atoms.
- Precision levels to indicate the certainty of the timestamp
"""
import langcodes
import re
from datetime import datetime, timezone
from decimal import Decimal, getcontext, ROUND_DOWN
from .CC00_Decimal_library import floor
from typing import Optional, Union
from abc import abstractmethod
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from .CC01_Calendar_Basics import Epoch_rd
from .CC02_Gregorian import is_gregorian_leap_year, rd_from_gregorian, gregorian_from_rd
from .CC03_Julian import is_julian_leap_year, rd_from_julian
from .CC08_Hebrew import rd_from_hebrew, last_day_of_hebrew_month, last_hebrew_month_of_year
from .CC19_Chinese_1645 import rd_from_chinese, chinese_new_moon_before, chinese_new_moon_on_or_after
from .Constants_aCommon import Calendar, CalendarAtts, Precision, PrecisionAtts
from .Constants_Gregorian import gregorian_MONTH_ATTS
from .Constants_Julian import julian_MONTH_ATTS
#from .UnivMoment import UnivMoment
# Set high precision Decimal computations
getcontext().prec = 50


class UnivMoment:
    """
    Attributes:
    A universal moment in time represented as a Rata Die (RD) decimal number.
    """

    # __slots__ #######################################################################################
    rd_day: Decimal  # Rata Die moment
    rd_time: tuple[int, int, Decimal]  # (hour, minute, second)
    precision: Precision  # Precision level of the moment
    # IMMUTABLE #######################################################################################
    __slots__ = ("rd_day", "rd_time", "precision", "description")

    def __setattr__(self, name, value):
        """Prevent modification of attributes after initialization"""
        if hasattr(self, name):
            raise AttributeError(f"Cannot modify attribute '{name}' of UnivMoment")
        super().__setattr__(name, value)
        return

    # CONSTANTS ##################################################################################################
    @staticmethod
    def __version__():
        return "1.0.0"

    @staticmethod
    def __file__():
        return "SPK_UniversalTimestamp\\Moment_aUniversal.py"

    # UnivMoment CONSTRUCTOR ###################################################################################
    def __init__(
        self,
        rd_day: str | int | Decimal,
        rd_time: Optional[tuple[int, int, Decimal]] = (0, 0, Decimal('0.0')),
        precision: Optional[Precision] = Precision.SECOND,
        description: Optional[str] = None
    ):
        """
        Initialize Universal Moment

        Args:
            rd_day (str | int | Decimal]): Rata Die
            td_time (Optional[tuple[int, int, Decimal]]): (hour, minute, second)
            precision (Optional[Precision]): Precision level of the moment
        """
        if isinstance(rd_day, int):
            self.rd_day = Decimal(rd_day)
        elif isinstance(rd_day, Decimal):
            self.rd_day = rd_day
        elif isinstance(rd_day, str):
            self.rd_day = Decimal(rd_day)
        else:
            raise TypeError("RD must be of type str, int, or Decimal")
        if isinstance(rd_time, tuple) and len(rd_time) == 3:
            hour, minute, second = rd_time
            if not (isinstance(hour, int) and 0 <= hour <= 23):
                raise ValueError("Hour must be an integer between 0 and 23")
            if not (isinstance(minute, int) and 0 <= minute <= 59):
                raise ValueError("Minute must be an integer between 0 and 59")
            if not (isinstance(second, (int, Decimal)) and Decimal('0') <= Decimal(second) < Decimal('60')):
                raise ValueError("Second must be an integer or Decimal between 0 and less than 60")
            self.rd_time = (hour, minute, Decimal(second))
        else:
            raise TypeError("rd_time must be a tuple of (hour : int, minute : int, second : int | Decimal)")
        self.precision = precision
        if description and isinstance(description, str):
            self.description = description
        return
    
    # Support for JSON serialization
    def to_dict(self) -> dict:
        """
        Convert the UnivMoment to a dictionary for JSON serialization.

        Returns:
            dict: Dictionary representation of the UnivMoment
        """
        data = {
            "rd_day": str(self.rd_day),
            "rd_time": (self.rd_time[0], self.rd_time[1], str(self.rd_time[2])),
            "precision": self.precision.name,
        }
        if hasattr(self, 'description'):
            data["description"] = self.description
        return data
    @staticmethod
    def from_dict(data: dict) -> "UnivMoment":
        """
        Create a UnivMoment from a dictionary.

        Args:
            data (dict): Dictionary representation of the UnivMoment
        Returns:
            UnivMoment: Created UnivMoment object
        """
        rd_day = Decimal(data["rd_day"])
        rd_time = (data["rd_time"][0], data["rd_time"][1], Decimal(data["rd_time"][2]))
        precision = Precision[data["precision"]]
        description = data.get("description", None)
        return UnivMoment(rd_day, rd_time, precision, description)



    def to_StdLexicalKey(self) -> str:
        """
        Convert the UnivMoment to a standardized lexical key for sorting and comparison.

        Returns:
            str: Standardized lexical key representing the UnivMoment
        """
        # Format rd_day with leading zeros and sign for proper lexical sorting
        if self.rd_day == Decimal("-Infinity"):
            rd_day_off = 0
        else:
            rd_day_int = int(self.rd_day )
            rd_day_off = rd_day_int + 100_000_000_000_000_000  # Offset to ensure positive and fixed width
        rd_day_str = f"{rd_day_off:018d}"
        rd_time_str = f"H{self.rd_time[0]:02d}M{self.rd_time[1]:02d}S{self.rd_time[2]:021.18f}"
        rd_lex_str = f"univRD{rd_day_str}{rd_time_str}UTC:{PrecisionAtts[self.precision]['level']:02d}"
        return rd_lex_str
    
    @staticmethod
    def from_StdLexicalKey(lex_key: str) -> "UnivMoment":
        """
        Create a UnivMoment from a standardized lexical key.

        Args:
            lex_key (str): Standardized lexical key representing the UnivMoment
        """
        pattern = r"univRD(?P<rd_day>\d{18})H(?P<hour>\d{2})M(?P<minute>\d{2})S(?P<second>\d{2}\.\d{18})UTC:(?P<precision>\d{2})$"
        match = re.match(pattern, lex_key)
        if not match:
            raise ValueError("Invalid lexical key format for UnivMoment")
        rd_day = Decimal(match.group("rd_day"))
        if rd_day <= 0:
            rd_day = Decimal('-infinity')
        else:
            rd_day = rd_day - 100_000_000_000_000_000
        hour = int(match.group("hour"))
        minute = int(match.group("minute"))
        second = Decimal(match.group("second"))
        precision_level = int(match.group("precision"))
        precision = None
        last_prec = Precision.BILLION_YEARS
        for prec in Precision:
            if PrecisionAtts[prec]['level'] == precision_level:
                precision = prec
                break
            elif PrecisionAtts[prec]['level'] > precision_level:
                precision = last_prec
                break
            last_prec = prec
        if precision is None:
            precision = Precision.ATTOSECOND
        return UnivMoment(rd_day, (hour, minute, second), precision)
    
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
    
    def rd_moment(self) -> tuple[Decimal, tuple[int, int, Decimal]]:
        """
        Get the Rata Die moment as a tuple of (rd_day, (hour, minute, second)).

        Returns:
            tuple: (rd_day, (hour, minute, second))
        """
        return (self.rd_day, self.rd_time)
    def __getitem__(self, key):
        if isinstance(key, int):
            if key == 0:
                return self.rd_day
            elif key == 1:
                return self.rd_time[0]
            elif key == 2:
                return self.rd_time[1]
            elif key == 3:
                return self.rd_time[2]
            else:
                raise IndexError("Index out of range for UnivMoment. Use 0 - day, 1 - hour, 2 - minute, 3 - second.")
        elif isinstance(key, str):
            if key == 'day':
                return self.rd_day
            elif key == 'hour':
                return self.rd_time[0]
            elif key == 'minute':
                return self.rd_time[1]
            elif key == 'second':
                return self.rd_time[2]
            else:
                raise KeyError("Key not found for UnivMoment. Use 'day', 'hour', 'minute', or 'second'.")
        else:
            raise TypeError("Key must be an integer index or string key for UnivMoment.")
        
    def _get_time_period(self, other) -> tuple[Decimal, int, int, Decimal]:
        if  (    isinstance(other, tuple) 
            and len(other) == 4
            and isinstance(other[0], (int, Decimal))
            and isinstance(other[1], int)
            and isinstance(other[2], int)
            and isinstance(other[3], (int, Decimal))):
            return other
        else:
            raise TypeError("Time period must be a tuple of (day : Decimal, hour : int, minute : int, second : Decimal)")
    @staticmethod    
    def _add_sub(x : tuple[Decimal, int, int, Decimal] | "UnivMoment",
            s : int, 
            y : tuple[Decimal, int, int, Decimal] | "UnivMoment")-> tuple[Decimal, int, int, Decimal]:
        """
        Add(s=1)/Subtract(s=-1) two time deltas represented as tuple. Indexing allows UnivMoment to look like a tuple.
        Args:
            x (tuple[Decimal, int, int, Decimal] | UnivMoment): First time delta/point in time
            s (int): Sign for addition (1) or subtraction (-1)
            y (tuple[Decimal, int, int, Decimal] | UnivMoment): Second time delta/point in time
            Returns:
            tuple[Decimal, int, int, Decimal]: Resulting time period (days, hours, minutes, seconds)
            NOTE : Not all combinations are valid. The valid ones are implemented in the _add__ and _sub__ methods.
        """
        carry = Decimal(0)
        base = (Decimal('+infinity'), 24, 60, Decimal('60'))
        result = [Decimal(0), 0, 0, Decimal(0)]
        for i in range(3, -1, -1):
            sum = x[i] + s*y[i] + carry
            if i > 0 :
                carry = 0
                if sum >= base[i]:
                    carry = floor(sum / base[i])
                    sum = sum - carry * base[i]
                elif sum < 0:
                    carry = floor(sum / base[i])
                    sum = sum - carry * base[i]
            result[i] = sum
        return (result[0], int(result[1]), int(result[2]), result[3])
    
    def __sub__(self, other) -> Decimal:
        """
        Subtract two UnivMoment objects to get the difference
        Subtract a time delta (days, hours, minutes, seconds) from a UnivMoment
        """
        if isinstance(other, self.__class__):
            # tuple = __class__ __sub__ __class__
            result = self._add_sub(self, -1, other)
            return result
        other = self._get_time_period(other)
        # __class__ = __class__ __sub__ tuple
        result = self._add_sub(self, -1, other)
        return UnivMoment(result[0], (result[1], result[2], result[3]), self.precision, getattr(self, 'description', None))
    
    def __add__(self, other : tuple[Decimal, int, int, Decimal]) -> "UnivMoment":
        """Add a time delta (days, hours, minutes, seconds) to the UnivMoment"""
        other = self._get_time_period(other)
        # __class__ = __class__ __add__ tuple
        result = self._add_sub(self, 1, other)
        return UnivMoment(result[0], (result[1], result[2], result[3]), self.precision, getattr(self, 'description', None))
    
    # COMPARISON METHODS ##########################################################################
    def __lt__(self, other) -> bool:
        """Less than comparison for sorting"""
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.rd_moment() < other.rd_moment()

    def __le__(self, other) -> bool:
        """Less than or equal comparison"""
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.rd_moment() <= other.rd_moment()

    def __gt__(self, other) -> bool:
        """Greater than comparison"""
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.rd_moment() > other.rd_moment()

    def __ge__(self, other) -> bool:
        """Greater than or equal comparison"""
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.rd_moment() >= other.rd_moment()

    def __eq__(self, other) -> bool:
        """Equality comparison"""
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.rd_moment() == other.rd_moment()
    
    def __hash__(self) -> int:
        """Hash function for UnivMoment"""
        return hash(self.rd_moment())

    def __ne__(self, other) -> bool:
        """Not equal comparison"""
        if not isinstance(other, self.__class__):
            return NotImplemented
        return not self.__eq__(other)

    # FORMATTING/PRESENTATION METHODS ########################################################################
    def __str__(self) -> str:
        """ Generate a visual representative string for UnivMoment."""
        return self.format_signature()

    def __repr__(self) -> str:
        """ Generate repr string for UnivMoment."""
        return f"UnivMoment(Decimal({repr(str(self.rd_day))}), {self.rd_time}, {self.precision}, description={repr(getattr(self, 'description', None))})"

    @staticmethod
    def eval_repr(repr_str) -> "UnivMoment":
        """Recreate a UnivMoment from its repr string."""
        recreated = eval(repr_str, {'UnivMoment' : UnivMoment, 'Decimal' : Decimal, 'Precision' : Precision}) 
        return recreated

    def format(self, format_ext : str) -> str:
        """
        Format the moment using an extended format string.

        Args:
            format_ext (str): Extended format string
            Allows specifying calendar and time zone in the format string
            Example: '^cal:GREGORIAN, tz:America/New_York, lng:en ::%Y-%m-%d %H:%M
        Returns:
            str: Formatted timestamp string
        """
        prefix_left = format_ext.find("{")
        prefix_right = format_ext.find("}")
        if prefix_left >=0 and prefix_right > prefix_left:
            prefix = format_ext[prefix_left + 1 : prefix_right].split(",")
            format_str = format_ext[prefix_right + 1 :]
        else:
            prefix = []
            format_str = format_ext
        calendar_str = 'GREGORIAN'  # Default calendar
        tz_str = 'UTC'  # Default time zone
        lang_code = 'en' # Default language
        for pair in prefix:
            if len(pair) < 3:
                continue
            tag, value = pair.split(":")
            if tag.lower() == "cal":
                calendar_str = value.upper()
            elif tag.lower() == "tz":
                tz_str = value
            elif tag.lower() == "lng":
                lang_code = value
            else:
                raise ValueError(f"Unknown prefix tag '{tag}' in format string.")
        # Map calendar string to Calendar enum
        try:
            calendar = Calendar[calendar_str]
        except KeyError:
            raise ValueError(f"Unknown calendar '{calendar_str}' in format string.")
        # Validate time zone and language code
        try:
            ZoneInfo(tz_str)
        except ZoneInfoNotFoundError:
            raise ValueError(f"Unknown time zone '{tz_str}' in format string.")      
        if not langcodes.tag_is_valid(lang_code):
            raise ValueError(f"Invalid language code '{lang_code}' in format string.")
        
        return self.present(calendar, format_str, tz_str, lang_code)
    
    def present(self, calendar: Calendar, format: str, tz = 'UTC', language: str = 'en') -> str:
        """
        Present the moment in a specific calendar format.

        Args:
            calendar (Calendar): Calendar system to use for presentation
            format (str): Format string for presentation
            language (str): Language for presentation
        Returns:
            str: Formatted timestamp string
        """
        if calendar == Calendar.GEOLOGICAL:
            from .Moment_bPresent_Geological import Present_Geological
            return Present_Geological(self)._format(format, language)
        elif self.rd_day < -9999*Decimal('365.25'):
            from .Moment_bPresent_Geological import Present_Geological
            return Present_Geological(self)._format("%y %O", language)
        elif calendar == Calendar.GREGORIAN:
            from .Moment_cPresent_Gregorian import Present_Gregorian
            return Present_Gregorian(self, tz)._format(format, language)
        elif calendar == Calendar.JULIAN:
            from .Moment_cPresent_Julian import Present_Julian
            return Present_Julian(self, tz)._format(format, language)
        elif calendar == Calendar.HEBREW:
            from .Moment_cPresent_Hebrew import Present_Hebrew
            return Present_Hebrew(self, tz)._format(format, language)
        elif calendar == Calendar.CHINESE:
            from .Moment_cPresent_Chinese import Present_Chinese
            return Present_Chinese(self, tz)._format(format, language)
        else:
            raise NotImplementedError(
                f"Calendar {calendar} not implemented in UnivMoment.present()"
            )

    def format_signature(self) -> str:
        """
        Format the complete timestamp for display.
        """
        if hasattr(self, 'description') and len(self.description) > 0:
            signature = f"{self.description} rd: {self.rd_moment()} pr: {self.precision.name}"
        else:
            signature = f"RD: {self.rd_moment()} pr: {self.precision.name}"
        return signature
        
        
    # PRESENTATION LAYER CLASS ##################################################################
    #   UnivMoment captures a point in time.  Calendars and the presentation of points in time are
    #   handled in a hierarchy of subclasses of the imbedded class moment_calendars
    class Presentation:
        """Abstract Base class for calendar-specific moment representations."""
        # moment_calendars CONSTRUCTOR ####################################################################
        def __init__(self, calendar : Calendar, moment: "UnivMoment", year : Decimal):
            self.calendar = calendar
            self.moment = moment
            self.precision = moment.precision
            self.year = year
            return

        # Presentation methods
        def _format(self, format: str, language: str = "en") -> str:
            """
            Format the timestamp using a custom format string.
            This is a simplified version and does not support all Python strftime features.

            Format specifier is a string split on % into text and insert segments
            1. Text segments are copied as is
            2. Insert segments are processed according to their type and modifiers
                a. For type modifier see Moment Geological and Moment Calendars
            """
            # format string
            fmt = ""
            # capture lead text
            for i in range(len(format)):
                if format[i] == "%":
                    break
                fmt += format[i]
                continue
            # split remainder into insert segments
            segments = format[i + 1 :].split("%")
            for segment in segments:
                # If the segment is empty, skip it
                if len(segment) == 0:
                    continue
                # get segment type and any modifiers
                seg_remainder_start = 1
                seg_eliminate_leading_zero = False
                seg_frac_digits = None
                seg_type = segment[0]
                if seg_type == "#":
                    seg_eliminate_leading_zero = True
                    if len(segment) > 1:
                        seg_type = segment[1]
                        seg_remainder_start = 2
                if seg_type == 'f':
                    if len(segment) > 1 and segment[1].isdigit():
                        # fractional seconds precision
                        frac_digits = 0
                        for i in range(1, len(segment)):
                            if not segment[i].isdigit():
                                break
                            frac_digits = frac_digits*10 + int(segment[i])
                        seg_frac_digits = frac_digits
                        seg_remainder_start = i+1
                # process the segment
                if seg_type in ['K']:
                    fmt += CalendarAtts[language][self.calendar]['name']
                elif seg_type in ['k']:
                    fmt += CalendarAtts[language][self.calendar]['abbrv']
                else:
                    fmt += self._format_segment({'type' : seg_type, 'eliminate_leading_zero' : seg_eliminate_leading_zero, 'frac_digits' : seg_frac_digits}, language)
                for i in range(seg_remainder_start, len(segment)):
                    fmt += segment[i]

            return fmt
        @abstractmethod
        def _format_segment(self, segment: dict, language: str) -> str:
            """
            Format a single segment based on the segment information and language.
            This method should be implemented in subclasses for specific calendar systems.
            """
            raise NotImplementedError(
                "Subclasses must implement _format_segment() method"
            )


    # END PRESENTATION LAYER CLASS ##############################################################

    # CONSTRUCTION LAYER FUNCTIONS ##########################################################
    # The construction layer allows for create of UnivMoment from various calendar systems
    # Each calendar system will have its own construction function 
    # Validation method for constructor arguments
    @staticmethod
    def _init_validate_constructor_args(constructor_args : list, num_required, args: list, init_precision) -> tuple[dict, Precision]:
        if len(args) < num_required:
            expected = ', '.join(arg[0] for arg in constructor_args[:num_required])
            raise ValueError(f"Too few arguments: expected at least {num_required} ({expected})")
        if len(args) > len(constructor_args):
            raise ValueError(f"Too many arguments: expected at most {len(constructor_args)}")

        arg_context = {}
        parm_precision = None
        for i, arg in enumerate(args):
            if arg is None:
                break
            name, types, is_valid_fn, parm_precision= constructor_args[i]
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
        if len(args) < len(constructor_args):
            for trailing in args[len(args):]:
                if trailing is not None:
                    raise ValueError("Parameters must be contiguous with no gaps")
        # Set trailing parameters to None
        if len(arg_context) < len(constructor_args):
            for name, _, _, _ in constructor_args[len(arg_context):]:
                arg_context[name] = None
        #self._cnst_validated = True
        return arg_context, precision
    
    # CONSTRUCT from GEOLOGICAL date
    def from_geological(
        years_ago: Union[int, float, str, Decimal],
        precision: Optional[Precision] = Precision.MILLION_YEARS,
        description: Optional[str] = None,
    ):
        """Create geological timestamp (years ago)"""
        if isinstance(years_ago, str):
            years_ago = -abs(Decimal(years_ago))
        elif isinstance(years_ago, (int, float)):
            years_ago = -abs(Decimal(str(years_ago)))
        elif isinstance(years_ago, Decimal):
            years_ago = -abs(years_ago)
        else:
            raise ValueError("years_ago must be an integer, float or decimal string")
        if years_ago != Decimal("-Infinity"):
            if (
                precision is None
                or PrecisionAtts[precision]["level"]
                > PrecisionAtts[Precision.YEAR]["level"]
            ):
                raise ValueError(
                    f"Invalid precision {precision} for geological time. Must be YEAR or higher."
                )
            power = PrecisionAtts[precision]["power"]
            years_ago *= Decimal("1e" + str(power))
            # Scale to the correct precision
            years_ago = int(years_ago)
        else:
            precision = Precision.YEAR
        """
        Convert the geological timestamp to Rata Die (fixed day number).
        For geological time, we assume a constant year length of 365.25 days.
        """
        days_ago = years_ago * Decimal('365.25')
        return UnivMoment(days_ago, precision=precision, description=description)
    # CONSTRUCT beginning of time
    @staticmethod
    def beginning_of_time() -> "UnivMoment":
        """Get the beginning of time in the Gregorian calendar."""
        return UnivMoment.from_geological('-Infinity')

    # CONSTRUCT from GREGORIAN date
    @staticmethod
    def _gregorian_days_in_month(year: int, month: int) -> int:
        num_days = gregorian_MONTH_ATTS['en'][month]['days']
        if month == 2 and is_gregorian_leap_year(year):
            return 29
        return num_days
    # Each tuple: (slot name, allowed_types, valid_function, precision_enum)
    _gregorian_CNST_ARGS = [
        ("year",   (int,), lambda arg, *_: (-9999 <= arg <= 9999), Precision.YEAR),
        ("month",  (int,), lambda arg, *_: (1 <= arg <=12), Precision.MONTH),
        ("day",    (int,), lambda arg, v: (1 <= arg <= UnivMoment._gregorian_days_in_month(v['year'], v['month'])),  Precision.DAY),
        ("hour",   (int,), lambda arg, *_: (0 <= arg <= 23), Precision.HOUR),
        ("minute", (int,), lambda arg, *_: (0 <= arg <= 59), Precision.MINUTE),
        ("second", (Union[int, Decimal],), lambda arg, *_: (Decimal("0") <= arg < Decimal("60")), Precision.SECOND),
    ]
    @staticmethod
    def from_gregorian(
        *args,
        precision: Optional[Precision] = None,
        description: Optional[str] = None
    ) -> "UnivMoment":
        """
        Construct a UnivMoment from Gregorian date components.

        Args:
            *args: Variable length argument list for year, month, day, hour, minute, second
            precision (Optional[Precision]): Precision level of the moment

        Returns:
            UnivMoment: Constructed UnivMoment object
        """
        # Validate constructor arguments
        arg_context, parm_precision = UnivMoment._init_validate_constructor_args(
            UnivMoment._gregorian_CNST_ARGS,
            1,  # Minimum required arguments: year
            args,
            precision
        )
        # Convert to Rata Die moment
        rd_day = rd_from_gregorian(arg_context['year'], arg_context['month'], arg_context['day'])
        rd_time = (
            arg_context['hour'] if arg_context['hour'] is not None else 0,
            arg_context['minute'] if arg_context['minute'] is not None else 0,
            arg_context['second'] if arg_context['second'] is not None else Decimal('0'),
        )
        return UnivMoment(rd_day, rd_time, parm_precision, description=description)
    
    # CONSTRUCT from JULIAN date
    @staticmethod
    def _julian_days_in_month(year: int, month: int) -> int:
        num_days = julian_MONTH_ATTS['en'][month]['days']
        if month == 2 and is_julian_leap_year(year):
            return 29
        return num_days
    # Each tuple: (slot name, allowed_types, valid_function, precision_enum)
    _julian_CNST_ARGS = [
        ("year",   (int,), lambda arg, *_: (-9999 <= arg <= 9999), Precision.YEAR),
        ("month",  (int,), lambda arg, *_: (1 <= arg <=12), Precision.MONTH),
        ("day",    (int,), lambda arg, v: (1 <= arg <= UnivMoment._gregorian_days_in_month(v['year'], v['month'])),  Precision.DAY),
        ("hour",   (int,), lambda arg, *_: (0 <= arg <= 23), Precision.HOUR),
        ("minute", (int,), lambda arg, *_: (0 <= arg <= 59), Precision.MINUTE),
        ("second", (Union[int, Decimal],), lambda arg, *_: (Decimal("0") <= arg < Decimal("60")), Precision.SECOND),
    ]
    @staticmethod
    def from_julian(
        *args,
        precision: Optional[Precision] = None,
        description: Optional[str] = None,
    ) -> "UnivMoment":
        """
        Construct a UnivMoment from Julian date components.

        Args:
            *args: Variable length argument list for year, month, day, hour, minute, second
            precision (Optional[Precision]): Precision level of the moment
        Returns:
            UnivMoment: Constructed UnivMoment object
        """
        # Validate constructor arguments
        arg_context, parm_precision = UnivMoment._init_validate_constructor_args(
            UnivMoment._julian_CNST_ARGS,
            1,  # Minimum required arguments: year
            args,
            precision
        )
        # Convert to Rata Die moment
        rd_day = rd_from_julian(arg_context['year'], arg_context['month'], arg_context['day'])
        rd_time = (
            arg_context['hour'] if arg_context['hour'] is not None else 0,
            arg_context['minute'] if arg_context['minute'] is not None else 0,
            arg_context['second'] if arg_context['second'] is not None else Decimal('0'),
        )
        return UnivMoment(rd_day, rd_time, parm_precision, description=description)
    
    # CONSTRUCT from HEBREW date
    @staticmethod
    # Each tuple: (slot name, allowed_types, valid_function, precision_enum)
    def hebrew_last_month_of_year(year: int) -> int:
        return last_hebrew_month_of_year(year)
    def hebrew_last_day_of_month(year: int, month: int) -> int:
        return last_day_of_hebrew_month(year, month)
    _hebrew_CNST_ARGS = [
        ("year",   (int,), lambda arg, *_: (1 <= arg <= 9999), Precision.YEAR),
        ("month",  (int,), lambda arg, v: (1 <= arg <= UnivMoment.hebrew_last_month_of_year(v['year'])), Precision.MONTH),
        ("day",    (int,), lambda arg, v: (1 <= arg <= UnivMoment.hebrew_last_day_of_month(v['year'], v['month'])),  Precision.DAY),
        ("hour",   (int,), lambda arg, *_: (0 <= arg <= 23), Precision.HOUR),
        ("minute", (int,), lambda arg, *_: (0 <= arg <= 59), Precision.MINUTE),
        ("second", (Union[int, Decimal],), lambda arg, *_: (Decimal("0") <= arg < Decimal("60")), Precision.SECOND),
    ]
    def from_hebrew(
        *args,
        precision: Optional[Precision] = None,
        description: Optional[str] = None,
    ) -> "UnivMoment":
        """
        Construct a UnivMoment from Hebrew date components.

        Args:
            *args: Variable length argument list for year, month, day, hour, minute, second
            precision (Optional[Precision]): Precision level of the moment
        Returns:
            UnivMoment: Constructed UnivMoment object
        """
        # Validate constructor arguments
        arg_context, parm_precision = UnivMoment._init_validate_constructor_args(
            UnivMoment._hebrew_CNST_ARGS,
            1,  # Minimum required arguments: year
            args,
            precision
        )
        # Convert to Rata Die moment
        rd_day = rd_from_hebrew(arg_context['year'], arg_context['month'], arg_context['day'])
        rd_time = (
            arg_context['hour'] if arg_context['hour'] is not None else 0,
            arg_context['minute'] if arg_context['minute'] is not None else 0,
            arg_context['second'] if arg_context['second'] is not None else Decimal('0'),
        )
        return UnivMoment(rd_day, rd_time, parm_precision, description=description)
    
    # CONSTRUCT from CHINESE date
    @staticmethod
    def _chinese_days_in_month(cycle: int, year: int, month: int, leap: bool) -> int:
        marker = rd_from_chinese(cycle, year, month, leap, 1)
        new_moon_t0 = floor(chinese_new_moon_before(marker))
        new_moon_t1 = floor(chinese_new_moon_on_or_after(marker))
        num_days = new_moon_t1 - new_moon_t0
        return num_days
    @staticmethod
    def _chinese_validate_month(arg, context):
        if isinstance(arg, int):
            return (1 <= arg <= 12)
        elif isinstance(arg, tuple):
            return (1 <= arg[0] <= 12) and isinstance(arg[1], bool)
        return False
    # Each tuple: (slot name, allowed_types, valid_function, precision_enum)
    _chinese_CNST_ARGS = [
        ("cycle",  (int,), lambda arg, *_: (1 <= arg <= 99999), None),
        ("year",   (int,), lambda arg, *_: (1 <= arg <= 60), Precision.YEAR),
        ("month",  (int, tuple), lambda arg, context : UnivMoment._chinese_validate_month(arg, context), Precision.MONTH),
        ("day",    (int,), 
            lambda arg, v: (
                1 <= arg <=
                UnivMoment._chinese_days_in_month(
                    v['cycle'], 
                    v['year'], 
                    v['month'][0] if isinstance(v['month'], tuple) else v['month'], 
                    v['month'][1] if isinstance(v['month'], tuple) else False
                    )
                ), 
            Precision.DAY),
        ("hour",   (int,), lambda arg, *_: (0 <= arg <= 23), Precision.HOUR),
        ("minute", (int,), lambda arg, *_: (0 <= arg <= 59), Precision.MINUTE),
        ("second", (Union[int, Decimal],), lambda arg, *_: (Decimal("0") <= arg < Decimal("60")), Precision.SECOND),
    ]

    @staticmethod
    def from_chinese(
        *args,
        precision: Optional[Precision] = None,
        description: Optional[str] = None,
    ) -> "UnivMoment":
        """
        Construct a UnivMoment from Chinese date components.

        Args:
            *args: Variable length argument list for cycle, year, month, day, hour, minute, second
            precision (Optional[Precision]): Precision level of the moment
        Returns:
            UnivMoment: Constructed UnivMoment object
        """
        # Validate constructor arguments
        arg_context, parm_precision = UnivMoment._init_validate_constructor_args(
            UnivMoment._chinese_CNST_ARGS,
            2,  # Minimum required arguments: cycle, year
            args,
            precision
        )
        cycle = arg_context['cycle']
        year = arg_context['year']
        month, leap = (arg_context['month'][0], arg_context['month'][1]) if isinstance(arg_context['month'], tuple) else (arg_context['month'], False)
        # Convert to Rata Die moment
        rd_day = rd_from_chinese(cycle, year, month, leap, arg_context['day'])
        rd_time = (
            arg_context['hour'] if arg_context['hour'] is not None else 0,
            arg_context['minute'] if arg_context['minute'] is not None else 0,
            arg_context['second'] if arg_context['second'] is not None else Decimal('0'),
        )
        return UnivMoment(rd_day, rd_time, parm_precision, description=description)
    
    # CONSTRUCT now moment from system Datetime.now(timezone.utc)
    @staticmethod
    def now() -> "UnivMoment":
        """
        Construct a UnivMoment representing the current system time.

        Returns:
            UnivMoment: Constructed UnivMoment object
        """
        now_utc = datetime.now(timezone.utc)
        rd_day = rd_from_gregorian(now_utc.year, now_utc.month, now_utc.day)
        rd_time = (
            now_utc.hour,
            now_utc.minute,
            Decimal(str(now_utc.second)) + (Decimal(str(now_utc.microsecond)) / Decimal('1_000_000'))
        )
        description = now_utc.strftime("now %Y-%m-%dT%H:%M:%S.%fZ")
        return UnivMoment(rd_day, rd_time, Precision.MICROSECOND, description=description)
    
    # CONSTRUCT moment from system datetime
    @staticmethod
    def from_datetime(dt : datetime, description=None) -> "UnivMoment":
        """
        Construct a UnivMoment representing the current system time.

        Returns:
            UnivMoment: Constructed UnivMoment object
        """
        utc_dt = dt.astimezone(timezone.utc)
        rd_day = rd_from_gregorian(utc_dt.year, utc_dt.month, utc_dt.day)
        rd_time = (
            utc_dt.hour,
            utc_dt.minute,
            Decimal(str(utc_dt.second)) + (Decimal(str(utc_dt.microsecond)) / Decimal('1_000_000'))
        )
        return UnivMoment(rd_day, rd_time, Precision.MICROSECOND, description=description)

    # CONSTRUCT moment from Julian Day Number
    @staticmethod
    def from_julian_day_number(
        jdn: int | Decimal | float | str,
        description: str = None
    ) -> "UnivMoment":
        """Create from Julian Day Number (JDN)"""
        if isinstance(jdn, str):
            jdn = Decimal(jdn)
        elif isinstance(jdn, int):
            jdn = Decimal(jdn)
        elif isinstance(jdn, float):
            jdn = Decimal(str(jdn))
        elif isinstance(jdn, Decimal):
            pass
        else:
            raise ValueError("jdn must be an integer, decimal, float or string")
        rd_day = jdn - Decimal(1721424.5)
        return UnivMoment(rd_day, precision=Precision.HOUR, description=description)
    # CONSTRUCT moment from UNIX timestamp
    @staticmethod
    def from_unix_timestamp( 
        timestamp: int,
        description: str = None
    ):
        """Create from Unix timestamp with nanosecond precision"""
        # Process the integer part to year, month, day, hour, minute, second
        date_ts = int(timestamp)
        moment_from_unix = Epoch_rd['unix'] + date_ts // (24 * 60 * 60)
        year, month, day = gregorian_from_rd(moment_from_unix)
        time_ts = date_ts % (24 * 60 * 60)
        hour_ts = time_ts // 3600
        time_ts %= 3600
        min_ts = time_ts // 60
        time_ts %= 60
        sec_ts = time_ts
        timestamp = Decimal(str(timestamp)).quantize(Decimal('1e-9'), rounding=ROUND_DOWN)
        frac_ts = timestamp % 1
        sec_frac_ts = Decimal(sec_ts) + frac_ts
        return UnivMoment.from_gregorian(
            year, month, day, hour_ts, min_ts, sec_frac_ts,
            precision=Precision.NANOSECOND,
            description=description,
        )
    
    # CONSTRUCT moment from ISO 8601 patterns
    _ISO_8601_PATTERNS = [
        # ISO 8601 with time
        (
            r"(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})\.(\d{3})",
            lambda m, description="" : UnivMoment.from_gregorian(
                int(m.group(1)),
                int(m.group(2)),
                int(m.group(3)),
                int(m.group(4)),
                int(m.group(5)),
                Decimal(f"{m.group(6)}.{m.group(7)}"),
                precision=Precision.MILLISECOND,
                description=description,
            ),
        ),
        (
            r"(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})",
            lambda m, description="" : UnivMoment.from_gregorian(
                int(m.group(1)),
                int(m.group(2)),
                int(m.group(3)),
                int(m.group(4)),
                int(m.group(5)),
                int(m.group(6)),
                precision=Precision.SECOND,
                description=description,
            ),
        ),
        # Space-separated datetime
        (
            r"(\d{4})-(\d{2})-(\d{2})\s+(\d{2}):(\d{2}):(\d{2})\.(\d{3})",
            lambda m, description="" : UnivMoment.from_gregorian(
                int(m.group(1)),
                int(m.group(2)),
                int(m.group(3)),
                int(m.group(4)),
                int(m.group(5)),
                Decimal(f"{m.group(6)}.{m.group(7)}"),
                precision=Precision.MILLISECOND,
                description=description,
            ),
        ),
        (
            r"(\d{4})-(\d{2})-(\d{2})\s+(\d{2}):(\d{2}):(\d{2})",
            lambda m, description="" : UnivMoment.from_gregorian(
                int(m.group(1)),
                int(m.group(2)),
                int(m.group(3)),
                int(m.group(4)),
                int(m.group(5)),
                int(m.group(6)),
                precision=Precision.SECOND,
                description=description,
            ),
        ),
    ]

    # Geological time patterns
    _GEOLOGICAL_PATTERNS = [
        (
            r"(\d+\.?\d*)\s*BYA",
            lambda m, description="": UnivMoment.from_geological(
                Decimal(m.group(1)),
                precision=Precision.BILLION_YEARS,
                description=description,
            ),
        ),
        (
            r"(\d+\.?\d*)\s*MYA",
            lambda m, description="": UnivMoment.from_geological(
                Decimal(m.group(1)),
                precision=Precision.MILLION_YEARS,
                description=description,
            ),
        ),
        (
            r"(\d+\.?\d*)\s*KYA",
            lambda m, description="" : UnivMoment.from_geological(
                Decimal(m.group(1)),
                precision=Precision.THOUSAND_YEARS,
                description=description,
            ),
        ),
    ]

    # Human calendar patterns
    _HUMAN_CALENDAR_PATTERNS = [
        # Gregorian
        (
            r"(\d{1,4})\s*BCE",
            lambda m, description="" : UnivMoment.from_gregorian(
                -int(m.group(1)), 
                None, 
                None,
                precision=Precision.YEAR,
                description=description,
            ),
        ),
        (
            r"(\d{1,4})\s*BCE-(\d{1,2})",
            lambda m, description="" : UnivMoment.from_gregorian(
                -int(m.group(1)), 
                int(m.group(2)), 
                None,
                precision=Precision.MONTH,
                description=description,
            ),
        ),
        (
            r"(\d{1,4})\s*BCE-(\d{1,2})-(\d{1,2})",
            lambda m, description="" : UnivMoment.from_gregorian(
                -int(m.group(1)), 
                int(m.group(2)), 
                int(m.group(3)),
                precision=Precision.DAY,
                description=description,
            ),
        ),
        (
            r"([+-]?\d{1,4})-(\d{1,2})-(\d{1,2})",
            lambda m, description="" : UnivMoment.from_gregorian(
                int(m.group(1)), 
                int(m.group(2)), 
                int(m.group(3)),
                precision=Precision.DAY,
                description=description,
            ),
        ),
        (
            r"([+-]?\d{1,4})-(\d{1,2})",
            lambda m, description="" : UnivMoment.from_gregorian(
                int(m.group(1)), 
                int(m.group(2)), 
                None,
                precision=Precision.MONTH,
                description=description,
            ),
        ),
        (
            r"([+-]?\d{1,4})",
            lambda m, description="" : UnivMoment.from_gregorian(
                int(m.group(1)), 
                None, 
                None,
                precision=Precision.YEAR,
                description=description,
            ),
        ),
        # Julian calendar
        (
            r"(\d{1,4})\s*bc-(\d{1,2})-(\d{1,2})",
            lambda m, description="" : UnivMoment.from_julian(
                -int(m.group(1)), 
                int(m.group(2)), 
                int(m.group(3)),
                description=description,
            ),
        ),
        (
            r"(\d{1,4})\s*bc-(\d{1,2})",
            lambda m, description="" : UnivMoment.from_julian(
                -int(m.group(1)), 
                int(m.group(2)), 
                None,
                description=description,
            ),
        ),
        (
            r"(\d{1,4})\s*bc",
            lambda m, description="" : UnivMoment.from_julian(
                -int(m.group(1)), 
                None, 
                None,
                description=description,
            ),
        ),
        (
            r"(\d{1,4})\s*bc-(\d{1,2})-(\d{1,2})\s*(OS|JC)",
            lambda m, description="" : UnivMoment.from_julian(
                -int(m.group(1)), 
                int(m.group(2)), 
                int(m.group(3)),
                description=description,
            ),
        ),
        (
            r"(\d{1,4})\s*bc-(\d{1,2})\s*(OS|JC)",
            lambda m, description="" : UnivMoment.from_julian(
                -int(m.group(1)), 
                int(m.group(2)), 
                None,
                description=description,
            ),
        ),
        (
            r"(\d{1,4})\s*bc\s*(OS|JC)",
            lambda m, description="" : UnivMoment.from_julian(
                -int(m.group(1)), 
                None, 
                None,
                description=description,
            ),
        ),
        (
            r"([+-]?\d{1,4})-(\d{1,2})-(\d{1,2})\s*(OS|JC)",
            lambda m, description="" : UnivMoment.from_julian(
                int(m.group(1)), 
                int(m.group(2)), 
                int(m.group(3)),
                description=description,
            ),
        ),
        (
            r"([+-]?\d{1,4})-(\d{1,2})\s*(OS|JC)",
            lambda m, description="" : UnivMoment.from_julian(
                int(m.group(1)), 
                int(m.group(2)), 
                None,
                description=description,
            ),
        ),
        (
            r"([+-]?\d{1,4})\s*(OS|JC)",
            lambda m, description="" : UnivMoment.from_julian(
                -int(m.group(1)), 
                None, 
                None,
                description=description,
            ),
        ),
        
        
        # Hebrew calendar
        (
            r"(\d{1,4})\s*AM",
            lambda m, description="" : UnivMoment.from_hebrew(
                int(m.group(1)),
                None, 
                None,
                description=description,
            ),
        ),
        (
            r"(\d{1,4})-(\d+)\s*AM",
            lambda m, description="" : UnivMoment.from_hebrew(
                int(m.group(1)), 
                int(m.group(2)), 
                None,
                description=description,
            ),
        ),
        (
            r"(\d{1,4})-(\d+)-(\d+)\s*AM",
            lambda m, description="" : UnivMoment.from_hebrew(
                int(m.group(1)), 
                int(m.group(2)), 
                int(m.group(3)),
                description=description,
            ),
        ),
    ]

    # Try all pattern groups in order of specificity
    _ALL_PATTERNS = (
        _HUMAN_CALENDAR_PATTERNS
        + _GEOLOGICAL_PATTERNS
        + _ISO_8601_PATTERNS
    )

    @staticmethod
    def from_iso_patterns(timestamp_str: str, accuracy : str = None, description : str = "") -> "UnivMoment":
        """Parse all time scales: geological, astronomical, and human calendars"""
        timestamp_str = timestamp_str.strip()

        for pattern, converter in UnivMoment._ALL_PATTERNS:
            match = re.fullmatch(pattern, timestamp_str)
            if match:
                try:
                    return converter(match, description=description)
                except Exception:
                    continue

        return None



    # END OF CONSTRUCTION LAYER  #############################################################