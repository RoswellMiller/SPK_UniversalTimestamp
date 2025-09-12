import os
import json
import bisect
from decimal import Decimal
from typing import Union, Tuple, List
from SPK_UniversalTimestamp import UnivTimestamp, Calendar, CalendarAtts, Precision, PrecisionAtts

# Load geological time scale data from JSON file
cwd = os.getcwd()
with open('SPK_UniversalTimestamp\\geological-time-scale.json', 'r') as f:
    GEOLOGICAL_TIME_STRUCTURE = json.load(f)
    
GEOLOGICAL_EONS = []
GEOLOGICAL_ERAS = []
GEOLOGICAL_PERIODS = []
GEOLOGICAL_EPOCHSandAGES = []

class UnivGEOLOGICAL(UnivTimestamp):
    """
    This class represents a geological timestamp.
    """
    # __slots__ ####################################################################################
    
    # IMMUTABLE #######################################################################################
    
    # CONSTANTS #########################################################################################     
    
    # CONSTRUCTOR ######################################################################################
    def __init__(self, 
        years_ago: Union[int, float, str, Decimal],
        precision: Precision = Precision.MILLION_YEARS,
        accuracy: Decimal = None,
        description: str = ""
    ):
        """Create geological timestamp (years ago)"""
        if isinstance(years_ago, str):
            years_ago = -abs(Decimal(years_ago))
        elif isinstance(years_ago, (int, float)):
            years_ago = -abs(Decimal(str(years_ago)))
        elif isinstance(years_ago, Decimal):
            years_ago = -abs(years_ago)
        else:
            raise ValueError("years_ago must be an integer, float or decimal string")
        if precision is None or PrecisionAtts[precision]['level'] > PrecisionAtts[Precision.YEAR]['level']:
            raise ValueError(f"Invalid precision {precision} for geological time. Must be YEAR or higher.")
        power = PrecisionAtts[precision]['power']
        years_ago *= Decimal('1e' + str(power))  # Scale to the correct precision
        years_ago = int(years_ago)
        super().__init__(            
            Calendar.GEOLOGICAL,
            years_ago,
            precision=precision,
            accuracy=accuracy,
            description=description
            )
        try:
            self.rd = self._self_rata_die()
            self.sort  = super()._calc_sort_value()
        except Exception as e:
            raise ValueError(f"Failed to initialize sort value: {e}")

    # TIMESTAMP/RD METHODS ######################################################################################
    def _self_rata_die(self) -> int:
        """
        Convert the geological timestamp to Rata Die (fixed day number).
        For geological time, we assume a constant year length of 365.25 days.
        """
        return int(self.year * Decimal(365.25))  # * 1_00_00_00_000_000_000_000_000_000
    def _get_utc(self) -> Tuple[int, int, Decimal]:
        """
        Convert the time to UTC components (day_adjust, hour, minute, second).
        This method should be implemented in subclasses for specific calendar systems.
        """
        return 0, 0, 0, Decimal('0')

    def _calc_rata_die(self, year: int, month: int = 0, day: int = 0) -> int:
        """
        Convert geological date components (year) to Rata Die (fixed day number).
        For geological time, we assume a constant year length of 365.25 days.
        """
        return int(year * Decimal(365.25)) * 1_00_00_00_000_000_000_000_000_000

    # FORMATTING METHODS ########################################################################
    def __str__(self) -> str:
        return self.format_signature()

    def __repr__(self) -> str:
        """Create a string representation that could be used to recreate the object."""
        # Safely represent string attributes by escaping quotes and special characters
        power = PrecisionAtts[self.precision]['power']
        years_ago = str(self.year / Decimal('1e' + str(power)))  # Scale to the correct precision
        if '.' in years_ago:
            years_ago = years_ago.rstrip('0')
            if years_ago.endswith('.'):
                years_ago = years_ago[:-1]
        safe_accuracy = f"'{str(self.accuracy)}'" if self.accuracy is not None else "None"
        safe_description = repr(self.description)
        
        # Build the string with proper escaping
        result = ("{"
                f"'class':'UnivGEOLOGICAL',"
                f"'ca':'{self.calendar.name}',"
                f"'yr':{years_ago},"
                f"'pr':'{self.precision.name}',"
                f"'ac':{safe_accuracy},"
                f"'de':{safe_description}"
                "}")
        return result  
    
    def _strftime_month(self, seg_type : str, language :str, eliminate_leading_zero: bool = False) -> str:
        global GEOLOGICAL_EONS
        def key_func(x):
            return x['start']
        ins_pnt = bisect.bisect_left([key_func(item) for item in GEOLOGICAL_EONS], self) - 1
        if ins_pnt <0:
            return "before the big-bang"
        period = GEOLOGICAL_EONS[ins_pnt]
        return period['name'] if period else "Unknown eon"

    def _strftime_day(self, seg_type : str, language :str, eliminate_leading_zero: bool = False) -> str:
        global GEOLOGICAL_ERAS
        def key_func(x):
            return x['start']
        ins_pnt = bisect.bisect_left([key_func(item) for item in GEOLOGICAL_ERAS], self) - 1
        if ins_pnt <0:
            return "pre-eras"
        period = GEOLOGICAL_ERAS[ins_pnt]
        return period['name'] if period else "Unknown era"

    def _strftime_time(self, seg_type : str, language :str, eliminate_leading_zero: bool = False) -> str:
        global GEOLOGICAL_PERIODS, GEOLOGICAL_EPOCHSandAGES
        if seg_type == 'H':
            def key_func(x):
                return x['start']
            ins_pnt = bisect.bisect_left([key_func(item) for item in GEOLOGICAL_PERIODS], self) - 1
            if ins_pnt <0:
                return "pre-periods"
            period = GEOLOGICAL_PERIODS[ins_pnt]
            return period['name'] if period else "Unknown period"
        elif seg_type == 'M':
            def key_func(x):
                return x['start']
            ins_pnt = bisect.bisect_left([key_func(item) for item in GEOLOGICAL_EPOCHSandAGES], self) - 1
            if ins_pnt <0:
                return "pre-epochs"
            period = GEOLOGICAL_EPOCHSandAGES[ins_pnt]
            return period['name'] if period else "Unknown epoch"
        elif seg_type == 'S':
            pass
        return ""
    
    def _strftime_compound(self, seg_type : str, language :str, eliminate_leading_zero: bool = False) -> str:
        return ""

    def format_signature_date(self) -> str:
        """Format the date component based on calendar system and precision"""
        result = ""
        if self.year is None:
            return "Unknown year cannot be NoneType"
        if self.precision == Precision.BILLION_YEARS:
            result += f"{self.year / 1_000_000_000:.2f}"
        elif self.precision == Precision.MILLION_YEARS:
            result += f"{self.year / 1_000_000:.2f}" 
        elif self.precision == Precision.THOUSAND_YEARS:
            result += f"{self.year / 1_000:.2f}"
        elif self.precision == Precision.CENTURY:
            result += f"{self.year / 100:.2f}"
        elif self.precision == Precision.DECADE:
            result += f"{self.year / 10:.1f}"
        else:
            result+= f"{self.year}"
        result += f" {PrecisionAtts[self.precision]['abbrv']}"
        return result
    
    def format_signature(self, include_precision: bool = False, include_accuracy: bool = False, include_confidence: bool = False ) -> str:
        """Format complete timestamp for display"""
        date_part = self.format_signature_date()
        result = date_part
        # Add precision if requested
        if include_precision:
            result += f" ±1\u00B7{self.precision.value}"
        # Add accuracy if requested
        if include_accuracy and self.accuracy:
            result += f" [{self.accuracy}]"
        # Add confidence level if requested
        if include_confidence and self.confidence is not None:
            result += f" ({self.confidence:.1%})"
        return result
    
    ############################################################################################### 
    # Reference Roswell C. Miller extension to Rata Die for geological time


