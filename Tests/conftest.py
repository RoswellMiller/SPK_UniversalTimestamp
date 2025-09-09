import pytest
from Tests.PlotManager import PlotManager


def pytest_collection_modifyitems(items):
    """Control the order in which test files are executed"""
    # Define the correct order of your test files
    file_order = {
        "test_001_UnivTimestamp.py": 1,
        "test_002_DecimalLibrary.py": 2,
        "test_100_Geological.py": 3,    
        "test_200_UnivCalendars.py": 4,
        "test_201_Gregorian.py": 5,
        "test_202_Julian.py": 6,
        "test_203_Hebrew.py": 7,
        "test_300_Astronomical.py": 8,
        "test_301_Chinese.py": 9,
        "test_302_Persian.py": 10,
        "test_500_UnivFactory.py": 11,
        "test_501_Sorting.py": 12,
        "test_502_readme_examples.py": 13,
        # Add other test files as needed
    }
    
    # Sort test items based on the file they come from
    items.sort(key=lambda item: file_order.get(
        item.module.__file__.split('\\')[-1],  # Extract filename from path
        999  # Default high value for unknown files
    ))
    
    # Optionally print the collection order for debugging
    for item in items:
        module_name = item.module.__file__.split('\\')[-1]
        print(f"Collected: {module_name} :: {item.name}")
        
# In conftest.py
@pytest.fixture(scope="session")
def plot_manager():
    """Fixture that provides a PlotManager for the entire test session"""
    manager = PlotManager()
    yield manager
    manager.close()