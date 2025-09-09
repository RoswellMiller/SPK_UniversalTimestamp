#!/usr/bin/env python3
"""
Test the newly added utility functions
"""

print("Testing newly added utility functions...")

try:
    from SPK_UniversalTimestamp import (
        get_default_min_time_compact,
        get_default_max_time_compact,
        get_default_min_time_minimal,
        get_default_max_time_minimal,
        convert_timestamps_for_json,
        UnivTimestamp
    )
    print("✅ All imports successful!")
    
    # Test the functions
    print("\n1. Testing default time functions:")
    print(f"   Min time (compact):  {get_default_min_time_compact()}")
    print(f"   Max time (compact):  {get_default_max_time_compact()}")
    print(f"   Min time (minimal):  {get_default_min_time_minimal()}")
    print(f"   Max time (minimal):  {get_default_max_time_minimal()}")
    
    print("\n2. Testing parse_timestamp_string (now static method):")
    test_strings = ["2023-12-25", "4.5 BYA", "1731-02-11 OS", "JD 2451545.0"]
    for test_str in test_strings:
        parsed = UnivTimestamp.parse_timestamp_string(test_str)
        if parsed:
            print(f"   ✅ '{test_str}' → {parsed.format_minimal()}")
        else:
            print(f"   ❌ '{test_str}' → Failed to parse")
    
    print("\n3. Testing convert_timestamps_for_json:")
    ts = UnivTimestamp.GREGORIAN(2023, 12, 25, 12, 0, 0)
    test_data = {
        "timestamp": ts,
        "list_of_timestamps": [ts, UnivTimestamp.GREGORIAN(2024, 1, 1)],
        "regular_data": "This is just a string"
    }
    
    json_data = convert_timestamps_for_json(test_data, preserve_metadata=True)
    print(f"   With metadata: {json_data}")
    
    json_minimal = convert_timestamps_for_json(test_data, preserve_metadata=False)
    print(f"   Minimal: {json_minimal}")
    
    print("\n✅ All utility functions are working!")
    
except ImportError as e:
    print(f"❌ Import failed: {e}")
except Exception as e:
    print(f"❌ Error: {e}")

# Test showing all available functions
print("\n4. Complete list of available utility functions:")
import SPK_UniversalTimestamp
for name in sorted(SPK_UniversalTimestamp.__all__):
    if callable(getattr(SPK_UniversalTimestamp, name, None)):
        obj = getattr(SPK_UniversalTimestamp, name)
        print(f"   • {name}: {type(obj)}")
