"""
Comprehensive tests for the Moment_Geological class.
"""
from decimal import Decimal
from SPK_UniversalTimestamp.Constants_aCommon import Calendar
from SPK_UniversalTimestamp.UnivMoment import UnivMoment, UnivMomPrecision

class Test_Geological: 
    """Test cases for Moment_Geological class."""
    
    # Tests for static methods can be added here
    def test_UnivMoment_creation(self):
        """Test UnivMoment creation."""
        moment = UnivMoment.from_geological(100.0, precision=UnivMomPrecision.MILLION_YEARS)
        #moment = UnivMoment(ts)
        assert moment.rd_day == Decimal('-100_000_000.0')*Decimal('365.25')
        assert moment.precision == UnivMomPrecision.MILLION_YEARS
        
        moment = UnivMoment(Decimal('-infinity'), precision=UnivMomPrecision.BILLION_YEARS)
        assert moment.rd_day == Decimal('-inf')
        assert moment.precision == UnivMomPrecision.BILLION_YEARS
        
        bot = UnivMoment.beginning_of_time()
        assert bot.rd_day == Decimal('-infinity')
        assert bot.precision == UnivMomPrecision.YEAR
        assert bot == moment
        print(f"✅ SUCCESS: {self.test_UnivMoment_creation.__doc__}")
        return
    
    def test_present_geological(self):
        """Test Geological moment presentation constraints."""
        try:
            moment = UnivMoment.from_geological(0.5, precision=UnivMomPrecision.DAY, description="Invalid Epoch")
            assert False, "Expected ValueError for Geological moment with day precision"
        except ValueError as ve:
            assert True, str(ve)
        
        moment = UnivMoment.from_geological(0.5, precision=UnivMomPrecision.MILLION_YEARS)
        assert moment.rd_day == Decimal('-500_000.0')*Decimal('365.25')
        assert moment.precision == UnivMomPrecision.MILLION_YEARS
        
        ts_formatted = moment.present(Calendar.GEOLOGICAL, format="%Y | %y | %O | %R | %P | %a", language="en")
        assert ts_formatted == '-500.00 k-yr | -500.00 k-yr | Phanerozoic | Cenozoic | Quarternary | pleistocene Chibanian'
        
        moment = UnivMoment.from_geological(6.0, precision=UnivMomPrecision.MILLION_YEARS)
        ts_formatted = moment.present(Calendar.GEOLOGICAL, format="%Y | %y | %O | %R | %P | %a", language="en")
        assert ts_formatted == '-6.00 M-yr | -6.00 M-yr | Phanerozoic | Cenozoic | (tertiary)Neogene | miocene Messinian'
        
        moment = UnivMoment.from_geological(146.0, precision=UnivMomPrecision.MILLION_YEARS)
        ts_formatted = moment.present(Calendar.GEOLOGICAL, format="%Y | %y | %O | %R | %P | %a", language="en")
        assert ts_formatted == '-146.00 M-yr | -146.00 M-yr | Phanerozoic | Mesozoic | Jurassic | late Tithonian'
        
        moment = UnivMoment.from_geological(330.9, precision=UnivMomPrecision.MILLION_YEARS)
        ts_formatted = moment.present(Calendar.GEOLOGICAL, format="%Y | %y | %O | %R | %P | %a", language="en")
        assert ts_formatted == '-330.90 M-yr | -330.90 M-yr | Phanerozoic | Paleozoic | Carboniferous | mississippian Visean'
        
        moment = UnivMoment.from_geological(3700.0, precision=UnivMomPrecision.MILLION_YEARS)
        ts_formatted = moment.present(Calendar.GEOLOGICAL, format="%Y | %y | %O | %R | %P | %a", language="en")
        assert ts_formatted == '-3700.00 M-yr | -3700.00 M-yr | Archean | Eoarchean | pre-periods | pre-epochs'
        print(f"✅ SUCCESS: {self.test_present_geological.__doc__}")
        return

    def test_geological_year_display_autoscaling(self):
        """Auto-scale display unit so at least one non-zero digit appears left of the decimal."""
        fmt = "%Y"

        # --- MILLION_YEARS precision, value < 1 M-yr → should display in k-yr ---
        # User's specific example: 0.77 M-yr → 770,000 yr → -770.00 k-yr
        m = UnivMoment.from_geological(0.77, precision=UnivMomPrecision.MILLION_YEARS)
        assert m.present(Calendar.GEOLOGICAL, format=fmt) == '-770.00 k-yr', \
            f"Expected '-770.00 k-yr', got '{m.present(Calendar.GEOLOGICAL, format=fmt)}'"

        # 0.001 M-yr = 1,000 yr → exactly 1.00 k-yr (boundary: stays in k-yr)
        m = UnivMoment.from_geological(0.001, precision=UnivMomPrecision.MILLION_YEARS)
        assert m.present(Calendar.GEOLOGICAL, format=fmt) == '-1.00 k-yr', \
            f"Expected '-1.00 k-yr', got '{m.present(Calendar.GEOLOGICAL, format=fmt)}'"

        # 0.0001 M-yr = 100 yr → |100| < 1000 → scale to yr
        m = UnivMoment.from_geological(0.0001, precision=UnivMomPrecision.MILLION_YEARS)
        assert m.present(Calendar.GEOLOGICAL, format=fmt) == '-100', \
            f"Expected '-100', got '{m.present(Calendar.GEOLOGICAL, format=fmt)}'"

        # Exactly 1.0 M-yr → no scaling, stays M-yr
        m = UnivMoment.from_geological(1.0, precision=UnivMomPrecision.MILLION_YEARS)
        assert m.present(Calendar.GEOLOGICAL, format=fmt) == '-1.00 M-yr', \
            f"Expected '-1.00 M-yr', got '{m.present(Calendar.GEOLOGICAL, format=fmt)}'"

        # 6.0 M-yr → well above threshold, no scaling
        m = UnivMoment.from_geological(6.0, precision=UnivMomPrecision.MILLION_YEARS)
        assert m.present(Calendar.GEOLOGICAL, format=fmt) == '-6.00 M-yr', \
            f"Expected '-6.00 M-yr', got '{m.present(Calendar.GEOLOGICAL, format=fmt)}'"

        # --- BILLION_YEARS precision, value < 1 G-yr → should display in M-yr ---
        # 0.5 G-yr = 500,000,000 yr → -500.00 M-yr
        m = UnivMoment.from_geological(0.5, precision=UnivMomPrecision.BILLION_YEARS)
        assert m.present(Calendar.GEOLOGICAL, format=fmt) == '-500.00 M-yr', \
            f"Expected '-500.00 M-yr', got '{m.present(Calendar.GEOLOGICAL, format=fmt)}'"

        # 0.000001 G-yr = 1,000 yr → cascades G → M → k-yr
        m = UnivMoment.from_geological(0.000001, precision=UnivMomPrecision.BILLION_YEARS)
        assert m.present(Calendar.GEOLOGICAL, format=fmt) == '-1.00 k-yr', \
            f"Expected '-1.00 k-yr', got '{m.present(Calendar.GEOLOGICAL, format=fmt)}'"

        # --- THOUSAND_YEARS precision, value < 1 k-yr → should display in yr ---
        # 0.5 k-yr = 500 yr → -500
        m = UnivMoment.from_geological(0.5, precision=UnivMomPrecision.THOUSAND_YEARS)
        assert m.present(Calendar.GEOLOGICAL, format=fmt) == '-500', \
            f"Expected '-500', got '{m.present(Calendar.GEOLOGICAL, format=fmt)}'"

        # Exactly 1.0 k-yr → no scaling
        m = UnivMoment.from_geological(1.0, precision=UnivMomPrecision.THOUSAND_YEARS)
        assert m.present(Calendar.GEOLOGICAL, format=fmt) == '-1.00 k-yr', \
            f"Expected '-1.00 k-yr', got '{m.present(Calendar.GEOLOGICAL, format=fmt)}'"

        print(f"✅ SUCCESS: {self.test_geological_year_display_autoscaling.__doc__}")
        return

    def test_format_G_annum_notation(self):
        """
        %G format code: ICS/USGS annum-style display (positive value, Ga/Ma/ka/a suffix).
        The sign is dropped — the suffix implies 'before present'.
        Auto-scales the same way as %Y/%y to avoid leading zeros.
        """
        fmt = "%G"

        # --- MILLION_YEARS: basic cases ---
        # 35.33 Ma (user's original example)
        m = UnivMoment.from_geological(35.33, precision=UnivMomPrecision.MILLION_YEARS)
        assert m.present(Calendar.GEOLOGICAL, format=fmt) == "35.33 Ma", \
            f"Expected '35.33 Ma', got '{m.present(Calendar.GEOLOGICAL, format=fmt)}'"

        # Cretaceous-Paleogene boundary
        m = UnivMoment.from_geological(66.0, precision=UnivMomPrecision.MILLION_YEARS)
        assert m.present(Calendar.GEOLOGICAL, format=fmt) == "66.00 Ma", \
            f"Expected '66.00 Ma', got '{m.present(Calendar.GEOLOGICAL, format=fmt)}'"

        # --- BILLION_YEARS: basic cases ---
        # Age of the solar system
        m = UnivMoment.from_geological(4.5, precision=UnivMomPrecision.BILLION_YEARS)
        assert m.present(Calendar.GEOLOGICAL, format=fmt) == "4.50 Ga", \
            f"Expected '4.50 Ga', got '{m.present(Calendar.GEOLOGICAL, format=fmt)}'"

        # --- THOUSAND_YEARS: basic cases ---
        m = UnivMoment.from_geological(12.0, precision=UnivMomPrecision.THOUSAND_YEARS)
        assert m.present(Calendar.GEOLOGICAL, format=fmt) == "12.00 ka", \
            f"Expected '12.00 ka', got '{m.present(Calendar.GEOLOGICAL, format=fmt)}'"

        # --- YEAR precision: bare 'a' suffix ---
        m = UnivMoment.from_geological(500, precision=UnivMomPrecision.YEAR)
        assert m.present(Calendar.GEOLOGICAL, format=fmt) == "500 a", \
            f"Expected '500 a', got '{m.present(Calendar.GEOLOGICAL, format=fmt)}'"

        # --- Auto-scale cascade (same logic as %Y/%y) ---
        # 0.77 M-yr = 770,000 yr → auto-scales M → k
        m = UnivMoment.from_geological(0.77, precision=UnivMomPrecision.MILLION_YEARS)
        assert m.present(Calendar.GEOLOGICAL, format=fmt) == "770.00 ka", \
            f"Expected '770.00 ka', got '{m.present(Calendar.GEOLOGICAL, format=fmt)}'"

        # 0.5 G-yr = 500,000,000 yr → auto-scales G → M
        m = UnivMoment.from_geological(0.5, precision=UnivMomPrecision.BILLION_YEARS)
        assert m.present(Calendar.GEOLOGICAL, format=fmt) == "500.00 Ma", \
            f"Expected '500.00 Ma', got '{m.present(Calendar.GEOLOGICAL, format=fmt)}'"

        # 0.5 k-yr = 500 yr → auto-scales k → a (yr)
        m = UnivMoment.from_geological(0.5, precision=UnivMomPrecision.THOUSAND_YEARS)
        assert m.present(Calendar.GEOLOGICAL, format=fmt) == "500 a", \
            f"Expected '500 a', got '{m.present(Calendar.GEOLOGICAL, format=fmt)}'"

        # --- Regression: %y still shows signed form ---
        m = UnivMoment.from_geological(35.33, precision=UnivMomPrecision.MILLION_YEARS)
        assert m.present(Calendar.GEOLOGICAL, format="%y") == "-35.33 M-yr", \
            f"Expected '-35.33 M-yr', got '{m.present(Calendar.GEOLOGICAL, format='%y')}'"

        # --- Combined format string: %G with eon name ---
        m = UnivMoment.from_geological(66.0, precision=UnivMomPrecision.MILLION_YEARS)
        result = m.present(Calendar.GEOLOGICAL, format="%G | %O | %R")
        assert result == "66.00 Ma | Phanerozoic | Mesozoic", \
            f"Expected '66.00 Ma | Phanerozoic | Mesozoic', got '{result}'"

        print(f"✅ SUCCESS: {self.test_format_G_annum_notation.__doc__}")

    # ------------------------------------------------------------------
    # Subtraction of geological moments
    # ------------------------------------------------------------------
    def test_geological_ka_subtraction(self):
        """Subtracting two ka-scale geological moments gives k-years, not M-years"""
        # 11.70 ka − 8.20 ka = 3.50 k-years (using explicit THOUSAND_YEARS precision)
        m1 = UnivMoment.from_geological(11.70, precision=UnivMomPrecision.THOUSAND_YEARS)
        m2 = UnivMoment.from_geological(8.20,  precision=UnivMomPrecision.THOUSAND_YEARS)
        dur = m1 - m2
        assert dur.precision == 5, \
            f"Expected precision 5 (THOUSAND_YEARS), got {dur.precision}"
        assert dur.format_for_display() == "-3.5000 k-years", \
            f"Expected '-3.5000 k-years', got '{dur.format_for_display()}'"
        print(f"✅ SUCCESS: {self.test_geological_ka_subtraction.__doc__}")

    def test_geological_ka_vs_ma_precision_difference(self):
        """Demonstrates why ka values require precision=THOUSAND_YEARS.

        Passing ka-scale values (e.g. 0.01170 Ma = 11.70 ka) with the default
        MILLION_YEARS precision causes the ~3.5 k-year difference to display as
        '-0.0035 M-years' at 4dp.  The negative-zero guard only suppresses the
        sign when ALL displayed digits are zero.
        """
        # Expressed as fractions of a million year (wrong approach for ka values)
        m1_ma = UnivMoment.from_geological(Decimal("0.01170"))   # default = MILLION_YEARS
        m2_ma = UnivMoment.from_geological(Decimal("0.00820"))
        dur_ma = m1_ma - m2_ma
        assert dur_ma.precision == 6, \
            "Both moments carry MILLION_YEARS precision → result must also be M-year scale"
        display = dur_ma.format_for_display()
        # 3.5 ka is visible at 4dp M-year scale; negative sign is preserved because
        # the guard only suppresses sign when all displayed digits are zero.
        assert display == "-0.0035 M-years", \
            f"Expected '-0.0035 M-years' (3.5 ka visible at 4dp M-year scale), got '{display}'"
        print(f"✅ SUCCESS: {self.test_geological_ka_vs_ma_precision_difference.__doc__}")