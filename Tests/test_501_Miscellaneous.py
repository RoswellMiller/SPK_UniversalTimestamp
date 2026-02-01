"""
Comprehensive tests for the UnivMoment class.
"""
import inspect
from SPK_UniversalTimestamp.Constants_aCommon import Precision
from SPK_UniversalTimestamp.Moment_aUniversal  import UnivMoment

# Add the parent directory to Python path so we can import the package
#sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

#from SPK_UniversalTimestamp.UnivCommonConstants import Precision

class TestUniversalTimestamp:
    
    def Test_repr_UnivMoment(self):
        moment = UnivMoment.from_gregorian(1947, 1, 20, 2, 36, 45, precision=Precision.SECOND)
        repr_str = repr(moment)
        recreated = UnivMoment.eval_repr(repr_str) 
        assert moment == recreated
        
        bot = UnivMoment.beginning_of_time()
        repr_str = repr(bot)
        recreated = UnivMoment.eval_repr(repr_str) 
        assert bot == recreated
        return
        
    """Test cases for UnivMoment class."""
    def test_sorting_and_comparison(self):
        """Test timestamp sorting and comparison."""
        # Create timestamps in different time scales
        bot = UnivMoment.beginning_of_time()                                            #"Beginning of Time"
        big_bang = UnivMoment.from_geological(13.8, precision=Precision.BILLION_YEARS)  #"Big Bang"
        dinosaurs = UnivMoment.from_geological(66.0, precision=Precision.MILLION_YEARS) #"Dinosaurs"
        bce = UnivMoment.from_julian(-44, 3, 15)                                        #"Julius Caesar assassination
        modern = UnivMoment.from_gregorian(2024, 1, 1)                                  #"Modern"
        modern_2 = UnivMoment.from_gregorian(2024, 1, 1, 12)                            #"Modern with time"
        future = UnivMoment.from_gregorian(2030, 1, 1)                                  #"Future event"
        
        # Test sorting
        timestamps = [modern_2, future, big_bang, modern, dinosaurs, bce, bot]
        timestamps.sort()
        
        # Should be: big_bang, dinosaurs, modern, future
        assert timestamps[0] == bot
        assert timestamps[1] == big_bang
        assert timestamps[2] == dinosaurs
        assert timestamps[3] == bce
        assert timestamps[4] == modern
        assert timestamps[5] == modern_2
        assert timestamps[6] == future

        # Test descending sort
        timestamps.sort(reverse=True)
        assert timestamps[0] == future
        assert timestamps[-1] == bot
        
        # Test individual comparisons
        assert big_bang < dinosaurs
        assert dinosaurs < modern
        assert modern < future
        assert future > modern
        print(f"✅ SUCCESS: {inspect.currentframe().f_code.co_name}")
        return
    
    def test_hashing(self):
        """Test hashing of UnivMoment instances."""
        moment1 = UnivMoment.from_gregorian(2000, 1, 1, 12, 0, 0)
        moment2 = UnivMoment.from_gregorian(2000, 1, 1, 12, 0, 0)
        moment3 = UnivMoment.from_gregorian(2020, 1, 1, 12, 0, 0)
        
        # Hashes of equal moments should be the same
        assert hash(moment1) == hash(moment2)
        
        # Hashes of different moments should be different
        assert hash(moment1) != hash(moment3)
        
        # Test usage in a set
        moment_set = {moment1, moment3}
        assert moment2 in moment_set
        assert len(moment_set) == 2
        
        print(f"✅ SUCCESS: {inspect.currentframe().f_code.co_name}")
        return
    