def main():
    global GEOLOGICAL_EONS, GEOLOGICAL_ERAS, GEOLOGICAL_PERIODS, GEOLOGICAL_EPOCHSandAGES
    # Created a start, end time sorted list of geological periods
    def create_eons(eons : List, eras : list, periods : List, epochs : List, start_date: "UnivGEOLOGICAL", eon_list : List)->"UnivGEOLOGICAL":       
        eon_end = float('-inf')
        for eon in eon_list:
            eon_name = eon.get('name', None)
            if eon_name is None:
                raise ValueError("Invalid file 'geological-time-scale.json' - missing eon name")
            eon_start = eon['start']
            if eon_start is None:
                raise ValueError(f"Eon {eon_name} has no start date")
            eon_start = UnivGEOLOGICAL(eon_start, precision=Precision.MILLION_YEARS, description=eon_name)   
            eon_end = eon.get('end', float('+inf'))
            if eon_end:
                eon_end = UnivGEOLOGICAL(eon_end, precision=Precision.MILLION_YEARS, description=eon_name)
            eons.append(
                { 
                    'type' : 'eon',
                    'name' : eon_name,
                    'start' : eon_start,
                    'end' : eon_end,
                })
            if 'eras' in eon:
                last_era = create_eras(eon_name, eras, periods, epochs, eon_start, eon.get('eras', []))
        return eon_end
        
    def create_eras(eon_name : str, eras : List, periods : List, epochs : List, start_date: "UnivGEOLOGICAL", era_list : List)->"UnivGEOLOGICAL":       
        era_end = float('-inf')
        for era in era_list:
            era_name = era.get('name', None)
            if era_name is None:
                raise ValueError(f"Invalid file 'geological-time-scale.json' - missing era name in {eon_name}")
            era_start = era['start']
            if era_start is None:
                raise ValueError(f"Era {era_name} has no start date")
            era_start = UnivGEOLOGICAL(era_start, precision=Precision.MILLION_YEARS, description=era_name)   
            era_end = era.get('end', float('+inf'))
            if era_end:
                era_end = UnivGEOLOGICAL(era_end, precision=Precision.MILLION_YEARS, description=era_name)
            eras.append(
                { 
                    'type' : 'era',
                    'name' : era_name,
                    'eon' : eon_name,
                    'start' : era_start,
                    'end' : era_end
                })
            if 'periods' in era:
                last_period = create_periods(era, era_name, periods, epochs, era_start, era.get('periods', []))
        return era_end
        
    def create_periods(eon_name : str, era_name, periods : List, epochs : List, start_date: "UnivGEOLOGICAL", period_list : List)->"UnivGEOLOGICAL":       
        period_end = float('-inf')
        for period in period_list:
            period_name = period.get('name', None)
            if period_name is None:
                raise ValueError(f"Invalid file 'geological-time-scale.json' - missing period name in {era_name}")
            period_start = period['start']
            if period_start is None:
                raise ValueError(f"Period {period_name} has no start date")
            period_start = UnivGEOLOGICAL(period_start, precision=Precision.MILLION_YEARS, description=period_name)   
            period_end = period.get('end', float('+inf'))
            if period_end:
                period_end = UnivGEOLOGICAL(period_end, precision=Precision.MILLION_YEARS, description=period_name)
            periods.append(
                { 
                    'type' : 'period',
                    'name' : period_name,
                    'eon' : eon_name,
                    'era' : era_name,
                    'start' : period_start,
                    'end' : period_end
                })
            if 'epochs' in period:
                last_period = create_epochs(eon_name, era_name, period_name, epochs, period_start, period.get('epochs', []))
        return period_end
        
    def create_epochs(eon_name : str, era_name, period_name : str, epochs : List, start_date: "UnivGEOLOGICAL", epoch_list : List)->"UnivGEOLOGICAL":       
        epoch_end = float('-inf')
        for epoch in epoch_list:
            epoch_name = epoch.get('name', None)
            if epoch_name is None:
                raise ValueError(f"Invalid file 'geological-time-scale.json' - missing period name in {era_name}")
            epoch_start = epoch['start']
            if epoch_start is None:
                raise ValueError(f"Period {epoch_name} has no start date")
            epoch_start = UnivGEOLOGICAL(epoch_start, precision=Precision.MILLION_YEARS, description=epoch_name)   
            epoch_end = epoch.get('end', float('+inf'))
            if epoch_end:
                epoch_end = UnivGEOLOGICAL(epoch_end, precision=Precision.MILLION_YEARS, description=epoch_name)
                
            if 'ages' in epoch:
                last_age = create_ages(eon_name, era_name, period_name, epoch_name, epochs, epoch_start, epoch.get('ages', []))
            else:
                epochs.append(
                    { 
                        'type' : 'period',
                        'name' : epoch_name,
                        'eon' : eon_name,
                        'era' : era_name,
                        'period' : period_name,
                        'start' : epoch_start,
                        'end' : epoch_end
                    })
        return epoch_end
        
    def create_ages(eon_name : str, era_name : str, period_name : str, epoch_name : str, epochs : List, start_date: "UnivGEOLOGICAL", ages_list : List)->"UnivGEOLOGICAL":       
        age_end = float('-inf')
        for age in ages_list:
            age_name = age.get('name', None)
            if age_name is None:
                raise ValueError(f"Invalid file 'geological-time-scale.json' - missing age name in {epoch_name}")
            age_start = age['start']
            if age_start is None:
                raise ValueError(f"Period {age_name} has no start date")
            age_start = UnivGEOLOGICAL(age_start, precision=Precision.MILLION_YEARS, description=age_name)   
            age_end = age.get('end', float('+inf'))
            if age_end:
                age_end = UnivGEOLOGICAL(age_end, precision=Precision.MILLION_YEARS, description=age_name)
                
            epochs.append(
                { 
                    'type' : 'epoch-age',
                    'name' : epoch_name.lower() + ' ' + age_name,
                    'eon' : eon_name,
                    'era' : era_name,
                    'period' : period_name,
                    'epoch' : epoch_name,
                    'start' : age_start,
                    'end' : age_end
                })
        return age_end
        
        
    GEOLOGICAL_EONS = []
    GEOLOGICAL_ERAS = []
    GEOLOGICAL_PERIODS = []
    GEOLOGICAL_EPOCHSandAGES = []
    
    begin_earth = UnivGEOLOGICAL(4550, Precision.MILLION_YEARS, Decimal('0.01'), "Earth formation era")
    pre_cam = GEOLOGICAL_TIME_STRUCTURE.get('pre-phanerozoic', [None])[0]
    last_date = create_eons(GEOLOGICAL_EONS, GEOLOGICAL_ERAS, GEOLOGICAL_PERIODS, GEOLOGICAL_EPOCHSandAGES, begin_earth, pre_cam.get('eons', []))
    last_date = create_eons(GEOLOGICAL_EONS, GEOLOGICAL_ERAS, GEOLOGICAL_PERIODS, GEOLOGICAL_EPOCHSandAGES, last_date, GEOLOGICAL_TIME_STRUCTURE.get('eons', []))
    
    # Sort end date, then start date 
    GEOLOGICAL_EONS.sort(key=lambda period: period['end'].sort if period['end'] else float('-inf'))
    GEOLOGICAL_EONS.sort(key=lambda period: period['start'].sort if period['start'] else float('-inf'))   
    return
 
