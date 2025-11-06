import inspect

# from SPK_UniversalTimestamp.CC01_Calendar_Basics import *
#from SPK_UniversalTimestamp.CC02_Gregorian import rd_from_gregorian
from SPK_UniversalTimestamp.CC03_Julian import rd_from_julian

from SPK_UniversalTimestamp import Precision, Calendar
from SPK_UniversalTimestamp.CC01_Calendar_Basics import Epoch_rd
from SPK_UniversalTimestamp.UnivTimestampFactory import UnivTimestampFactory
from SPK_UniversalTimestamp.UnivHEBREW import UnivHEBREW

class TestUniversalTimestamp:
    """Test cases for UnivTimestamp class."""
    def test_hebrew_creation(self):
        """Test Hebrew calendar conversion."""
        hebrew_epoch = rd_from_julian(-3761, 10, 7)
        univ_hebrew_epoch = Epoch_rd['hebrew']
        assert hebrew_epoch == univ_hebrew_epoch  # R.D. for 1 Tishrei 3761 BCE
        
        timestamp = UnivHEBREW(
            4773, 2, 6,  
            description="p 448 ex. 8"
        )      
        rd = timestamp.rd
        need_rd = 369740
        signature = timestamp.format_signature()
        _str = timestamp.__str__()
        _repr = timestamp.__repr__()
        assert timestamp.calendar == Calendar.HEBREW
        assert timestamp.year == 4773
        assert timestamp.month == 2
        assert timestamp.day == 6
        assert timestamp.precision == Precision.DAY
        assert rd == need_rd
        assert signature == "4773-02-06 AM"
        assert _str == "4773-02-06 AM"
        assert _repr == "{'class':'UnivHEBREW','ca':'HEBREW','yr':4773,'mo':2,'da':6,'hr':None,'mi':None,'sc':None,'pr':'DAY','tz':'UTC','fo':0,'ac':None,'de':'p 448 ex. 8'}"
        
        timestamp = UnivHEBREW(
            4773, 1, 6,  
            description="p 448 "
        )      
        heb_rd = timestamp.rd
        assert timestamp.calendar == Calendar.HEBREW
        assert timestamp.year == 4773
        assert timestamp.month == 1
        assert timestamp.day == 6
        assert timestamp.precision == Precision.DAY
        assert heb_rd == 369710
        
        greg_ts = UnivTimestampFactory.convert(Calendar.GREGORIAN, timestamp)
        
        heb_ts_back = UnivTimestampFactory.convert(Calendar.HEBREW, greg_ts)
        heb_rd_back = heb_ts_back.rd
        assert heb_ts_back == timestamp, "Hebrew timestamp conversion mismatch!"
        assert heb_rd_back == heb_rd, "Hebrew R.D. conversion mismatch!"
        
        print(f"✅ SUCCESS: {inspect.currentframe().f_code.co_name}")
        return
    
    def test_string__str__(self):
        """Test string representations."""
        timestamp = UnivHEBREW(
            2024, 7, 15,
            description="Test timestamp"
        )
        
        # Test __str__
        str_repr = str(timestamp)
        assert "2024-07-15 AM" == str_repr
        print(f"✅ SUCCESS: {inspect.currentframe().f_code.co_name}")
        return

    def test_string__repr__(self):
        timestamp = UnivHEBREW(
            2024, 7, 15, 11, 30, 15,
            timezone='Asia/Jerusalem',
            description="Test timestamp"
        )         
        # Test __repr__
        repr_str = repr(timestamp)
        assert repr_str ==  "{'class':'UnivHEBREW','ca':'HEBREW','yr':2024,'mo':7,'da':15,'hr':11,'mi':30,'sc':'15','pr':'SECOND','tz':'Asia/Jerusalem','fo':0,'ac':None,'de':'Test timestamp'}"
        
        ts_repro = UnivTimestampFactory.parse_repr(repr_str)
        assert ts_repro == timestamp, "Repr conversion mismatch!"
        
        print(f"✅ SUCCESS: {inspect.currentframe().f_code.co_name}")
        return


    
