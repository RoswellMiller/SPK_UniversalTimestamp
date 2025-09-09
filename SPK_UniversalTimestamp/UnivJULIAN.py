from decimal import Decimal
from typing import Union, Tuple

from SPK_UniversalTimestamp.CC03_Julian import is_julian_leap_year, rd_from_julian, julian_from_rd
from SPK_UniversalTimestamp import Calendar, Precision
from SPK_UniversalTimestamp import UnivCalendars


class UnivJULIAN(UnivCalendars):
    """
    This class represents a Julian timestamp.
    It inherits from the UnivTimestamp class and is used to handle
    Hebrew calendar data.
    """
    # __slots__ ####################################################################################
    
    # IMMUTABLE #######################################################################################
    
    # CONSTANTS #########################################################################################
    MONTH_ATTS = {
        'en': {
            1: {'name': "January", 'abbrv': "Jan", 'days': 31},
            2: {'name': "February", 'abbrv': "Feb", 'days': 28},
            3: {'name': "March", 'abbrv': "Mar", 'days': 31},
            4: {'name': "April", 'abbrv': "Apr", 'days': 30},
            5: {'name': "May", 'abbrv': "May", 'days': 31},
            6: {'name': "June", 'abbrv': "Jun", 'days': 30},
            7: {'name': "July", 'abbrv': "Jul", 'days': 31},
            8: {'name': "August", 'abbrv': "Aug", 'days': 31},
            9: {'name': "September", 'abbrv': "Sep", 'days': 30},
            10: {'name': "October", 'abbrv': "Oct", 'days': 31},
            11: {'name': "November", 'abbrv': "Nov", 'days': 30},
            12: {'name': "December", 'abbrv': "Dec", 'days': 31}
        },
        'fr': {
            1: {'name': "Janvier", 'abbrv': "Jan", 'days': 31},
            2: {'name': "Février", 'abbrv': "Fév", 'days': 28},
            3: {'name': "Mars", 'abbrv': "Mar", 'days': 31},
            4: {'name': "Avril", 'abbrv': "Avr", 'days': 30},
            5: {'name': "Mai", 'abbrv': "Mai", 'days': 31},
            6: {'name': "Juin", 'abbrv': "Jun", 'days': 30},
            7: {'name': "Juillet", 'abbrv': "Jul", 'days': 31},
            8: {'name': "Août", 'abbrv': "Aoû", 'days': 31},
            9: {'name': "Septembre", 'abbrv': "Sep", 'days': 30},
            10: {'name': "Octobre", 'abbrv': "Oct", 'days': 31},
            11: {'name': "Novembre", 'abbrv': "Nov", 'days': 30},
            12: {'name': "Décembre", 'abbrv': "Déc", 'days': 31}
        },
        'es': {
            1: {'name': "Enero", 'abbrv': "Ene", 'days': 31},
            2: {'name': "Febrero", 'abbrv': "Feb", 'days': 28},
            3: {'name': "Marzo", 'abbrv': "Mar", 'days': 31},
            4: {'name': "Abril", 'abbrv': "Abr", 'days': 30},
            5: {'name': "Mayo", 'abbrv': "May", 'days': 31},
            6: {'name': "Junio", 'abbrv': "Jun", 'days': 30},
            7: {'name': "Julio", 'abbrv': "Jul", 'days': 31},
            8: {'name': "Agosto", 'abbrv': "Ago", 'days': 31},
            9: {'name': "Septiembre", 'abbrv': "Sep", 'days': 30},
            10: {'name': "Octubre", 'abbrv': "Oct", 'days': 31},
            11: {'name': "Noviembre", 'abbrv': "Nov", 'days': 30},
            12: {'name': "Diciembre", 'abbrv': "Dic", 'days': 31}
        },
        'de': {
            1: {'name': "Januar", 'abbrv': "Jan", 'days': 31},
            2: {'name': "Februar", 'abbrv': "Feb", 'days': 28},
            3: {'name': "März", 'abbrv': "Mär", 'days': 31},
            4: {'name': "April", 'abbrv': "Apr", 'days': 30},
            5: {'name': "Mai", 'abbrv': "Mai", 'days': 31},
            6: {'name': "Juni", 'abbrv': "Jun", 'days': 30},
            7: {'name': "Juli", 'abbrv': "Jul", 'days': 31},
            8: {'name': "August", 'abbrv': "Aug", 'days': 31},
            9: {'name': "September", 'abbrv': "Sep", 'days': 30},
            10: {'name': "Oktober", 'abbrv': "Okt", 'days': 31},
            11: {'name': "November", 'abbrv': "Nov", 'days': 30},
            12: {'name': "Dezember", 'abbrv': "Dez", 'days': 31}
        },
        'it': {
            1: {'name': "Gennaio", 'abbrv': "Gen", 'days': 31},
            2: {'name': "Febbraio", 'abbrv': "Feb", 'days': 28},
            3: {'name': "Marzo", 'abbrv': "Mar", 'days': 31},
            4: {'name': "Aprile", 'abbrv': "Apr", 'days': 30},
            5: {'name': "Maggio", 'abbrv': "Mag", 'days': 31},
            6: {'name': "Giugno", 'abbrv': "Giu", 'days': 30},
            7: {'name': "Luglio", 'abbrv': "Lug", 'days': 31},
            8: {'name': "Agosto", 'abbrv': "Ago", 'days': 31},
            9: {'name': "Settembre", 'abbrv': "Set", 'days': 30},
            10: {'name': "Ottobre", 'abbrv': "Ott", 'days': 31},
            11: {'name': "Novembre", 'abbrv': "Nov", 'days': 30},
            12: {'name': "Dicembre", 'abbrv': "Dic", 'days': 31}
        }
    }
    
    # CONSTRUCTOR ######################################################################################
    @staticmethod
    def _days_in_month(year: int, month: int) -> int:
        num_days = UnivJULIAN.MONTH_ATTS['en'][month]['days']
        if month == 2 and is_julian_leap_year(year):
            return 29
        return num_days
    # Each tuple: (slot name, allowed_types, valid_function, precision_enum)
    CNST_ARGS = [
        ("year",   (int,), lambda arg, *_: (-9999 <= arg <= 9999), Precision.YEAR),
        ("month",  (int,), lambda arg, *_: (1 <= arg <=12), Precision.MONTH),
        ("day",    (int,), lambda arg, v: (1 <= arg <= UnivJULIAN._days_in_month(v['year'], v['month'])),  Precision.DAY),
        ("hour",   (int,), lambda arg, *_: (0 <= arg <= 23), Precision.HOUR),
        ("minute", (int,), lambda arg, *_: (0 <= arg <= 59), Precision.MINUTE),
        ("second", (Union[int, Decimal],), lambda arg, *_: (Decimal("0") <= arg < Decimal("60")), Precision.SECOND),
    ]
    def __init__(self, *args, timezone: str = 'UTC', fold: int = 0,
        precision: Precision = None, 
        accuracy: Decimal = None, 
        description: str = ""
        ):
        """Create Julian timestamp (Old Style calendar)"""
        v_args, precision = self._init_validate_constructor_args(1, args, precision)
        super().__init__(
            Calendar.JULIAN,
            v_args['year'], v_args['month'], v_args['day'], v_args['hour'], v_args['minute'], v_args['second'], timezone=timezone, fold=fold,
            precision=precision,
            accuracy=accuracy,
            description=description
        )
    
    # TIMESTAMP METHODS ######################################################################################
    def _self_rata_die(self) -> int:
        return rd_from_julian(self.year, self.month, self.day)
    def _calc_rata_die(self, year, month, day) -> int:
        return rd_from_julian(year, month, day)
    
    # CALENDARS METHODS ######################################################################################
    def _calc_date_from_rd(self, rd: int) -> Tuple[int, int, int]:
        """
        Convert Rata Die (rd) fixed day number to Julian date
        "Calendrical Calculations" by Reingold and Dershowitz pp 59-63
        """
        return UnivJULIAN._julian_from_rd(rd)

    def month_attr(self, attr : str, language : str='en') -> Union[int, str]:
        """
        Get a month attribute.
        """
        return self.MONTH_ATTS[language][self.month][attr] if self.month in self.MONTH_ATTS[language] else '...'
    
    # JULIAN METHODS ######################################################################################
    
    # FORMATTING METHODS ###########################################################################
    
    
    ###########################################################################################