try:  
    main()
except Exception as e:
    print(f"Error creating geological periods: {e}")
    print("Please check the geological time scale JSON file for correctness.")

# Predefined geological periods
# GEOLOGICAL_PERIODS = {
#     "Hadean": UnivGEOLOGICAL(
#         4540, Precision.MILLION_YEARS, "±1%", "Earth formation era"
#     ),
#     "Archean": UnivGEOLOGICAL(
#         4000, Precision.MILLION_YEARS, "±2%", "Early life era"
#     ),
#     "Proterozoic": UnivGEOLOGICAL(
#         2500, Precision.MILLION_YEARS, "±1%", "Complex cells era"
#     ),
#     "Phanerozoic": UnivGEOLOGICAL(
#         541, Precision.MILLION_YEARS, "±0.5%", "Visible life era"
#     ),
#     "Paleozoic": UnivGEOLOGICAL(
#         541, Precision.MILLION_YEARS, "±0.5%", "Ancient life era"
#     ),
#     "Mesozoic": UnivGEOLOGICAL(
#         252, Precision.MILLION_YEARS, "±0.3%", "Middle life era"
#     ),
#     "Cenozoic": UnivGEOLOGICAL(
#         66, Precision.MILLION_YEARS, "±0.1%", "Recent life era"
#     ),
#     "Quaternary": UnivGEOLOGICAL(
#         "2.6", Precision.THOUSAND_YEARS, "±1%", "Ice age era"
#     ),
#     "Holocene": UnivGEOLOGICAL(
#         11700, Precision.YEAR, "±50 years", "Human civilization era"
#     ),
# }
