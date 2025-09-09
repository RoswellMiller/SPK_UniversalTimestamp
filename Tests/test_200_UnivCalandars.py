import sys
from datetime import datetime 

from SPK_UniversalTimestamp import *

class TestUniversalTimestamp:
    """Test cases for UnivTimestamp class."""

    def test_calendar_creation(self):
        """Test creating timestamps with different calendar systems."""
        print("\nUnivCalendars is ABSTRACT and cannot be instantiated directly.")
        
    # Test for static methods can be added here as needed
    def test_tzdata_installation(self):
        """Check if tzdata is properly installed"""   
        print("Python version:", sys.version)
        
        try:
            import tzdata
            print("tzdata is installed:", tzdata.__version__)
        except ImportError:
            print("tzdata is not installed")
        
        try:
            from zoneinfo import ZoneInfo, available_timezones
            # Try a very common timezone that should always exist
            tz = ZoneInfo("UTC")
            print("ZoneInfo is working with UTC timezone")
            all_timezones = sorted(available_timezones())
            print(f"Total available timezones: {len(all_timezones)}")
                
                # Sample the first few timezones to show their properties
            sample_size = min(10, len(all_timezones))
            print(f"\nShowing details for first {sample_size} timezones:")
            
            current_time = datetime.now()
            for tz_name in all_timezones[:sample_size]:
                tz = ZoneInfo(tz_name)
                # Get current time in this timezone
                time_in_tz = current_time.astimezone(tz)
                
                # Calculate UTC offset in hours
                utc_offset = time_in_tz.utcoffset().total_seconds() / 3600
                
                # Check if DST is in effect
                is_dst = time_in_tz.dst().total_seconds() > 0
                
                print(f"Timezone: {tz_name}")
                print(f"  Current time: {time_in_tz.strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"  UTC offset: {utc_offset:+.1f} hours")
                print(f"  DST in effect: {is_dst}")
                print()
        except Exception as e:
            print(f"ZoneInfo error: {e}")
        
        return