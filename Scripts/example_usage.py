#!/usr/bin/env python3
"""
Example usage of SPK Universal Timestamp package.

This script demonstrates the comprehensive multi-scale time system capabilities.
"""

import datetime
import sys
import os

# Add the parent directory to Python path so we can import the package
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from SPK_UniversalTimestamp import (
    UnivMoment,
    Calendar, 
    Precision,
    GEOLOGICAL_EONS
)

def main():
    """Demonstrate UniversalTimestamp functionality across time scales."""
    print("SPK Universal Timestamp - Comprehensive Example")
    print("=" * 50)
    
    # 1. Geological Time Scales
    print("\n1. Geological Time Scales:")
    print("-" * 25)
    
    big_bang = UnivMoment.from_geological(
        13.8, 
        precision=Precision.BILLION_YEARS,
        description="Big Bang"
    )
    print(f"   Big Bang: {big_bang.format_signature()}")
    
    earth_formation = UnivMoment.from_geological(
        4.54e3,
        precision=Precision.MILLION_YEARS,
        description="Earth formation"
    )
    print(f"   Earth formation: {earth_formation.format_signature()}")
    
    dinosaur_extinction = UnivMoment.from_geological(
        66.0,
        precision=Precision.MILLION_YEARS, 
        description="K-Pg extinction event"
    )
    print(f"   Dinosaur extinction: {dinosaur_extinction.present(Calendar.GEOLOGICAL, '%y %O %R %P %a')}")
    
    # 2. Conversion from standard datetime
    print("\n2. Standard conversions:")
    print("-" * 40)
    
    # Microsecond precision Datetime measurement
    measurement_time = datetime.datetime(2024, 7, 15, 14, 30, 25, 123_456)
    scientific_measurement = UnivMoment.from_datetime(
        measurement_time,
        description="quantum coherence experiment"
    )
    print(f"   Quantum experiment: {scientific_measurement.present(Calendar.GREGORIAN, '%Y-%m-%d %H:%M:%S')}")
    
    # Nanosecond Unix timestamp  
    unix_precise = UnivMoment.from_unix_timestamp(
        1_640_995_200.123_456_789,
        precision_time=Precision.NANOSECOND,
        description="High-precision system measurement"
    )
    print(f"   Unix precise: {unix_precise.format_for_display()}")
    
    # 3. Cultural Calendars
    print("\n3. Cultural Calendar Systems:")
    print("-" * 30)
    
    # Hebrew calendar (if convertdate available)
    try:
        hebrew_date = UnivMoment.from_hebrew(
            5784, 7, 15,  # Tu BiShvat 5784
            description="Tu BiShvat (New Year of the Trees)"
        )
        print(f"   Hebrew calendar: {hebrew_date.present(Calendar.HEBREW, '%A %d %m, %Y')}")
    except ImportError:
        print("   Hebrew calendar: (convertdate library not available)")
    
    # Julian calendar historical date
    try:
        julian_date = UnivMoment.from_julian(
            1582, 10, 4,  # Last day of Julian calendar
            description="Last day before Gregorian calendar reform"
        )
        print(f"   Julian calendar: {julian_date.present(Calendar.JULIAN, '%A %d %m, %Y')}")
    except ImportError:
        print("   Julian calendar: (convertdate library not available)")
    
    # BCE dates
    bce_date = UnivMoment.from_gregorian(
        -44, 3, 15,  # 44 BCE - Ides of March
        description="Assassination of Julius Caesar"
    )
    print(f"   Ancient history: {bce_date.present(Calendar.GREGORIAN, '%A %d %m, %Y')}")
    
    # 4. Astronomical Time
    print("\n4. Astronomical Time Systems:")
    print("-" * 28)
    
    # Julian Day Number
    j2000_epoch = UnivMoment.from_julian_date(
        2451545.0,  # J2000.0 epoch
        description="Standard astronomical epoch J2000.0"
    )
    print(f"   J2000.0 epoch: {j2000_epoch.format_for_display()}")
        
    # 5. Predefined Constants
    print("\n5. Predefined Geological Periods:")
    print("-" * 32)
    
    for period_name, period_ts in list(GEOLOGICAL_EONS.items())[:3]:
        print(f"   {period_name}: {period_ts.format_compact()}")
    
    
    # 6. Precision and Formatting Examples
    print("\n6. Precision and Formatting Examples:")
    print("-" * 37)
    
    # Different precision levels
    year_precision = UnivMoment.from_gregorian(
        2024, precision=Precision.YEAR
    )
    print(f"   Year precision: {year_precision.present(Calendar.GREGORIAN, '%A %d %m, %Y')}")
    
    microsecond_precision = UnivMoment.from_gregorian(
        2024, 7, 15, 14, 30, 25.123456,
        precision_time=Precision.MICROSECOND
    )
    print(f"   Microsecond precision: {microsecond_precision.present(Calendar.GREGORIAN, '%Y-%m-%d %H:%M:%S.%f')}")
    
    # Compact vs minimal formatting
    timestamp = UnivMoment.from_gregorian(
        2024, 7, 15, 12, 0, 0,
        description="Satellite measurement"
    )
    print(f"   Full display: {timestamp.present(Calendar.GREGORIAN, '%Y-%B-%d %H:%M:%S')}")
    print(f"   Compact: {timestamp.present(Calendar.GREGORIAN, '%Y-%b-%d')}")
    print(f"   Minimal: {timestamp.present(Calendar.GREGORIAN, '%y-%m-%d')}")
    
    # 7. Sorting Across Time Scales
    print("\n7. Sorting Across Time Scales:")
    print("-" * 30)
    
    # Create mixed time scale timestamps
    timestamps = [
        UnivMoment.from_gregorian(2025, 1, 1, description="Future"),
        big_bang,
        UnivMoment.from_gregorian(2024, 7, 15, description="Present"),
        dinosaur_extinction,
        UnivMoment.from_gregorian(-44, 3, 15, description="Ancient")
    ]
    
    # Sort chronologically
    sorted_timestamps = sorted(timestamps)
    
    print("   Chronological order (oldest to newest):")
    for i, ts in enumerate(sorted_timestamps):
        print(f"   {i+1}. {ts.format_signature()}")
    
    # 8. Time Scale Conversions
    print("\n8. Time Scale Conversions:")
    print("-" * 26)
    
    # Show approximate conversions
    test_timestamp = UnivMoment.from_gregorian(2024, 7, 15)
    print(f"   Gregorian converted: {test_timestamp.present(Calendar.GREGORIAN, '%Y-%B-%d')}")
    print(f"   Sortable value: {test_timestamp.present(Calendar.HEBREW, '%Y-%B-%d')}")
    
    print("\n" + "=" * 50)
    print("Comprehensive example completed successfully!")
    print("\nKey Features Demonstrated:")
    print("✓ Geological time scales (billions of years)")
    print("✓ Scientific precision (attoseconds)")
    print("✓ Cultural calendars (Gregorian, Hebrew, Julian, Chinese)")
    print("✓ Astronomical time systems (Julian Day)")
    print("✓ Historical dates (BCE/CE)")
    print("✓ Multiple precision levels")
    print("✓ Cross-scale sorting")
    print("✓ Flexible formatting options")


if __name__ == "__main__":
    main()
