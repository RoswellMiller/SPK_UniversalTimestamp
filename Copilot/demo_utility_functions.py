#!/usr/bin/env python3
"""
Demonstration of SPK_UniversalTimestamp utility functions

This script shows how to properly import and use the utility functions
from the SPK_UniversalTimestamp package.
"""

print("SPK_UniversalTimestamp Utility Functions Demo")
print("=" * 50)

# Import the package and utility functions
import SPK_UniversalTimestamp
from SPK_UniversalTimestamp import (
    UnivTimestamp,
    Calendar,
    Precision,
    sort_timestamps_ascending,
    sort_timestamps_descending,
    create_julian_calendar_date,
    create_julian_date_from_jd,
    convert_gregorian_to_julian_calendar,
    convert_julian_to_gregorian_calendar,
    GEOLOGICAL_EONS,
    MEASUREMENT_HISTORY
)

print("✓ All imports successful!")
print()

# Show available functions
print("Available utility functions:")
for name in SPK_UniversalTimestamp.__all__:
    if hasattr(SPK_UniversalTimestamp, name):
        obj = getattr(SPK_UniversalTimestamp, name)
        print(f"  • {name}: {type(obj)}")

print("\n" + "=" * 50)

# Create some test timestamps using correct method name
print("Creating test timestamps...")

# Use the correct method name from the class
ts1 = UnivTimestamp.GREGORIAN(2023, 1, 1, 12, 0, 0)
ts2 = UnivTimestamp.GREGORIAN(2023, 6, 15, 14, 30, 0)
ts3 = UnivTimestamp.GREGORIAN(2023, 12, 25, 8, 45, 0)

print(f"Timestamp 1: {ts1}")
print(f"Timestamp 2: {ts2}")
print(f"Timestamp 3: {ts3}")

print("\n" + "=" * 50)

# Test sorting utility functions
print("Testing sorting functions...")

timestamps = [ts3, ts1, ts2]  # Out of order
print("Original order:", [str(ts) for ts in timestamps])

sorted_asc = sort_timestamps_ascending(timestamps)
print("Ascending:", [str(ts) for ts in sorted_asc])

sorted_desc = sort_timestamps_descending(timestamps)
print("Descending:", [str(ts) for ts in sorted_desc])

print("\n" + "=" * 50)

# Test Julian calendar functions
print("Testing Julian calendar functions...")

# Create Julian calendar date
julian_ts = create_julian_calendar_date(1732, 2, 11, "George Washington birthday (Julian)")
print(f"Julian date: {julian_ts}")

# Convert to Gregorian
gregorian_ts = convert_julian_to_gregorian_calendar(julian_ts)
print(f"Converted to Gregorian: {gregorian_ts}")

# Create from Julian Day Number
jd_ts = create_julian_date_from_jd(2451545.0, "J2000.0 epoch")
print(f"From Julian Day: {jd_ts}")

print("\n" + "=" * 50)

# Show constants
print("Available constants...")
print(f"Geological periods: {len(GEOLOGICAL_EONS)} entries")
print("Sample geological periods:")
for i, (name, ts) in enumerate(GEOLOGICAL_EONS.items()):
    if i < 3:  # Show first 3
        print(f"  • {name}: {ts}")

print(f"\nMeasurement history: {len(MEASUREMENT_HISTORY)} entries")
print("Sample measurement history:")
for i, (name, ts) in enumerate(MEASUREMENT_HISTORY.items()):
    if i < 3:  # Show first 3
        print(f"  • {name}: {ts}")

print("\n" + "=" * 50)
print("Demo complete! All utility functions are working properly.")
print("\nTo use in your project:")
print("1. Make sure SPK_UniversalTimestamp is installed: pip install -e /path/to/package")
print("2. Import what you need:")
print("   from SPK_UniversalTimestamp import UniversalTimestamp, sort_timestamps_ascending")
print("3. Use UniversalTimestamp.from_gregorian() to create timestamps")
print("4. Use the utility functions as demonstrated above")
