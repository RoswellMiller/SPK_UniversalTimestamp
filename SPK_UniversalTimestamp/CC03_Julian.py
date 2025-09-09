from .CC01_Calendar_Basics import Epoch_rd

# Calendrical Calculations Chapter 3
def is_julian_leap_year(j_year: int) -> bool:
    """
    Check if a year is a leap year in the Julian calendar
    "Calendrical Calculations" by Reingold and Dershowitz pp 75-77
    """
    return j_year % 4 == (0 if j_year > 0 else 3)
    
def rd_from_julian(year: int, month: int = 1, day: int = 1) -> int:
    """
    Convert Julian date to Rata Die (rd) fixed day number
    "Calendrical Calculations" by Reingold and Dershowitz pp 75-77
    """
    day = day if day is not None else 1
    month = month if month is not None else 1
    #year = self.year if self.year is not None else 1
    # Validate input
    if not isinstance(year, int) or not isinstance(month, int) or not isinstance(day, int):
        raise ValueError("Year, month, and day must be integers")
    if month < 1 or month > 12:
        raise ValueError("Month must be between 1 and 12")
    if day < 1 or day > 31:
        raise ValueError("Day must be between 1 and 31")

    # Calculate rd from Julian date
    y = year + 1 if year < 0 else year  # Adjust for BCE
    d0 = Epoch_rd['julian'] - 1
    d0 += (y - 1) * 365 
    d0 += (y - 1) // 4 
    d0 += (367 * month - 362) // 12 
    if month <=2 :
        pass
    elif is_julian_leap_year(year):
        d0 += -1
    else:
        d0 += -2
    rd = d0 + day
    return rd
    
def julian_from_rd(rd: int) -> dict:
    """
    Convert Rata Die (rd) fixed day number to Julian date
    "Calendrical Calculations" by Reingold and Dershowitz pp 75-77
    """
    # Convert rd to datetime
    try:
        approx = (4 * (rd - Epoch_rd['julian']) + 1464) // 1461
        year = approx - 1 if approx <= 0 else approx
        prior_days = rd - rd_from_julian(year, 1, 1)
        if rd < rd_from_julian(year, 3, 1):
            correction = 0
        elif is_julian_leap_year(year):
            correction = 1
        else:
            correction = 2
        month = (12 * (prior_days + correction) + 373) // 367
        day = rd - rd_from_julian(year, month, 1) + 1
        # Return Julian date as dictionary
        return year, month, day
    except ValueError as e:
        raise ValueError(f"Invalid Rata Die date: {rd}: {e}")       
    

