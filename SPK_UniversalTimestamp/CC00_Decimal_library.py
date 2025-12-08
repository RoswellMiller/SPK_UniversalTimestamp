"""
This is a Decimal based library which provides a more standardized definition
of common mathematical functions.  It is also designed to meet the mathematical
requirements of "Calendrical Calculations" by Reingold and Dershowitz.
"""

from typing import Callable
from decimal import Decimal, getcontext
import math
import mpmath 

ctx = getcontext()
ctx.prec = 30  # set desired precision
mpmath.mp.dps = 30  # Set precision to match your Decimal context

# High-precision PI (truncate/extend to your needed precision)
PI = Decimal('3.14159265358979323846264338327950288419716939937510')
# Radians PI = 180 degrees
TWO_PI = PI * Decimal(2)        # 360 degrees
HALF_PI = PI / Decimal(2)       # 90 degrees
DEG2RAD = PI / Decimal(180)
RAD2DEG = Decimal(180) / PI

# Square Root Function
def sqrt(x: Decimal) -> Decimal:
    """
    Calculate the square root of a Decimal number.
    
    Args:
        x: A Decimal number (must be non-negative)
        
    Returns:
        The square root as a Decimal
    """
    if x < 0:
        raise ValueError("Cannot take square root of negative number")
    
    # Using Newton's method for calculating square root
    if x == 0:
        return Decimal('0')
    
    # Initial guess
    guess = x / 2
    
    # Precision - adjust as needed
    precision = Decimal('1e-50')
    
    # Newton's method
    while True:
        better_guess = (guess + x / guess) / 2
        if abs(better_guess - guess) < precision:
            return better_guess
        guess = better_guess# Add these utility functions
        
def sin(x: Decimal) -> Decimal:
    """Calculate sine of x (in radians) with high precision"""
    return Decimal(str(mpmath.sin(mpmath.mpf(str(x)))))

def cos(x: Decimal) -> Decimal:
    """Calculate cosine of x (in radians) with high precision"""
    return Decimal(str(mpmath.cos(mpmath.mpf(str(x)))))

def tan(x: Decimal) -> Decimal:
    """Calculate tangent of x (in radians) with high precision"""
    return Decimal(str(mpmath.tan(mpmath.mpf(str(x)))))

def sign(x: Decimal) -> int:
    """Return the sign of x: -1 for negative, 0 for zero, 1 for positive"""
    if x < 0:
        return -1
    elif x > 0:
        return 1
    return 0

def abs(x : int | Decimal) -> Decimal:
    """Return the absolute value of x."""
    if x < 0:
        return -x
    return x

def floor(x: int | float | Decimal) -> int:
    """Return the largest integer not greater than x."""
    if isinstance(x,int):
        return x
    elif isinstance(x,float):
        return math.floor(x)
    return x.to_integral_value(rounding='ROUND_FLOOR')

def ceil(x: int | Decimal) -> Decimal:
    """Return the largest integer not greater than x."""
    if isinstance(x,int):
        return x
    return x.to_integral_value(rounding='ROUND_CEILING')

def trunc(x: Decimal, decimals=0) -> Decimal:
    """Truncate x to a given number of decimal places."""
    factor = Decimal(10) ** Decimal(decimals)
    return (x * factor).to_integral_value(rounding='ROUND_DOWN') / factor

# Some general purpose functions particular to Reingold and Dershowitz
def round(x: Decimal) -> Decimal:
    return floor(x + Decimal(0.5))

def round_at(x: Decimal, decimals=0) -> Decimal:
    """Round x to a given number of decimal places."""
    factor = Decimal(10) ** Decimal(decimals)
    result = (x * factor)
    result = trunc(result +  Decimal(0.5))
    result /= factor
    return result

def mod(x : Decimal, y : Decimal) -> Decimal:
    """Return x mod y, ensuring a non-negative result."""
    if y <= 0:
        raise ValueError("y must be positive")
    return ((x % y) + y) % y

def mod_adj(x : Decimal, y : Decimal) -> Decimal:
    x_ = int(x)
    y_ = abs(int(y))
    if (x!= x_) or (y != y_):
        raise ValueError("x must be integer and y integer and positive")
    result  =  y if x % y == 0 else x % y
    return Decimal(result)

def mod_interval(x: Decimal, a: int | Decimal, b: int| Decimal) -> Decimal:
    if a == b:
        return x
    return a + (x - a) % (b - a)

def MAX(start : Decimal, test : Callable [[Decimal], bool]) -> Decimal:
    """Find the first value that does not satisfy test(x)."""
    x = start
    last_x = None
    while test(x):
        last_x = x
        x += 1
    return last_x

def min(x: Decimal, y: Decimal) -> Decimal:
    """Return the smaller of x and y."""
    return x if x < y else y

def MIN(start : Decimal, test : Callable [[Decimal], bool]) -> Decimal:
    """Find the first value which satisfies test(x)"""
    x = start
    while not test(x):
        x += 1
    return x

# Converts permissible values to Decimal
def decimal_(_value : Decimal | int | float | str) -> Decimal:
    """Convert value to Decimal, preserving precision"""
    if isinstance(_value, Decimal):
        return _value
    elif isinstance(_value, float):
        return Decimal(str(_value))
    return Decimal(_value)

def count_decimal_places(value: Decimal) -> int:
    """
    Return the number of decimal places in a Decimal number.
    Handles scientific notation correctly.
    """
    if not isinstance(value, Decimal):
        value = decimal_(value)
        
    # Get the tuple representation
    tup = value.as_tuple()
    
    # The exponent tells us about decimal places
    # If exponent is negative, it's the number of decimal places
    if tup.exponent < 0:
        return abs(tup.exponent)
    return 0

def to_roman_numeral(num : int | Decimal, lowercase=True):
    """
    Convert integer to Roman numeral.
    
    Args:
        num: Integer to convert
        lowercase: 
            If True, returns lowercase numerals (i, ii, iii, etc.)
            If False, returns uppercase numerals (I, II, III, etc.)
    
    Returns:
        String containing Roman numeral representation
    """
    val = [
        1000, 900, 500, 400,
        100, 90, 50, 40,
        10, 9, 5, 4,
        1
    ]
    syms = [
        "M", "CM", "D", "CD",
        "C", "XC", "L", "XL",
        "X", "IX", "V", "IV",
        "I"
    ]
    if isinstance(num, Decimal):
        num = int(num)
    roman_num = ''
    i = 0
    while num > 0:
        for _ in range(num // val[i]):
            roman_num += syms[i]
            num -= val[i]
        i += 1
    
    return roman_num.lower() if lowercase else roman_num

def within_precision(a: Decimal, b: Decimal, exp: int) -> bool:
    """
    Test if |a - b| < 10^exp, where exp is the precision exponent.
    """
    tolerance = Decimal(10) ** Decimal(exp)
    return abs(a - b) < tolerance

