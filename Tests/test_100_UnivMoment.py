"""
Comprehensive tests for the UnivMoment class.
"""
from decimal import Decimal

from SPK_UniversalTimestamp.Constants_aCommon import Calendar
from SPK_UniversalTimestamp.UnivMoment import UnivMoment, UnivMomPrecision


class Test_Moment_aUniversal: 
    """Test cases for UnivMoment class."""
    
    # Tests for static methods can be added here
    def test_UnivMoment_creation(self):
        """Test UnivMoment creation."""
        moment = UnivMoment.from_gregorian(1492, 4, 9, 12, 30)  #, description="creator day")
        assert moment.rd_moment() == (Decimal('544676'),(12,30,0))  
        assert moment.precision == UnivMomPrecision.MINUTE
        
        moment = UnivMoment(Decimal('2451545'), (12,0,0), precision=UnivMomPrecision.DAY)
        assert moment.rd_moment() == (Decimal('2451545'),(12,0,0))
        assert moment.precision == UnivMomPrecision.DAY
        
        print(f"✅ SUCCESS: {self.test_UnivMoment_creation.__doc__}")
        return
    
    def test_now_creation(self):
        """Test UnivMoment.now() creation."""
        moment_now = UnivMoment.now()
        assert isinstance(moment_now.rd_moment()[0], Decimal)
        assert isinstance(moment_now.rd_moment()[1][0], int)
        assert isinstance(moment_now.rd_moment()[1][1], int)
        assert isinstance(moment_now.rd_moment()[1][2], Decimal)
        assert moment_now.precision == UnivMomPrecision.MICROSECOND
        
        print(f"✅ SUCCESS: {self.test_now_creation.__doc__}")
        return
    def test_json_serialization(self):
        """Test UnivMoment.to_dict/from_dict() serialization."""
        moment_now = UnivMoment.now()
        data = moment_now.to_dict()
        moment_restored = UnivMoment.from_dict(data)
        assert moment_now == moment_restored
        print(f"✅ SUCCESS: {self.test_json_serialization.__doc__}")
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
        assert delta1.seconds == Decimal('365') * 86400   # 31 536 000 s
        # test __class__ __sub__ __class__
        moment1 = UnivMoment.from_gregorian(224, 3, 1, 12, 30, 30)
        moment2 = UnivMoment.from_gregorian(-200, 2, 28, 10, 15, 15)
        delta2 = moment1 - moment2
        assert delta2.seconds == Decimal('13380257715')   # 154864d 2h 15m 15s
        # test __class__ __sub__ __class__
        delta3 = moment2 - moment1
        assert delta3.seconds == Decimal('-13380257715')
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

    # ------------------------------------------------------------------
    # __format__ spec
    # ------------------------------------------------------------------
    def test_format_spec(self):
        """f-string format spec: '' | 'umom' | 'ugeo:<fmt>' | 'ucal:<cal>:<fmt>'"""
        import pytest

        moment = UnivMoment.from_gregorian(2025, 9, 8, description="Format spec test date")

        # --- empty spec and 'umom' delegate to format_signature() ---
        assert f"{moment}"       == moment.format_signature()
        assert f"{moment:umom}"  == moment.format_signature()
        assert format(moment, "")     == moment.format_signature()
        assert format(moment, "umom") == moment.format_signature()

        # --- Gregorian: ucal: short mnemonic and full name ---
        greg_fmt = moment.present(Calendar.GREGORIAN, "%Y-%m-%d")
        assert f"{moment:ucal:greg:%Y-%m-%d}"      == greg_fmt
        assert f"{moment:ucal:gregorian:%Y-%m-%d}" == greg_fmt

        # --- Julian calendar: mnemonic and CalendarAtts code ---
        jul_fmt = moment.present(Calendar.JULIAN, "%Y-%m-%d")
        assert f"{moment:ucal:jul:%Y-%m-%d}" == jul_fmt
        assert f"{moment:ucal:jc:%Y-%m-%d}"  == jul_fmt

        # --- Hebrew calendar: mnemonic and CalendarAtts code ---
        heb_fmt = moment.present(Calendar.HEBREW, "%d/%m/%Y")
        assert f"{moment:ucal:heb:%d/%m/%Y}" == heb_fmt
        assert f"{moment:ucal:am:%d/%m/%Y}"  == heb_fmt

        # --- Geological calendar: ugeo: (no calendar specifier needed) ---
        geo_moment = UnivMoment.from_geological(0.5, precision=UnivMomPrecision.MILLION_YEARS)
        geo_fmt = geo_moment.present(Calendar.GEOLOGICAL, "%Y | %O | %R")
        assert f"{geo_moment:ugeo:%Y | %O | %R}" == geo_fmt

        # --- fmt_str containing ':' characters is preserved intact ---
        time_fmt = moment.present(Calendar.GREGORIAN, "%H:%M:%S")
        assert f"{moment:ucal:greg:%H:%M:%S}" == time_fmt

        # --- full datetime format string (contains colons) ---
        full_fmt = moment.present(Calendar.GREGORIAN, "%Y-%m-%d %H:%M:%S")
        assert f"{moment:ucal:greg:%Y-%m-%d %H:%M:%S}" == full_fmt

        # --- "wrong prefix" fallbacks ---
        # ugeo: on a positive-rdate (calendar) date → format_signature() as calendar default
        assert f"{moment:ugeo:%Y | %O | %R}" == moment.format_signature()

        # ucal: on a geological (very ancient) date → geological default "%G %O"
        ancient = UnivMoment.from_geological(100, precision=UnivMomPrecision.MILLION_YEARS)
        geo_default = ancient.present(Calendar.GEOLOGICAL, "%G %O")
        assert f"{ancient:ucal:greg:%Y-%m-%d}" == geo_default

        # --- unknown calendar abbreviation raises ValueError ---
        with pytest.raises(ValueError, match="Unknown calendar abbreviation"):
            format(moment, "ucal:xyz:%Y-%m-%d")

        # --- missing format string (no second colon) raises ValueError ---
        with pytest.raises(ValueError, match="missing format string"):
            format(moment, "ucal:greg")

        # --- spec without recognised prefix raises ValueError ---
        with pytest.raises(ValueError, match="Unsupported UnivMoment format spec"):
            format(moment, "bad_spec")

        print(f"✅ SUCCESS: {self.test_format_spec.__doc__}")