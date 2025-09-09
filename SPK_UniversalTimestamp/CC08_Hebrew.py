from enum import Enum
from typing import Tuple
from .CC01_Calendar_Basics import Epoch_rd

class months(Enum):
    """Hebrew months enumeration"""
    NISAN = 1
    IYYAR = 2
    SIVAN = 3
    TAMMUZ = 4
    AV = 5
    ELUL = 6
    TISHRI = 7
    MARHESHVAN = 8
    KISLEV = 9
    TEVET = 10
    SHEVAT = 11
    ADAR_I = 12
    ADAR_II = 13
    

# Calendrical Calculations pp Chapter 8
# (8.14)
def is_hebrew_leap_year(h_year: int) -> bool:
    return ((7 * h_year + 1) % 19) < 7

# (8.15) 
def last_hebrew_month_of_year(h_year) -> int:
    """Get the last month of a Hebrew year"""
    if is_hebrew_leap_year(h_year):
        return months.ADAR_II.value
    return months.ADAR_I.value

# (8.16)
def _is_sabbatical_year(h_year: int) -> bool:
    """Is Sabbatical year for a given Hebrew year"""
    return h_year % 7 == 0
    
# (8.19)
# def _molad(h_year : int, h_month: int, hour : int = 0) -> int:
#     """Calculate the molad (new moon) for a given Hebrew year and month"""
#     y = h_year + 1  if h_month < UnivHEBREW.months.TISHRI.value else h_year 
#     months_elapsed = h_month - UnivHEBREW.months.TISHRI.value + (235 * y - 214) // 19
#     m = super().Epoch_rd['Hebrew']
#     m -= 876 // 25920
#     m += months_elapsed * (29 + 12**hour + 793 // 25920)
#     return m

# (8.20)
def _calendar_elapsed_days(h_year : int) -> int :
    months_elapsed = (235 * h_year - 234) // 19
    parts_elapsed = 12084 + 13753 * months_elapsed 
    days = 29 * months_elapsed + parts_elapsed // 25920
    d = days + 1 if ((3 * (days + 1)) % 7) < 3 else days
    return d

# (8.21)
def _year_length_correction(h_year : int) -> int:
    ny1 = _calendar_elapsed_days(h_year)
    ny2 = _calendar_elapsed_days(h_year+1)
    if ny2-ny1 == 356 :
        return 2
    else:
        ny0 = _calendar_elapsed_days(h_year-1)
        if ny1-ny0 == 382 :
            return 1
    return 0

# (8.22)
def _new_year(h_year : int):
    v = Epoch_rd['hebrew'] 
    v += _calendar_elapsed_days(h_year) 
    v += _year_length_correction(h_year) 
    return v

# (8.23)
def last_day_of_hebrew_month(h_year : int, h_month : int) -> int:
    if h_month in [months.IYYAR.value, months.TAMMUZ.value, months.ELUL.value,months.TEVET.value, months.ADAR_II.value]:
        day = 29
    elif h_month == months.ADAR_I.value and not is_hebrew_leap_year(h_year):
        day = 29
    elif h_month == months.MARHESHVAN.value and not _is_long_marheshvan(h_year):
        day = 29
    elif h_month == months.KISLEV.value and _is_short_kislev(h_year):
        day = 29
    else:
        day = 30
    return day

# (8.24)
def _is_long_marheshvan(h_year : int) -> bool:
    b = _days_in_year(h_year) in [355, 385 ]
    return b

# (8.25)
def _is_short_kislev(h_year : int) -> bool:
    b = _days_in_year(h_year) in [353, 383 ]
    return b

# (8,26)
def _days_in_year(h_year: int) -> int: 
    d = _new_year(h_year + 1) - _new_year(h_year)
    return d

# (8.27)
def rd_from_hebrew(year: int, month: int = 1, day: int = 1) -> int:
    day = day if day is not None else 1
    month = month if month is not None else 1
    # Fixed start date
    rd = _new_year(year) + day - 1
    if month < months.TISHRI.value:
        for m in range(months.TISHRI.value, last_hebrew_month_of_year(year) + 1):
            rd += last_day_of_hebrew_month(year, m)
        for m in range(months.NISAN.value, month):    
            rd += last_day_of_hebrew_month(year, m)
    else:
        for m in range(months.TISHRI.value, month):
            rd += last_day_of_hebrew_month(year, m)        
    return rd

# (8.28)
def hebrew_from_rd(date: int) -> Tuple[int, int, int]:
    """Convert Rata Die to Hebrew date"""
    approx = (98496 * (date - Epoch_rd['hebrew']) // 35975351) + 1
    
    for y in range(approx - 1, approx + 2):
        y_rd = _new_year(y)
        if y_rd >= date:
            year = y - 1
            break
        continue
    
    if date < rd_from_hebrew(year, months.NISAN.value, 1):  
        start = months.TISHRI.value
    else:
        start = months.NISAN.value
        
    for m in range(start, last_hebrew_month_of_year(year) + 1):
        m_rd = rd_from_hebrew(year, m, last_day_of_hebrew_month(year, m))
        if date <= m_rd:
            break
    month = m
        
    day = date - rd_from_hebrew(year, month, 1) + 1
    return year, month, day

