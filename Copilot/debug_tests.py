#!/usr/bin/env python3
"""
Debug runner for SPK UniversalTimestamp tests.
This script allows you to debug individual test methods.
"""

import os
import sys
import datetime

# Add the parent directory to Python path so we can import the package
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from SPK_UniversalTimestamp import (
    UnivTimestamp, 
    Calendar, 
    Precision,
    GEOLOGICAL_EONS,
)

def debug_geological_epoch_test():
    """Debug the geological epoch creation test."""
    print("Testing geological epoch creation...")
    
    # Set a breakpoint here by clicking in the gutter
    big_bang = UnivTimestamp.GEOLOGICAL(
        13.8e9,
        precision=Precision.BILLION_YEARS,
        accuracy="±1%",
        description="Big Bang"
    )
    
    print(f"Big Bang timestamp: {big_bang.format_for_display()}")
    print(f"Calendar system: {big_bang.calendar}")
    print(f"Date precision: {big_bang.date_precision}")
    print(f"Accuracy: {big_bang.accuracy_estimate}")
    print(f"Description: {big_bang.source_description}")
    print(f"Is geological time: {big_bang.is_geological_time()}")
    
    # Test million years ago
    dinosaur_extinction = UnivTimestamp.GEOLOGICAL(
        66e6,
        precision=Precision.MILLION_YEARS,
        accuracy="±0.1%",
        description="K-Pg extinction"
    )
    
    print(f"\nDinosaur extinction: {dinosaur_extinction.format_for_display()}")
    print(f"Date component: {dinosaur_extinction.format_date_component()}")
    
    return big_bang, dinosaur_extinction

def debug_gregorian_test():
    """Debug the Gregorian calendar test."""
    print("\nTesting Gregorian calendar creation...")
    
    # Modern date
    timestamp = UnivTimestamp.GREGORIAN(
        2024, 7, 15, 14, 30, 25.123456,
        precision_date=Precision.DAY,
        precision_time=Precision.MICROSECOND
    )
    
    print(f"Modern timestamp: {timestamp.format_for_display()}")
    print(f"Date value type: {type(timestamp.date_value)}")
    print(f"Year: {timestamp.date_value.year}")
    
    # BCE date
    bce_timestamp = UnivTimestamp.GREGORIAN(
        -44, 3, 15,  # 44 BCE - Ides of March
        description="Assassination of Julius Caesar"
    )
    
    print(f"BCE timestamp: {bce_timestamp.format_for_display()}")
    print(f"BCE date value: {bce_timestamp.date_value}")
    
    return timestamp, bce_timestamp

if __name__ == "__main__":
    print("SPK UniversalTimestamp Debug Runner")
    print("=" * 50)
    
    # Run debug tests
    geological_results = debug_geological_epoch_test()
    gregorian_results = debug_gregorian_test()
    
    print("\n" + "=" * 50)
    print("Debug session completed!")
    print("Set breakpoints and run with F5 to step through the code.")
