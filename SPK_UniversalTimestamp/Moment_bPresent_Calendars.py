"""
Moment_bPresent_Calendars — base class for every human-calendar
presentation layer (Gregorian, Julian, Hebrew, Chinese).

**Purpose.**  `Present_Calendars` factors out the plumbing that
every arithmetic-calendar presentation shares:

  * localised day-of-week names (`DAY_OF_THE_WEEK_ATTS`);
  * timezone → UTC-offset resolution with historical awareness
    (`get_utc_offset`);
  * a strftime-like dispatcher (`_format_segment` + the
    `_strftime_year` / `_strftime_month` / `_strftime_day` /
    `_strftime_time` / `_strftime_compound` methods);
  * the abstract seam `_strftime_month_attr` that each calendar
    subclass supplies by consulting its own `Constants_*` table.

**Public surface (star-exported via `__init__.py`).**
    `Present_Calendars` (abstract-ish; instantiated only via the
    `Present_Gregorian` / `_Julian` / `_Hebrew` / `_Chinese`
    subclasses).

**Historical note (embedded in code comments).**  Britain
introduced the first timezone (GMT) in 1847 for train schedules;
North American railroads adopted time zones in November 1883
("the Day of Two Noons").  Any pre-1847 `tz != 'UTC'` argument
returns a timezone offset that is technically anachronistic — the
library trusts the caller to know what they mean.

**Format-directive table.**  A block-comment docstring inside
`Present_Calendars` (immediately before `_format_segment`) lists
every `%X` code recognised by the strftime dispatcher and its
intended output.  Kept there because that dispatcher is the
family contract that all `_strftime_*` helpers implement.

**Not in scope.**  Geological presentation (`Moment_bPresent_Geological`),
UnivMoment core (`UnivMoment`), calendar-specific arithmetic
(`CC02`–`CC19`).

**Change history.**  See `CHANGELOG.md`.
"""

from abc import abstractmethod
from datetime import datetime
from decimal import Decimal

from tzlocal import get_localzone
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from .CC00_Decimal_library import trunc
from .CC02_Gregorian import gregorian_from_rd
from .Constants_aCommon import Calendar, CalendarAtts
from .UnivMoment import UnivMoment, UnivMomPrecision


