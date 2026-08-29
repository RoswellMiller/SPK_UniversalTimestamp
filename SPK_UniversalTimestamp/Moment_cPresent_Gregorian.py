"""
Moment_cPresent_Gregorian — Gregorian-calendar presentation layer for
`UnivMoment`.

**Purpose.**  Adapter class `Present_Gregorian` that converts a
`UnivMoment` into a Gregorian `(year, month, day)` presentation
with strftime-style month formatting hooks.  Calendar arithmetic
lives in `CC02_Gregorian`; this module is purely presentation.

**Public surface (star-exported via `__init__.py`).**
    `Present_Gregorian` (subclass of `Present_Calendars`).

**Sentinel handling.**  A moment whose `rd_day` is
`Decimal('-Infinity')` is treated as "before recorded time" — the
adapter carries the sentinel as its year and drops month/day
rather than attempting the R.D. conversion (which would fail).

**Change history.**  See `CHANGELOG.md`.
"""

from decimal import Decimal

from .CC02_Gregorian import gregorian_from_rd
from .Constants_aCommon import Calendar
from .Constants_Gregorian import gregorian_MONTH_ATTS
from .Moment_bPresent_Calendars import Present_Calendars
from .UnivMoment import UnivMoment, UnivMomPrecision


class Present_Gregorian(Present_Calendars):
    """
    Gregorian-calendar presentation adapter for a `UnivMoment`.  See
    `Moment_cPresent_Julian.Present_Julian` for the shared shape of
    these calendar adapters; the Gregorian variant additionally
    handles the `-Infinity` R.D. sentinel described in the module
    docstring.
    """
    # CONSTRUCTOR ############################################################################
    def __init__(self, moment: UnivMoment, tz : str | tuple[float,float] = 'UTC'):
        """
        Build a `Present_Gregorian` view of `moment`.

        Args:
            moment:  `UnivMoment` to present.  May carry the
                `Decimal('-Infinity')` sentinel R.D. (deep-time /
                unknown moment).
            tz:      Timezone identifier or `(lat, lon)` tuple.
                Forced to `None` when the sentinel is present.
        """
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
            if UnivMoment.PREC_LEVEL[self.precision] <= UnivMoment.PREC_LEVEL[UnivMomPrecision.DAY]:
                self.month = month
            if UnivMoment.PREC_LEVEL[self.precision] <= UnivMoment.PREC_LEVEL[UnivMomPrecision.DAY]: 
                self.day = day
        return
    
    # PRESENTATION LAYER METHODS ############################################################
    def _strftime_month_attr(self, attr : str, language : str='en') -> int | str:
        """
        Look up a Gregorian month attribute from
        `gregorian_MONTH_ATTS[language]`.

        Args:
            attr:      One of ``'name'``, ``'abbrv'``, ``'days'``.
            language:  ISO language code; defaults to English.

        Returns:
            The requested value, or ``'...'`` if `self.month` is
            not present in the language table.
        """
        return gregorian_MONTH_ATTS[language][self.month][attr] if self.month in gregorian_MONTH_ATTS[language] else '...'
    
