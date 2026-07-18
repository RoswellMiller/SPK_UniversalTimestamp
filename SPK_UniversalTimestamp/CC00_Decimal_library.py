"""
CC00_Decimal_library — fixed-precision arithmetic helpers for the
calendrical code paths that need more accuracy than `float` provides.

**Purpose.**
    Wrap the standard library `decimal` module and `mpmath` in a
    single-import surface with the exact numerical conventions that
    Reingold & Dershowitz (R&D) *Calendrical Calculations* assumes:
    a `mod` that always returns non-negative, a `mod_adj` that maps
    exact multiples to `y` instead of `0`, floor/ceil/round matching
    R&D's mathematical (not IEEE) definitions, and 30-decimal
    working precision on both back-ends.

**Public surface (star-exported via `__init__.py`).**
    Constants: ``PI``, ``TWO_PI``, ``HALF_PI``, ``DEG2RAD``, ``RAD2DEG``.
    Arithmetic: ``sqrt``, ``sin``, ``cos``, ``tan``, ``sign``, ``abs``.
    Rounding: ``floor``, ``ceil``, ``trunc``, ``round``, ``round_at``.
    Modular: ``mod``, ``mod_adj``, ``mod_interval``.
    Search:   ``MAX``, ``min``, ``MIN``.
    Conversion / diagnostic: ``decimal_``, ``count_decimal_places``,
        ``to_roman_numeral``, ``within_precision``.

**R&D references.**
    R&D ch. 1 (Calendar Basics) is the source for the mod / mod_adj /
    mod_interval semantics; specific equations are cited inline where
    they apply (e.g. `mod_adj` follows the ``x mod₁ y`` definition on
    p. 20).

**Not in scope.**
    Complex numbers, matrix algebra, or any function whose R&D use
    site does not need it — do not add "nice to have" helpers here.
    Keep the surface minimal so calendar code paths do not silently
    grow dependencies.

**Change history.**  See `CHANGELOG.md`; this module is stable and
changes to its public surface are rare and always version-bumped.
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
    Newton's-method square root of a non-negative `Decimal`.

    Args:
        x:  Non-negative `Decimal` radicand.  Zero returns exact zero;
            positive values iterate until successive approximations
            differ by less than ``1e-50``.

    Returns:
        `Decimal` `r` such that ``r * r`` is `x` to within the
        30-decimal working precision of `getcontext()`.

    Raises:
        `ValueError`: `x` is strictly negative.  Complex results are
            deliberately unsupported here — the calendrical code paths
            that call `sqrt` are always in real-number domains.

    Notes:
        The internal tolerance (``1e-50``) is finer than the module's
        30-digit context on purpose: it guarantees the returned value
        is stable to the last decimal `getcontext()` will retain.
    """
    if x < 0:
        raise ValueError("Cannot take square root of negative number")
    
    # Using Newton's method for calculating square root
    if x == 0:
        return Decimal('0')
    
    # Initial guess
    guess = x / 2
    
    # UnivMomPrecision - adjust as needed
    precision = Decimal('1e-50')
    
    # Newton's method
    while True:
        better_guess = (guess + x / guess) / 2
        if abs(better_guess - guess) < precision:
            return better_guess
        guess = better_guess

# Trigonometric wrappers around `mpmath`
def sin(x: Decimal) -> Decimal:
    """
    Sine of `x` (radians), routed through `mpmath` at 30-decimal precision.

    The `Decimal` argument is stringified into an `mpmath.mpf`, the
    trig is done in `mpmath`, and the result is stringified back to
    `Decimal`.  Round-tripping through strings avoids the FP path
    entirely so the returned value is exact to the current context
    precision.

    Args:
        x:  Angle in radians as `Decimal`.  No wrapping is done; very
            large `x` will still work but pays the full `mpmath` cost.

    Returns:
        `Decimal` sine of `x`, precision equal to `mpmath.mp.dps`.
    """
    return Decimal(str(mpmath.sin(mpmath.mpf(str(x)))))

def cos(x: Decimal) -> Decimal:
    """
    Cosine of `x` (radians).  See `sin` for the precision contract
    and the reason for string round-tripping through `mpmath`.

    Args:
        x:  Angle in radians as `Decimal`.

    Returns:
        `Decimal` cosine of `x`.
    """
    return Decimal(str(mpmath.cos(mpmath.mpf(str(x)))))

