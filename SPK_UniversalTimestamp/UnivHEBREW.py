from decimal import Decimal
from typing import Union, Tuple, List

from .CC08_Hebrew import * #last_hebrew_month_of_year, last_day_of_hebrew_month, rd_from_hebrew, hebrew_from_rd

from SPK_UniversalTimestamp import Calendar, Precision
from SPK_UniversalTimestamp import UnivCalendars


class UnivHEBREW(UnivCalendars):
    """
    This class represents a Hebrew timestamp.
    It inherits from the UnivTimestamp class and is used to handle
    Hebrew calendar data.
    """
    # __slots__ ####################################################################################
    
    # IMMUTABLE #######################################################################################
    
    # CONSTANTS #########################################################################################
    MONTH_ATTS = {
        'en': {
            months.NISAN.value: {'name': "Nisan", 'abbrv': "Nis", 'days': 30},
            months.IYYAR.value: {'name': "Iyyar", 'abbrv': "Iyy", 'days': 29},
            months.SIVAN.value: {'name': "Sivan", 'abbrv': "Siv", 'days': 30},
            months.TAMMUZ.value: {'name': "Tammuz", 'abbrv': "Tam", 'days': 29},
            months.AV.value: {'name': "Av", 'abbrv': "Av", 'days': 30},
            months.ELUL.value: {'name': "Elul", 'abbrv': "Elu", 'days': 29},
            months.TISHRI.value: {'name': "Tishri", 'abbrv': "Tis", 'days': 30},
            months.MARHESHVAN.value: {'name': "Marheshvan", 'abbrv': "Mar", 'days': 29},  # or 30
            months.KISLEV.value: {'name': "Kislev", 'abbrv': "Kis", 'days': 30},  # or 29
            months.TEVET.value: {'name': "Tevet", 'abbrv': "Tev", 'days': 29},
            months.SHEVAT.value: {'name': "Shevat", 'abbrv': "She", 'days': 30},
            months.ADAR_I.value: {'name': "Adar I", 'abbrv': "Ad1", 'days': 30},  # in leap years
            months.ADAR_II.value: {'name': "Adar II", 'abbrv': "Ad2", 'days': 29}   # in leap years
        },
        'fr': {
            months.NISAN.value: {'name': "Nissan", 'abbrv': "Nis", 'days': 30},
            months.IYYAR.value: {'name': "Iyar", 'abbrv': "Iyy", 'days': 29},
            months.SIVAN.value: {'name': "Sivan", 'abbrv': "Siv", 'days': 30},
            months.TAMMUZ.value: {'name': "Tammouz", 'abbrv': "Tam", 'days': 29},
            months.AV.value: {'name': "Av", 'abbrv': "Av", 'days': 30},
            months.ELUL.value: {'name': "Eloul", 'abbrv': "Elu", 'days': 29},
            months.TISHRI.value: {'name': "Tichri", 'abbrv': "Tis", 'days': 30},
            months.MARHESHVAN.value: {'name': "Marheshvan", 'abbrv': "Mar", 'days': 29},  # or 30
            months.KISLEV.value: {'name': "Kislev", 'abbrv': "Kis", 'days': 30},  # or 29
            months.TEVET.value: {'name': "Tevet", 'abbrv': "Tev", 'days': 29},
            months.SHEVAT.value: {'name': "Shevat", 'abbrv': "She", 'days': 30},
            months.ADAR_I.value: {'name': "Adar I", 'abbrv': "Ad1", 'days': 30},  # in leap years
            months.ADAR_II.value: {'name': "Adar II", 'abbrv': "Ad2", 'days': 29}   # in leap years
        },
        'es': {
            months.NISAN.value: {'name': "Nisán", 'abbrv': "Nis", 'days': 30},
            months.IYYAR.value: {'name': "Iyar", 'abbrv': "Iyy", 'days': 29},
            months.SIVAN.value: {'name': "Siván", 'abbrv': "Siv", 'days': 30},
            months.TAMMUZ.value: {'name': "Tamuz", 'abbrv': "Tam", 'days': 29},
            months.AV.value: {'name': "Av", 'abbrv': "Av", 'days': 30},
            months.ELUL.value: {'name': "Elul", 'abbrv': "Elu", 'days': 29},
            months.TISHRI.value: {'name': "Tishri", 'abbrv': "Tis", 'days': 30},
            months.MARHESHVAN.value: {'name': "Marheshván", 'abbrv': "Mar", 'days': 29},  # or 30
            months.KISLEV.value: {'name': "Kislev", 'abbrv': "Kis", 'days': 30},  # or 29
            months.TEVET.value: {'name': "Tevet", 'abbrv': "Tev", 'days': 29},
            months.SHEVAT.value: {'name': "Shevat", 'abbrv': "She", 'days': 30},
            months.ADAR_I.value: {'name': "Adar I", 'abbrv': "Ad1", 'days': 30},  # in leap years
            months.ADAR_II.value: {'name': "Adar II", 'abbrv': "Ad2", 'days': 29}   # in leap years
        },
        'de': {
            months.NISAN.value: {'name': "Nisan", 'abbrv': "Nis", 'days': 30},
            months.IYYAR.value: {'name': "Ijar", 'abbrv': "Iyy", 'days': 29},
            months.SIVAN.value: {'name': "Siwan", 'abbrv': "Siv", 'days': 30},
            months.TAMMUZ.value: {'name': "Tammus", 'abbrv': "Tam", 'days': 29},
            months.AV.value: {'name': "Aw", 'abbrv': "Av", 'days': 30},
            months.ELUL.value: {'name': "Elul", 'abbrv': "Elu", 'days': 29},
            months.TISHRI.value: {'name': "Tischri", 'abbrv': "Tis", 'days': 30},
            months.MARHESHVAN.value: {'name': "Marheschwan", 'abbrv': "Mar", 'days': 29},  # or 30
            months.KISLEV.value: {'name': "Kislew", 'abbrv': "Kis", 'days': 30},  # or 29
            months.TEVET.value: {'name': "Tevet", 'abbrv': "Tev", 'days': 29},
            months.SHEVAT.value: {'name': "Schewat", 'abbrv': "She", 'days': 30},
            months.ADAR_I.value: {'name': "Adar I", 'abbrv': "Ad1", 'days': 30},  # in leap years
            months.ADAR_II.value: {'name': "Adar II", 'abbrv': "Ad2", 'days': 29}   # in leap years
        },
        'it': {
            months.NISAN.value: {'name': "Nisàn", 'abbrv': "Nis", 'days': 30},
            months.IYYAR.value: {'name': "Iyar", 'abbrv': "Iyy", 'days': 29},
            months.SIVAN.value: {'name': "Sivàn", 'abbrv': "Siv", 'days': 30},
            months.TAMMUZ.value: {'name': "Tamuz", 'abbrv': "Tam", 'days': 29},
            months.AV.value: {'name': "Av", 'abbrv': "Av", 'days': 30},
            months.ELUL.value: {'name': "Elul", 'abbrv': "Elu", 'days': 29},
            months.TISHRI.value: {'name': "Tishrì", 'abbrv': "Tis", 'days': 30},
            months.MARHESHVAN.value: {'name': "Marhesvan", 'abbrv': "Mar", 'days': 29},  # or 30
            months.KISLEV.value: {'name': "Kislev", 'abbrv': "Kis", 'days': 30},  # or 29
            months.TEVET.value: {'name': "Tevet", 'abbrv': "Tev", 'days': 29},
            months.SHEVAT.value: {'name': "Shevat", 'abbrv': "She", 'days': 30},
            months.ADAR_I.value: {'name': "Adar I", 'abbrv': "Ad1", 'days': 30},  # in leap years
            months.ADAR_II.value: {'name': "Adar II", 'abbrv': "Ad2", 'days': 29}   # in leap years
        }
    }
    
    # CONSTRUCTOR ######################################################################################
    # Each tuple: (slot name, allowed_types, valid_function, precision_enum)
    def _last_month_of_year(year: int) -> int:
        return last_hebrew_month_of_year(year)
    def _last_day_of_month(year: int, month: int) -> int:
        return last_day_of_hebrew_month(year, month)
    CNST_ARGS = [
        ("year",   (int,), lambda arg, *_: (1 <= arg <= 9999), Precision.YEAR),
        ("month",  (int,), lambda arg, v: (1 <= arg <= UnivHEBREW._last_month_of_year(v['year'])), Precision.MONTH),
        ("day",    (int,), lambda arg, v: (1 <= arg <= UnivHEBREW._last_day_of_month(v['year'], v['month'])),  Precision.DAY),
        ("hour",   (int,), lambda arg, *_: (0 <= arg <= 23), Precision.HOUR),
        ("minute", (int,), lambda arg, *_: (0 <= arg <= 59), Precision.MINUTE),
        ("second", (Union[int, Decimal],), lambda arg, *_: (Decimal("0") <= arg < Decimal("60")), Precision.SECOND),
    ]
    def __init__(self, *args, timezone: str = 'UTC', fold: int = 0,
        precision: Precision = None,
        accuracy: Decimal = None,
        description: str = ""
    ):
        """Create Hebrew timestamp"""
        v_args, precision = self._init_validate_constructor_args(1, args, precision)
        super().__init__(
            Calendar.HEBREW,
            v_args['year'], v_args['month'], v_args['day'], v_args['hour'], v_args['minute'], v_args['second'], timezone=timezone, fold=fold,
            precision=precision,
            accuracy=accuracy,
            description=description  
            )
    
    # TIMESTAMP METHODS ######################################################################################
    def _self_rata_die(self) -> int:
        return rd_from_hebrew(self.year, self.month, self.day)

    def _calc_rata_die(self, year, month, day) -> int:
        return rd_from_hebrew(year, month, day)

    # CALENDARS METHODS ######################################################################################
    def _calc_date_from_rd(self, rd: int) -> Tuple[int, int, int]:
        """
        Convert Rata Die (rd) fixed day number to Hebrew date
        "Calendrical Calculations" by Reingold and Dershowitz pp 59-63
        """
        return hebrew_from_rd(rd)

    def month_attr(self, attr : str, language : str='en') -> Union[int, str]:
        """
        Get a month attribute.
        """
        return self.MONTH_ATTS[language][self.month][attr] if self.month in self.MONTH_ATTS[language] else '...'
    

    # HEBREW METHODS ######################################################################################
    
    ############################################################################
    @staticmethod
    def failure_analysis(failure_list: List[Tuple[int, str, int, int, int]]) -> None:
        def tf(v : bool) -> str: return 'T' if v else 'F'
        """Analyze failures in Hebrew calendar tests"""
        print("\nFailure Analysis:")
        print("-" * 20)
        for i, calendar, year, month, day in failure_list:
            print(f"Failure {i:2d}: {calendar:<15} - {year:5d}-{month:02d}-{day:02d}"
                    + f" {tf(UnivHEBREW._is_leap_year(year)):^1}"
                    + f" {UnivHEBREW._days_in_year(year):3d}"
                    + f" {tf(UnivHEBREW._is_long_marheshvan(year)):^1}"
                    + f" {tf(UnivHEBREW._is_short_kislev(year)):^1}"
                    + f" {UnivHEBREW._last_day_of_month(year, month):2d}"
                    + f" {UnivHEBREW._new_year(year):5d}"
                    )
        print("End of failure analysis.")

    # End of class UnivHEBREW #########################################################################