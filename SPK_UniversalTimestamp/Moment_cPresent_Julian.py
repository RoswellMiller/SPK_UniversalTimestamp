"""
Moment_cPresent_Julian — Julian-calendar presentation layer for `UnivMoment`.

**Purpose.**  Adapter class `Present_Julian` that converts a
`UnivMoment` (universal R.D. moment) into a Julian `(year, month,
day)` presentation with strftime-style month formatting hooks.
Calendar arithmetic lives in `CC03_Julian`; this module is purely
presentation.

**Public surface (star-exported via `__init__.py`).**
    `Present_Julian` (subclass of `Present_Calendars`).

**Not in scope.**  R.D. arithmetic, leap-year tests, month tables
(those live in `CC03_Julian` and `Constants_Julian`).

**Change history.**  See `CHANGELOG.md`.
"""

from .CC03_Julian import julian_from_rd
from .Constants_aCommon import Calendar
from .Constants_Julian import julian_MONTH_ATTS
from .UnivMoment import UnivMoment, UnivMomPrecision
from .Moment_bPresent_Calendars import Present_Calendars

class Present_Julian(Present_Calendars):
    """
    Julian-calendar presentation adapter for a `UnivMoment`.

    Constructing an instance decomposes the moment's R.D. day into
    `(year, month, day)` via `julian_from_rd`, then defers to
    `Present_Calendars` for the shared plumbing (locale, timezone,
    strftime dispatch).  Sub-day precision follows the same
    `UnivMomPrecision` gate as the other calendar adapters: month
    and day are only populated when precision reaches `DAY`.
    """
    # CONSTRUCTOR ############################################################################
    def __init__(self, moment: UnivMoment, tz : str | tuple[float,float] = 'UTC'):
        """
        Build a `Present_Julian` view of `moment`.

        Args:
            moment:  `UnivMoment` to present.
            tz:      IANA timezone string (e.g. ``'Europe/Paris'``)
                or an `(lat, lon)` tuple that will be looked up.
                Defaults to UTC.
        """
        rd = moment.rd_day
        year, month, day = julian_from_rd(int(str(rd)))
        super().__init__(Calendar.JULIAN, moment, year, tz)
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
        Look up a month attribute (``'name'``, ``'abbrv'``, ``'days'``)
        from `julian_MONTH_ATTS[language]`.

        Args:
            attr:      Key into the per-month attribute dict.
            language:  ISO language code; defaults to English.

        Returns:
            The requested value, or ``'...'`` if `self.month` is
            not in the language's table (defensive fallback).
        """
        return julian_MONTH_ATTS[language][self.month][attr] if self.month in julian_MONTH_ATTS[language] else '...'