class Present_Calendars(UnivMoment.Presentation):
    """
    Base class for arithmetic-calendar presentations of a `UnivMoment`.

    Subclasses (`Present_Gregorian`, `Present_Julian`, `Present_Hebrew`,
    `Present_Chinese`) supply their calendar-specific R.D. ↔
    (year, month, day) conversion in `__init__` and implement
    `_strftime_month_attr` to look up month attributes from their
    `Constants_<Calendar>` table.  All other formatting logic —
    day-of-week, time, timezone, compound (`%x`, `%X`) — is
    inherited from this class.

    Attributes:
        tz:          Timezone identifier (IANA name, ``'local'``,
            or ``'UTC'``).
        tz_offset:   `(hours, minutes)` tuple resolved from `tz`.
        calendar:    `Calendar` enum member identifying this system.
        year, month, day, hour, minute, seconds:  Set by subclass
            `__init__` after R.D. decomposition.
    """
    # CONSTANTS #########################################################################
    DAY_OF_THE_WEEK_ATTS = {
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
    # Get the correct UTC offset for the timezone
    # NOTE Britain introduced the first timezone GMT in 1847 in order to standardize
    # timing for train schedules. North American railroads adopted time zones in November 1883,
    # known as "the Day of Two Noons".
    @staticmethod
    def get_utc_offset(tz_name: str, rd_day : Decimal) -> tuple[Decimal, int ,int, Decimal]:
        """
        Resolve a timezone identifier and R.D. day to a UTC offset.

        Args:
            tz_name:  IANA timezone name (e.g. ``'America/New_York'``)
                or the literal string ``'local'`` to consult the
                system default via `tzlocal.get_localzone`.
            rd_day:   R.D. day the moment falls on.  Needed to pick
                the correct offset across DST or historical
                timezone transitions (e.g. WWII shifts).

        Returns:
            `(hours, minutes)` — the timezone's UTC offset on that
            Gregorian date, both fields as `int`.

        Raises:
            `ValueError`:  `tz_name` cannot be resolved by
                `zoneinfo.ZoneInfo` (re-raises
                `ZoneInfoNotFoundError` with a friendlier message).

        Notes:
            The declared return type
            ``tuple[Decimal, int, int, Decimal]`` is legacy — the
            body actually returns a 2-tuple `(int, int)`.  Repair
            deferred to a future Task 1 pass (out of scope for
            PL-01's non-behavioral charter).
        """
        try:
            if tz_name.lower() == 'local':
                tz = get_localzone()
            else:
                tz = ZoneInfo(tz_name)
        except ZoneInfoNotFoundError:
            raise ValueError(f"Timezone '{tz_name}' not found.")
        year, month, day = gregorian_from_rd(rd_day)
        if year < 1847:
            return (Decimal(0), 0, 0, Decimal(0))
        dt = datetime(int(year), int(month), int(day), 0, 0, 0, 0, tzinfo=tz)
        offset = dt.utcoffset()
        # Format as ±HH:MM
        hours, remainder = divmod(offset.total_seconds(), 3600)
        minutes = remainder // 60
        return (int(hours), int(minutes))
    
    # CONSTRUCTOR ############################################################################
    def __init__(self, calendar : Calendar, moment: UnivMoment, year: Decimal, tz : str | dict = 'UTC'):
        """
        Construct a calendar presentation of `moment`.

        Args:
            calendar:  `Calendar` enum member.  Used by the format
                dispatcher to pick era suffixes, locale conventions,
                etc.
            moment:    `UnivMoment` to present.
            year:      Pre-computed year value for this calendar
                (subclass computes this from `moment.rd_day` before
                calling `super().__init__`).
            tz:        Timezone: IANA name (``'Europe/Paris'``),
                ``'local'`` (system default), ``'UTC'``, or a
                pre-built offset dict.  When not UTC, the moment
                is shifted by the resolved offset before further
                processing so that all downstream code can assume
                wall-clock local time.

        Notes:
            The `-Infinity` year sentinel (deep-time / undefined
            moment) skips the sub-day decomposition; `hour`,
            `minute`, and `seconds` remain unset.
        """
        self.tz = tz
        self.tz_offset = (0,0)  # (hours, minutes)        
        if tz and tz != 'UTC':
            self.tz_offset = Present_Calendars.get_utc_offset(tz, moment.rd_day)
            moment = moment + (Decimal(0), self.tz_offset[0], self.tz_offset[1], Decimal(0))
        super().__init__(calendar, moment, year)
        if year != Decimal('-Infinity'):
            self.hour, self.minute, self.seconds = moment.rd_time
        return
    
    # PRESENTATION LAYER METHODS ############################################################
    """
    def strftime(self, format: str, language: str = "en") -> str:
    
    Format the Moment using a custom format string.
    This is a simplified version and does not support all Python strftime features.

    Date Components
    Directive	Meaning	                            Example
                YEAR
    %C          Cycle long (Chinese calendar)
    %c          Cycle short (Chinese calendar)      1
    %Y	        Year long                   	    2025
    %y	        Year short                          25

                MONTH
    %m	        Month as a decimal number (01-12)	08
    %B	        Full month name	                    August
    %b	        Abbreviated month name	            Aug

                DAY
    %d	        Day of the month (01-31)	        02
    %A	        Full weekday name	                Saturday
    %a	        Abbreviated weekday name	        Sat
    %j	        Day of the year (001-366)	        214

    Time Components
    Directive	Meaning	                            Example
                HOUR
    %H	        Hour (24-hour clock) (00-23)	    14
    %I	        Hour (12-hour clock) (01-12)	    02
    %p	        AM or PM	                        pm, am

                MINUTE
    %M	        Minute (00-59)	                    35

                SECOND
    %S	        Second (00-59)	                    23
    %f          fractional part                     .35654

                TIMEZONE
    %z	        UTC offset (+HHMM or -HHMM)	        +0200
    %Z	        Timezone name	                    UTC

    Complete Formats
    Directive	Meaning	                            Example
    %K          calender system name	            Gregorian
    %k          calender                	        JD
    %y	        Locale's appropriate date and time	Sat Aug 2 14:35:45 2025
    %x	        Locale's appropriate date	        08/02/25
    %X	        Locale's appropriate time	        14:35:45

    Modifiers
    %#m,%#d,%#j - eliminates leading 0s
    """   
    def _format_segment(self, segment : dict, language : str) -> str:
        seg_type = segment['type']
        eliminate_leading_zero = segment.get('eliminate_leading_zero', False)
        frac_digits = segment.get('frac_digits', None)
        # 
        if seg_type in 'YyCc':
            return self._strftime_year(seg_type, language, eliminate_leading_zero)
        elif seg_type in 'mBb':
            return self._strftime_month(seg_type, language, eliminate_leading_zero)
        elif seg_type in 'dAaj':
            return self._strftime_day(seg_type, language, eliminate_leading_zero)
        elif seg_type in 'HIpMSfZz':
            return self._strftime_time(seg_type, language, eliminate_leading_zero, frac_digits)
        elif seg_type in 'Xx':
            return self._strftime_compound(seg_type, language, eliminate_leading_zero)
        else:
            return f'%{seg_type}'  # Unknown segment, return as is
        
    def _strftime_year(
        self, seg_type: str, language: str, eliminate_leading_zero: bool
    ) -> str:
        """
        Format the year component based on the segment type and language.
        """
        if UnivMoment.PREC_LEVEL[self.precision] > UnivMoment.PREC_LEVEL[UnivMomPrecision.YEAR]:
            raise ValueError("Year is not defined for the current precision level.")
        else:
            year = f"{self.year}"
        # Handle negative vales
        fmt = year
        if seg_type == "Y":
            if (UnivMoment.PREC_LEVEL[self.precision] > UnivMoment.PREC_LEVEL[UnivMomPrecision.YEAR]):
                fmt += f" {UnivMoment.PREC_ABBREV[self.precision]}"
        elif seg_type == "y":
            if self.year < 0:
                fmt = year[1:]
                fmt += f" {CalendarAtts[language][self.calendar]['bce_suffix']}"
            if (UnivMoment.PREC_LEVEL[self.precision] > UnivMoment.PREC_LEVEL[UnivMomPrecision.YEAR]):
                fmt += f" {UnivMoment.PREC_ABBREV[self.precision]}"
        return fmt

    def _strftime_month(self, seg_type : str, language :str, eliminate_leading_zero: bool = False) -> str:
        if self.year == Decimal('-Infinity'):
            return ""
        if self.month is None:
            return ""
        if seg_type == 'm':
            zs = '02d' if not eliminate_leading_zero else 'd'
            return f"{self.month:{zs}}"  # Zero-padded month number
        elif seg_type == 'B':
            return self._strftime_month_attr('name', language)  # Full month name
        elif seg_type == 'b':
            return self._strftime_month_attr('abbrv', language)  # Abbreviated month name
        return ""
    @abstractmethod
    def _strftime_month_attr(self, attr : str, language :str) -> int | str:
        """
        Abstract - Needs to implemented in each sub-class
        """
        raise NotImplementedError("Sub-classes must implement this method")
    
    def _strftime_day(self, seg_type : str, language :str, eliminate_leading_zero: bool = False) -> str:
        if self.year == Decimal('-Infinity'):
            return ""
        fmt = ""
        if self.day is None:
            return ""
        elif seg_type == 'd':
            zs = '02d' if not eliminate_leading_zero else 'd'
            fmt +=  f"{self.day:{zs}}"  # Zero-padded day of the month
    
        elif seg_type == 'A':
            fmt +=  self._strftime_day_of_week_attr('name', language)  # Full weekday name
        elif seg_type == 'a':
            fmt += self._strftime_day_of_week_attr('abbrv', language)  # Abbreviated weekday name
        elif seg_type == 'j':
            zs = '03d' if not eliminate_leading_zero else 'd'
            fmt += f"{self.day_of_year():{zs}}"  # Day of the year (001-366)
        return fmt
    
    def _strftime_day_of_week_attr(self, attr : str, language : str='en') -> int | str:
        """
        Get a day of the week attribute.
        """
        if self.year == Decimal('-Infinity'):
            return "..."
        index = int(self.moment.rd_day - 1) % 7
        return Present_Calendars.DAY_OF_THE_WEEK_ATTS[language][index][attr]


    def _strftime_time(self, seg_type : str, language :str, eliminate_leading_zero: bool = False, frac_digits : int = None) -> str:
        if self.year == Decimal('-Infinity'):
            return ""
        # Hour ###############################################################################
        fmt = ""
        if seg_type in 'HIp':
            if self.hour is None:
                return ".."
            elif UnivMoment.PREC_LEVEL[self.precision] <= UnivMoment.PREC_LEVEL[UnivMomPrecision.HOUR]:
                if seg_type == 'H':
                    # 24-hour clock
                    fmt = f"{self.hour:02.0f}" 
                elif seg_type == 'I':
                    # 12-hour clock
                    fmt = f"{self.hour % 12:02.0f}"
                else:
                    # AM/PM
                    fmt = "am" if self.hour < 12 else "pm"
            else:
                fmt = ".."    
        # Minute ############################################################################### 
        elif seg_type == 'M':
            if self.minute is None:
                fmt = ".."
            elif UnivMoment.PREC_LEVEL[self.precision] <= UnivMoment.PREC_LEVEL[UnivMomPrecision.MINUTE]:
                fmt =  f"{self.minute:02.0f}"
            else:
                fmt = '..'
        # Second ###############################################################################
        elif seg_type in 'S':
            if self.seconds is None:
                fmt = ".."
            elif UnivMoment.PREC_LEVEL[self.precision] <= UnivMoment.PREC_LEVEL[UnivMomPrecision.SECOND]:
                # decimal_places = -UnivMoment.PREC_POWER[self.precision]
                # fmt = f"0{2 + (1 if decimal_places>0 else 0) + decimal_places}.{decimal_places}f"
                # fmt = f"{trunc(self.seconds,decimals=decimal_places):{fmt}}"
                integer_part = int(self.seconds)
                if eliminate_leading_zero:
                    fmt = f"{integer_part:d}"
                else:
                    fmt = f"{integer_part:02d}"
                pass
            else:
                fmt = '..'  
        elif seg_type == 'f':
            if self.seconds is None:
                fmt = ".."
            elif UnivMoment.PREC_LEVEL[self.precision] <= UnivMoment.PREC_LEVEL[UnivMomPrecision.SECOND]:
                # fractional seconds
                decimal_places = -UnivMoment.PREC_POWER[self.precision]
                if frac_digits is not None:
                    decimal_places = min(frac_digits, decimal_places)
                fractional_part = self.seconds - Decimal(int(self.seconds))
                fmt = f"0.{decimal_places}f"
                fmt = f"{trunc(fractional_part,decimals=decimal_places):{fmt}}"[1:]  # Skip "0"
            else:
                fmt = '..'   
        # Timezone ###############################################################################           
        elif seg_type == 'z':
            # UTC offset, assuming no timezone information is available
            if self.tz_offset is not None:
                offset_hours, offset_minutes = self.tz_offset[0], self.tz_offset[1]
                sign = '+' if (offset_hours > 0 or (offset_hours == 0 and offset_minutes >= 0)) else '-'
                fmt = f"{sign}{abs(offset_hours):02d}:{abs(offset_minutes):02d}"
        # Internal Timezone Name ###################################################################
        elif seg_type == 'Z':
            if self.tz is not None:
                fmt = self.tz
            else:
                fmt = "UTC"
        return fmt
    
    def _strftime_compound(self, seg_type : str, language :str, eliminate_leading_zero: bool = False) -> str:
        if seg_type == 'y':
            # Locale's appropriate date and time
            return self.format_signature()
        elif seg_type == 'x':
            # Locale's appropriate date
            return self.format_signature_date()
        elif seg_type == 'X':
            # Locale's appropriate time
            return self.format_signature_time()
        return ""