def tan(x: Decimal) -> Decimal:
    """
    Tangent of `x` (radians).  See `sin` for the precision contract.

    Args:
        x:  Angle in radians as `Decimal`.  No guard against
            odd-multiples-of-π/2; the underlying `mpmath.tan` returns
            a very large finite value there rather than raising.

    Returns:
        `Decimal` tangent of `x`.
    """
    return Decimal(str(mpmath.tan(mpmath.mpf(str(x)))))

def sign(x: Decimal) -> int:
    """
    Three-valued sign function returning a Python `int`.

    Args:
        x:  `Decimal` to test.

    Returns:
        `-1` if `x < 0`, `0` if exactly zero, `+1` if `x > 0`.
    """
    if x < 0:
        return -1
    elif x > 0:
        return 1
    return 0

def abs(x : int | Decimal) -> Decimal:
    """
    Absolute value that keeps the argument's type family.

    Shadows the built-in `abs` on purpose — the calendrical code
    paths in this package all use `from CC00_Decimal_library import *`
    and want the guaranteed-`Decimal`-out contract.

    Args:
        x:  `int` or `Decimal` argument.

    Returns:
        `|x|` as a value of the same type as `x`.
    """
    if x < 0:
        return -x
    return x

def floor(x: int | float | Decimal) -> int:
    """
    Largest integer not greater than `x`, in R&D's mathematical sense.

    Unlike Python's built-in `math.floor` (which always returns
    `int`), this returns the same numeric kind for `int` and
    `Decimal` inputs — the `Decimal` branch uses `ROUND_FLOOR`
    which is mathematical floor even for negative numbers.  This
    matters for the R&D formulae that iterate over signed R.D. day
    counts.

    Args:
        x:  `int`, `float`, or `Decimal`.

    Returns:
        For `int`, `x` unchanged.  For `float`, `math.floor(x)`
        (a Python `int`).  For `Decimal`, a `Decimal` whose value
        is the mathematical floor.  The declared `-> int` return
        type is intentionally the loose union; callers that need a
        `Decimal` back should pass a `Decimal` in.
    """
    if isinstance(x,int):
        return x
    elif isinstance(x,float):
        return math.floor(x)
    return x.to_integral_value(rounding='ROUND_FLOOR')

def ceil(x: int | Decimal) -> Decimal:
    """
    Smallest integer not less than `x`.

    Mirror of `floor`; uses `ROUND_CEILING` on the `Decimal` branch
    so negative inputs round toward zero as R&D expects, not toward
    negative infinity.

    Args:
        x:  `int` or `Decimal`.

    Returns:
        The mathematical ceiling, in the same numeric kind as `x`.
    """
    if isinstance(x,int):
        return x
    return x.to_integral_value(rounding='ROUND_CEILING')

def trunc(x: Decimal, decimals: int = 0) -> Decimal:
    """
    Truncate `x` toward zero at a given decimal place.

    `ROUND_DOWN` is truncation toward zero (not toward negative
    infinity); this matches R&D's use of `trunc` in reduction
    formulae where sign preservation matters.

    Args:
        x:         Value to truncate.
        decimals:  Number of fractional digits to preserve; may be
            negative to truncate to a power of ten (`decimals=-3`
            drops units, tens, and hundreds).  Defaults to `0` for
            integer truncation.

    Returns:
        `Decimal` truncated to the requested precision.
    """
    factor = Decimal(10) ** Decimal(decimals)
    return (x * factor).to_integral_value(rounding='ROUND_DOWN') / factor

# Some general purpose functions particular to Reingold and Dershowitz
def round(x: Decimal) -> Decimal:
    """
    Round `x` to the nearest integer using R&D's half-up rule.

    Shadows the built-in `round` — the built-in uses banker's
    rounding (round-half-to-even), which introduces sign-dependent
    parity artifacts that R&D's day-count arithmetic will not
    tolerate.  This variant is ``floor(x + 0.5)``, i.e. half-up for
    positive `x` and half-down for negative.

    Args:
        x:  `Decimal` argument.

    Returns:
        Nearest integer to `x` as `Decimal`, with the R&D
        half-away-from-negative-infinity convention.
    """
    return floor(x + Decimal(0.5))

def round_at(x: Decimal, decimals: int = 0) -> Decimal:
    """
    Round `x` to `decimals` fractional digits using the half-up rule.

    Same half-up convention as `round` (via `trunc(_ + 0.5)`) but
    applied at an arbitrary decimal place.  Used by presentation
    layers that need a fixed-precision display of a computed
    quantity without switching to bank-rounding surprises.

    Args:
        x:         `Decimal` argument.
        decimals:  Number of fractional digits to keep (default `0`).

    Returns:
        `Decimal` rounded to the requested precision.
    """
    factor = Decimal(10) ** Decimal(decimals)
    result = (x * factor)
    result = trunc(result +  Decimal(0.5))
    result /= factor
    return result

