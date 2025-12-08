"""
Comprehensive tests for the Moment_Geological class.
"""
from decimal import Decimal
from SPK_UniversalTimestamp.Constants_aCommon import Calendar, Precision
from SPK_UniversalTimestamp.Moment_aUniversal import UnivMoment

class Test_Geological: 
    """Test cases for Moment_Geological class."""
    
    # Tests for static methods can be added here
    def test_UnivMoment_creation(self):
        """Test UnivMoment creation."""
        moment = UnivMoment.from_geological(100.0, precision=Precision.MILLION_YEARS)
        #moment = UnivMoment(ts)
        assert moment.rd_day == Decimal('-100_000_000.0')*Decimal('365.25')
        assert moment.precision == Precision.MILLION_YEARS
        
        moment = UnivMoment(Decimal('-infinity'), precision=Precision.BILLION_YEARS)
        assert moment.rd_day == Decimal('-inf')
        assert moment.precision == Precision.BILLION_YEARS
        
        bot = UnivMoment.beginning_of_time()
        assert bot.rd_day == Decimal('-infinity')
        assert bot.precision == Precision.YEAR
        assert bot == moment
        print(f"✅ SUCCESS: {self.test_UnivMoment_creation.__doc__}")
        return
    
    def test_present_geological(self):
        """Test Geological moment presentation constraints."""
        try:
            moment = UnivMoment.from_geological(0.5, precision=Precision.DAY, description="Invalid Epoch")
            assert False, "Expected ValueError for Geological moment with day precision"
        except ValueError as ve:
            assert True, str(ve)
        
        moment = UnivMoment.from_geological(0.5, precision=Precision.MILLION_YEARS)
        assert moment.rd_day == Decimal('-500_000.0')*Decimal('365.25')
        assert moment.precision == Precision.MILLION_YEARS
        
        ts_formatted = moment.present(Calendar.GEOLOGICAL, format="%Y | %y | %O | %R | %P | %a", language="en")
        assert ts_formatted == '-0.50 M-yr | -0.50 M-yr | Phanerozoic | Cenozoic | Quarternary | pleistocene Chibanian'
        
        moment = UnivMoment.from_geological(6.0, precision=Precision.MILLION_YEARS)
        ts_formatted = moment.present(Calendar.GEOLOGICAL, format="%Y | %y | %O | %R | %P | %a", language="en")
        assert ts_formatted == '-6.00 M-yr | -6.00 M-yr | Phanerozoic | Cenozoic | (tertiary)Neogene | miocene Messinian'
        
        moment = UnivMoment.from_geological(146.0, precision=Precision.MILLION_YEARS)
        ts_formatted = moment.present(Calendar.GEOLOGICAL, format="%Y | %y | %O | %R | %P | %a", language="en")
        assert ts_formatted == '-146.00 M-yr | -146.00 M-yr | Phanerozoic | Mesozoic | Jurassic | late Tithonian'
        
        moment = UnivMoment.from_geological(330.9, precision=Precision.MILLION_YEARS)
        ts_formatted = moment.present(Calendar.GEOLOGICAL, format="%Y | %y | %O | %R | %P | %a", language="en")
        assert ts_formatted == '-330.90 M-yr | -330.90 M-yr | Phanerozoic | Paleozoic | Carboniferous | mississippian Visean'
        
        moment = UnivMoment.from_geological(3700.0, precision=Precision.MILLION_YEARS)
        ts_formatted = moment.present(Calendar.GEOLOGICAL, format="%Y | %y | %O | %R | %P | %a", language="en")
        assert ts_formatted == '-3700.00 M-yr | -3700.00 M-yr | Archean | Eoarchean | pre-periods | pre-epochs'
        print(f"✅ SUCCESS: {self.test_present_geological.__doc__}")
        return