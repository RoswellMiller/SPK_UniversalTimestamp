"""
Comprehensive tests for the UnivMoment class.
"""
from decimal import Decimal

from SPK_UniversalTimestamp.Constants_aCommon import Calendar, Precision
from SPK_UniversalTimestamp.Moment_aUniversal import UnivMoment

class Test_Moment_aUniversal: 
    """Test cases for UnivMoment class."""
    
    # Tests for static methods can be added here
    def test_UnivMoment_creation(self):
        """Test UnivMoment creation."""
        moment = UnivMoment.from_gregorian(1492, 4, 9, 12, 30)  #, description="creator day")
        assert moment.rd_moment() == (Decimal('544676'),(12,30,0))  
        assert moment.precision == Precision.MINUTE
        
        moment = UnivMoment(Decimal('2451545'), (12,0,0), precision=Precision.DAY)
        assert moment.rd_moment() == (Decimal('2451545'),(12,0,0))
        assert moment.precision == Precision.DAY
        
        print(f"✅ SUCCESS: {self.test_UnivMoment_creation.__doc__}")
        return
    
    def test_now_creation(self):
        """Test UnivMoment.now() creation."""
        moment_now = UnivMoment.now()
        assert isinstance(moment_now.rd_moment()[0], Decimal)
        assert isinstance(moment_now.rd_moment()[1][0], int)
        assert isinstance(moment_now.rd_moment()[1][1], int)
        assert isinstance(moment_now.rd_moment()[1][2], Decimal)
        assert moment_now.precision == Precision.MICROSECOND
        
        print(f"✅ SUCCESS: {self.test_now_creation.__doc__}")
        return
    
    def test_indexing(self):
        """Test indexing of UnivMoment."""
        moment = UnivMoment.from_gregorian(2000, 1, 1, 12, 25, Decimal('34.6'))
        
        assert moment[0] == Decimal('730120')
        assert moment[1] == 12
        assert moment[2] == 25
        assert moment[3] == Decimal('34.6')
        assert moment['day'] == moment[0]
        assert moment['hour'] == moment[1]
        assert moment['minute'] == moment[2]
        assert moment['second'] == moment[3]        
        print(f"✅ SUCCESS: {self.test_indexing.__doc__}")
        return
    
    def test_subtraction(self):
        """Test subtraction of UnivMoment instances."""
        # test __class__ __sub__ __class__
        moment1 = UnivMoment.from_gregorian(2020, 1, 1, 0, 0, 0)
        moment2 = UnivMoment.from_gregorian(2019, 1, 1, 0, 0, 0)       
        delta1 = moment1 - moment2
        assert delta1 == (Decimal('365'),0,0,0)
        # test __class__ __sub__ __class__
        moment1 = UnivMoment.from_gregorian(224, 3, 1, 12, 30, 30)
        moment2 = UnivMoment.from_gregorian(-200, 2, 28, 10, 15, 15)
        delta2 = moment1 - moment2
        assert delta2 == (Decimal('154864'),2,15,15)
        # test __class__ __sub__ __class__
        delta3 = moment2 - moment1
        assert delta3 == (Decimal('-154865'),21,44,45)
        # test __class__ __add__ tuple
        moment3 = moment1 + delta3
        present = moment3.present(Calendar.GREGORIAN, "%Y-%m-%d %H:%M:%S", language="en")
        assert present == "-200-02-28 10:15:15"
        # test __class__ __sub__ tuple
        moment4 = moment1 - (180, 7, 35, 0)
        present = moment4.present(Calendar.GREGORIAN, "%Y-%m-%d %H:%M:%S", language="en")
        assert present == "223-09-03 04:55:30"
        # test "borrowing" properties of subtract
        moment5 = moment1 - (0, 63, 120, 122)
        present = moment5.present(Calendar.GREGORIAN, "%Y-%m-%d %H:%M:%S", language="en")
        assert present == "224-02-27 19:28:28"    
        # test "carry" properties of add
        moment5 = moment1 + (0, 63, 120, 122)
        present = moment5.present(Calendar.GREGORIAN, "%Y-%m-%d %H:%M:%S", language="en")
        assert present == "224-03-04 05:32:32"
        
        
        print(f"✅ SUCCESS: {self.test_subtraction.__doc__}")
        return