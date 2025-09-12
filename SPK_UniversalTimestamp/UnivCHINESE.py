from decimal import Decimal
from typing import Union, Tuple

from .UnivDecimalLibrary import *
from .CC19_Chinese_1645 import *

from SPK_UniversalTimestamp import Calendar, Precision, CalendarAtts
from SPK_UniversalTimestamp import UnivCalendars


class UnivCHINESE(UnivCalendars):
    """
    This class represents a Hebrew timestamp.
    It inherits from the UnivTimestamp class and is used to handle
    Chinese calendar data.
    """
    # __slots__ ####################################################################################
    
    # IMMUTABLE #######################################################################################
    
    # CONSTANTS #########################################################################################
    
    
    # CONSTRUCTOR ######################################################################################
    @staticmethod
    def _days_in_month(cycle: int, year: int, month: int, leap: bool) -> int:
        marker = rd_from_chinese(cycle, year, month, leap, 1)
        new_moon_t0 = floor(chinese_new_moon_before(marker))
        new_moon_t1 = floor(chinese_new_moon_on_or_after(marker))
        num_days = new_moon_t1 - new_moon_t0
        return num_days
    @staticmethod
    def _validate_month(arg, context):
        if isinstance(arg, int):
            return (1 <= arg <= 12)
        elif isinstance(arg, tuple):
            return (1 <= arg[0] <= 12) and isinstance(arg[1], bool)
        return False
    # Each tuple: (slot name, allowed_types, valid_function, precision_enum)
    CNST_ARGS = [
        ("cycle",  (int,), lambda arg, *_: (1 <= arg <= 99999), None),
        ("year",   (int,), lambda arg, *_: (1 <= arg <= 60), Precision.YEAR),
        ("month",  (int, Tuple), lambda arg, context : UnivCHINESE._validate_month(arg, context), Precision.MONTH),
        ("day",    (int,), 
            lambda arg, v: (
                1 <= arg <=
                UnivCHINESE._days_in_month(
                    v['cycle'], 
                    v['year'], 
                    v['month'][0] if isinstance(v['month'], Tuple) else v['month'], 
                    v['month'][1] if isinstance(v['month'], Tuple) else False
                    )
                ), 
            Precision.DAY),
        ("hour",   (int,), lambda arg, *_: (0 <= arg <= 23), Precision.HOUR),
        ("minute", (int,), lambda arg, *_: (0 <= arg <= 59), Precision.MINUTE),
        ("second", (Union[int, Decimal],), lambda arg, *_: (Decimal("0") <= arg < Decimal("60")), Precision.SECOND),
    ]
    def __init__(self, *args, timezone: str = 'UTC', fold: int = 0,
        precision: Precision = None,
        accuracy: Decimal = None,
        description: str = ""
    ):
        """Create Chinese timestamp"""
        v_args, precision = self._init_validate_constructor_args(2, args, precision)
        super().__init__(
                Calendar.CHINESE,
                (v_args['cycle'] -1)*60 + v_args['year'] -1, v_args['month'], v_args['day'], v_args['hour'], v_args['minute'], v_args['second'], timezone=timezone, fold=fold,
                precision=precision,
                accuracy=accuracy,
                description=description    
                )
    
    # TIMESTAMP METHODS ######################################################################################
    def _self_rata_die(self) -> int:
        cycle, year = UnivCHINESE.cycle_year(self.year)
        month, leap_month = UnivCHINESE.month_leap(self.month)
        return rd_from_chinese(cycle, year, month, leap_month, self.day)

    def _calc_rata_die(self, ts_year, month, day) -> int:
        cycle, year = UnivCHINESE.cycle_year(ts_year)
        month, leap = UnivCHINESE.month_leap(month)
        return rd_from_chinese(cycle, year, month, leap, day)

    # CALENDARS METHODS ######################################################################################
    def _calc_date_from_rd(self, rd: int) -> Tuple[int, int, int]:
        """
        Convert Rata Die (rd) fixed day number to Chinese date
        "Calendrical Calculations" by Reingold and Dershowitz pp 59-63
        """
        cycle, year, month, leap, day = chinese_from_rd(rd)
        rd_year = UnivCHINESE.rd_year(cycle, year)
        rd_month = (month, leap) if leap else month
        return rd_year, rd_month, day

    # def month_attr(self, attr : str, language : str='en') -> Union[int, str]:
    #     """
    #     Get a month attribute.
    #     """
    #     return TERM_ATTS[language][self.month][attr] if self.month in TERM_ATTS[language] else '...'
    

    # CHINESE METHODS ######################################################################################
    @staticmethod
    def cycle_year(year) -> Tuple[int, int]:
        return ((year // 60) + 1, year % 60 + 1)
    
    @staticmethod
    def rd_year(cycle: int, year: int) -> int:
        return (cycle -1)*60 + year - 1
    
    @staticmethod
    def month_leap(month : int| Tuple)-> Tuple[int, bool]:
        if isinstance(month, Tuple):
            return (month[0], month[1])
        return (month, False)
    
    def leap_month(self) -> bool:
        """
        Return True if the month is a leap month, False otherwise.
        """
        return self.month[1] if isinstance(self.month, Tuple) else False

    # FORMATTING METHODS ######################################################################################
    """ General strftime modifiers_
    Modifiers
    %#m,%#d,%#j - eliminates leading 0s
    """
    # def _strftime_year(self, seg_type: str, language: str, eliminate_leading_zero: bool) -> str:
    #     """
    #     Format the year component based on the segment type and language.
    #     Directive	Meaning	                            Example
    #                 YEAR
    #     %Y	        Year long                   	    2025, 66.45 Gyr BCE
    #     %y	        Year short                          25, -66.45 Gyr
        
    #     """
    #     return result
    def _strftime_month(self, seg_type : str, language :str, eliminate_leading_zero: bool = False) -> str:
        """
        Format the month component based on seg_type, language, and modifiers.
        Directive	Meaning	                            Example
                    MONTH 
        %m	        Month as a decimal number (01-12)	08
        %B	        Full month name	                    August
        %b	        Abbreviated month name	            Aug
        """
        if self.month is None:
            return ""
        if isinstance(self.month, Tuple):
            m_num = self.month[0]
            m_leap = self.month[1]
            m_suffix = 'L' if self.month[1] else ''
        else:
            m_num = self.month
            m_leap = False
            m_suffix = ''   
        if seg_type == 'm':
            zs = '02d' if not eliminate_leading_zero else 'd'
            return f"{m_num:{zs}}{m_suffix}"  # Zero-padded month number
        elif seg_type == 'B' or seg_type == 'b':
            return Table_19_1_Dict[m_num][m_leap]['pinyin']  # Full month name
        return ""

    # def _strftime_day(self, seg_type : str, language :str, eliminate_leading_zero: bool = False) -> str:
    #     """
    #     Format the day component based on the segment type and language and modifiers.
    #     Directive	Meaning	                            Example
    #                 DAY
    #     %d	        Day of the month (01-31)	        02
    #     %A	        Full weekday name	                Saturday
    #     %a	        Abbreviated weekday name	        Sat
    #     %j	        Day of the year (001-366)	        214

    #     """
    def format_signature_date(self) -> str:
        """Format the date component based on calendar system and precision"""
        result = ""
        if self.year is None:
            return "????"
        result+= f"{self.year}"        
        if self.month is not None:
            result += "-"
            result += self._strftime_month('m', 'en')
            if self.day is not None:
                result += f"-{self.day:02d}"

        cal_abbrv = CalendarAtts['en'][self.calendar]['abbrv']
        if cal_abbrv and len(cal_abbrv) > 0:
            result += f" {cal_abbrv}"
        return result


    # End of class UnivHEBREW #########################################################################