"""
pytest configuration for the SPK_UniversalTimestamp test suite.

Test-file ordering: the `test_NNN_...py` numeric-prefix naming already
gives pytest alphabetical sort in the intended order, so no custom
`pytest_collection_modifyitems` hook is needed.  A previous hook here
maintained a stale `file_order` map that referenced filenames retired
long ago (`test_001_UnivTimestamp.py`, `test_100_Geological.py`, etc.);
it also used a Windows-only path separator.  Removed 2026-07-18 during
PL-01 Phase 3 \u2014 no test relies on ordering.
"""
import pytest

from Tests.PlotManager import PlotManager


@pytest.fixture(scope="session")
def plot_manager():
    """PlotManager shared across the whole test session; closed at teardown."""
    manager = PlotManager()
    yield manager
    manager.close()
