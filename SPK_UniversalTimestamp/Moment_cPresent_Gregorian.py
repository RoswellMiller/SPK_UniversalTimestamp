from decimal import Decimal
from .CC02_Gregorian import gregorian_from_rd
from .Constants_aCommon import Calendar, Precision, PrecisionAtts
from .Constants_Gregorian import gregorian_MONTH_ATTS
from .Moment_aUniversal import UnivMoment
from .Moment_bPresent_Calendars import Present_Calendars

class Present_Gregorian(Present_Calendars):
    """
    Gregorian calendar representation of a UnivMoment.
    """
    # CONSTRUCTOR ############################################################################
    def __init__(self, moment: UnivMoment, tz : str | tuple[float,float] = 'UTC'):
        rd = moment.rd_day
        if rd == Decimal('-Infinity'):
            year = rd
            tz = None
        else:
            year, month, day = gregorian_from_rd(int(str(rd)))
        super().__init__(Calendar.GREGORIAN, moment, year, tz)
        if self.year != Decimal('-Infinity'):
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
        return gregorian_MONTH_ATTS[language][self.month][attr] if self.month in gregorian_MONTH_ATTS[language] else '...'
    
