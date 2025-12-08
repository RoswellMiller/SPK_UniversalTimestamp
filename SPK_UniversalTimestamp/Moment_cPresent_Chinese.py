
from .CC19_Chinese_1645 import chinese_from_rd
from .Constants_aCommon import Calendar, Precision, PrecisionAtts
from .Constants_Chinese import chinese_MONTH_ATTS
from .Moment_aUniversal import UnivMoment
from .Moment_bPresent_Calendars import Present_Calendars


class Present_Chinese(Present_Calendars):
    """
    Chinese calendar representation of a UnivMoment.
    """
    # CONSTRUCTOR ############################################################################
    def __init__(self, moment: UnivMoment, tz : str | tuple[float,float] = 'UTC'):
        rd = moment.rd_day
        cycle, year, month, leap, day = chinese_from_rd(rd)
        super().__init__(Calendar.CHINESE, moment, (cycle,year), tz)
        self.month = ( 1, False)
        self.day = 1
        if PrecisionAtts[self.precision]['level'] >= PrecisionAtts[Precision.MONTH]['level']:
            self.month = (month, leap)
        if PrecisionAtts[self.precision]['level'] >= PrecisionAtts[Precision.DAY]['level']:
            self.day = day
        return
    
    # PRESENTATION LAYER METHODS ############################################################
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
    def _strftime_year(self, seg_type: str, language: str, eliminate_leading_zero: bool = False) -> str:
        """
        Format the year component based on the segment type and language.
        Directive	Meaning	                            Example
                    YEAR
        %Y	        Year first long                   	Twenty-Fifth
        %y	        Year first short                    25
        %C          Cycle first long                    Rat
        %c          Cycle first short                   10?
        """
        if self.year is None:
            return ""
        if seg_type in 'Cc':
            return f"{self.year[0]:d}"
        elif seg_type  in 'Yy':
            return f"{self.year[1]:d}"
        else:
            return f"%{seg_type}"
    
    def _strftime_month(self, seg_type : str, language :str, eliminate_leading_zero: bool = False) -> str:
        """
        Format the month component based on seg_type, language, and modifiers.
        Directive	Meaning	                            Example
                    MONTH 
        %m	        Month as a decimal number (01-12)	08 {L}
        %B	        Full month name	                    August {L}
        %b	        Abbreviated month name	            Aug {L}
        """
        if self.month is None:
            return ""
        if isinstance(self.month, tuple):
            m_num = self.month[0]
            m_leap = self.month[1]
            m_suffix = 'L' if m_leap else ''
        else:
            raise ValueError("Chinese month should be a tuple of (month_number, is_leap_month).")
        if seg_type == 'm':
            zs = '02d' if not eliminate_leading_zero else 'd'
            return f"{m_num:{zs}}{m_suffix}"  # Zero-padded month number
        elif seg_type == 'B' or seg_type == 'b':
            return chinese_MONTH_ATTS[m_num][m_leap]['pinyin']  # Full month name
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