def mod(x : Decimal, y : Decimal) -> Decimal:
    """
    Non-negative modulo, matching R&D's ``x mod y`` convention.

    R&D define ``x mod y`` as the unique value in ``[0, y)`` congruent
    to `x` modulo `y`.  Python's built-in ``%`` already returns a
    non-negative result when `y` is positive — the extra ``+ y) % y``
    step is defensive: it costs one addition and one modulo but
    guarantees the invariant even if the numeric back-end changes.

    Args:
        x:  Numerator `Decimal`; may be negative, zero, or positive.
        y:  Strictly positive `Decimal` modulus.

    Returns:
        `Decimal` `r` in the half-open interval ``[0, y)``.

    Raises:
        `ValueError`: `y` is zero or negative.  R&D's definition is
            only defined for a positive modulus and calendar code
            never needs the negative-`y` case; failing loudly here
            catches upstream sign-flip mistakes.

    See also:
        `mod_adj` — the same idea but returning `y` for exact
        multiples instead of `0`.  `mod_interval` — wrap into an
        arbitrary half-open ``[a, b)`` window.
    """
    if y <= 0:
        raise ValueError("y must be positive")
    return ((x % y) + y) % y

def mod_adj(x : Decimal, y : Decimal) -> Decimal:
    """
    R&D's ``x mod₁ y`` — like `mod` but returns `y` on exact multiples.

    Where ``mod(x, y)`` maps the values ``0, y, 2y, …`` to `0`,
    ``mod_adj(x, y)`` maps them to `y`.  This variant is what several
    R&D calendar tables want when they name the "last" element of a
    cycle (day-of-month, month-of-year) rather than the "zero-th":
    it keeps the ordinal 1-based across the wrap.

    Args:
        x:  Integer-valued `Decimal` numerator (fractional parts are
            not allowed — R&D's definition is on integers only).
        y:  Strictly positive integer-valued `Decimal` modulus.

    Returns:
        `Decimal` `r` in the closed interval ``[1, y]``.

    Raises:
        `ValueError`: `x` or `y` are non-integer, or `y` is non-positive.
            The integrality check compares each value against its
            `int()` truncation; this rejects `Decimal('1.5')` even
            though it would pass an ``isinstance(_, int)`` test.
    """
    x_ = int(x)
    y_ = abs(int(y))
    if (x!= x_) or (y != y_):
        raise ValueError("x must be integer and y integer and positive")
    result  =  y if x % y == 0 else x % y
    return Decimal(result)

def mod_interval(x: Decimal, a: int | Decimal, b: int| Decimal) -> Decimal:
    """
    Wrap `x` into the half-open interval ``[a, b)``.

    Generalizes `mod` from ``[0, y)`` to any half-open window; used
    by R&D formulae that normalize longitudes into ``[0, 360)`` or
    angular coordinates into ``[-180, 180)``.  The degenerate case
    ``a == b`` returns `x` unchanged: the interval is empty and the
    only sensible "wrap" is no-op.

    Args:
        x:  Value to wrap; may lie anywhere on the real line.
        a:  Lower bound (inclusive).
        b:  Upper bound (exclusive).

    Returns:
        `Decimal` `r` in ``[a, b)`` congruent to `x` modulo `b - a`,
        or `x` itself if `a == b`.
    """
    if a == b:
        return x
    return a + (x - a) % (b - a)

def MAX(start : Decimal, test : Callable [[Decimal], bool]) -> Decimal:
    """
    Return the largest integer `x >= start` for which `test(x)` is still true.

    Linear upward search: starts at `start`, increments by one each
    iteration, and returns the **previous** value the moment `test`
    flips to false.  Mirrors R&D's ``MAX`` search notation and is used
    by lookup tables that walk forward until a boundary condition
    fails (e.g. "largest day such that the month-length invariant
    still holds").

    Args:
        start:  First value to try.  `test(start)` MUST return true
            — otherwise the search never enters the loop and the
            return value is `None`, which is almost never what the
            caller wants.  This precondition is not checked.
        test:   Monotone predicate: caller guarantees that once
            `test(x)` returns false it never returns true again for
            larger `x`.  If the predicate is not monotone the result
            is undefined.

    Returns:
        `Decimal` last `x` for which `test(x)` was true, or `None`
        if the loop body never executed (see `start` precondition).

    See also:
        `MIN` — the mirror function that returns the *first* `x`
        which does satisfy `test`.
    """
    x = start
    last_x = None
    while test(x):
        last_x = x
        x += 1
    return last_x

