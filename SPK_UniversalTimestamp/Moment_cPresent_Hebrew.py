from .CC08_Hebrew import hebrew_from_rd
from .Constants_aCommon import Calendar, Precision, PrecisionAtts
from .Constants_Hebrew import hebrew_MONTH_ATTS
from .Moment_aUniversal import UnivMoment
from .Moment_bPresent_Calendars import Present_Calendars

class Present_Hebrew(Present_Calendars):
    """
    Hebrew calendar representation of a UnivMoment.
    """
    # CONSTRUCTOR ############################################################################
    def __init__(self, moment: UnivMoment, tz : str | tuple[float,float] = 'UTC'):
        rd = moment.rd_day
        year, month, day = hebrew_from_rd(int(str(rd)))
        super().__init__(Calendar.HEBREW, moment, year, tz)
        self.month = 1
        self.day = 1
        if PrecisionAtts[self.precision]['level'] >= PrecisionAtts[Precision.MONTH]['level']:
            self.month = month
        if PrecisionAtts[self.precision]['level'] >= PrecisionAtts[Precision.DAY]['level']: 
            self.day = day
        return
    
    # PRESENTATION LAYER METHODS ############################################################
    def _strftime_month_attr(self, attr : str, language : str='en') -> int | str:
        """
        Get a month attribute.
        """
        return hebrew_MONTH_ATTS[language][self.month][attr] if self.month in hebrew_MONTH_ATTS[language] else '...'
