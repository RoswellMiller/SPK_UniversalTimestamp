from decimal import Decimal, ROUND_DOWN
from datetime import datetime
from typing import Union, Tuple

from SPK_UniversalTimestamp.CC01_Calendar_Basics import Epoch_rd

from SPK_UniversalTimestamp import *
from SPK_UniversalTimestamp.CC02_Gregorian import *

class UnivGREGORIAN(UnivCalendars):
    """
    This class represents a Gregorian timestamp.
    It inherits from the UnivTimestamp class and is used to handle
    Hebrew calendar data.
    """
    # __slots__ ####################################################################################
    
    # IMMUTABLE #######################################################################################
    
    # CONSTANTS #########################################################################
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
        num_days = UnivGREGORIAN.MONTH_ATTS['en'][month]['days']
        if month == 2 and is_gregorian_leap_year(year):
            return 29
        return num_days
    # Each tuple: (slot name, allowed_types, valid_function, precision_enum)
    CNST_ARGS = [
        ("year",   (int,), lambda arg, *_: (-9999 <= arg <= 9999), Precision.YEAR),
        ("month",  (int,), lambda arg, *_: (1 <= arg <=12), Precision.MONTH),
        ("day",    (int,), lambda arg, v: (1 <= arg <= UnivGREGORIAN._days_in_month(v['year'], v['month'])),  Precision.DAY),
        ("hour",   (int,), lambda arg, *_: (0 <= arg <= 23), Precision.HOUR),
        ("minute", (int,), lambda arg, *_: (0 <= arg <= 59), Precision.MINUTE),
        ("second", (Union[int, Decimal],), lambda arg, *_: (Decimal("0") <= arg < Decimal("60")), Precision.SECOND),
    ]

    def __init__(self, *args,  timezone: str = 'UTC', fold: int =0,
        precision: Precision = None, 
        accuracy: Decimal = None,
        description: str = ""
        ):
        """Create from Gregorian timestamp"""
        v_args, precision = self._init_validate_constructor_args(1, args, precision)
        super().__init__(
            Calendar.GREGORIAN,
            v_args['year'], v_args['month'], v_args['day'], v_args['hour'], v_args['minute'], v_args['second'], timezone=timezone, fold=fold,
            precision=precision,
            accuracy=accuracy,
            description=description
        )
    
    # TIMESTAMP/RD METHODS ######################################################################################
    def _self_rata_die(self) -> int:
        return rd_from_gregorian(self.year, self.month, self.day)

    def _calc_rata_die(self, year, month, day) -> int:
        return rd_from_gregorian(year, month, day)

    # CALENDARS METHODS ######################################################################################
    def _calc_date_from_rd(self, rd: int) -> Tuple[int, int, int]:
        """
        Convert Rata Die (rd) fixed day number to Gregorian date
        "Calendrical Calculations" by Reingold and Dershowitz pp 59-63
        """
        return gregorian_from_rd(rd)
    
    def month_attr(self, attr : str, language : str='en') -> Union[int, str]:
        """
        Get a month attribute.
        """
        return self.MONTH_ATTS[language][self.month][attr] if self.month in self.MONTH_ATTS[language] else '...'
    
    # GREGORIAN METHODS ######################################################################################
    
    # FORMATTING METHODS ###########################################################################
    
    
    
# End of class UnivGREGORIAN #################################################################################################################

# Scientific measurement history for SI units
MEASUREMENT_HISTORY = {
    "meter_definition_1793": UnivGREGORIAN(
        1793, 3, 30, description="Original meter definition by French Academy"
    ),
    "atomic_second_1967": UnivGREGORIAN(
        1967, 10, 13, description="13th CGPM atomic second definition"
    ),
    "si_redefinition_2019": UnivGREGORIAN(
        2019, 5, 20, description="SI base units redefined by constants"
    ),
}







    # ########################################################################
    # # Construct SCIENTIFIC 
    # @classmethod
    # def SCIENTIFIC(cls, year: int, month: int, day: int, hour: int, minute: int, second: Union[int, float, str, Decimal],
    #     precision: Precision,        
    #     description: str = "", 
    #     confidence: float = None
    #     ) -> "UnivTimestamp":
    #     """Create timestamp for scientific measurements to seconds with microsecond precision"""
    #     if precision is None or PrecisionAtts[precision]['level'] < PrecisionAtts[Precision.SECOND]['level']:
    #         raise ValueError(f"Invalid precision {precision} for scientific timestamp. Must be SECOND to ATTOSECOND.")
    #     dv, tv = cls._construct_valid_365x12_dv_dt(UnivTimestamp._is_gregorian_leap_year, year, month, day, hour, minute, second)
    #     return cls(
    #         date_value=dv,
    #         time_value=tv,
    #         calendar=Calendar.SCIENTIFIC,
    #         precision=precision,
    #         accuracy=f"±{PrecisionAtts[precision]['abbrv']}",
    #         source_description=description,
    #         confidence_level=confidence,
    #     )

    # @classmethod
    # def SCIENTIFIC_from_datetime(cls, measurement_time: datetime,        
    #     description: str = "", 
    #     confidence: float = None
    #     ) -> "UnivTimestamp":
    #     """Create timestamp for scientific measurements to seconds with microsecond precision"""
    #     dv, tv = cls._construct_valid_365x12_dv_dt(UnivTimestamp._is_gregorian_leap_year, 
    #         measurement_time.year, 
    #         measurement_time.month, 
    #         measurement_time.day, 
    #         measurement_time.hour, 
    #         measurement_time.minute, 
    #         Decimal(measurement_time.second) + Decimal(measurement_time.microsecond) / Decimal(1e6)
    #     )
    #     # secs = Decimal(measurement_time.second) + Decimal(measurement_time.microsecond) / Decimal(1_000_000)
    #     # dv={'date': True, 'year': measurement_time.year, 'month': measurement_time.month, 'day': measurement_time.day}
    #     # tv={'time': True, 'hour': measurement_time.hour, 'minute': measurement_time.minute, 'second': secs}
    #     return cls(
    #         date_value=dv,
    #         time_value=tv,
    #         calendar=Calendar.SCIENTIFIC,
    #         precision=Precision.MICROSECOND,
    #         accuracy=f"±{PrecisionAtts[Precision.MICROSECOND]['abbrv']}",
    #         source_description=description,
    #         confidence_level=confidence,
    #     )


