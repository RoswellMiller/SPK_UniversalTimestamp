from .CC01_Calendar_Basics import Epoch_rd

# "Calendrical Calculations" by Reingold and Dershowitz
# p 59 (2.16)
def is_gregorian_leap_year(g_year: int) -> bool:
    """
    Check if a year is a leap year in the Gregorian calendar
    """
    return (g_year % 4 == 0 and g_year % 100 != 0) or (g_year % 400 == 0)

# p 60 (2.17)
def rd_from_gregorian(year: int, month: int = 1, day: int = 1) -> int:
    """
    Convert Gregorian date to Rata Die (rd) fixed day number
    """
    day = day if day is not None else 1
    month = month if month is not None else 1
    #year = year if year is not None else 1
    # Validate input
    if not isinstance(year, int) or not isinstance(month, int) or not isinstance(day, int):
        raise ValueError("Year, month, and day must be integers")
    if month < 1 or month > 12:
        raise ValueError("Month must be between 1 and 12")
    if day < 1 or day > 31:
        raise ValueError("Day must be between 1 and 31")

    # Calculate rd from Gregorian date
    d0 = Epoch_rd['gregorian'] - 1
    d0 += (year - 1) * 365 
    d0 += (year - 1) // 4 
    d0 -= (year - 1) // 100 
    d0 += (year - 1) // 400
    d0 += (367 * month - 362) // 12 
    if month <=2 :
        pass
    elif is_gregorian_leap_year(year):
        d0 -= 1
    else:
        d0 -= 2
    rd = d0 + day
    return rd

# p 60 (2.18)
def gregorian_new_year(g_year:int) -> int:
    return rd_from_gregorian(g_year, 1, 1)
# p 60 (2.19)
def gregorian_end_year(g_year: int) -> int:
    return rd_from_gregorian(g_year, 12, 31)
    
# p 61 (2.21)
def gregorian_year_from_rd(rd : int) -> int:
    """
    Get the year from a Rata Die (rd) fixed day number
    """
    # Calculate year from rd
    try:
        d0 = rd - Epoch_rd['gregorian']
        n400 = d0 // 146097
        d1 = d0 % 146097
        n100 = d1 // 36524  
        d2 = d1 % 36524
        n4 = d2 // 1461
        d3 = d2 % 1461
        n1 = d3 // 365
        year = 400 * n400 + 100 * n100 + 4 * n4 + n1
        if n100 != 4 and n1 != 4:
            year += 1
        return year
    except Exception as e:
        raise ValueError(f"Invalid Rata Die date: {rd}: {e}")

# p 62 (2.23)    
def gregorian_from_rd(rd: int) -> dict:
    """
        Convert Rata Die (rd) fixed day number to Gregorian date
    """
    # Convert rd to datetime
    try:
        year = gregorian_year_from_rd(rd)
        prior_days = rd -  rd_from_gregorian(year, 1, 1)
        if rd < rd_from_gregorian(year, 3, 1):
            correction = 0
        elif is_gregorian_leap_year(year):
            correction = 1
        else:
            correction = 2
        month = (12 * (prior_days + correction) + 373) // 367   
        day = rd - rd_from_gregorian(year, month, 1) + 1
        return year, month, day
    except ValueError as e:
        raise ValueError(f"Invalid Rata Die date: {rd}: {e}")
    
# p 62 (2.24)
def gregorian_date_difference(g_date_1 : tuple, g_date_2 : tuple) -> int:
    """
    Calculate the difference in days between two Gregorian dates
    """
    rd1 = rd_from_gregorian(g_date_1[0], g_date_1[1], g_date_1[2])
    rd2 = rd_from_gregorian(g_date_2[0], g_date_2[1], g_date_2[2])
    return rd2 - rd1
