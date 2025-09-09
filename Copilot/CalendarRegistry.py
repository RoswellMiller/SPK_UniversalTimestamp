def save_calendar_solution():
    """Save the multilingual calendar solution as both documentation and code."""
    
    # First, define the implementation code that will be saved as a usable Python module
    implementation = """# filepath: calendar_registry.py
from enum import Enum
from dataclasses import dataclass
from typing import Dict, Optional, Union, List, Tuple

@dataclass
class NamedProperty:
    \"\"\"\Representation of a calendar property in a specific language\"\"\"
    id: Union[int, str]  # The internal identifier (number, code, etc.)
    name: str            # Full name
    abbrev: str          # Abbreviated name
    alt_names: List[str] = None  # Alternative names/spellings

class CalendarRegistry:
    \"\"\"\Registry for calendar properties in multiple languages\"\"\"
    
    def __init__(self):
        self._month_data = {}  # Dict[language_code, Dict[month_id, NamedProperty]]
        self._day_data = {}    # Similar structure for days
        
    def add_language(self, language_code: str):
        \"\"\"\Initialize data structures for a new language\"\"\"
        if language_code not in self._month_data:
            self._month_data[language_code] = {}
        if language_code not in self._day_data:
            self._day_data[language_code] = {}
            
    def register_month(self, language: str, month_id: int, name: str, abbrev: str, alt_names: List[str] = None):
        \"\"\"\Register a month in a specific language\"\"\"
        if language not in self._month_data:
            self.add_language(language)
        self._month_data[language][month_id] = NamedProperty(month_id, name, abbrev, alt_names)
    
    def get_month_by_number(self, month_number: int, language: str = "en") -> Optional[NamedProperty]:
        \"\"\"\Get month information by its number in the specified language\"\"\"
        if language in self._month_data and month_number in self._month_data[language]:
            return self._month_data[language][month_number]
        return None
        
    def get_month_by_name(self, name: str, language: str = "en") -> Optional[NamedProperty]:
        \"\"\"\Get month information by its name in the specified language\"\"\"
        name = name.lower()
        for month_prop in self._month_data.get(language, {}).values():
            if month_prop.name.lower() == name:
                return month_prop
            if month_prop.alt_names and name in [alt.lower() for alt in month_prop.alt_names]:
                return month_prop
        return None
        
    def get_month_by_abbrev(self, abbrev: str, language: str = "en") -> Optional[NamedProperty]:
        \"\"\"\Get month information by its abbreviation in the specified language\"\"\"
        abbrev = abbrev.lower()
        for month_prop in self._month_data.get(language, {}).values():
            if month_prop.abbrev.lower() == abbrev:
                return month_prop
        return None

# Global registry instance
_registry = None

def get_global_registry() -> CalendarRegistry:
    \"\"\"\Get or create the global calendar registry\"\"\"
    global _registry
    if _registry is None:
        _registry = CalendarRegistry()
        # Initialize with some default values
        _initialize_default_months()
    return _registry

def _initialize_default_months():
    \"\"\"\Initialize the registry with English months\"\"\"
    registry = get_global_registry()
    
    # English months
    registry.register_month("en", 1, "January", "Jan", ["Jan."])
    registry.register_month("en", 2, "February", "Feb", ["Feb."])
    registry.register_month("en", 3, "March", "Mar", ["Mar."])
    registry.register_month("en", 4, "April", "Apr", ["Apr."])
    registry.register_month("en", 5, "May", "May")
    registry.register_month("en", 6, "June", "Jun", ["Jun."])
    registry.register_month("en", 7, "July", "Jul", ["Jul."])
    registry.register_month("en", 8, "August", "Aug", ["Aug."])
    registry.register_month("en", 9, "September", "Sep", ["Sept.", "Sep."])
    registry.register_month("en", 10, "October", "Oct", ["Oct."])
    registry.register_month("en", 11, "November", "Nov", ["Nov."])
    registry.register_month("en", 12, "December", "Dec", ["Dec."])

# Example usage
if __name__ == "__main__":
    registry = get_global_registry()
    
    # Add some Hebrew months
    registry.register_month("he", 1, "Nisan", "Nis")
    registry.register_month("he", 2, "Iyar", "Iya")
    registry.register_month("he", 3, "Sivan", "Siv")
    
    # Test lookups
    month = registry.get_month_by_number(1, "en")
    print(f"Month 1 in English: {month.name} ({month.abbrev})")
    
    month = registry.get_month_by_name("February", "en")
    print(f"February is month number: {month.id}")
    
    month = registry.get_month_by_abbrev("Nis", "he")
    print(f"Nis in Hebrew is: {month.name}, month {month.id}")
"""

    # Save the implementation file
    with open("calendar_registry.py", "w", encoding="utf-8") as f:
        f.write(implementation)
    
    print("✅ Implementation saved to 'calendar_registry.py'")
    
    # Now create a documentation file with markdown formatting
    documentation = """# Multilingual Calendar Properties Management System

## Overview

This system provides a flexible way to handle calendar properties (months, days, etc.) across different languages and representations. It separates the conceptual entities from their language-specific representations.

## Key Components

1. `NamedProperty` - Dataclass for storing property details in a specific language
2. `CalendarRegistry` - Main class for managing multilingual calendar properties
3. Global registry accessor - Singleton pattern for accessing properties throughout the application

## Usage Examples

Here's how to use the registry:

    # Get the global registry
    from calendar_registry import get_global_registry
    registry = get_global_registry()

    # Add Spanish months
    registry.register_month("es", 1, "Enero", "Ene")
    registry.register_month("es", 2, "Febrero", "Feb")

    # Look up months in different ways
    january = registry.get_month_by_number(1, "en")
    print(f"Month: {january.name}, Abbrev: {january.abbrev}")

    febrero = registry.get_month_by_name("Febrero", "es")
    print(f"Month number: {febrero.id}")
"""

    # Save the documentation file
    with open("calendar_registry_docs.md", "w", encoding="utf-8") as f:
        f.write(documentation)
    
    print("✅ Documentation saved to 'calendar_registry_docs.md'")

if __name__ == "__main__":
    save_calendar_solution()