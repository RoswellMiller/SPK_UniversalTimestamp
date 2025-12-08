"""
Comprehensive tests for the Moment_Unix_Timestamp.
"""
import os
import json

from SPK_UniversalTimestamp.Moment_aUniversal import UnivMoment
from SPK_UniversalTimestamp.Moment_bPresent_Calendars import Present_Calendars

class Test_Moment_Unix_Timestamp: 
    """Test cases for Moment_Unix_Timestamp."""
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
            calendar = 'Unix'
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
            unix_timestamp = self.appendix_c_table[f'{calendar}'][appendix_c_ndx]
            msg = f"Row {appendix_c_ndx+1} {calendar} timestamp: {unix_timestamp}"
            try:
                moment = UnivMoment.from_unix_timestamp(unix_timestamp)
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
            assert False, f"❌ {failures} test(s) failed in Appendix C."
        else:
            print("✅ All CONSTRUCTION tests in Appendix C passed successfully!")
        return
    