def min(x: Decimal, y: Decimal) -> Decimal:
    """
    Return the smaller of `x` and `y` — two-argument only.

    Shadows the built-in `min` deliberately for the same reason
    `abs` does: to give the star-import surface a guaranteed
    `Decimal`-typed comparator.  For n-ary `min` use the built-in
    directly (this module does not re-implement it).

    Args:
        x, y:  `Decimal` values to compare.

    Returns:
        `x` if `x < y`, otherwise `y`.  Ties return `y`.
    """
    return x if x < y else y

def MIN(start : Decimal, test : Callable [[Decimal], bool]) -> Decimal:
    """
    Return the smallest integer `x >= start` for which `test(x)` is true.

    Mirror of `MAX`: walks upward from `start`, incrementing by one,
    and returns the first `x` that satisfies `test`.  Used by R&D
    lookup tables that need the first candidate meeting a threshold.

    Args:
        start:  First value to test.
        test:   Predicate on `Decimal`.  If no value in
            ``[start, +∞)`` satisfies it the search never terminates —
            callers MUST guarantee reachability.

    Returns:
        First `x` satisfying `test(x)`.

    See also:
        `MAX` — the mirror function that returns the *last* `x`
        which still satisfies `test`.
    """
    x = start
    while not test(x):
        x += 1
    return x

# Converts permissible values to Decimal
def decimal_(_value : Decimal | int | float | str) -> Decimal:
    """
    Convert a mixed-type numeric input to `Decimal` without precision loss.

    The `float` case round-trips through `str` deliberately —
    ``Decimal(float_value)`` captures the FP representation error
    (``Decimal(0.1)`` becomes ``0.1000000000000000055...``), while
    ``Decimal(str(float_value))`` gives the intended tenth exactly.

    Args:
        _value:  `Decimal`, `int`, `float`, or numeric `str`.
            Already-`Decimal` inputs are returned unchanged.

    Returns:
        `Decimal` representation of `_value`.

    Raises:
        `decimal.InvalidOperation`: `_value` is a `str` that does not
            parse as a decimal number (propagated from the underlying
            `Decimal(_value)` call).
    """
    if isinstance(_value, Decimal):
        return _value
    elif isinstance(_value, float):
        return Decimal(str(_value))
    return Decimal(_value)

def count_decimal_places(value: Decimal) -> int:
    """
    Return the number of fractional digits in `value`'s canonical form.

    Uses `Decimal.as_tuple().exponent` rather than string parsing,
    which correctly handles scientific notation (`Decimal('1E-5')`
    reports 5, not 3).  Non-`Decimal` inputs are coerced through
    `decimal_` first so a caller can pass a `float` or `str`
    directly.

    Args:
        value:  `Decimal` to inspect; other numeric types are
            accepted and coerced.

    Returns:
        Number of digits after the decimal point (`0` for integer
        values, positive `int` otherwise).
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

def to_roman_numeral(num: int | Decimal, lowercase: bool = True) -> str:
    """
    Convert a positive integer to its Roman-numeral representation.

    Uses the standard subtractive notation (`IV`, `IX`, `XL`, `XC`,
    `CD`, `CM`) driven by a fixed value/symbol table.  Only positive
    integers up to a few thousand yield conventional-looking
    results; there is no upper bound check, so very large values
    just accumulate leading `M`s.

    Args:
        num:        Integer to convert.  `Decimal` inputs are
            truncated to `int` — no fractional-value warning.
            Non-positive values return the empty string (the loop
            body never executes) rather than raising.
        lowercase:  `True` (default) returns lowercase letters
            (``i, ii, iii, …``); `False` returns uppercase.

    Returns:
        Roman-numeral `str`.  Empty for `num <= 0`.
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
    Return `True` when `a` and `b` agree to within ``10**exp``.

    Used as an epsilon-comparator in the numerical-solver-adjacent
    tests where the calendars converge iteratively (e.g. moment-of-new-moon
    root-finding).  A negative `exp` gives a tight tolerance
    (``exp=-6`` tolerates a millionth); a positive `exp` gives a
    loose one.

    Args:
        a, b:  `Decimal` values to compare.
        exp:   Signed integer exponent of the tolerance in base 10.

    Returns:
        `True` if `|a - b| < 10**exp`, else `False`.
    """
    tolerance = Decimal(10) ** Decimal(exp)
    return abs(a - b) < tolerance

