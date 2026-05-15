from decimal import Decimal
from SPK_UniversalTimestamp.Constants_aCommon import Calendar, UnivMomPrecision
from SPK_UniversalTimestamp.UnivMoment import UnivMoment
from SPK_UniversalTimestamp.UnivDuration import UnivDuration

class Test_UnivDuration:
    """
    Tests for the UnivDuration class and its functionality
    """
    def test_univ_duration_creation(self):
        """Test creating a UnivDuration instance"""
        duration = UnivDuration(10)
        assert duration.seconds == 10, "UnivDuration value should be initialized to 10"
        assert duration.precision == 0, "Default precision should be SECOND (0)"
        assert duration.precision == 0, "Precision 0 = SECOND"
        duration = UnivDuration(Decimal('0.001'), precision=-3)
        assert duration.seconds == Decimal('0.001'), "UnivDuration value should be initialized to 0.001"
        assert duration.precision == -3, "Precision should be -3 for sub-second (10⁻³) precision"
        assert duration.precision == -3, "Precision -3 = millisecond"
        duration = UnivDuration(Decimal('10E6')*UnivDuration.LEVEL_QUANTUM[6], precision=6)
        assert duration.seconds == Decimal('10E6')*UnivDuration.LEVEL_QUANTUM[6], "UnivDuration value should be initialized to 10E6"
        assert duration.precision == 6, "Precision should be 6 = MILLION_YEAR"
        assert duration.precision == 6, "Precision 6 = MILLION_YEAR"
        duration = UnivDuration(3600*24, precision=3)
        assert duration.seconds == Decimal(3600*24), "UnivDuration value should be initialized to 3600*24"
        assert duration.precision == 3, "Precision should be 3 = DAY"
        assert duration.precision == 3, "Precision 3 = DAY"
            
        return
    
    def test_univ_duration_addition(self):
        """Test adding two UnivDuration instances"""
        duration1 = UnivDuration(10)
        duration2 = UnivDuration(5)
        result = duration1 + duration2
        assert result.seconds == 15, "Adding two UnivDurations should give the correct sum"
        assert result.precision == 0, "Result precision should be 0 (SECOND) when both operands are SECOND"
        duration3 = UnivDuration(Decimal('0.551'), precision=-3)
        result = duration1 + duration3
        assert result.seconds == Decimal('11'), "Adding a sub-second duration should give the correct sum"
        assert result.precision == 0, "Result precision should be 0 (SECOND) when one operand is SECOND and the other is sub-second"
        assert result.precision == 0, "Result precision 0 = SECOND"
    
    def test_univ_duration_str(self):
        """Test the string representation of a UnivDuration instance"""
        duration = UnivDuration(10)
        dur_str = str(duration)
        assert dur_str == "UnivDuration(10)", "String representation should match expected format"

    # ------------------------------------------------------------------
    # to_dict / from_dict round-trip
    # ------------------------------------------------------------------
    def test_to_dict_from_dict(self):
        """to_dict / from_dict preserves seconds and precision"""
        # SECOND precision (default)
        d1 = UnivDuration(Decimal('3600'))
        rt1 = UnivDuration.from_dict(d1.to_dict())
        assert rt1.seconds    == d1.seconds
        assert rt1.precision  == 0
        assert rt1.precision  == 0   # SECOND

        # Sub-second precision  (precision stored as negative int)
        d2 = UnivDuration(Decimal('0.001'), precision=-3)
        rt2 = UnivDuration.from_dict(d2.to_dict())
        assert rt2.seconds    == d2.seconds
        assert rt2.precision  == -3
        assert rt2.precision  == -3   # millisecond

        # Coarse precision
        d3 = UnivDuration(Decimal('10E6') * UnivDuration.LEVEL_QUANTUM[6], precision=6)
        rt3 = UnivDuration.from_dict(d3.to_dict())
        assert rt3.seconds    == d3.seconds
        assert rt3.precision  == 6
        assert rt3.precision  == 6   # MILLION_YEAR

    # ------------------------------------------------------------------
    # to_StdLexicalKey / from_StdLexicalKey
    # ------------------------------------------------------------------
    def test_std_lexical_key(self):
        """Lexical keys have the correct 3-part format and round-trip cleanly"""
        # --- integer seconds, SECOND precision ---
        d1  = UnivDuration(Decimal('1234'), precision=0)
        k1  = d1.to_StdLexicalKey()
        assert k1 == "univDU000000000000001234.000000000000000000.00P"
        rt1 = UnivDuration.from_StdLexicalKey(k1)
        assert rt1.seconds    == d1.seconds
        assert rt1.precision  == 0

        # --- sub-second: 1 ms, precision = -3 ---
        d2  = UnivDuration(Decimal('0.001'), precision=-3)
        k2  = d2.to_StdLexicalKey()
        assert k2 == "univDU000000000000000000.001000000000000000.15L"
        rt2 = UnivDuration.from_StdLexicalKey(k2)
        assert rt2.seconds    == d2.seconds
        assert rt2.precision  == -3

        # --- coarse: 1 day, DAY precision ---
        d3  = UnivDuration(Decimal('86400'), precision=3)
        k3  = d3.to_StdLexicalKey()
        assert k3 == "univDU000000000000086400.000000000000000000.03P"
        rt3 = UnivDuration.from_StdLexicalKey(k3)
        assert rt3.seconds   == d3.seconds
        assert rt3.precision == 3

        # --- lexicographic sort order mirrors duration magnitude ---
        d_hour = UnivDuration(Decimal('3600'),  precision=2)
        d_day  = UnivDuration(Decimal('86400'), precision=3)
        assert d_hour.to_StdLexicalKey() < d_day.to_StdLexicalKey()

        # --- invalid key raises ValueError ---
        import pytest
        with pytest.raises(ValueError):
            UnivDuration.from_StdLexicalKey("bad_key")

    # ------------------------------------------------------------------
    # Precision propagation in + / -
    # ------------------------------------------------------------------
    def test_precision_in_add_subtract(self):
        """_combine always adopts the coarser of the two precisions"""
        # Same precision → result keeps that precision
        s = UnivDuration(Decimal('3600'), precision=2)   # HOUR
        assert (s + s).precision == 2   # HOUR
        assert (s + s).seconds   == Decimal('7200')

        # SECOND + MINUTE → MINUTE (coarser); 10s + 60s = 70s rounds to 60s
        sec = UnivDuration(Decimal('10'),  precision=0)   # SECOND
        mnt = UnivDuration(Decimal('60'),  precision=1)   # MINUTE
        result = sec + mnt
        assert result.precision == 1   # MINUTE
        assert result.seconds   == Decimal('60')   # 70 rounds to nearest 60

        # HOUR + DAY → DAY; 3600s + 86400s = 90000s rounds to 86400s (1 day)
        hr  = UnivDuration(Decimal('3600'),  precision=2)   # HOUR
        day = UnivDuration(Decimal('86400'), precision=3)   # DAY
        result = hr + day
        assert result.precision == 3   # DAY
        assert result.seconds   == Decimal('86400')

        # Sub-second + SECOND → SECOND; 0.001s + 5s = 5.001s rounds to 5s
        ms  = UnivDuration(Decimal('0.001'), precision=-3)
        sec5 = UnivDuration(Decimal('5'),   precision=0)   # SECOND
        result = ms + sec5
        assert result.precision == 0   # SECOND
        assert result.precision == 0   # SECOND (no sub-second fraction)
        assert result.seconds           == Decimal('5')

        # Two sub-second same precision → stays sub-second
        ms1 = UnivDuration(Decimal('0.001'), precision=-3)
        ms2 = UnivDuration(Decimal('0.002'), precision=-3)
        result = ms1 + ms2
        assert result.precision == -3
        assert result.seconds           == Decimal('0.003')

        # Coarser sub-second wins: -3 (ms) + -2 (cs) → -2 (cs)
        ms_ = UnivDuration(Decimal('0.001'), precision=-3)
        cs_ = UnivDuration(Decimal('0.01'),  precision=-2)
        result = ms_ + cs_
        assert result.precision == -2
        assert result.seconds           == Decimal('0.01')  # 0.011 rounds to 0.01

        # Subtraction: YEAR - DAY → YEAR precision
        yr  = UnivDuration(Decimal('31557600'), precision=4)   # YEAR
        day = UnivDuration(Decimal('86400'),    precision=3)   # DAY
        result = yr - day
        assert result.precision == 4   # YEAR

    # ------------------------------------------------------------------
    # format_for_display
    # ------------------------------------------------------------------
    def test_format_for_display(self):
        """format_for_display decomposes to the right units, singular when count==1"""

        # --- classic all-singular compound (docstring example) ---
        # 90061 s = 1 day + 1 hr + 1 min + 1 s
        assert UnivDuration(90061, precision=0).format_for_display() == "1 day 1 hr 1 min 1 s"

        # --- all-plural compound ---
        # 2*86400 + 3*3600 + 4*60 + 5 = 183845 s
        assert UnivDuration(183845, precision=0).format_for_display() == "2 days 3 hrs 4 mins 5 s"

        # --- MINUTE precision: floor stops decomposition at minute ---
        # 3661 s = 1 hr 1 min  (the trailing 1 s is below the MINUTE floor)
        assert UnivDuration(3661, precision=1).format_for_display() == "1 hr 1 min"

        # --- HOUR precision: 2 hrs 1 min of raw seconds but floor=HOUR ---
        # 7261 s = 2 hrs + 61 s; HOUR floor discards the residual 61 s
        assert UnivDuration(7261, precision=2).format_for_display() == "2 hrs"

        # --- DAY precision: singular and plural ---
        assert UnivDuration(86400,     precision=3).format_for_display() == "1 day"
        assert UnivDuration(3 * 86400, precision=3).format_for_display() == "3 days"

        # --- YEAR precision: singular and plural ---
        assert UnivDuration(Decimal('31557600'),          precision=4).format_for_display() == "1 year"
        assert UnivDuration(Decimal('2') * UnivDuration.LEVEL_QUANTUM[4], precision=4).format_for_display() == "2 years"

        # --- k-year, M-year, B-year: singular stripping ---
        assert UnivDuration(UnivDuration.LEVEL_QUANTUM[5],            precision=5).format_for_display() == "1 k-year"
        assert UnivDuration(Decimal('3') * UnivDuration.LEVEL_QUANTUM[5], precision=5).format_for_display() == "3 k-years"
        assert UnivDuration(UnivDuration.LEVEL_QUANTUM[6],            precision=6).format_for_display()  == "1 M-year"
        assert UnivDuration(UnivDuration.LEVEL_QUANTUM[7],            precision=7).format_for_display()  == "1 B-year"

        # --- sub-second compound: s + ms ---
        assert UnivDuration(Decimal('5.123'), precision=-3).format_for_display() == "5 s 123 ms"

        # --- pure sub-second (no whole seconds) ---
        assert UnivDuration(Decimal('0.001'), precision=-3).format_for_display() == "1 ms"

        # --- µs precision: compound and pure ---
        assert UnivDuration(Decimal('1.000001'), precision=-6).format_for_display() == "1 s 1 \u00b5s"
        assert UnivDuration(Decimal('0.000001'), precision=-6).format_for_display() == "1 \u00b5s"

        # --- zero duration at whole-second and sub-second ---
        assert UnivDuration(0,              precision=0).format_for_display() == "0 s"
        assert UnivDuration(Decimal('0'),   precision=-3).format_for_display() == "0 ms"

        # --- negative duration: sign prepended, magnitudes identical ---
        assert UnivDuration(-3661, precision=0).format_for_display() == "-1 hr 1 min 1 s"

    def test_class_constants(self):
        """LEVEL_QUANTUM and LEVEL_ABBREV are public, read-only MappingProxyType class vars"""
        # --- accessible as class attributes ---
        assert UnivDuration.LEVEL_QUANTUM[0] == Decimal("1")
        assert UnivDuration.LEVEL_QUANTUM[3] == Decimal("86400")
        assert UnivDuration.LEVEL_ABBREV[0]  == "s"
        assert UnivDuration.LEVEL_ABBREV[-3] == "ms"
        assert UnivDuration.LEVEL_ABBREV[4]  == "years"

        # --- accessible via instance (same object) ---
        dur = UnivDuration(1)
        assert dur.LEVEL_QUANTUM is UnivDuration.LEVEL_QUANTUM
        assert dur.LEVEL_ABBREV  is UnivDuration.LEVEL_ABBREV

        # --- read-only: mutation raises TypeError ---
        try:
            UnivDuration.LEVEL_QUANTUM[0] = Decimal("2")
            assert False, "Should have raised TypeError"
        except TypeError:
            pass
        try:
            UnivDuration.LEVEL_ABBREV[0] = "sec"
            assert False, "Should have raised TypeError"
        except TypeError:
            pass

    def test_from_string(self):
        """Test constructing a UnivDuration from a human-readable compound string"""
        # --- single integer pair ---
        d = UnivDuration.from_string("5 s")
        assert d.seconds   == Decimal("5")
        assert d.precision == 0

        # --- decimal: precision determined by decimal places ---
        d = UnivDuration.from_string("10.001 s")
        assert d.seconds   == Decimal("10.001")
        assert d.precision == -3    # 0 (s) - 3 decimal places = ms

        # --- coarse unit with decimal: subdivides one level per digit ---
        d = UnivDuration.from_string("10.5 M-years")
        assert d.precision == 5    # 6 - 1 = k-years
        assert d.format_for_display() == "10 M-years 500 k-years"

        # --- compound string: precision = finest level across all pairs ---
        d = UnivDuration.from_string("1 day 2 hrs 30 mins")
        assert d.seconds   == Decimal("95400")
        assert d.precision == 1    # mins
        assert d.format_for_display() == "1 day 2 hrs 30 mins"

        # --- singular form accepted alongside plural ---
        d_sing = UnivDuration.from_string("1 day")
        d_plur = UnivDuration.from_string("1 days")
        assert d_sing.seconds   == Decimal("86400")
        assert d_sing.precision == 3
        assert d_sing.seconds   == d_plur.seconds

        # --- decimal on compound: finest effective precision wins ---
        d = UnivDuration.from_string("1 day 2.5 hrs")
        assert d.precision == 1    # min(3, 2-1=1) = 1 (mins)
        assert d.format_for_display() == "1 day 2 hrs 30 mins"

        # --- round-trip with format_for_display ---
        original = UnivDuration(90061, precision=0)
        restored = UnivDuration.from_string(original.format_for_display())
        assert restored.seconds   == original.seconds
        assert restored.precision == original.precision

        # --- invalid input raises ValueError ---
        try:
            UnivDuration.from_string("not a duration at all")
            assert False, "Should have raised ValueError"
        except ValueError:
            pass