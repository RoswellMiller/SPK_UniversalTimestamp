from decimal import Decimal
from abc import abstractmethod
from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
from tzlocal import get_localzone
from .CC00_Decimal_library import trunc
from .CC02_Gregorian import gregorian_from_rd
from .Constants_aCommon import Calendar, CalendarAtts, Precision, PrecisionAtts
from .Moment_aUniversal import UnivMoment

class Present_Calendars(UnivMoment.Presentation):
    """
    Calendar representation of a UnivMoment.
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
        Return the UTC offset for a given time zone name and datetime.
        If dt is None, use current time.
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
        self.tz = 'UTC'
        self.tz_offset = (0,0)  # (hours, minutes)        
        if tz != 'UTC':
            self.tz = tz
            self.tz_offset = Present_Calendars.get_utc_offset(tz, moment.rd_day)
            moment = moment + (Decimal(0), self.tz_offset[0], self.tz_offset[1], Decimal(0))
        super().__init__(calendar, moment, year)
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
    %S	        Second (00-59)	                    23, 45.35654

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
        # 
        if seg_type in 'YyCc':
            return self._strftime_year(seg_type, language, eliminate_leading_zero)
        elif seg_type in 'mBb':
            return self._strftime_month(seg_type, language, eliminate_leading_zero)
        elif seg_type in 'dAaj':
            return self._strftime_day(seg_type, language, eliminate_leading_zero)
        elif seg_type in 'HIpMSfZz':
            return self._strftime_time(seg_type, language, eliminate_leading_zero)
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
        if PrecisionAtts[self.precision]['level'] < PrecisionAtts[ Precision.YEAR]['level']:
            raise ValueError("Year is not defined for the current precision level.")
        else:
            year = f"{self.year}"
        # Handle negative vales
        fmt = year
        if seg_type == "Y":
            if (PrecisionAtts[self.precision]["level"] < PrecisionAtts[Precision.YEAR]["level"]):
                fmt += f" {PrecisionAtts[self.precision]['abbrv']}"
        elif seg_type == "y":
            if self.year < 0:
                fmt = year[1:]
                fmt += f" {CalendarAtts[language][self.calendar]['bce_suffix']}"
            if (PrecisionAtts[self.precision]["level"] < PrecisionAtts[Precision.YEAR]["level"]):
                fmt += f" {PrecisionAtts[self.precision]['abbrv']}"
        return fmt

    def _strftime_month(self, seg_type : str, language :str, eliminate_leading_zero: bool = False) -> str:
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
        index = int(self.moment.rd_day - 1) % 7
        return Present_Calendars.DAY_OF_THE_WEEK_ATTS[language][index][attr]


    def _strftime_time(self, seg_type : str, language :str, eliminate_leading_zero: bool = False) -> str:
        # Hour ###############################################################################
        fmt = ""
        if seg_type in 'HIp':
            if self.hour is None:
                return ".."
            elif PrecisionAtts[self.precision]['level'] >= PrecisionAtts[ Precision.HOUR]['level']:
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
            elif PrecisionAtts[self.precision]['level'] >= PrecisionAtts[ Precision.MINUTE]['level']:
                fmt =  f"{self.minute:02.0f}"
            else:
                fmt = '..'
        # Second ###############################################################################
        elif seg_type in 'S':
            if self.seconds is None:
                fmt = ".."
            elif PrecisionAtts[self.precision]['level'] >= PrecisionAtts[Precision.SECOND]['level']:
                decimal_places = -PrecisionAtts[self.precision]['power']
                fmt = f"0{2 + (1 if decimal_places>0 else 0) + decimal_places}.{decimal_places}f"
                fmt = f"{trunc(self.seconds,decimals=decimal_places):{fmt}}"
                pass
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

