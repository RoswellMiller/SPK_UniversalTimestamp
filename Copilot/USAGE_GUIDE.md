"""
SPK_UniversalTimestamp Package Usage Guide
==========================================

## The utility functions ARE working! Here's what you need to know:

### What functions are actually available:
✓ sort_timestamps_ascending()
✓ sort_timestamps_descending()  
✓ sort_mixed_timestamps_and_strings()
✓ create_julian_date_from_jd()
✓ create_julian_calendar_date()
✓ convert_gregorian_to_julian_calendar()
✓ convert_julian_to_gregorian_calendar()
✓ get_default_min_time_compact()
✓ get_default_max_time_compact()
✓ get_default_min_time_minimal()
✓ get_default_max_time_minimal()
✓ convert_timestamps_for_json()
✓ parse_timestamp_string()
✓ GEOLOGICAL_PERIODS (dict)
✓ MEASUREMENT_HISTORY (dict)

### How to use in your other project:

1. **Make sure the package is installed:**
   ```bash
   cd /path/to/SPK_UniversalTimestamp
   pip install -e .
   ```

2. **Import in your other project:**
   ```python
   from SPK_UniversalTimestamp import (
       UniversalTimestamp,
       sort_timestamps_ascending,
       create_julian_calendar_date,
       get_default_min_time_compact,
       convert_timestamps_for_json,
       parse_timestamp_string,
       GEOLOGICAL_PERIODS
   )
   ```

3. **Create timestamps correctly:**
   ```python
   # Use from_gregorian() method (NOT create_from_gregorian_date)
   ts = UniversalTimestamp.from_gregorian(2023, 12, 25, 12, 0, 0)
   ```

4. **Use utility functions:**
   ```python
   # Sort timestamps
   timestamps = [ts1, ts2, ts3]
   sorted_timestamps = sort_timestamps_ascending(timestamps)
   
   # Create Julian calendar date
   julian_ts = create_julian_calendar_date(1732, 2, 11)
   
   # Access constants
   print(GEOLOGICAL_PERIODS['Hadean'])
   
   # Get default time ranges
   min_time = get_default_min_time_compact()  # "13.8 BYA ±BY [±1%] (Big Bang)"
   max_time = get_default_max_time_compact()  # "9999-01-01 ±Y [exact] (Far future)"
   
   # Parse timestamp strings
   parsed = parse_timestamp_string("1731-02-11 OS")  # Julian calendar date
   
   # Convert data for JSON storage
   data = {"timestamp": ts, "info": "some data"}
   json_ready = convert_timestamps_for_json(data, preserve_metadata=True)
   ```

### Common issues and solutions:

❌ **Problem**: "utility functions not showing"
✅ **Solution**: They ARE there! Check your import statement and make sure you're using the correct function names listed above.

❌ **Problem**: "AttributeError: 'UniversalTimestamp' has no attribute 'create_from_gregorian_date'"
✅ **Solution**: Use `UniversalTimestamp.from_gregorian()` instead.

❌ **Problem**: Functions like `create_hebrew_calendar_date` not found
✅ **Solution**: These don't exist in the current implementation. Only Julian calendar functions are available.

### Test your imports:
```python
# Quick test in your other project
import SPK_UniversalTimestamp
print("Available functions:", [x for x in SPK_UniversalTimestamp.__all__ if callable(getattr(SPK_UniversalTimestamp, x, None))])
```

### All available utility functions tested and working:
- **Timestamp sorting**: ascending/descending, mixed types
- **Julian calendar functions**: creation and conversion
- **Default time ranges**: compact/minimal format for Big Bang to far future
- **Timestamp parsing**: parse strings into UniversalTimestamp objects
- **JSON conversion**: convert data structures with timestamps for storage
- **Julian Day Number**: creation from astronomical references
- **Constants**: geological periods and measurement history dictionaries

### NEW utility functions added:
- `get_default_min_time_compact()` - Returns formatted Big Bang timestamp
- `get_default_max_time_compact()` - Returns formatted far future timestamp  
- `get_default_min_time_minimal()` - Returns minimal Big Bang timestamp
- `get_default_max_time_minimal()` - Returns minimal far future timestamp
- `convert_timestamps_for_json()` - Converts data structures for JSON storage
- `parse_timestamp_string()` - Parses various timestamp string formats
"""
