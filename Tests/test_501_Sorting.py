"""
Comprehensive tests for the UnivMoment class.
"""
import os
import sys
import inspect


# Add the parent directory to Python path so we can import the package
#sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

#from SPK_UniversalTimestamp.UnivCommonConstants import Precision

class TestUniversalTimestamp:
    pass
    """Test cases for UnivMoment class."""
    # def test_sorting_and_comparison(self):
    #     """Test timestamp sorting and comparison."""
    #     # Create timestamps in different time scales
    #     bot = UnivTimestampFactory.beginning_of_time()
    #     big_bang = UnivGEOLOGICAL(13.8, precision=Precision.BILLION_YEARS, description="Big Bang")
    #     dinosaurs = UnivGEOLOGICAL(66.0, precision=Precision.MILLION_YEARS, description="Dinosaurs")
    #     bce = UnivGREGORIAN(-44, 3, 15, description="Julius Caesar assassination")
    #     modern = UnivGREGORIAN(2024, 1, 1, description="Modern")
    #     modern_2 = UnivGREGORIAN(2024, 1, 1, 12, description="Modern with time")
    #     future = UnivGREGORIAN(2026, 1, 1, description="Future event")
        
    #     # Test sorting
    #     timestamps = [modern_2, future, big_bang, modern, dinosaurs, bce, bot]
    #     timestamps.sort(key=lambda ts: ts.sort)
        
    #     # Should be: big_bang, dinosaurs, modern, future
    #     assert timestamps[0] == bot
    #     assert timestamps[1] == big_bang
    #     assert timestamps[2] == dinosaurs
    #     assert timestamps[3] == bce
    #     assert timestamps[4] == modern
    #     assert timestamps[5] == modern_2
    #     assert timestamps[6] == future

    #     # Test descending sort
    #     timestamps.sort(key=lambda ts: ts.sort, reverse=True)
    #     assert timestamps[0] == future
    #     assert timestamps[-1] == bot
        
    #     # Test individual comparisons
    #     assert big_bang < dinosaurs
    #     assert dinosaurs < modern
    #     assert modern < future
    #     assert future > modern
    #     print(f"✅ SUCCESS: {inspect.currentframe().f_code.co_name}")
    #     return
    
