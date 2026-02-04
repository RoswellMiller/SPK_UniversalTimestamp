"""
Comprehensive tests for the Moment_Gregorian class.
"""
import os
import json
import random

from decimal import Decimal
from SPK_UniversalTimestamp.CC00_Decimal_library import trunc
from SPK_UniversalTimestamp.Constants_aCommon import Calendar, Precision
from SPK_UniversalTimestamp.Constants_Gregorian import gregorian_MONTH_ATTS
from SPK_UniversalTimestamp.Moment_aUniversal import UnivMoment
from SPK_UniversalTimestamp.Moment_bPresent_Calendars import Present_Calendars

class Test_Present_Gregorian: 
    """Test cases for Moment_Gregorian class."""
    def setup_method(self):
        """Setup for each test method."""
        cwd = os.getcwd()
        print(f"Current working directory: {cwd}")
        with open("Tests\\RandD_appendix_c.json", "r") as f:
            self.appendix_c_table = json.load(f)
        return
    
    def test_appendix_c_Construction(self):
        """Test Appendix C: Calendar construction."""
        print("\n1. APPENDIX C: CALENDAR CONSTRUCTION page 447")
        print("-" * 40)
        failures = 0
        failure_list = []
        for appendix_c_ndx in range(len(self.appendix_c_table['R.D.'])):
            calendar = 'Gregorian'
            test_rd = self.appendix_c_table['R.D.'][appendix_c_ndx] 
            test_weekday = self.appendix_c_table['Weekday'][appendix_c_ndx]
            test_weekday_ndx = None
            for ndx in range(7):
                if Present_Calendars.DAY_OF_THE_WEEK_ATTS['en'][ndx]['name'] == test_weekday:
                    test_weekday_ndx = ndx
                    break   
            if test_weekday_ndx is None:
                print(f"    ❌ Invalid weekday name in Appendix C row {appendix_c_ndx+1}: {test_weekday}")
                failures += 1
                continue      
            test_year = self.appendix_c_table[f'{calendar}-year'][appendix_c_ndx]
            test_month = self.appendix_c_table[f'{calendar}-month'][appendix_c_ndx]
            test_day = self.appendix_c_table[f'{calendar}-day'][appendix_c_ndx]
            test_date = (appendix_c_ndx, calendar, test_year, test_month, test_day)
            msg = f"Row {appendix_c_ndx+1} {calendar} date: {test_year}-{test_month:02d}-{test_day:02d}"
            try:
                moment = UnivMoment.from_gregorian(test_year, test_month, test_day, precision=Precision.DAY)
                if (test_rd,(0,0,0)) == moment.rd_moment():
                    print(f"    ✅ {msg}")
                else:
                    print(f"    ❌ R.D.Error {test_rd}")
                    print(f"         Returned     : {moment.rd_moment()}")
                    failures += 1
                    failure_list.append(test_date)
            except Exception as e:
                print(f"    ❌{msg}")
                print(f"        Exception : {e}")
                failures += 1
            continue
        if failures > 0:
            assert False, f"❌ {failures} test(s) failed in Appendix C."
        else:
            print("✅ All tests in Appendix C passed successfully!")
        return
    
    def test_appendix_c_Presentation(self):
        """Test Appendix C: Calendar presentation."""
        print("\n2. APPENDIX C: CALENDAR PRESENTATION page 447")
        print("-" * 40)
        failures = 0
        failure_list = []
        for appendix_c_ndx in range(len(self.appendix_c_table['R.D.'])):
            calendar = 'Gregorian'
            test_rd = self.appendix_c_table['R.D.'][appendix_c_ndx] 
            test_weekday = self.appendix_c_table['Weekday'][appendix_c_ndx]
            test_weekday_ndx = None
            for ndx in range(7):
                if Present_Calendars.DAY_OF_THE_WEEK_ATTS['en'][ndx]['name'] == test_weekday:
                    test_weekday_ndx = ndx
                    break   
            if test_weekday_ndx is None:
                print(f"    ❌ Invalid weekday name in Appendix C row {appendix_c_ndx+1}: {test_weekday}")
                failures += 1
                continue      
            test_year = self.appendix_c_table[f'{calendar}-year'][appendix_c_ndx]
            test_month = self.appendix_c_table[f'{calendar}-month'][appendix_c_ndx]
            test_day = self.appendix_c_table[f'{calendar}-day'][appendix_c_ndx]
            test_date = (appendix_c_ndx, calendar, test_year, test_month, test_day)
            msg = f"Row {appendix_c_ndx+1} {calendar} date: {test_year}-{test_month:02d}-{test_day:02d}"
            test_cases = [
            {   'format': "%d/%m/%Y", 'condition' : lambda : True,
                'answer': f"{test_day:02d}/{test_month:02d}/{test_year:d}"},
            {   'format': "%#d/%#m/%Y", 'condition' : lambda : True,
                'answer': f"{test_day:d}/{test_month:d}/{test_year:d}"},
            {   'format': "%d %b. %Y",  'condition' : lambda : True,
                'answer': f"{test_day:02d} {gregorian_MONTH_ATTS['en'][test_month]['abbrv']}. {test_year:d}"},
            {   'format': "%A %d %B, %Y",  'condition' : lambda : True,
                'answer': f"{test_weekday} {test_day:02d} {gregorian_MONTH_ATTS['en'][test_month]['name']}, {test_year:d}"},
            {   'format': "%A %d %B, %y", 'condition' : lambda : test_year >= 0,
                'answer': f"{test_weekday} {test_day:02d} {gregorian_MONTH_ATTS['en'][test_month]['name']}, {test_year:d}"},
            {   'format': "%a %d %B, %y", 'condition' : lambda : test_year < 0,
                'answer': f"{Present_Calendars.DAY_OF_THE_WEEK_ATTS['en'][test_weekday_ndx]['abbrv']} {test_day:02d} {gregorian_MONTH_ATTS['en'][test_month]['name']}, {abs(test_year):d} BCE"},
            ]
            try:
                for test_case in test_cases:
                    if not test_case['condition']():
                        continue
                    moment = UnivMoment(test_rd, precision=Precision.DAY)
                    presentation = moment.present(Calendar.GREGORIAN, test_case['format'], language='en')
                    if presentation == test_case['answer']:
                        print(f"    ✅ {msg}")
                    else:
                        print(f"    ❌ R.D.Error {test_rd}")
                        print(f"         Format string: {test_case['format']}")
                        print(f"         Returned     : {presentation}")
                        print(f"         Expected     : {test_case['answer']}")
                        failures += 1
                        failure_list.append(test_date)
                    continue
            except ValueError as e:
                print(f"    ❌ValueError : {e}")
                failures += 1
            continue
        if failures > 0:
            assert False, f"❌ {failures} test(s) failed in Appendix C."
        else:
            print("✅ All tests in Appendix C passed successfully!")
        return

    def test_Precision_and_Time(self):
        """Test Appendix C: Calendar presentation."""
        print("\n3. APPENDIX C: Precision and Time")
        print("-" * 40)
        failures = 0
        failure_list = []
        for appendix_c_ndx in range(len(self.appendix_c_table['R.D.'])):
            calendar = 'Gregorian'
            test_rd = self.appendix_c_table['R.D.'][appendix_c_ndx] 
            test_weekday = self.appendix_c_table['Weekday'][appendix_c_ndx]
            test_weekday_ndx = None
            for ndx in range(7):
                if Present_Calendars.DAY_OF_THE_WEEK_ATTS['en'][ndx]['name'] == test_weekday:
                    test_weekday_ndx = ndx
                    break   
            if test_weekday_ndx is None:
                print(f"    ❌ Invalid weekday name in Appendix C row {appendix_c_ndx+1}: {test_weekday}")
                failures += 1
                continue      
            test_year = self.appendix_c_table[f'{calendar}-year'][appendix_c_ndx]
            test_month = self.appendix_c_table[f'{calendar}-month'][appendix_c_ndx]
            test_day = self.appendix_c_table[f'{calendar}-day'][appendix_c_ndx]
            test_date = (appendix_c_ndx, calendar, test_year, test_month, test_day)
            
            test_hour = random.randint(0, 23)
            test_minute = random.randint(0, 59)
            test_second = random.randint(0, 59)
            test_fractional_second = random.randint(0, 999_999)
            test_seconds = Decimal(f"{test_second}.{test_fractional_second:06d}")
            msg = f"Row {appendix_c_ndx+1} {calendar} date: {test_year}-{test_month:02d}-{test_day:02d} {test_hour:02d}:{test_minute:02d}:{test_seconds:09.6f}"
            test_cases = [
            {   'format': "%d/%m/%Y %H:%M:%S%f", 'condition' : lambda : True,
                'precision': Precision.MICROSECOND,
                'answer': f"{test_day:02d}/{test_month:02d}/{test_year:d} {trunc(test_hour):02.0f}:{trunc(test_minute):02.0f}:{trunc(test_seconds, decimals=6):09.6f}"},
            {   'format': "%d/%m/%Y %H:%M:%S%f", 'condition' : lambda : True,
                'precision': Precision.MILLISECOND,
                'answer': f"{test_day:02d}/{test_month:02d}/{test_year:d} {trunc(test_hour):02.0f}:{trunc(test_minute):02.0f}:{trunc(test_seconds, decimals=3):06.3f}"},
            
            {   'format': "%d/%m/%Y %H:%M:%S%f2", 'condition' : lambda : True,
                'precision': Precision.MILLISECOND,
                'answer': f"{test_day:02d}/{test_month:02d}/{test_year:d} {trunc(test_hour):02.0f}:{trunc(test_minute):02.0f}:{trunc(test_seconds, decimals=2):05.2f}"},
            
            {   'format': "%d/%m/%Y %H:%M:%S%f", 'condition' : lambda : True,
                'precision': Precision.SECOND,
                'answer': f"{test_day:02d}/{test_month:02d}/{test_year:d} {trunc(test_hour):02.0f}:{trunc(test_minute):02.0f}:{trunc(test_seconds):02.0f}"},
            {   'format': "%d/%m/%Y %H:%M", 'condition' : lambda : True,
                'precision': Precision.MINUTE,
                'answer': f"{test_day:02d}/{test_month:02d}/{test_year:d} {trunc(test_hour):02.0f}:{trunc(test_minute):02.0f}"},
            {   'format': "%d/%m/%Y %I%p", 'condition' : lambda : True,
                'precision': Precision.HOUR,
                'answer': f"{test_day:02d}/{test_month:02d}/{test_year:d} {trunc(test_hour % 12):02.0f}{'am' if test_hour < 12 else 'pm'}"},
            {   'format': "%d/%m/%Y", 'condition' : lambda : True,
                'precision': Precision.DAY,
                'answer': f"{test_day:02d}/{test_month:02d}/{test_year:d}"},
            {   'format': "%m/%Y", 'condition' : lambda : True,
                'precision': Precision.MONTH,
                'answer': f"{test_month:02d}/{test_year:d}"},
            {   'format': "%Y", 'condition' : lambda : True,
                'precision': Precision.YEAR,
                'answer': f"{test_year:d}"},
            ]
            try:
                for test_case in test_cases:
                    if not test_case['condition']():
                        continue
                    if test_case['precision'] == Precision.MICROSECOND:
                        moment = UnivMoment.from_gregorian(
                            test_year, test_month, test_day,
                            test_hour, test_minute, test_seconds,
                            precision=test_case['precision']
                        )
                    elif test_case['precision'] == Precision.MILLISECOND:
                        moment = UnivMoment.from_gregorian(
                            test_year, test_month, test_day,
                            test_hour, test_minute, test_seconds,
                            precision=test_case['precision']
                        )
                    elif test_case['precision'] == Precision.SECOND:
                        moment = UnivMoment.from_gregorian(
                            test_year, test_month, test_day,
                            test_hour, test_minute, int(test_seconds),
                            precision=test_case['precision']
                        )
                    elif test_case['precision'] == Precision.MINUTE:
                        moment = UnivMoment.from_gregorian(
                            test_year, test_month, test_day,
                            test_hour, test_minute,
                            precision=test_case['precision']
                        )
                    elif test_case['precision'] == Precision.HOUR:
                        moment = UnivMoment.from_gregorian(
                            test_year, test_month, test_day,
                            test_hour,
                            precision=test_case['precision']
                        )
                    elif test_case['precision'] == Precision.DAY:
                        moment = UnivMoment.from_gregorian(
                            test_year, test_month, test_day,
                            precision=test_case['precision']
                        )
                    elif test_case['precision'] == Precision.MONTH:
                        moment = UnivMoment.from_gregorian(
                            test_year, test_month,
                            precision=test_case['precision']
                        )
                    elif test_case['precision'] == Precision.YEAR:
                        moment = UnivMoment.from_gregorian(
                            test_year,
                            precision=test_case['precision']
                        )
                    else:
                        raise ValueError(f"Unsupported precision in test case: {test_case['precision']}")
                    presentation = moment.present(Calendar.GREGORIAN, test_case['format'], language='en')
                    if presentation == test_case['answer']:
                        print(f"    ✅ {msg}")
                    else:
                        print(f"    ❌ R.D.Error {test_rd}")
                        print(f"         Format string: {test_case['format']}")
                        print(f"         Returned     : {presentation}")
                        print(f"         Expected     : {test_case['answer']}")
                        failures += 1
                        failure_list.append(test_date)
                    continue
            except ValueError as e:
                print(f"    ❌ValueError : {e}")
                failures += 1
            continue
        if failures > 0:
            assert False, f"❌ {failures} test(s) failed in Appendix C."
        else:
            print("✅ All tests in Appendix C passed successfully!")
        return
