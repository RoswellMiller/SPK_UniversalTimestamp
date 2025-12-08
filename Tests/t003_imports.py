#!/usr/bin/env python3
"""
Test script to verify what can be imported from SPK_UniversalTimestamp package
"""

print("Testing imports from SPK_UniversalTimestamp...")

try:
    import SPK_UniversalTimestamp
    print("✓ Successfully imported SPK_UniversalTimestamp")
    
    # Check what's available
    print(f"Available attributes: {dir(SPK_UniversalTimestamp)}")
    
    # Check if __all__ is properly exported
    if hasattr(SPK_UniversalTimestamp, '__all__'):
        print(f"__all__ contents: {SPK_UniversalTimestamp.__all__}")
    else:
        print("No __all__ attribute found")
        
except ImportError as e:
    print(f"✗ Failed to import SPK_UniversalTimestamp: {e}")

print("\n" + "="*60)

# Test specific imports
utilities_to_test = [
    'UnivMoment',
    'CalendarSystem', 
    'PrecisionLevel',
    'sort_timestamps_ascending',
    'sort_timestamps_descending',
    'create_julian_calendar_date',
    'create_hebrew_calendar_date',
    'create_islamic_calendar_date',
    'create_chinese_calendar_date',
    'create_persian_calendar_date',
    'create_indian_calendar_date',
    'convert_between_systems',
    'calculate_time_difference',
    'format_timestamp_for_display',
    'JULIAN_DAY_ZERO',
    'UNIX_EPOCH_JULIAN_DAY'
]

for utility in utilities_to_test:
    try:
        obj = getattr(SPK_UniversalTimestamp, utility)
        print(f"✓ {utility}: {type(obj)}")
    except AttributeError:
        print(f"✗ {utility}: Not found")

print("\n" + "="*60)

# Test specific function calls
print("Testing utility function calls...")

try:
    from SPK_UniversalTimestamp import sort_timestamps_ascending
    print("✓ Successfully imported sort_timestamps_ascending")
    print(f"Function: {sort_timestamps_ascending}")
except ImportError as e:
    print(f"✗ Failed to import sort_timestamps_ascending: {e}")

# try:
#     from SPK_UniversalTimestamp import UnivMoment, CalendarSystem
#     print("✓ Successfully imported UnivMoment and CalendarSystem")
    
#     # Create a test timestamp
#     ts = UnivMoment.create_from_gregorian_date(2023, 12, 25, 12, 0, 0)
#     print(f"Created test timestamp: {ts}")
    
# except ImportError as e:
#     print(f"✗ Failed to import core classes: {e}")
