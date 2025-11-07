import re
import ast
from typing import Union
from abc import abstractmethod

from decimal import Decimal, ROUND_DOWN
from datetime import datetime, timezone
from SPK_UniversalTimestamp.CC02_Gregorian import gregorian_from_rd
from SPK_UniversalTimestamp.CC03_Julian import julian_from_rd
from SPK_UniversalTimestamp.CC08_Hebrew import hebrew_from_rd
from SPK_UniversalTimestamp.CC19_Chinese_1645 import chinese_from_rd

from SPK_UniversalTimestamp import UnivTimestamp, Calendar, Precision, Epoch_rd
from SPK_UniversalTimestamp.UnivGEOLOGICAL import UnivGEOLOGICAL
from SPK_UniversalTimestamp.UnivGREGORIAN import UnivGREGORIAN
from SPK_UniversalTimestamp.UnivJULIAN import UnivJULIAN
from SPK_UniversalTimestamp.UnivHEBREW import UnivHEBREW
from SPK_UniversalTimestamp.UnivCHINESE import UnivCHINESE

# Centralized time stamp converter/special purpose constructors factory
class UnivTimestampFactory:
    """
    Factory class for creating and converting UnivTimestamp instances.
    This class provides static methods to create timestamps in various calendar systems
    and to convert between different calendar systems.
    NOTE : This is an abstract base class and should not be instantiated directly.
    """
    @staticmethod 
    def __version__():
        return "1.0.1-beta"
    @staticmethod
    def __file__():
        return "SPK_UniversalTimestamp\\UnivTimestampFactory.py"
    @abstractmethod
    def __init__(self):
        pass
    @staticmethod
    def beginning_of_time() -> "UnivTimestamp":
        """Get the beginning of time in the Gregorian calendar."""
        return UnivGEOLOGICAL('-Infinity', description="Beginning of Time")
    @staticmethod
    def now() -> "UnivTimestamp":
        """Get the current timestamp in the Gregorian calendar."""
        dt = datetime.now(timezone.utc)
        return UnivGREGORIAN(dt.year, dt.month, dt.day, dt.hour, dt.minute, Decimal(dt.second) + Decimal(dt.microsecond) / 1_000_000, precision=Precision.MICROSECOND)
    # Dictionary of conversion functions
    @staticmethod
    def convert(to_calendar, from_timestamp) -> "UnivTimestamp":
        """Convert any timestamp to any other calendar system"""
        if from_timestamp.calendar == to_calendar:
            return from_timestamp
            
        converters = {
            Calendar.GREGORIAN: UnivTimestampFactory._to_gregorian,
            Calendar.JULIAN: UnivTimestampFactory._to_julian,
            Calendar.HEBREW: UnivTimestampFactory._to_hebrew,
            Calendar.CHINESE: UnivTimestampFactory._to_chinese
            # Add all other converters here
        }
        
        # Get the appropriate converter function
        converter = converters.get(to_calendar)
        if converter:
            return converter(from_timestamp)
        else:
            raise ValueError(f"Conversion from {from_timestamp.calendar} to {to_calendar} not supported")
        
    # convert to GREGORIAN from another calendar
    @staticmethod
    def _to_gregorian(from_timestamp : "UnivTimestamp") -> "UnivTimestamp":
        """Convert from Julian calendar to Gregorian"""
        if from_timestamp.calendar == Calendar.GREGORIAN:
            return from_timestamp
        rd = from_timestamp.rd
        year, month, day = gregorian_from_rd(rd)
        return UnivGREGORIAN(
            year, month, day, from_timestamp.hour, from_timestamp.minute, from_timestamp.second,
            precision=from_timestamp.precision,
            accuracy=from_timestamp.accuracy,
            description=from_timestamp.description
        )

    # convert to JULIAN from another calendar
    @staticmethod
    def _to_julian(from_timestamp) -> "UnivJULIAN":
        """Convert to Julian calendar (Old Style)"""
        if from_timestamp.calendar == Calendar.JULIAN:
            return from_timestamp
        rd  = from_timestamp.rd
        year, month, day = julian_from_rd(rd)
        return UnivJULIAN(
            year, month, day, from_timestamp.hour, from_timestamp.minute, from_timestamp.second,
            precision=from_timestamp.precision,
            accuracy=from_timestamp.accuracy,
            description=from_timestamp.description
        )
        
    # convert to JULIAN from another calendar
    @staticmethod
    def _to_hebrew(from_timestamp) -> "UnivHEBREW":
        """Convert to Hebrew calendar"""
        if from_timestamp.calendar == Calendar.HEBREW:
            # Already in HEBREW calendar, return self
            return from_timestamp
        rd  = from_timestamp.rd
        year, month, day = hebrew_from_rd(rd)
        return UnivHEBREW(
            year, month, day, from_timestamp.hour, from_timestamp.minute, from_timestamp.second,
            precision=from_timestamp.precision,
            accuracy=from_timestamp.accuracy,
            description=from_timestamp.description
        )

    # convert to CHINESE from another calendar
    @staticmethod
    def _to_chinese(from_timestamp) -> "UnivCHINESE":
        """Convert to Hebrew calendar"""
        if from_timestamp.calendar == Calendar.CHINESE:
            # Already in CHINESE calendar, return self
            return from_timestamp
        rd  = from_timestamp.rd
        cycle, year, month, leap, day = chinese_from_rd(rd)
        return UnivCHINESE(
            cycle, year, month, leap, day, from_timestamp.hour, from_timestamp.minute, from_timestamp.second,
            precision=from_timestamp.precision,
            accuracy=from_timestamp.accuracy,
            description=from_timestamp.description
        )

        # Enhanced time patterns

    # ISO 8601 patterns
    _ISO_8601_PATTERNS = [
        # ISO 8601 with time
        (
            r"(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})\.(\d{3})",
            lambda m, accuracy=None, confidence=None, description="" : UnivGREGORIAN(
                int(m.group(1)),
                int(m.group(2)),
                int(m.group(3)),
                int(m.group(4)),
                int(m.group(5)),
                float(f"{m.group(6)}.{m.group(7)}"),
                precision=Precision.MILLISECOND,
                accuracy=accuracy,
                confidence=confidence,
                description=description,
            ),
        ),
        (
            r"(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})",
            lambda m, accuracy=None, confidence=None, description="" : UnivGREGORIAN(
                int(m.group(1)),
                int(m.group(2)),
                int(m.group(3)),
                int(m.group(4)),
                int(m.group(5)),
                int(m.group(6)),
                precision=Precision.SECOND,
                accuracy=accuracy,
                confidence=confidence,
                description=description,
            ),
        ),
        # Space-separated datetime
        (
            r"(\d{4})-(\d{2})-(\d{2})\s+(\d{2}):(\d{2}):(\d{2})\.(\d{3})",
            lambda m, accuracy=None, confidence=None, description="" : UnivGREGORIAN(
                int(m.group(1)),
                int(m.group(2)),
                int(m.group(3)),
                int(m.group(4)),
                int(m.group(5)),
                Decimal(f"{m.group(6)}.{m.group(7)}"),
                precision=Precision.MILLISECOND,
                accuracy=accuracy,
                confidence=confidence,
                description=description,
            ),
        ),
        (
            r"(\d{4})-(\d{2})-(\d{2})\s+(\d{2}):(\d{2}):(\d{2})",
            lambda m, accuracy=None, confidence=None, description="" : UnivGREGORIAN(
                int(m.group(1)),
                int(m.group(2)),
                int(m.group(3)),
                int(m.group(4)),
                int(m.group(5)),
                int(m.group(6)),
                precision=Precision.SECOND,
                accuracy=accuracy,
                confidence=confidence,
                description=description,
            ),
        ),
    ]

    # Geological time patterns
    _GEOLOGICAL_PATTERNS = [
        (
            r"(\d+\.?\d*)\s*BYA",
            lambda m, accuracy=None, confidence=None, description="": UnivGEOLOGICAL(
                Decimal(m.group(1)),
                precision=Precision.BILLIION_YEARS,
                accuracy=accuracy,
                confidence=confidence,
                description=description,
            ),
        ),
        (
            r"(\d+\.?\d*)\s*MYA",
            lambda m, accuracy=None, confidence=None, description="": UnivGEOLOGICAL(
                Decimal(m.group(1)),
                precision=Precision.MILLION_YEARS,
                accuracy=accuracy,
                confidence=confidence,
                description=description,
            ),
        ),
        (
            r"(\d+\.?\d*)\s*KYA",
            lambda m, accuracy=None, confidence=None, description="" : UnivGEOLOGICAL(
                Decimal(m.group(1)),
                precision=Precision.THOUSAND_YEARS,
                accuracy=accuracy,
                confidence=confidence,
                description=description,
            ),
        ),
    ]

    # Human calendar patterns
    _HUMAN_CALENDAR_PATTERNS = [
        # Gregorian
        (
            r"(\d{1,4})\s*BCE",
            lambda m, accuracy=None, confidence=None, description="" : UnivGREGORIAN(
                -int(m.group(1)), 
                None, 
                None,
                precision=Precision.YEAR,
                accuracy=accuracy,
                confidence=confidence,
                description=description,
            ),
        ),
        (
            r"(\d{1,4})\s*BCE-(\d{1,2})",
            lambda m, accuracy=None, description="" : UnivGREGORIAN(
                -int(m.group(1)), 
                int(m.group(2)), 
                None,
                precision=Precision.MONTH,
                accuracy=accuracy,
                description=description,
            ),
        ),
        (
            r"(\d{1,4})\s*BCE-(\d{1,2})-(\d{1,2})",
            lambda m, accuracy=None, description="" : UnivGREGORIAN(
                -int(m.group(1)), 
                int(m.group(2)), 
                int(m.group(3)),
                precision=Precision.DAY,
                accuracy=accuracy,
                description=description,
            ),
        ),
        (
            r"([+-]?\d{1,4})-(\d{1,2})-(\d{1,2})",
            lambda m, accuracy=None, description="" : UnivGREGORIAN(
                int(m.group(1)), 
                int(m.group(2)), 
                int(m.group(3)),
                precision=Precision.DAY,
                accuracy=accuracy,
                description=description,
            ),
        ),
        (
            r"([+-]?\d{1,4})-(\d{1,2})",
            lambda m, accuracy=None, description="" : UnivGREGORIAN(
                int(m.group(1)), 
                int(m.group(2)), 
                None,
                precision=Precision.MONTH,
                accuracy=accuracy,
                description=description,
            ),
        ),
        (
            r"([+-]?\d{1,4})",
            lambda m, accuracy=None, description="" : UnivGREGORIAN(
                int(m.group(1)), 
                None, 
                None,
                precision=Precision.YEAR,
                accuracy=accuracy,
                description=description,
            ),
        ),
        # Julian calendar
        (
            r"(\d{1,4})\s*bc-(\d{1,2})-(\d{1,2})",
            lambda m, accuracy=None, description="" : UnivJULIAN(
                -int(m.group(1)), 
                int(m.group(2)), 
                int(m.group(3)),
                accuracy=accuracy,
                description=description,
            ),
        ),
        (
            r"(\d{1,4})\s*bc-(\d{1,2})",
            lambda m, accuracy=None, description="" : UnivJULIAN(
                -int(m.group(1)), 
                int(m.group(2)), 
                None,
                accuracy=accuracy,
                description=description,
            ),
        ),
        (
            r"(\d{1,4})\s*bc",
            lambda m, accuracy=None, description="" : UnivJULIAN(
                -int(m.group(1)), 
                None, 
                None,
                accuracy=accuracy,
                description=description,
            ),
        ),
        (
            r"(\d{1,4})\s*bc-(\d{1,2})-(\d{1,2})\s*(OS|JC)",
            lambda m, accuracy=None, description="" : UnivJULIAN(
                -int(m.group(1)), 
                int(m.group(2)), 
                int(m.group(3)),
                accuracy=accuracy,
                description=description,
            ),
        ),
        (
            r"(\d{1,4})\s*bc-(\d{1,2})\s*(OS|JC)",
            lambda m, accuracy=None, description="" : UnivJULIAN(
                -int(m.group(1)), 
                int(m.group(2)), 
                None,
                accuracy=accuracy,
                description=description,
            ),
        ),
        (
            r"(\d{1,4})\s*bc\s*(OS|JC)",
            lambda m, accuracy=None, confidence=None, description="" : UnivJULIAN(
                -int(m.group(1)), 
                None, 
                None,
                accuracy=accuracy,
                confidence=confidence,
                description=description,
            ),
        ),
        (
            r"([+-]?\d{1,4})-(\d{1,2})-(\d{1,2})\s*(OS|JC)",
            lambda m, accuracy=None, description="" : UnivJULIAN(
                int(m.group(1)), 
                int(m.group(2)), 
                int(m.group(3)),
                accuracy=accuracy,
                description=description,
            ),
        ),
        (
            r"([+-]?\d{1,4})-(\d{1,2})\s*(OS|JC)",
            lambda m, accuracy=None, description="" : UnivJULIAN(
                int(m.group(1)), 
                int(m.group(2)), 
                None,
                accuracy=accuracy,
                description=description,
            ),
        ),
        (
            r"([+-]?\d{1,4})\s*(OS|JC)",
            lambda m, accuracy=None, description="" : UnivJULIAN(
                -int(m.group(1)), 
                None, 
                None,
                accuracy=accuracy,
                description=description,
            ),
        ),
        
        
        # Hebrew calendar
        (
            r"(\d{1,4})\s*AM",
            lambda m, accuracy=None, description="" : UnivHEBREW(
                int(m.group(1)),
                None, 
                None,
                accuracy=accuracy,
                description=description,
            ),
        ),
        (
            r"(\d{1,4})-(\d+)\s*AM",
            lambda m, accuracy=None, description="" : UnivHEBREW(
                int(m.group(1)), 
                int(m.group(2)), 
                None,
                accuracy=accuracy,
                description=description,
            ),
        ),
        (
            r"(\d{1,4})-(\d+)-(\d+)\s*AM",
            lambda m, accuracy=None, description="" : UnivHEBREW(
                int(m.group(1)), 
                int(m.group(2)), 
                int(m.group(3)),
                accuracy=accuracy,
                description=description,
            ),
        ),
    ]

    # Try all pattern groups in order of specificity
    _ALL_PATTERNS = (
        _HUMAN_CALENDAR_PATTERNS
        + _GEOLOGICAL_PATTERNS
        + _ISO_8601_PATTERNS
    )

    @staticmethod
    def parse(timestamp_str: str, accuracy : str = None, description : str = "") -> "UnivTimestamp":
        """Parse all time scales: geological, astronomical, and human calendars"""
        timestamp_str = timestamp_str.strip()

        for pattern, converter in UnivTimestampFactory._ALL_PATTERNS:
            match = re.fullmatch(pattern, timestamp_str)
            if match:
                try:
                    return converter(match, accuracy=accuracy, description=description)
                except Exception:
                    continue

        return None

    def parse_repr(repr_str) -> "UnivTimestamp":
        """Parse a timestamp representation created with __repr__"""
        try:
            # Use ast.literal_eval to safely parse the dictionary
            data = ast.literal_eval(repr_str)
            data['ac'] = None if data['ac'] is None else Decimal(data['ac'])
            data['sc'] = None if data['sc'] is None else Decimal(data['sc'])
            # Convert string enum names back to enum values
            calendar = Calendar[data['ca']]
            precision = Precision[data['pr']]
            
            if calendar == Calendar.GEOLOGICAL:
                return UnivGEOLOGICAL(
                    data['yr'],
                    precision=precision,
                    accuracy=data['ac'],
                    description=data['de']
                )
            elif calendar == Calendar.GREGORIAN:
                return UnivGREGORIAN(
                    data['yr'],
                    data['mo'],
                    data['da'],
                    data['hr'],
                    data['mi'],
                    data['sc'],
                    timezone=data['tz'],
                    fold=data['fo'],
                    precision=precision,
                    accuracy=data['ac'],
                    description=data['de']
                )
            elif calendar == Calendar.JULIAN:
                return UnivJULIAN(
                    data['yr'],
                    data['mo'],
                    data['da'],
                    data['hr'],
                    data['mi'],
                    data['sc'],
                    timezone=data['tz'],
                    fold=data['fo'],
                    precision=precision,
                    accuracy=data['ac'],
                    description=data['de']
                )
            elif calendar == Calendar.HEBREW:
                return UnivHEBREW(
                    data['yr'],
                    data['mo'],
                    data['da'],
                    data['hr'],
                    data['mi'],
                    data['sc'],
                    timezone=data['tz'],
                    fold=data['fo'],
                    precision=precision,
                    accuracy=data['ac'],
                    description=data['de']
                )
            elif calendar == Calendar.CHINESE:
                cycle, year = UnivCHINESE.cycle_year(data['yr'])
                return UnivCHINESE(
                    cycle,
                    year,
                    data['mo'],
                    data['da'],
                    data['hr'],
                    data['mi'],
                    data['sc'],
                    timezone=data['tz'],
                    fold=data['fo'],
                    precision=precision,
                    accuracy=data['ac'],
                    description=data['de']
                )
            else:
                raise ValueError(f"Unsupported calendar type: {calendar}")      
        except (SyntaxError, ValueError, KeyError) as e:
            print(f"Error parsing repr string: {e}")
            return None

    # from Microsoft datetime
    @staticmethod
    def from_ms_datetime(
        datetime_stamp: datetime, 
        description: str = ""
    
        ) -> "UnivGREGORIAN":
        """Create from Gregorian timestamp from a ms- datetime"""
        year = datetime_stamp.year
        month = datetime_stamp.month    
        day = datetime_stamp.day
        hour = datetime_stamp.hour
        minute = datetime_stamp.minute           
        secs = Decimal(datetime_stamp.second) + Decimal(datetime_stamp.microsecond) / Decimal(1_000_000)
        return UnivGREGORIAN(
            year, month, day, hour, minute, secs,
            precision=Precision.MICROSECOND,
            accuracy=Decimal('0.001'),
            description=f"{description} ({abs(year)} CE)"
            if description else f"{abs(year)} CE",
        
        )
    # from UNIX timestamp
    @staticmethod
    def from_unix_timestamp( 
        timestamp: float,
        description: str = ""
    ):
        """Create from Unix timestamp with nanosecond precision"""
        # Process the integer part to year, month, day, hour, minute, second
        date_ts = int(timestamp)
        moment_from_unix = Epoch_rd['unix'] + date_ts // (24 * 60 * 60)
        year, month, day = gregorian_from_rd(moment_from_unix)
        time_ts = date_ts % (24 * 60 * 60)
        hour_ts = time_ts // 3600
        time_ts %= 3600
        min_ts = time_ts // 60
        time_ts %= 60
        sec_ts = time_ts
        timestamp = Decimal(str(timestamp)).quantize(Decimal('1e-9'), rounding=ROUND_DOWN)
        frac_ts = timestamp % 1
        sec_frac_ts = Decimal(sec_ts) + frac_ts
        return UnivGREGORIAN(
            year, month, day, hour_ts, min_ts, sec_frac_ts,
            precision=Precision.NANOSECOND,
            accuracy=Decimal('0.001'),
            description=description,
        )
    @staticmethod
    def for_SCIENTIFIC(
            year: Union[int, Decimal],
            month: int,    
            day: int,
            hour: int,
            minute: int,
            second: Union[int, str, Decimal],
            description: str = ""
        ) -> "UnivGREGORIAN":
        """
        Create a scientific timestamp with attosecond precision.
        """
        return UnivGREGORIAN(
            year, month, day, hour, minute, second,
            precision=Precision.ATTOSECOND,
            description=description
        ) 
    # End of class UnivTimestampFactory #########################################################################        