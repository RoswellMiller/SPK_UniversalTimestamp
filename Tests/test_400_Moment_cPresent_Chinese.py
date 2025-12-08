"""
Comprehensive tests for the Moment_Chinese class.
"""
import os
import json

from SPK_UniversalTimestamp.Constants_aCommon import Calendar, Precision
from SPK_UniversalTimestamp.Constants_Chinese import chinese_MONTH_ATTS
from SPK_UniversalTimestamp.Moment_aUniversal import UnivMoment
from SPK_UniversalTimestamp.Moment_bPresent_Calendars import Present_Calendars


class Test_Moment_Chinese: 
    """Test cases for Moment_Chinese class."""

    def setup_method(self):
        """Setup for each test method."""
        cwd = os.getcwd()
        print(f"Current working directory: {cwd}")
        with open("Tests\\RandD_appendix_c.json", "r") as f:
            self.appendix_c_table = json.load(f)

        # with open("Tests\\random_cases.json", "r") as f:
        #     self.random_case_table = json.load(f)
        return
    
    def test_appendix_c_Construction(self):
        """Test Appendix C: Calendar construction."""
        print("\n1. APPENDIX C: CALENDAR CONSTRUCTION page 447")
        print("-" * 40)
        failures = 0
        for appendix_c_ndx in range(len(self.appendix_c_table['R.D.'])):
            calendar = 'Chinese Date'
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
            test_cycle = self.appendix_c_table[f'{calendar}-cycle'][appendix_c_ndx]
            test_year = self.appendix_c_table[f'{calendar}-year'][appendix_c_ndx]
            test_month = self.appendix_c_table[f'{calendar}-month'][appendix_c_ndx]
            test_leap = self.appendix_c_table[f'{calendar}-leap'][appendix_c_ndx]
            test_suffix = 'L' if test_leap else ''
            test_month_name = chinese_MONTH_ATTS[test_month][test_leap]['pinyin']
            test_day = self.appendix_c_table[f'{calendar}-day'][appendix_c_ndx]
            test_date = (appendix_c_ndx, calendar, test_cycle, test_year, test_month, test_leap, test_day)
            msg = f"Row {appendix_c_ndx+1} {calendar} R.D. {test_rd} => "
            print(msg)
            print(f"  test :: {test_cycle} | {test_year} | {test_month} | {test_leap} | {test_day}")
            
            try:
                moment = UnivMoment.from_chinese(test_cycle, test_year, (test_month, test_leap), test_day, precision=Precision.DAY)
                if (test_rd, (0,0,0)) == moment.rd_moment():
                    print(f"    ✅ {msg}")
                else:
                    print(f"    ❌ R.D.Error {test_rd}")
                    print(f"         Returned     : {moment.rd_moment()}")
                    failures += 1
            except Exception as e:
                print(f"    ❌{msg}")
                print(f"        Exception : {e}")
                failures += 1
            continue
        if failures > 0:
            assert False, f"❌ {failures} cases failed in Appendix C."
        else:
            print("✅ All construction tests in Appendix C passed successfully!")
        return
    
    def test_appendix_c_Presentation(self):
        """Test Appendix C: Calendar presentation."""
        print("\n4. APPENDIX C: CALENDAR PRESENTATION page 447")
        print("-" * 40)
        failures = 0
        failure_list = []
        for appendix_c_ndx in range(len(self.appendix_c_table['R.D.'])):
            calendar = 'Chinese Date'
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
            test_cycle = self.appendix_c_table[f'{calendar}-cycle'][appendix_c_ndx]
            test_year = self.appendix_c_table[f'{calendar}-year'][appendix_c_ndx]
            test_month = self.appendix_c_table[f'{calendar}-month'][appendix_c_ndx]
            test_leap = self.appendix_c_table[f'{calendar}-leap'][appendix_c_ndx]
            test_suffix = 'L' if test_leap else ''
            test_month_name = chinese_MONTH_ATTS[test_month][test_leap]['pinyin']
            test_day = self.appendix_c_table[f'{calendar}-day'][appendix_c_ndx]
            test_date = (appendix_c_ndx, calendar, test_cycle, test_year, test_month, test_leap, test_day)
            msg = f"Row {appendix_c_ndx+1} {calendar} R.D. {test_rd} => "
            print(msg)
            print(f"  test :: {test_cycle} | {test_year} | {test_month} | {test_leap} | {test_day}")
            
            test_cases = [
            {   'format': "%K %d/%m/%Y (%C)", 'condition' : lambda : True,
                'answer': f"Chinese {test_day:02d}/{test_month:02d}/{test_year:d} ({test_cycle:d})"},
            {   'format': "%k %#d/%#m/%Y (%c)", 'condition' : lambda : True,
                'answer': f"CC {test_day:d}/{test_month:d}/{test_year:d} ({test_cycle:d})"},
            {   'format': "%d %b %Y",  'condition' : lambda : True,
                'answer': f"{test_day:02d} {test_month_name} {test_year:d}"},
            {   'format': "%A %d %m, %Y",  'condition' : lambda : True,
                'answer': f"{test_weekday} {test_day:02d} {test_month:02d}{test_suffix}, {test_year:d}"},
            {   'format': "%A %d %B, %y", 'condition' : lambda : test_year >= 0,
                'answer': f"{test_weekday} {test_day:02d} {test_month_name}, {test_year:d}"},
            {   'format': "%a %d %B, %y", 'condition' : lambda : test_year < 0,
                'answer': f"{Present_Calendars.DAY_OF_THE_WEEK_ATTS['en'][test_weekday_ndx]['abbrv']} {test_day:02d} {test_month_name}, {abs(test_year):d} BCE"},
            ]
            test_case = {'format' : 'None'}
            try:
                for test_case in test_cases:
                    if not test_case['condition']():
                        continue
                    moment = UnivMoment(test_rd, precision=Precision.DAY)
                    presentation = moment.present(Calendar.CHINESE, test_case['format'], language='en')
                    greg = moment.present(Calendar.GREGORIAN, "%Y-%m-%d", language='en')
                    if presentation == test_case['answer']:
                        print(f"    ✅ R.D. {test_rd}")
                        print(f"         Format string: {test_case['format']}")
                        print(f"         Presentation : {presentation}")
                        print(f"         Gregorian    : {greg}")
                    else:
                        print(f"    ❌ R.D.Error {test_rd}")
                        print(f"         Format string: {test_case['format']}")
                        print(f"         Returned     : {presentation}")
                        print(f"         Expected     : {test_case['answer']}")
                        print(f"         Gregorian    : {greg}")
                        failures += 1
                        failure_list.append(test_date)
                        break
                    continue
            except Exception as e:
                print(f"    ❌{msg}")
                print(f"       format={test_case['format']}")
                print(f"    ❌ValueError : {e}")
                failures += 1
            continue
        if failures > 0:
            assert False, f"❌ {failures} cases failed in Appendix C."
        else:
            print("✅ All presentation tests in Appendix C passed successfully!")
        return
