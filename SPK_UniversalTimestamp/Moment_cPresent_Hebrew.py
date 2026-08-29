"""
Moment_cPresent_Hebrew — Hebrew-calendar presentation layer for `UnivMoment`.

**Purpose.**  Adapter class `Present_Hebrew` that converts a
`UnivMoment` into a Hebrew `(year, month, day)` presentation with
strftime-style month formatting hooks.  Calendar arithmetic lives
in `CC08_Hebrew`; this module is purely presentation.

**Public surface (star-exported via `__init__.py`).**
    `Present_Hebrew` (subclass of `Present_Calendars`).

**Not in scope.**  Adar / Adar I / Adar II month-mapping logic in
leap years — `CC08_Hebrew.hebrew_from_rd` returns the correct
month index and `Constants_Hebrew.hebrew_MONTH_ATTS` supplies the
name; this module just plumbs them together.

**Change history.**  See `CHANGELOG.md`.
"""

from .CC08_Hebrew import hebrew_from_rd
from .Constants_aCommon import Calendar
from .Constants_Hebrew import hebrew_MONTH_ATTS
from .Moment_bPresent_Calendars import Present_Calendars
from .UnivMoment import UnivMoment, UnivMomPrecision


class Present_Hebrew(Present_Calendars):
    """
    Hebrew-calendar presentation adapter for a `UnivMoment`.  See
    `Moment_cPresent_Julian.Present_Julian` for the shared shape of
    these calendar adapters.
    """
    # CONSTRUCTOR ############################################################################
    def __init__(self, moment: UnivMoment, tz : str | tuple[float,float] = 'UTC'):
        """
        Build a `Present_Hebrew` view of `moment`.

        Args:
            moment:  `UnivMoment` to present.
            tz:      Timezone identifier or `(lat, lon)` tuple.
        """
        rd = moment.rd_day
        year, month, day = hebrew_from_rd(int(str(rd)))
        super().__init__(Calendar.HEBREW, moment, year, tz)
        self.month = 1
        self.day = 1
        if UnivMoment.PREC_LEVEL[self.precision] <= UnivMoment.PREC_LEVEL[UnivMomPrecision.DAY]:
            self.month = month
        if UnivMoment.PREC_LEVEL[self.precision] <= UnivMoment.PREC_LEVEL[UnivMomPrecision.DAY]: 
            self.day = day
        return
    
    # PRESENTATION LAYER METHODS ############################################################
    def _strftime_month_attr(self, attr : str, language : str='en') -> int | str:
        """
        Look up a Hebrew month attribute from `hebrew_MONTH_ATTS[language]`.

        Args:
            attr:      One of ``'name'``, ``'abbrv'``, ``'days'``.
            language:  ISO language code; defaults to English.

        Returns:
            The requested value, or ``'...'`` if `self.month` is
            not present in the language table.
        """
        return hebrew_MONTH_ATTS[language][self.month][attr] if self.month in hebrew_MONTH_ATTS[language] else '...'
