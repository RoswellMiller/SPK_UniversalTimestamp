"""
Comprehensive tests for the Moment_Calendars class.
"""
from datetime import datetime
from decimal import Decimal
from SPK_UniversalTimestamp.Constants_aCommon import Calendar, Precision
from SPK_UniversalTimestamp.Moment_aUniversal import UnivMoment

class Test_Moment_Calendars: 
    """Test cases for Moment_Calendars class."""
    def test_time_Presentation(self):
        test_rd_day = Decimal(728_714) # R.D. for 1996-2-25
        test_year = 1996
        test_month = 2
        test_day = 25
        now = datetime.now()
        test_hour = now.hour
        test_minute = now.minute
        test_second = Decimal(now.second) + (Decimal(now.microsecond) / Decimal(1_000_000))
        test_rd_time = (test_hour, test_minute, test_second)
        msg = f"Moment Presentation Test for R.D. {test_rd_day} at {test_hour}:{test_minute}:{test_second:09.6f}"
        test_cases = [
        {   'format': "%d/%m/%Y", 'tz' : 'UTC',
            'answer': f"{test_day:02d}/{test_month:02d}/{test_year:d}"},
        {   'format': "%H:%M:%S", 'tz' : 'UTC',
            'answer': f"{test_hour:02}:{test_minute:02}:{test_second:09.6f}"},
        {   'format': "%I:%M:%S %p", 'tz' : 'UTC',
            'answer': f"{test_hour % 12:02}:{test_minute:02}:{test_second:09.6f} {'am' if test_hour < 12 else 'pm'}"},
        {   'format': "%H:%M:%S %z %Z", 'tz' : 'UTC',
            'answer': f"{test_hour:02}:{test_minute:02}:{test_second:09.6f} +00:00 UTC"},
        {   'format': "%H:%M %z %Z", 'tz' : 'America/New_York',
            'answer': f"{(test_hour-5) % 24:02}:{test_minute:02} -05:00 America/New_York"},
        {   'format': "%H:%M %z %Z", 'tz' : 'America/Los_Angeles',
            'answer': f"{(test_hour-8) % 24:02}:{test_minute:02} -08:00 America/Los_Angeles"},
        {   'format': "%H:%M %z %Z", 'tz' : 'Europe/Paris',
            'answer': f"{(test_hour+1) % 24:02}:{test_minute:02} +01:00 Europe/Paris"},
        {   'format': "%H:%M %z %Z", 'tz' : 'Asia/Tokyo',
            'answer': f"{(test_hour+9) % 24:02}:{test_minute:02} +09:00 Asia/Tokyo"},
        {   'format': "%H:%M %z %Z", 'tz' : 'Africa/Johannesburg',
            'answer': f"{(test_hour+2) % 24:02}:{test_minute:02} +02:00 Africa/Johannesburg"},
        {   'format': "%H:%M %z %Z", 'tz' : 'Australia/Sydney',
            'answer': f"{(test_hour+11) % 24:02}:{test_minute:02} +11:00 Australia/Sydney"},
        ]
        failures = 0
        try:
            for test_case in test_cases:
                tz = test_case['tz']
                moment = UnivMoment(test_rd_day, test_rd_time, precision=Precision.MICROSECOND)
                presentation = moment.present(Calendar.GREGORIAN, test_case['format'], tz, language='en')
                if presentation == test_case['answer']:
                    print(f"    ✅ {msg}")
                else:
                    print(f"    ❌ R.D.Error {test_rd_day}")
                    print(f"         Format string: {test_case['format']}")
                    print(f"         Returned     : {presentation}")
                    print(f"         Expected     : {test_case['answer']}")
                    failures += 1
                continue
        except Exception as e:
            print(f"    ❌ValueError : {e}")
            failures += 1
            
        if failures > 0:
            assert False, f"❌ {failures} time presentation test(s) FAILED."
        else:
            print("✅ All time presentation tests passed successfully!")
        return
