import os
import json
from datetime import datetime, timezone
from random import randint
from decimal import Decimal
import inspect

from SPK_UniversalTimestamp.CC01_Calendar_Basics import *
from SPK_UniversalTimestamp.CC02_Gregorian import *
from SPK_UniversalTimestamp.CC03_Julian import *

from SPK_UniversalTimestamp import *
from SPK_UniversalTimestamp.UnivGREGORIAN import UnivGREGORIAN
from SPK_UniversalTimestamp.UnivJULIAN import UnivJULIAN    
from SPK_UniversalTimestamp.UnivTimestampFactory import UnivTimestampFactory
from SPK_UniversalTimestamp.UnivGEOLOGICAL import UnivGEOLOGICAL
from SPK_UniversalTimestamp.UnivHEBREW import UnivHEBREW
from SPK_UniversalTimestamp.UnivCHINESE import UnivCHINESE


class TestUniversalTimestamp:
    """Test cases for UnivTimestamp class."""
    def setup_method(self):
        """Setup for each test method."""
        cwd = os.getcwd()
        print(f"Current working directory: {cwd}")
        with open("Tests\\RandD_appendix_c.json", "r") as f:
            self.appendix_c_table = json.load(f)

        with open("Tests\\random_cases.json", "r") as f:
            self.random_case_table = json.load(f)
            
    def test_scientific_creation(self):
        """Test scientific measurement with high precision."""
        timestamp = UnivTimestampFactory.for_SCIENTIFIC(
            2035, 7, 28, 21, 47, Decimal("30.123_123_123_123_123_123"),
            description="quantum experiment"
        )
        
        assert timestamp.calendar == Calendar.GREGORIAN
        assert timestamp.precision == Precision.ATTOSECOND
        assert timestamp.year == 2035
        assert timestamp.month == 7
        assert timestamp.day == 28
        assert timestamp.hour == 21
        assert timestamp.minute == 47
        assert timestamp.second == Decimal('30.123123123123123123')
        
        print(f"✅ SUCCESS: {inspect.currentframe().f_code.co_name}")
        return
        
    def test_unix_timestamp_creation(self):
        """Test Unix timestamp conversion with precision."""
        unix_time = 1640995200.123456789
        dt = datetime.fromtimestamp(unix_time, tz=timezone.utc)
        
        timestamp = UnivTimestampFactory.from_unix_timestamp(
            unix_time,
            description="Unix timestamp"
        )
        assert timestamp.calendar == Calendar.GREGORIAN
        assert timestamp.precision == Precision.NANOSECOND
        assert timestamp.year == dt.year
        assert timestamp.month == dt.month    
        assert timestamp.day == dt.day
        assert timestamp.hour == dt.hour
        assert timestamp.minute == dt.minute
        assert timestamp.second == Decimal('0.123456700')
        print(f"✅ SUCCESS: {inspect.currentframe().f_code.co_name}")
        return
    
    def test_now(self):
        """Test getting the current timestamp."""
        now = UnivTimestampFactory.now()
        now_str = now.format_signature()
        print(f"Current timestamp: {now_str}")
        now_rd = now.rd
        print(f"Current Rata Die: {now_rd}")
        now_en = now.strftime("%A, %B %d, %Y %H:%M:%S.%f", language='en')
        print(f"Current timestamp (English): {now_en}")
        now_fr = now.strftime("%A %d %B %Y %H:%M:%S", language='fr')
        print(f"Current timestamp (French): {now_fr}")
        now_de = now.strftime("%A %d %B %Y %H:%M:%S", language='de')
        print(f"Current timestamp (German): {now_de}")
        now_es = now.strftime("%A %d %B %Y %I:%M:%S %p", language='es')
        print(f"Current timestamp (Spanish): {now_es}")
        now_it = now.strftime("%A %d %B %Y %I:%M:%S %p", language='it')
        print(f"Current timestamp (Italian): {now_it}")
        assert isinstance(now, UnivGREGORIAN)
        assert now.calendar == Calendar.GREGORIAN
        
        # Check if the current date matches
        current_dt = datetime.now(timezone.utc)
        assert now.year == current_dt.year
        assert now.month == current_dt.month
        assert now.day == current_dt.day
        
        print(f"✅ SUCCESS: {inspect.currentframe().f_code.co_name}")
        return
    
    def test_beginning_of_time(self):
        """Test the beginning of time representation."""
        bot = UnivTimestampFactory.beginning_of_time()
        bot_str = bot.format_signature()
        print(f"Beginning of Time timestamp: {bot_str}")
        assert isinstance(bot, UnivGEOLOGICAL)
        assert bot.precision == Precision.YEAR
        assert bot.year.is_infinite()
        
        print(f"✅ SUCCESS: {inspect.currentframe().f_code.co_name}")
        return
    
    def test_min_max_rata_die(self):
        """Test Minimium and Maxium Rata Diw (R.D.) for Gregorian Calendar."""
        # Test minimum R.D. for Julian calendar
        min_greg = UnivGREGORIAN(-9999, 1, 1)
        rd = min_greg.rd
        assert rd == -3652424 # R.D. for 1 Jan -9999
        max_greg = UnivGREGORIAN(9999, 12, 31)
        rd = max_greg.rd
        assert rd == 3652059  # R.D
        print(f"✅ SUCCESS: {inspect.currentframe().f_code.co_name}")
        return        
        
    def test_error_handling(self):
        """Test error handling for invalid inputs."""

        print("❌ERROR HANDLING TESTS DISABLED ===============================❌")
    #     # Test invalid calendar date
    #     with pytest.raises(ValueError):
    #         UnivHEBREW(-23, 1, 1)
    #     with pytest.raises(ValueError):
    #         UnivHEBREW(5778, 13, 1)  # Invalid month
    #     with pytest.raises(ValueError):
    #         UnivHEBREW(5779, 1, 32)
    #     with pytest.raises(ValueError):
    #         UnivGREGORIAN(10240, 1, 1)  # Invalid year
    #     with pytest.raises(ValueError):
    #         UnivGREGORIAN(2024, 13, 1)  # Invalid month
    #     with pytest.raises(ValueError):
    #         UnivGREGORIAN(2024, 5, -3)  # Invalid day
    #     with pytest.raises(ValueError):
    #         UnivJULIAN(1752, 1, 1, 45)  # Invalid hour
    #     with pytest.raises(ValueError):
    #         UnivJULIAN(1752, 1, 1, 12, -8)  # Invalid minute
    #     with pytest.raises(ValueError):
    #         UnivJULIAN(1752, 1, 1, 12, 34, -567)  # Invalid second
    #     with pytest.raises(TypeError):
    #         UnivGREGORIAN("2024", 1, 1)
    #     with pytest.raises(TypeError):
    #         UnivGREGORIAN(2024, "January", 1)
    #     with pytest.raises(ValueError):
    #         UnivGREGORIAN(2024, None, 1)
            
    def test_appendex_c(self):
        """Test Appendix C: Calendar conversion."""
        print("\n4. APPENDIX C: CALENDAR CONVERSION page 447")
        print("-" * 40)
        test_calendars = ['Unix', 'Gregorian', 'Julian Date', 'Hebrew Standard', 'Chinese Date']
        calendar_classes = {
            'Gregorian': UnivGREGORIAN,
            'Julian Date': UnivJULIAN,
            'Hebrew Standard': UnivHEBREW,
            'Chinese Date': UnivCHINESE,
        }

        failures = 0
        failure_list = []
        for i in range(len(self.appendix_c_table['R.D.'])):
            test_rd = self.appendix_c_table['R.D.'][i]           
            for calendar in test_calendars:
                try:
                    if calendar == 'Unix':
                        test_unix = self.appendix_c_table['Unix'][i]
                        test_date = ModuleNotFoundError
                        msg = f"Row {i+1} Unix timestamp: {test_unix}"
                        univ = UnivTimestampFactory.from_unix_timestamp(test_unix, description=msg)
                    elif calendar == 'Chinese Date':
                        test_cycle = self.appendix_c_table[f'{calendar}-cycle'][i]
                        test_year = self.appendix_c_table[f'{calendar}-year'][i]
                        test_month = self.appendix_c_table[f'{calendar}-month'][i]
                        test_leap = self.appendix_c_table[f'{calendar}-leap'][i]
                        test_day = self.appendix_c_table[f'{calendar}-day'][i]
                        test_date = (i, calendar, test_cycle, test_year, test_month, test_leap, test_day)
                        msg = f"Row {i+1} {calendar} date: {test_cycle},{test_year}-{test_month:02d} {test_leap}-{test_day:02d}"
                        selected_class = calendar_classes[calendar]
                        univ = selected_class(test_cycle, test_year, (test_month, test_leap), test_day, description=msg)
                    else:
                        test_year = self.appendix_c_table[f'{calendar}-year'][i]
                        test_month = self.appendix_c_table[f'{calendar}-month'][i]
                        test_day = self.appendix_c_table[f'{calendar}-day'][i]
                        test_date = (i, calendar, test_year, test_month, test_day)
                        msg = f"Row {i+1} {calendar} date: {test_year}-{test_month:02d}-{test_day:02d}"
                        selected_class = calendar_classes[calendar]
                        univ = selected_class(test_year, test_month, test_day, description=msg)
                        
                    assert_rd = univ.rd
                    if assert_rd == test_rd:
                        print(f"    ✅ {msg}")
                    else:
                        print(f"    ❌ R.D.Error {test_rd}, got {assert_rd} for {msg}")
                        failures += 1
                        failure_list.append(test_date)
                except ValueError as e:
                    print(f"    ❌ValueError : {e}")
                    failures += 1
                continue
            continue
        if failures > 0:
            assert False, print(f"❌ {failures} test(s) failed in Appendix C.")
        else:
            print("✅ All tests in Appendix C passed successfully!")
        return
    
    def test_parse_appendex_c(self):
        """Test Appendix C: Calendar conversion."""
        print("\n5. APPENDIX C: Signature Production and Parsing")
        print("-" * 40)
        test_calendars = ['Gregorian', 'Julian Date', 'Hebrew Standard']
        calendar_classes = {
            'Gregorian': UnivGREGORIAN,
            'Julian Date': UnivJULIAN,
            'Hebrew Standard': UnivHEBREW
        }

        failures = 0
        failure_list = []
        for i in range(len(self.appendix_c_table['R.D.'])):
            for calendar in test_calendars:
                try:
                    test_year = self.appendix_c_table[f'{calendar}-year'][i]
                    test_month = self.appendix_c_table[f'{calendar}-month'][i]
                    test_day = self.appendix_c_table[f'{calendar}-day'][i]
                    test_date = (i, calendar, test_year, test_month, test_day)
                    msg = f"Row {i+1} {calendar} date: {test_year}-{test_month:02d}-{test_day:02d}"
                    selected_class = calendar_classes[calendar]
                    univ = selected_class(test_year, test_month, test_day, description=msg)
                    univ_str = univ.format_signature()
                    print(f"    {univ_str}")
                    univ_p = UnivTimestampFactory.parse(univ_str, description=univ.description)
                    if univ_p is None:
                        print(f"    ❌ Parse failed on [{univ_str}] for {msg}")
                        failures += 1
                        failure_list.append(test_date)
                        continue
                    #univ_rd = univ.rd
                    #assert_rd = univ_p.rd 
                    if univ == univ_p:
                        print(f"    ✅ {msg}")
                    else:
                        print(f"    ❌ Parse failed on [{univ_str}] for {msg}")
                        failures += 1
                        failure_list.append(test_date)
                except ValueError as e:
                    print(f"    ❌ValueError : {e}")
                    failures += 1
                continue
            continue
        if failures > 0:
            assert False, f"❌ {failures} test(s) failed in Appendix C."
        else:
            print("✅ All tests in Appendix C passed successfully!")
        return
    
    def test_random_cases(self):    
        """Test Appendix C: Calendar conversion."""
        print("\n6. RANDOM CASES TEST")
        print("-" * 40)
        calendar_classes = {
            'Gregorian': UnivGREGORIAN,
            'Julian': UnivJULIAN,
            'Hebrew': UnivHEBREW,
            'Geological' : UnivGEOLOGICAL,
        }
        format_list = [
            '%Y-%m-%d %H:%M:%S %K',
            '%y-%B-%d %A %H:%M:%S %k',
            '%Y-%b-%d %a %H:%M:%S.%f',
            '%Y-%m-%d %I:%M:%S.%f %p',
            '%c',
            '%x',
            '%X',
        ]
        precision_by_level = {}
        for precision in Precision:
            precision_by_level[PrecisionAtts[precision]['level']] = precision
        failures = 0
        failure_list = []
        msg = ''
        fmt = ''
        ts =UnivTimestampFactory.now()
        self.random_case_table.append({'index': 'now', 'calendar': 'Gregorian', 'year': ts.year, 'month': ts.month, 'day': ts.day, 'hour': ts.hour, 'minute': ts.minute, 'second': ts.second, 'precision': 11, 'description': 'Current timestamp'})
        for case in self.random_case_table:
            msg = f"Construct case {case['index']}:" 
            fmt = ''
            try:
                calendar = case['calendar']
                year = case['year']
                month = case['month']
                day = case['day']
                hour = case['hour']
                minute = case['minute']
                second = Decimal(case['second']) if case['second'] is not None else None
                precision = precision_by_level[case['precision']]
                description = case['description']
                selected_class = calendar_classes[calendar]
                if calendar == 'Geological':
                    univ = selected_class(year, precision=precision, description=description)
                else:
                    univ = selected_class(year, month, day, hour, minute, second, precision=precision, description=description)
                msg = univ.format_signature()

                for i in range(len(format_list)):
                    fmt =  f"{i}. >" + format_list[i]
                    univ_str = univ.strftime(fmt)
                    
                if case['calendar'] != 'Geological':          
                    if case['index'] == 'now':
                        lng = 'en'
                    else:
                        lng = ('en','fr','de','es','it')[randint(0,4)]
                    msg = univ.strftime("%A %#d %B, %Y %k %I:%M:%S.%f %p %Z", language=lng)
                else:
                    msg = univ.strftime("%Y %B: %A, %H, %M", language='en')    
                if True:
                    if case['index'] == 'now':
                        print(f"    ✅ {case['index']:<4} - {msg}")
                    else:
                        print(f"    ✅ {case['index']:>4} - {msg}")
                else:
                    print(f"    ❌ Parse failed on [{univ_str}] for {msg}")
                    failures += 1
                    failure_list.append(case)
            except (ValueError, TypeError, AttributeError) as e:
                print(f"    ❌Error[{case['index']}. {msg}->{fmt}] {e}")
                failures += 1
                failure_list.append(case)
            continue
        
        if failures > 0:
            assert False, f"❌ {failures} test(s) failed in Random Cases."
        else:
            print("✅ All tests in Random Cases passed successfully!")
        return
    
    
