
from decimal import Decimal
import convertdate as CVD
import inspect

# Add the parent directory to Python path so we can import the package
#sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from SPK_UniversalTimestamp.CC01_Calendar_Basics import *
from SPK_UniversalTimestamp.CC02_Gregorian import *
from SPK_UniversalTimestamp.CC03_Julian import *

from SPK_UniversalTimestamp import *
from SPK_UniversalTimestamp.UnivJULIAN import UnivJULIAN    
from SPK_UniversalTimestamp.UnivTimestampFactory import UnivTimestampFactory


class TestUniversalTimestamp:
    """Test cases for UnivTimestamp class."""
    def test_julian_creation(self):
        """Test Gregorian calendar timestamp creation."""
        # Test normal CE date
        timestamp = UnivJULIAN(
            1739, 7, 15, 14, 30, Decimal(25.123),
            precision=Precision.MILLISECOND
        )
        
        rd = timestamp.rd
        need_rd = 634998
        signature = timestamp.format_signature()
        _str = timestamp.__str__()
        _repr = timestamp.__repr__()
        assert timestamp.calendar == Calendar.JULIAN
        assert timestamp.precision == Precision.MILLISECOND        
        assert timestamp.year == 1739
        assert timestamp.month == 7
        assert timestamp.day == 15
        assert timestamp.hour == 14
        assert timestamp.minute == 30
        assert timestamp.second == Decimal('25.123')
        assert timestamp.accuracy is None
        assert timestamp.description == ""
        assert rd == need_rd
        assert signature == "1739-07-15 JC 14:30:25.123"
        assert _str == "1739-07-15 JC 14:30:25.123"
        assert _repr == "{'class':'UnivJULIAN','ca':'JULIAN','yr':1739,'mo':7,'da':15,'hr':14,'mi':30,'sc':25.123,'pr':'MILLISECOND','tz':'UTC','fo':0,'ac':None,'de':''}"
        
        # Test BCE date
        bce_timestamp = UnivJULIAN(
            -44, 3, 15, 
            description="Assassination of Julius Caesar"
        )
        
        rd = bce_timestamp.rd
        need_rd = -15999
        signature = bce_timestamp.format_signature()
        _str = bce_timestamp.__str__()
        _repr = bce_timestamp.__repr__()
        assert bce_timestamp.calendar == Calendar.JULIAN
        assert bce_timestamp.precision == Precision.DAY
        assert bce_timestamp.year == -44
        assert bce_timestamp.month == 3
        assert bce_timestamp.day == 15
        assert bce_timestamp.hour is None
        assert bce_timestamp.minute is None
        assert bce_timestamp.second is None
        assert bce_timestamp.accuracy is None
        assert bce_timestamp.description == "Assassination of Julius Caesar"
        assert rd == need_rd
        assert signature == "44 bc-03-15 JC"
        assert _str == "44 bc-03-15 JC"
        assert _repr == "{'class':'UnivJULIAN','ca':'JULIAN','yr':-44,'mo':3,'da':15,'hr':None,'mi':None,'sc':None,'pr':'DAY','tz':'UTC','fo':0,'ac':None,'de':'Assassination of Julius Caesar'}"
        
        print(f"✅ SUCCESS: {inspect.currentframe().f_code.co_name}")
        return

    def test_george_washington_birthday(self):
        """Test George Washington's birthday conversion from Julian to Gregorian."""
        print("\n1. GEORGE WASHINGTON'S BIRTHDAY CONVERSION:")
        print("-" * 35)
        
        # Create Julian calendar timestamp (Old Style)
        washington_julian = UnivJULIAN(1731, 2, 11, description="George Washington's birthday")
        print(f"Julian input: {washington_julian.format_signature()}")
        
        # Convert to Gregorian
        washington_gregorian = UnivTimestampFactory.convert(Calendar.GREGORIAN, washington_julian)
        print(f"Converted to Gregorian: {washington_gregorian.format_signature()}")
        
        # Check if it matches expected
        actual_date = f"{washington_gregorian.year}-{washington_gregorian.month:02d}-{washington_gregorian.day:02d}"
        expected_date = "1731-02-22"
        
        assert actual_date == expected_date
        print(f"✅ SUCCESS: {inspect.currentframe().f_code.co_name}")
        return 
    
    def test_julian_round_trip_conversion(self):
        print("\n2. ROUND-TRIP CONVERSION TEST:")
        print("-" * 35)
        # Create Julian calendar timestamp (Old Style)
        washington_julian = UnivJULIAN(1731, 2, 11, description="George Washington's birthday")
        print(f"Julian input: 1731-02-11 OS")
        print(f"Created timestamp: {washington_julian.format_signature()}")
        #print(f"Internal date_value: {washington_julian.date_value}")

        # Test conversion to Gregorian
        washington_gregorian = UnivTimestampFactory.convert(Calendar.GREGORIAN, washington_julian)
        print(f"Converted to Gregorian: {washington_gregorian.format_signature()}")
        print(f"Expected: 1731-02-22 NS")

        # Check if it matches expected
        actual_date = f"{washington_gregorian.year}-{washington_gregorian.month:02d}-{washington_gregorian.day:02d}"
        expected_date = "1731-02-22"

        cvd_gregorian = CVD.julian.to_gregorian(1731, 2, 11)
        assert actual_date == expected_date

        # Test round-trip conversion
        julian_back = UnivTimestampFactory.convert(Calendar.JULIAN, washington_gregorian)
        print(f"Round-trip back to Julian: {julian_back.format_signature()}")
        assert washington_julian == julian_back, "Round-trip conversion mismatch!"
        print("✅ SUCCESS: Round-trip conversion matches original Julian date.")
        return
    
    def test_round_trip_conversion(self):
        print("\n3. TEST OTHER HISTORICAL DATES CONVERSION TESTS:")
        test_dates_julian = [
            (1700, 2, 28, "1700 leap day (Julian had it, Gregorian didn't)"),
            (1582, 10, 4, "Last day of Julian calendar (Catholic countries)"),
            (1731, 2, 11, "George Washington birthday (Julian)"),
            (1752, 9, 2, "Last day of Julian calendar (Britain)"),
            (1731, 3, 24, "Day before Julian New Year 1731"),
            (1731, 3, 25, "Julian New Year 1731"),
        ]

        for year, month, day, description in test_dates_julian:
            print(f"      Testing {description}...")
            julian_ts = UnivJULIAN(year, month, day, description=description)
            print(f"      Input Julian date: {julian_ts.format_signature()}")
            
            gregorian_ts = UnivTimestampFactory.convert(Calendar.GREGORIAN, julian_ts)        
            print(f"      Output Gregorian date:: {gregorian_ts.format_signature()}")
            
            julian_back = UnivTimestampFactory.convert(Calendar.JULIAN, gregorian_ts)
            print(f"      Round-trip back to Julian: {julian_back.format_signature()}") 
            
            assert julian_ts == julian_back, "Round-trip conversion mismatch!"
            print(f"   ✅ SUCCESS")       

        print(f"✅ SUCCESS: {inspect.currentframe().f_code.co_name}")
        return
    
    def test_string__str__(self):
        """Test string representations."""
        timestamp = UnivJULIAN(
            2024, 7, 15,
            description="Test timestamp"
        )
        
        # Test __str__
        str_repr = str(timestamp)
        assert "2024-07-15 JC" == str_repr
        print(f"✅ SUCCESS: {inspect.currentframe().f_code.co_name}")
        return

    def test_string__repr__(self):
        timestamp = UnivJULIAN(
            2024, 7, 15, 11,
            description="Test timestamp"
        )         
        # Test __repr__
        repr_str = repr(timestamp)
        assert repr_str ==  "{'class':'UnivJULIAN','ca':'JULIAN','yr':2024,'mo':7,'da':15,'hr':11,'mi':None,'sc':None,'pr':'HOUR','tz':'UTC','fo':0,'ac':None,'de':'Test timestamp'}"
        
        ts_repro = UnivTimestampFactory.parse_repr(repr_str)
        assert ts_repro == timestamp, "Repr conversion mismatch!"
        
        print(f"✅ SUCCESS: {inspect.currentframe().f_code.co_name}")
        return

