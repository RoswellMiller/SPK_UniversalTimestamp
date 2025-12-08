from decimal import Decimal

from SPK_UniversalTimestamp.CC00_Decimal_library import DEG2RAD, sin, cos, tan, sqrt, floor, ceil, mod_adj, MAX, MIN, within_precision

class TestDecimalLibrary:
    
    def test_decimal_creation(self):
        """Test creating Decimal objects with various precisions."""
        d1 = Decimal('0.1')
        d2 = Decimal('0.01')
        d3 = Decimal('0.001')
        
        assert d1 == Decimal('0.1')
        assert d2 == Decimal('0.01')
        assert d3 == Decimal('0.001')

    def test_decimal_arithmetic(self):
        """Test basic arithmetic operations with Decimals."""
        d1 = Decimal('0.1')
        d2 = Decimal('0.2')
        
        assert d1 + d2 == Decimal('0.3')
        assert d1 - d2 == Decimal('-0.1')
        assert d1 * d2 == Decimal('0.02')
        assert d2 / d1 == Decimal('2')

    def test_decimal_precision(self):
        """Test precision handling in Decimal operations."""
        d1 = Decimal('1.12345678901234567890')
        d2 = Decimal('1.98765432109876543210')
        
        result = d1 + d2
        assert result == Decimal('3.11111111011111111100')  # Adjusted for precision
        
    def test_trig_functions(self):
        """Test trigonometric functions with Decimal inputs."""
        angle = DEG2RAD * Decimal('45')
        sin_ = sin(angle)
        ans_ = Decimal(1) / sqrt(Decimal(2))
        diff_ = abs(sin_ - ans_)
        assert diff_ < Decimal('1e-29'), f"sin({angle}) = {sin_}, expected {ans_}, difference {diff_}"
    
        cos_ = cos(angle)
        diff_ = abs(cos_ - ans_)
        assert diff_ < Decimal('1e-29'), f"cos({angle}) = {cos_}, expected {ans_}, difference {diff_}"
        
        tan_ = tan(angle)
        diff = abs(tan_ - Decimal(1))
        assert diff < Decimal('1e-29'), f"tan({angle}) = {tan_}, expected {Decimal(1)}, difference {diff}"
        return
    
    def test_mods_functions(self):
        n = Decimal('10.345')
        n_int = floor(n)
        assert n_int == Decimal('10'), f"floor({n}) = {n_int}"
        
        n = Decimal('-10.345')
        n_int = floor(n)
        assert n_int == Decimal('-11'), f"floor({n}) = {n_int}"
        
        n = Decimal('10.345')
        n_int = ceil(n)
        assert n_int == Decimal('11'), f"floor({n}) = {n_int}"
        
        n = Decimal('-10.345')
        n_int = ceil(n)
        assert n_int == Decimal('-10'), f"floor({n}) = {n_int}"
        
        n = Decimal('10')
        n_int = mod_adj(n, 12)
        assert n_int == Decimal('10'), f"floor({n}) = {n_int}"
        
        n = Decimal('12')
        n_int = mod_adj(n, 12)
        assert n_int == Decimal('12'), f"floor({n}) = {n_int}"
        
        
    def test_MIN_MAX_function(self):
        n = MAX(1, lambda x: x < 10)
        assert n == Decimal('9'), f"MAX result = {n}"
        n = MIN(1, lambda x: x > 10)
        assert n == Decimal('11'), f"MIN result = {n}"
            
    def test_within_precision(self):
        a = Decimal('1.0001')
        b = Decimal('1.0002')
        assert within_precision(a, b, -3)  # 10^-3 = 0.001
        assert not within_precision(a, b, -5)  # 10^-5 = 0.00001
        
    def test_round_(self):
        n = Decimal('12.345')
        n_r = round(n)
        #print(f"Original(n): {n}, round(n): {n_r}")
        assert n_r == Decimal('12'), "Round function failed"
        
        n = Decimal('12.545')
        n_r = round(n)
        #print(f"Original(n): {n}, round(n): {n_r}")
        assert n_r == Decimal('13'), "Round function failed"
        return
    
