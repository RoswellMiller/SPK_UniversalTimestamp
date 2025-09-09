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
    UnivTimestamp, 
    Precision,
    GEOLOGICAL_EONS,
    MEASUREMENT_HISTORY,
    sort_timestamps_ascending
)


def main():
    """Demonstrate UniversalTimestamp functionality across time scales."""
    print("SPK Universal Timestamp - Comprehensive Example")
    print("=" * 50)
    
    # 1. Geological Time Scales
    print("\n1. Geological Time Scales:")
    print("-" * 25)
    
    big_bang = UnivTimestamp.GEOLOGICAL(
        13.8e9, 
        precision=Precision.BILLION_YEARS,
        accuracy="±1%",
        description="Big Bang"
    )
    print(f"   Big Bang: {big_bang.format_for_display()}")
    
    earth_formation = UnivTimestamp.GEOLOGICAL(
        4.54e9,
        precision=Precision.MILLION_YEARS,
        accuracy="±0.05%",
        description="Earth formation"
    )
    print(f"   Earth formation: {earth_formation.format_for_display()}")
    
    dinosaur_extinction = UnivTimestamp.GEOLOGICAL(
        66e6,
        precision=Precision.MILLION_YEARS, 
        accuracy="±0.1%",
        description="K-Pg extinction event"
    )
    print(f"   Dinosaur extinction: {dinosaur_extinction.format_for_display()}")
    
    # 2. Scientific Measurements
    print("\n2. High-Precision Scientific Measurements:")
    print("-" * 40)
    
    # Nanosecond precision measurement
    measurement_time = datetime.datetime(2024, 7, 15, 14, 30, 25, 123456)
    scientific_measurement = UnivTimestamp.SCIENTIFIC(
        measurement_time,
        precision_ns=1,
        accuracy_description="atomic clock synchronization",
        measurement_description="quantum coherence experiment"
    )
    print(f"   Quantum experiment: {scientific_measurement.format_for_display()}")
    
    # Unix timestamp with nanosecond precision  
    unix_precise = UnivTimestamp.UNIX_EPOCH(
        1640995200.123456789,
        precision_time=Precision.NANOSECOND,
        description="High-precision system measurement"
    )
    print(f"   Unix precise: {unix_precise.format_for_display()}")
    
    # 3. Cultural Calendars
    print("\n3. Cultural Calendar Systems:")
    print("-" * 30)
    
    # Hebrew calendar (if convertdate available)
    try:
        hebrew_date = UnivTimestamp.from_hebrew_calendar_accurate(
            5784, 7, 15,  # Tu BiShvat 5784
            description="Tu BiShvat (New Year of the Trees)"
        )
        print(f"   Hebrew calendar: {hebrew_date.format_for_display()}")
    except ImportError:
        print("   Hebrew calendar: (convertdate library not available)")
    
    # Julian calendar historical date
    try:
        julian_date = UnivTimestamp.from_julian_calendar_accurate(
            1582, 10, 4,  # Last day of Julian calendar
            description="Last day before Gregorian calendar reform"
        )
        print(f"   Julian calendar: {julian_date.format_for_display()}")
    except ImportError:
        print("   Julian calendar: (convertdate library not available)")
    
    # BCE dates
    bce_date = UnivTimestamp.GREGORIAN(
        -44, 3, 15,  # 44 BCE - Ides of March
        description="Assassination of Julius Caesar"
    )
    print(f"   Ancient history: {bce_date.format_for_display()}")
    
    # 4. Astronomical Time
    print("\n4. Astronomical Time Systems:")
    print("-" * 28)
    
    # Julian Day Number
    j2000_epoch = UnivTimestamp.from_julian_date(
        2451545.0,  # J2000.0 epoch
        description="Standard astronomical epoch J2000.0"
    )
    print(f"   J2000.0 epoch: {j2000_epoch.format_for_display()}")
    
    # Using Astropy if available
    try:
        astropy_jd = UnivTimestamp.from_julian_date_astropy(
            2451545.0,
            description="J2000.0 with Astropy precision"
        )
        print(f"   Astropy JD: {astropy_jd.format_for_display()}")
    except ImportError:
        print("   Astropy JD: (astropy library not available)")
    
    # 5. Predefined Constants
    print("\n5. Predefined Geological Periods:")
    print("-" * 32)
    
    for period_name, period_ts in list(GEOLOGICAL_EONS.items())[:3]:
        print(f"   {period_name}: {period_ts.format_compact()}")
    
    print("\n6. Scientific Measurement History:")
    print("-" * 34)
    
    for measurement_name, measurement_ts in list(MEASUREMENT_HISTORY.items())[:3]:
        print(f"   {measurement_name}: {measurement_ts.format_compact()}")
    
    # 7. Precision and Formatting Examples
    print("\n7. Precision and Formatting Examples:")
    print("-" * 37)
    
    # Different precision levels
    year_precision = UnivTimestamp.GREGORIAN(
        2024, precision_date=Precision.YEAR
    )
    print(f"   Year precision: {year_precision.format_for_display()}")
    
    microsecond_precision = UnivTimestamp.GREGORIAN(
        2024, 7, 15, 14, 30, 25.123456,
        precision_time=Precision.MICROSECOND
    )
    print(f"   Microsecond precision: {microsecond_precision.format_for_display()}")
    
    # Compact vs minimal formatting
    timestamp = UnivTimestamp.GREGORIAN(
        2024, 7, 15, 12, 0, 0,
        accuracy="GPS synchronization",
        description="Satellite measurement"
    )
    print(f"   Full display: {timestamp.format_for_display()}")
    print(f"   Compact: {timestamp.format_compact()}")
    print(f"   Minimal: {timestamp.format_minimal()}")
    
    # 8. Sorting Across Time Scales
    print("\n8. Sorting Across Time Scales:")
    print("-" * 30)
    
    # Create mixed time scale timestamps
    timestamps = [
        UnivTimestamp.GREGORIAN(2025, 1, 1, description="Future"),
        big_bang,
        UnivTimestamp.GREGORIAN(2024, 7, 15, description="Present"),
        dinosaur_extinction,
        UnivTimestamp.GREGORIAN(-44, 3, 15, description="Ancient")
    ]
    
    # Sort chronologically
    sorted_timestamps = sort_timestamps_ascending(timestamps)
    
    print("   Chronological order (oldest to newest):")
    for i, ts in enumerate(sorted_timestamps):
        print(f"   {i+1}. {ts.format_compact()}")
    
    # 9. Time Scale Conversions
    print("\n9. Time Scale Conversions:")
    print("-" * 26)
    
    # Show approximate conversions
    test_timestamp = UnivTimestamp.GREGORIAN(2024, 7, 15)
    print(f"   Gregorian converted: {test_timestamp.to_gregorian().format_for_display()}")
    print(f"   Sortable value: {test_timestamp.sort_value():.6f}")
    
    # Julian Day conversion
    try:
        julian_day = test_timestamp.to_julian_day_number()
        print(f"   Julian Day Number: {julian_day:.1f}")
    except Exception:
        print("   Julian Day Number: (conversion not available)")
    
    # 10. Confidence and Uncertainty
    print("\n10. Confidence and Uncertainty:")
    print("-" * 31)
    
    uncertain_measurement = UnivTimestamp.from_nanoseconds_with_uncertainty(
        123456789.123,  # nanoseconds since midnight
        uncertainty_ns=0.001,
        description="Ultra-precise atomic measurement"
    )
    print(f"   Uncertain measurement: {uncertain_measurement.format_for_display(include_confidence=True)}")
    
    print("\n" + "=" * 50)
    print("Comprehensive example completed successfully!")
    print("\nKey Features Demonstrated:")
    print("✓ Geological time scales (billions of years)")
    print("✓ Scientific precision (nanoseconds)")
    print("✓ Cultural calendars (Hebrew, Julian)")
    print("✓ Astronomical time systems (Julian Day)")
    print("✓ Historical dates (BCE/CE)")
    print("✓ Multiple precision levels")
    print("✓ Uncertainty tracking")
    print("✓ Cross-scale sorting")
    print("✓ Flexible formatting options")


if __name__ == "__main__":
    main()
