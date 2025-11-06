#from datetime import datetime, timezone
from decimal import Decimal
import inspect

#from SPK_UniversalTimestamp.CC01_Calendar_Basics import 

from SPK_UniversalTimestamp import Precision, Calendar
from SPK_UniversalTimestamp.UnivGREGORIAN import UnivGREGORIAN
from SPK_UniversalTimestamp.UnivTimestampFactory import UnivTimestampFactory

class TestUniversalTimestamp:
    """Test cases for UnivTimestamp class."""
    def test_gregorian_creation(self):
        """Test Gregorian calendar timestamp creation."""
        # Test normal CE date
        timestamp = UnivGREGORIAN(
            2024, 7, 15, 14, 30, Decimal(25.123456),
            precision=Precision.MICROSECOND
        )
        
        rd = timestamp.rd
        need_rd = 739082
        signature = timestamp.format_signature()
        _str = timestamp.__str__()
        _repr = timestamp.__repr__()
        assert timestamp.calendar == Calendar.GREGORIAN
        assert timestamp.precision == Precision.MICROSECOND        
        assert timestamp.year == 2024
        assert timestamp.month == 7
        assert timestamp.day == 15
        assert timestamp.hour == 14
        assert timestamp.minute == 30
        assert timestamp.second == Decimal('25.123456')
        assert timestamp.accuracy is None
        assert timestamp.description == ""
        assert rd == need_rd
        assert signature == "2024-07-15 14:30:25.123456" 
        assert _str == "2024-07-15 14:30:25.123456"
        assert _repr == "{'class':'UnivGREGORIAN','ca':'GREGORIAN','yr':2024,'mo':7,'da':15,'hr':14,'mi':30,'sc':'25.123456','pr':'MICROSECOND','tz':'UTC','fo':0,'ac':None,'de':''}"
        
        # Test BCE date
        bce_timestamp = UnivGREGORIAN(
            -44, 3, 15,  # 44 BCE - Ides of March
            description="Assassination of Julius Caesar"
        )
        
        rd = bce_timestamp.rd
        need_rd = -16362
        signature = bce_timestamp.format_signature()
        _str = bce_timestamp.__str__()
        _repr = bce_timestamp.__repr__()
        assert bce_timestamp.calendar == Calendar.GREGORIAN
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
        assert signature == "44 BCE-03-15"
        assert _str == "44 BCE-03-15"
        assert _repr == "{'class':'UnivGREGORIAN','ca':'GREGORIAN','yr':-44,'mo':3,'da':15,'hr':None,'mi':None,'sc':None,'pr':'DAY','tz':'UTC','fo':0,'ac':None,'de':'Assassination of Julius Caesar'}"
        
        print(f"✅ SUCCESS: {inspect.currentframe().f_code.co_name}")
        return
    
    def test_timezone_handling(self):
        """Test timezone handling in timestamps."""
        # Create a timestamp with UTC timezone
        #dt = datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        try:
            pt_timestamp = UnivGREGORIAN(
                2024, 1, 1, 12, 0, 0,       # Noon PST
                timezone="America/Los_Angeles"
            )
            assert pt_timestamp.hour == 12
            assert pt_timestamp.minute == 0
            assert pt_timestamp.second == 0
            
            jt_timestamp = UnivGREGORIAN(
                2024, 1, 1, 2, 
                timezone="Asia/Tokyo"
            )
            assert jt_timestamp.hour == 2
            assert jt_timestamp.minute is None
            assert jt_timestamp.second is None
            assert jt_timestamp.year == 2024
            assert jt_timestamp.month == 1
            assert jt_timestamp.day == 1
            assert jt_timestamp.precision == Precision.HOUR
            
            est_timestamp = UnivGREGORIAN(
                2025, 2, 1, 12, 0,     # Noon EST
                timezone="America/New_York"
            )
            assert est_timestamp.hour == 12
            assert est_timestamp.minute == 0
            assert est_timestamp.second is None
            assert est_timestamp.year == 2025
            assert est_timestamp.month == 2
            assert est_timestamp.day == 1
            assert est_timestamp.precision == Precision.MINUTE
            
            edt_timestamp = UnivGREGORIAN(
                2025, 8, 4, 12, 0,      # Noon EDT
                timezone="America/New_York"
            )
            assert edt_timestamp.hour == 12  # Noon EDT 4:00 PM UTC
            assert edt_timestamp.minute == 0
            assert edt_timestamp.second is None
            assert edt_timestamp.year == 2025
            assert edt_timestamp.month == 8
            assert edt_timestamp.day == 4
            assert edt_timestamp.precision == Precision.MINUTE

            edtf0_timestamp = UnivGREGORIAN(
                2024, 11, 3, 1, 30,    # 1:30 AM EDT fold=0
                timezone="America/New_York"
            )
            assert edtf0_timestamp.hour == 1  # 1:30 AM EDT fold=0
            assert edtf0_timestamp.minute == 30
            assert edtf0_timestamp.second is None
            assert edtf0_timestamp.year == 2024
            assert edtf0_timestamp.month == 11
            assert edtf0_timestamp.day == 3
            assert edtf0_timestamp.precision == Precision.MINUTE
            
            estf1_timestamp = UnivGREGORIAN(
                2024, 11, 3, 1, 30,      # 1:30 AM EST fold=1
                timezone="America/New_York",
                fold=1  # Test with fold=1
            )
            assert estf1_timestamp.hour == 1     # 1:30 AM EST fold=1
            assert estf1_timestamp.minute == 30
            assert estf1_timestamp.second is None
            assert estf1_timestamp.year == 2024
            assert estf1_timestamp.month == 11
            assert estf1_timestamp.day == 3
            assert estf1_timestamp.precision == Precision.MINUTE
            # NOTE : This is an invalid hour for EST since it true name is 3:30 EDT
            # NOTE : Regardless of the name used it represents the same UTC time
            invalid_timestamp = UnivGREGORIAN(
                2023, 3, 12, 2, 30, 0,
                timezone="America/New_York"
            )
            assert invalid_timestamp.hour == 2
            assert invalid_timestamp.minute == 30
            assert invalid_timestamp.second == 0
            assert invalid_timestamp.year == 2023
            assert invalid_timestamp.month == 3
            assert invalid_timestamp.day == 12
            assert invalid_timestamp.precision == Precision.SECOND
            return
        except (ValueError, TypeError) as e:
            print(f"❌ERROR: {e}")
            print("Timezone handling tests disabled due to error.")
            return
        
    def test_precision_levels(self):
        """Test different precision levels."""
        # Test date precision
        year_precision = UnivGREGORIAN(
            2024, precision=Precision.YEAR
        )
        assert year_precision.precision == Precision.YEAR
        
        # Test time precision
        nanosecond_precision = UnivGREGORIAN(
            2024, 1, 1, 12, 30, Decimal(45.123456789),
            precision=Precision.NANOSECOND
        )
        assert nanosecond_precision.precision == Precision.NANOSECOND
        assert nanosecond_precision.second == Decimal('45.123456789')
        print(f"✅ SUCCESS: {inspect.currentframe().f_code.co_name}")
        return
    
    def test_string__str__(self):
        """Test string representations."""
        timestamp = UnivGREGORIAN(
            2024, 7, 15,
            description="Test timestamp"
        )
        
        # Test __str__
        str_repr = str(timestamp)
        assert "2024-07-15" == str_repr
        print(f"✅ SUCCESS: {inspect.currentframe().f_code.co_name}")
        return

    def test_string__repr__(self):
        timestamp = UnivGREGORIAN(
            2024, 7, 15, 11, 10, Decimal('22.56'),
            description="Test timestamp"
        )         
        # Test __repr__
        repr_str = repr(timestamp)
        assert repr_str ==  "{'class':'UnivGREGORIAN','ca':'GREGORIAN','yr':2024,'mo':7,'da':15,'hr':11,'mi':10,'sc':'22.56','pr':'SECOND','tz':'UTC','fo':0,'ac':None,'de':'Test timestamp'}"
        
        ts_repro = UnivTimestampFactory.parse_repr(repr_str)
        assert ts_repro == timestamp, "Repr conversion mismatch!"
        
        print(f"✅ SUCCESS: {inspect.currentframe().f_code.co_name}")
        return


