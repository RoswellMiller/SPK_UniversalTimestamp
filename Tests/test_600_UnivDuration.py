from decimal import Decimal
from SPK_UniversalTimestamp.UnivDuration import UnivDuration
from SPK_UniversalTimestamp.UnivMoment import UnivMoment, UnivMomPrecision

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
        r = UnivDuration(90061, precision=0).format_for_display()
        assert r == "1 day 1 hr 1 min 1 s"

        # --- all-plural compound ---
        # 2*86400 + 3*3600 + 4*60 + 5 = 183845 s
        r = UnivDuration(183845, precision=0).format_for_display()
        assert r == "2 days 3 hrs 4 mins 5 s"

        # --- MINUTE precision: floor stops decomposition at minute ---
        # 3661 s = 1 hr 1 min  (the trailing 1 s is below the MINUTE floor)
        r = UnivDuration(3661, precision=1).format_for_display()
        assert r == "1 hr 1 min"

        # --- HOUR precision: 2 hrs 1 min of raw seconds but floor=HOUR ---
        # 7261 s = 2 hrs + 61 s; HOUR floor discards the residual 61 s
        r = UnivDuration(7261, precision=2).format_for_display()
        assert r == "2 hrs"

        # --- DAY precision: singular and plural ---
        r = UnivDuration(86400,     precision=3).format_for_display()
        assert r  == "1 day"
        r = UnivDuration(3 * 86400, precision=3).format_for_display()
        assert r == "3 days"

        # --- YEAR precision: singular and plural ---
        r = UnivDuration(Decimal('31557600'),          precision=4).format_for_display()
        assert r == "1 year"
        r = UnivDuration(Decimal('2') * UnivDuration.LEVEL_QUANTUM[4], precision=4).format_for_display()
        assert r == "2 years"

        # --- k-year, M-year, B-year: singular stripping ---
        r = UnivDuration(UnivDuration.LEVEL_QUANTUM[5],            precision=5).format_for_display()
        assert r == "1 k-year"
        r = UnivDuration(Decimal('3') * UnivDuration.LEVEL_QUANTUM[5], precision=5).format_for_display()
        assert r == "3 k-years"
        r = UnivDuration(UnivDuration.LEVEL_QUANTUM[6],            precision=6).format_for_display()
        assert r   == "1 M-year"
        r = UnivDuration(UnivDuration.LEVEL_QUANTUM[7],            precision=7).format_for_display()
        assert r   == "1 B-year"

        # --- sub-second: seconds expressed as a decimal to abs(precision) places ---
        r = UnivDuration(Decimal('5.123'), precision=-3).format_for_display()
        assert r  == "5.123 s"

        # --- pure sub-second (no whole seconds) ---
        r = UnivDuration(Decimal('0.001'), precision=-3).format_for_display()
        assert r  == "0.001 s"

        # --- µs precision: compound and pure ---
        r = UnivDuration(Decimal('1.000001'), precision=-6).format_for_display()
        assert r  == "1.000001 s"
        r = UnivDuration(Decimal('0.000001'), precision=-6).format_for_display()
        assert r  == "0.000001 s"

        # --- coarse part + decimal seconds ---
        r = UnivDuration(Decimal('90061.123'), precision=-3).format_for_display()
        assert r  == "1 day 1 hr 1 min 1.123 s"

        # --- zero duration at whole-second and sub-second ---
        r = UnivDuration(0,              precision=0).format_for_display()
        assert r  == "0 s"
        r = UnivDuration(Decimal('0'),   precision=-3).format_for_display()
        assert r  == "0.000 s"

        # --- negative duration: sign prepended, magnitudes identical ---
        r = UnivDuration(-3661, precision=0).format_for_display()
        assert r  == "-1 hr 1 min 1 s"

    def test_format_for_display_fractional_coarse_units(self):
        """format_for_display preserves decimal fraction for year-scale and coarser units"""
        Q = UnivDuration.LEVEL_QUANTUM

        # --- M-years: 1.70 M-years worth of seconds → "1.70 M-years" ---
        assert UnivDuration(Decimal('1.7') * Q[6], precision=6).format_for_display() == "1.70 M-years"

        # --- The motivating case: (-23.03 M-yr) - (-5.33 M-yr) = 17.70 M-yr ---
        m1 = UnivMoment.from_geological(23.03, precision=UnivMomPrecision.MILLION_YEARS)
        m2 = UnivMoment.from_geological(5.33,  precision=UnivMomPrecision.MILLION_YEARS)
        dur = m1 - m2
        assert dur.format_for_display() == "-17.70 M-years", \
            f"Expected '-17.70 M-years', got '{dur.format_for_display()}'"

        # --- k-years fractional: 1.50 k-years ---
        assert UnivDuration(Decimal('1.5') * Q[5], precision=5).format_for_display() == "1.50 k-years"

        # --- B-years fractional: 2.25 B-years ---
        assert UnivDuration(Decimal('2.25') * Q[7], precision=7).format_for_display() == "2.25 B-years"

        # --- Whole-number values are unchanged (no spurious .00 added) ---
        assert UnivDuration(Q[6],            precision=6).format_for_display() == "1 M-year"
        assert UnivDuration(Decimal('3') * Q[5], precision=5).format_for_display() == "3 k-years"
        assert UnivDuration(Q[7],            precision=7).format_for_display() == "1 B-year"

        # --- Negative fractional coarse duration ---
        assert UnivDuration(Decimal('-1.7') * Q[6], precision=6).format_for_display() == "-1.70 M-years"

        print(f"✅ SUCCESS: {self.test_format_for_display_fractional_coarse_units.__doc__}")

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
        assert d.format_for_display() == "10.50 M-years"

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

        # --- precision-span validation: absurd combinations raise ValueError ---
        import pytest

        # B-years + ms: coarsest=7, finest=-3 → too fine (allowed finest=4)
        with pytest.raises(ValueError, match="Precision span too large"):
            UnivDuration.from_string("1 B-years 500 ms")

        # M-years + µs: coarsest=6, finest=-6 → too fine (allowed finest=2)
        with pytest.raises(ValueError, match="Precision span too large"):
            UnivDuration.from_string("1 M-years 1 µs")

        # years + ns: coarsest=4, finest=-9 → too fine (allowed finest=-6)
        with pytest.raises(ValueError, match="Precision span too large"):
            UnivDuration.from_string("1 years 1 ns")

        # On the boundary: years + ds (level -1) must succeed
        d = UnivDuration.from_string("1 year 1 ds")
        assert d.precision == -1

        # Decimal years: 0.615187 years (6 decimal places → effective_prec = 4-6 = -2)
        d = UnivDuration.from_string("0.615187 years")
        assert d.precision == -2   # centiseconds
        assert d.seconds == Decimal("0.615187") * UnivDuration.LEVEL_QUANTUM[4]

        # B-years + years (level 4) is exactly at the limit — must succeed
        d = UnivDuration.from_string("1 B-years 1 year")
        assert d.precision == 4

        # days + µs (level -6) is exactly at the days limit — must succeed
        d = UnivDuration.from_string("1 day 1 µs")
        assert d.precision == -6

    # ------------------------------------------------------------------
    # __format__ spec
    # ------------------------------------------------------------------
    def test_format_spec(self):
        """f-string format spec: '' | 'udur' | 'udur:<abbrev>'"""
        import pytest

        # 90 061 s = 1 day 1 hr 1 min 1 s
        dur = UnivDuration(90061, precision=0)

        # --- empty spec auto-detects coarsest unit (days for 90 061 s) ---
        assert f"{dur}"        == "1 day"
        assert format(dur, "") == "1 day"

        # --- 'udur' delegates to format_for_display() at stored precision ---
        assert f"{dur:udur}"       == dur.format_for_display()
        assert format(dur, "udur") == dur.format_for_display()

        # --- precision override: abbreviation coarser than stored ---
        dur_s = UnivDuration(Decimal("259200"), precision=0)   # 3 days in seconds, sec precision
        assert f"{dur_s:udur:days}" == "3 days"                # coarsen to DAY

        # --- precision override: abbreviation finer than stored ---
        dur_d = UnivDuration(Decimal("86400"), precision=3)    # 1 day, day precision
        # at SECOND precision it expands to the full second count
        assert f"{dur_d:udur:s}" == UnivDuration(Decimal("86400"), precision=0).format_for_display()

        # --- sub-second: seconds expressed as decimal to abs(precision) places ---
        dur_ms = UnivDuration(Decimal("5.123"), precision=-3)
        assert f"{dur_ms:udur}"    == "5.123 s"
        assert f"{dur_ms:udur:ms}" == "5.123 s"

        # --- coarse geological level ---
        by_secs = UnivDuration.LEVEL_QUANTUM[7] * Decimal("4")
        dur_geo = UnivDuration(by_secs, precision=7)
        assert f"{dur_geo:udur}"          == "4 B-years"
        assert f"{dur_geo:udur:B-years}"  == "4 B-years"

        # --- microsecond abbreviation (Unicode µ) ---
        dur_us = UnivDuration(Decimal("0.000001"), precision=-6)
        assert f"{dur_us:udur:\u00b5s}" == "0.000001 s"

        # --- unknown abbreviation raises ValueError ---
        with pytest.raises(ValueError, match="Unknown duration precision abbreviation"):
            format(dur, "udur:fortnight")

        # --- spec without recognized prefix raises ValueError ---
        with pytest.raises(ValueError, match="Unsupported UnivDuration format spec"):
            format(dur, "bad_spec")

    # ------------------------------------------------------------------
    # Negative-zero display guard
    # ------------------------------------------------------------------
    def test_no_negative_zero_display(self):
        """format_for_display never emits '-0…' when the value rounds to zero"""
        Q = UnivDuration.LEVEL_QUANTUM

        # Small negative seconds at M-year precision → rounds to zero display
        small_neg = UnivDuration(-110_451_600_000, precision=6)   # ~ -3.5 k-years at M-yr scale
        display = small_neg.format_for_display()
        assert not display.startswith("-"), \
            f"Expected no leading '-' for near-zero M-year display, got '{display}'"
        assert display == "0.00 M-years", f"Expected '0.00 M-years', got '{display}'"

        # Exact zero → no sign
        assert UnivDuration(0, precision=6).format_for_display() == "0 M-years"
        assert UnivDuration(Decimal("0"), precision=5).format_for_display() == "0 k-years"

    # ------------------------------------------------------------------
    # Auto-detection of coarseness in f"{dur}" (empty spec)
    # ------------------------------------------------------------------
    def test_format_auto_detect_coarse(self):
        """f'{dur}' (no spec) auto-detects the coarsest unit whose quantum <= abs(seconds)"""
        Q = UnivDuration.LEVEL_QUANTUM

        # years (level 4): 1 Julian year stored at second precision
        dur_yr = UnivDuration(Q[4], precision=0)
        assert f"{dur_yr}" == "1 year"

        dur_3yr = UnivDuration(Decimal("3") * Q[4], precision=0)
        assert f"{dur_3yr}" == "3 years"

        # k-years (level 5)
        dur_kyr = UnivDuration(Q[5], precision=0)
        assert f"{dur_kyr}" == "1 k-year"

        dur_4kyr = UnivDuration(Decimal("4") * Q[5], precision=0)
        assert f"{dur_4kyr}" == "4 k-years"

        # M-years (level 6)
        dur_myr = UnivDuration(Q[6], precision=0)
        assert f"{dur_myr}" == "1 M-year"

        dur_5myr = UnivDuration(Decimal("5") * Q[6], precision=0)
        assert f"{dur_5myr}" == "5 M-years"

        # G/B-years (level 7 — 10^9 Julian years)
        dur_byr = UnivDuration(Q[7], precision=0)
        assert f"{dur_byr}" == "1 B-year"

        dur_2byr = UnivDuration(Decimal("2") * Q[7], precision=0)
        assert f"{dur_2byr}" == "2 B-years"

        # Fractional M-years stored at M-year precision
        dur_frac_m = UnivDuration(Decimal("2.5") * Q[6], precision=6)
        assert f"{dur_frac_m}" == "2.50 M-years"

        # Fractional k-years stored at k-year precision
        dur_frac_k = UnivDuration(Decimal("1.75") * Q[5], precision=5)
        assert f"{dur_frac_k}" == "1.75 k-years"

        # Sub-year value: 90 061 s → auto-detects days
        dur_day = UnivDuration(90061, precision=0)
        assert f"{dur_day}" == "1 day"

        # Zero → falls back to seconds
        dur_zero = UnivDuration(0, precision=0)
        assert f"{dur_zero}" == "0 s"

        # Negative: 2 M-years in the past
        dur_neg = UnivDuration(Decimal("-2") * Q[6], precision=6)
        assert f"{dur_neg}" == "-2 M-years"

