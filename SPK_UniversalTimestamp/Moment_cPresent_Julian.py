from .CC03_Julian import julian_from_rd
from .Constants_aCommon import Calendar, Precision, PrecisionAtts
from .Constants_Julian import julian_MONTH_ATTS
from .Moment_aUniversal import UnivMoment
from .Moment_bPresent_Calendars import Present_Calendars

class Present_Julian(Present_Calendars):
    """
    Julian calendar representation of a UnivMoment.
    """
    # CONSTRUCTOR ############################################################################
    def __init__(self, moment: UnivMoment, tz : str | tuple[float,float] = 'UTC'):
        rd = moment.rd_day
        year, month, day = julian_from_rd(int(str(rd)))
        super().__init__(Calendar.JULIAN, moment, year, tz)
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
        return julian_MONTH_ATTS[language][self.month][attr] if self.month in julian_MONTH_ATTS[language] else '...'
