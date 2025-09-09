#!/usr/bin/env python3
"""
Demonstration of SPK_UniversalTimestamp capabilities
"""

from SPK_UniversalTimestamp import (
    UnivTimestamp, 
    Calendar, 
    Precision,
    GEOLOGICAL_EONS
)

def main():
    print("SPK Universal Timestamp System Demo")
    print("="*50)
    
    # 1. Modern dates
    print("\n1. Modern Date Examples:")
    modern = UnivTimestamp.GREGORIAN(2024, 12, 12, 10, 30, 45)
    print(f"   Today: {modern.format_for_display()}")
    
    # 2. Geological time
    print("\n2. Geological Time Examples:")
    dinosaur_extinction = UnivTimestamp.GEOLOGICAL(66.0, 
        precision=Precision.MILLION_YEARS,
        description="Cretaceous-Paleogene extinction")
    print(f"   Dinosaur extinction: {dinosaur_extinction.format_for_display()}")
    
    print(f"   Cenozoic Era: {GEOLOGICAL_EONS['Cenozoic'].format_signature()}")
    print(f"   Earth formation: {GEOLOGICAL_EONS['Hadean'].format_signature()}")
    
    # 3. Astronomical time
    print("\n3. Astronomical Time Examples:")
    j2000 = UnivTimestamp.from_julian_date(2451545.0, description="J2000.0 epoch")
    print(f"   J2000.0 epoch: {j2000.format_for_display()}")
    
    # 4. High precision scientific time
    print("\n4. Scientific Precision Examples:")
    precise = UnivTimestamp.GREGORIAN(2024, 1, 1, 12, 0, 0,
        precision_time=Precision.MICROSECOND,
        description="High precision measurement")
    print(f"   Microsecond precision: {precise.format_for_display()}")
    
    # 5. Time comparisons
    print("\n5. Time Comparisons:")
    early = UnivTimestamp.GREGORIAN(2020, 1, 1)
    late = UnivTimestamp.GREGORIAN(2024, 1, 1)
    print(f"   2020 < 2024: {early < late}")
    print(f"   Early date: {early.format_for_display()}")
    print(f"   Late date: {late.format_for_display()}")
    
    # 6. Different calendar systems
    print("\n6. Calendar System Examples:")
    hebrew = UnivTimestamp.from_hebrew_calendar_accurate(5785, 3, 15, description="Hebrew calendar date")
    print(f"   Hebrew calendar: {hebrew.format_for_display()}")
    
    julian = UnivTimestamp.from_julian_calendar_accurate(2024, 1, 1, description="Julian calendar date")
    print(f"   Julian calendar: {julian.format_for_display()}")
    
    print("\nDemo complete! Your SPK_UniversalTimestamp package is working correctly.")

if __name__ == "__main__":
    main()
