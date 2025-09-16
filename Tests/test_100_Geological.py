import os
import sys
from decimal import Decimal
import inspect
from SPK_UniversalTimestamp import *

from SPK_UniversalTimestamp import *
from SPK_UniversalTimestamp.UnivTimestampFactory import UnivTimestampFactory
from SPK_UniversalTimestamp.UnivGEOLOGICAL import UnivGEOLOGICAL

class TestUniversalTimestamp:
    """Test cases for UnivTimestamp class."""
    def test_geological_creation(self):
        """Test geological epoch timestamp creation."""
        # Test billion years ago
        big_bang = UnivGEOLOGICAL(
            13.8,
            precision=Precision.BILLION_YEARS,
            accuracy=Decimal('0.01'),
            description="Big Bang"
        )
        rd = big_bang.rd
        need_rd = int(-13_800_000_000 * 365.25) # R.D. for Big Bang
        signature = big_bang.format_signature()
        _str = big_bang.__str__()
        _repr = big_bang.__repr__()
        assert big_bang.calendar == Calendar.GEOLOGICAL
        assert big_bang.precision == Precision.BILLION_YEARS
        assert big_bang.year == -13_800_000_000  # 13.8 billion years
        assert big_bang.accuracy == Decimal('0.01')
        assert big_bang.description == "Big Bang"
        assert rd == need_rd
        assert signature == "-13.80 G-yr"
        assert _str == "-13.80 G-yr"
        assert _repr == "{'class':'UnivGEOLOGICAL','ca':'GEOLOGICAL','yr':-13.8,'pr':'BILLION_YEARS','ac':'0.01','de':'Big Bang'}"
        
        # Test million years ago
        dinosaur_extinction = UnivGEOLOGICAL(
            66.0,
            precision=Precision.MILLION_YEARS,
            accuracy=Decimal('0.001'),
            description="K-Pg extinction"
        )
        
        rd = dinosaur_extinction.rd
        need_rd = int(-66_000_000 * 365.25)  # R.D. for Big Bang
        signature = dinosaur_extinction.format_signature()
        _str = dinosaur_extinction.__str__()
        _repr = dinosaur_extinction.__repr__()
        
        assert dinosaur_extinction.calendar == Calendar.GEOLOGICAL
        assert dinosaur_extinction.precision == Precision.MILLION_YEARS
        assert dinosaur_extinction.year == -66_000_000  # 66.0 million years
        assert dinosaur_extinction.accuracy == Decimal('0.001')
        assert dinosaur_extinction.description == "K-Pg extinction"
        assert rd == need_rd
        assert signature == "-66.00 M-yr"
        assert _str == "-66.00 M-yr"
        assert _repr == "{'class':'UnivGEOLOGICAL','ca':'GEOLOGICAL','yr':-66,'pr':'MILLION_YEARS','ac':'0.001','de':'K-Pg extinction'}"
        
        # Test million years ago
        end_last_ice_age = UnivGEOLOGICAL(
            11.7,
            precision=Precision.THOUSAND_YEARS,
            accuracy=Decimal('0.001'),
            description= "End of last ice age"
        )
        
        rd = end_last_ice_age.rd
        need_rd = int(-11_700 * 365.25) # R.D. for Big Bang
        signature = end_last_ice_age.format_signature()
        _str = end_last_ice_age.__str__()
        _repr = end_last_ice_age.__repr__()
        assert end_last_ice_age.calendar == Calendar.GEOLOGICAL
        assert end_last_ice_age.precision == Precision.THOUSAND_YEARS
        assert end_last_ice_age.year == -11_700
        assert end_last_ice_age.accuracy == Decimal('0.001')
        assert end_last_ice_age.description == "End of last ice age"
        assert rd == need_rd
        assert signature == "-11.70 k-yr"
        assert _str == "-11.70 k-yr"
        assert _repr == "{'class':'UnivGEOLOGICAL','ca':'GEOLOGICAL','yr':-11.7,'pr':'THOUSAND_YEARS','ac':'0.001','de':'End of last ice age'}"
        
        print(f"✅ SUCCESS: {inspect.currentframe().f_code.co_name}")
        return
    
    def test_string__str__(self):
        """Test string representations."""
        timestamp = UnivGEOLOGICAL(
            11.7,
            precision=Precision.THOUSAND_YEARS,
            accuracy=Decimal('0.001'),
            description= "End of last ice age"
        )
        
        # Test __str__
        str_repr = str(timestamp)
        assert '-11.70 k-yr' == str_repr
        print(f"✅ SUCCESS: {inspect.currentframe().f_code.co_name}")
        return

    def test_string__repr__(self):
        timestamp = UnivGEOLOGICAL(
            11.7,
            precision=Precision.THOUSAND_YEARS,
            accuracy=Decimal('0.001'),
            description= "End of last ice age"
        )         
        # Test __repr__
        repr_str = repr(timestamp)
        assert repr_str ==  "{'class':'UnivGEOLOGICAL','ca':'GEOLOGICAL','yr':-11.7,'pr':'THOUSAND_YEARS','ac':'0.001','de':'End of last ice age'}"
        
        ts_repro = UnivTimestampFactory.parse_repr(repr_str)
        assert ts_repro == timestamp, "Repr conversion mismatch!"
        
        print(f"✅ SUCCESS: {inspect.currentframe().f_code.co_name}")
        return

