"""
CC19_Chinese_1645 — Chinese lunisolar calendar (1645-onwards Beijing rules)
from R&D chapter 19.

**Purpose.**  Implement the astronomical Chinese calendar as R&D
formalise it: solar-term boundaries derived from apparent solar
longitude, month boundaries from apparent new moons, both computed
at the meridian of Beijing (with the pre-1929 local-mean-time
adjustment).  All of the search idioms (`MIN`, `MAX`) come from
`CC00_Decimal_library`; the astronomical primitives come from
`CC14_Time_and_Astronomy`.

**Known deviations from R&D reference.**  Two Appendix-C rows in
`Tests/test_400_Moment_cPresent_Chinese.py` fail with off-by-one
month counts — tracked as backlog entry B-01 in
`docs/TODO_BACKLOG.md`.  These are the load-bearing "allowed-red"
tests: every PL-01 checkpoint must reproduce exactly this set of
failures, no more and no fewer.

**Public surface (re-exported via `__init__.py`).**
    Solar-term:  `current_major_solar_term`,
        `major_solar_term_on_or_after`, `current_minor_solar_term`,
        `minor_solar_term_on_or_after`.
    Astronomy:   `chinese_location`, `midnight_in_china`,
        `chinese_solar_longitude_on_or_after`,
        `chinese_winter_solstice_on_or_before`,
        `chinese_new_moon_on_or_after`, `chinese_new_moon_before`.
    Leap-month:  `is_chinese_no_major_solar_term`,
        `is_chinese_prior_leap_month`.
    Year:        `chinese_new_year_in_sui`,
        `chinese_new_year_on_or_before`.
    Conversion:  `chinese_from_rd`, `rd_from_chinese`.
    Sexagesimal: `chinese_sexagesimal_tuple`, `chinese_name_difference`,
        `chinese_year_tuple`, `chinese_month_epoch`,
        `chinese_month_tuple`, `chinese_day_epoch`,
        `chinese_day_tuple`, `chinese_day_tuple_on_or_before`.

**R&D references.**  Each function is preceded by ``# p NNN (19.X)``
giving the page and equation number in R&D chapter 19 (Ultimate
Edition); these citations are load-bearing and must never be
removed during refactor.

**Not in scope.**  Chinese calendar constants (`Constants_Chinese`),
presentation / localisation (`Moment_cPresent_Chinese`).

**Change history.**  See `CHANGELOG.md`.  Any change that could
alter the allowed-red set for B-01 (either fixing it or breaking
additional rows) requires an explicit acceptance-test update and
an entry in the plan's change log.
"""

from decimal import Decimal

from .CC00_Decimal_library import mod_adj, floor, ceil, MIN, round
from .CC01_Calendar_Basics import Epoch_rd
from .CC02_Gregorian import gregorian_year_from_rd
from .CC14_Time_and_Astronomy import solar_longitude, universal_from_standard, location, solar_longitude_after, standard_from_universal
from .CC14_Time_and_Astronomy import estimate_prior_solar_longitude, new_moon_at_or_after, new_moon_before, mean_synodic_month, mean_tropical_year
from .CC14_Time_and_Astronomy import winter

# page 306 (19.1)
def current_major_solar_term(date : Decimal) -> int:
    """
    R&D (19.1): index (1–12) of the last major solar term at or
    before `date`, using apparent solar longitude at the Beijing
    meridian.

    Args:
        date:  R.D. moment as `Decimal`.

    Returns:
        Integer 1–12 identifying the current major solar term.
    """
    s = solar_longitude(universal_from_standard(date, chinese_location(date)))
    return mod_adj(2 + floor(s / Decimal(30)), 12)

# page 306 (19.2)
def chinese_location(date: Decimal) -> Decimal:
    """
    R&D (19.2): observer location for Chinese-calendar computations.

    Always Beijing (39°55′ N, 116°25′ E, 43.5 m elevation).  The
    timezone offset changes on the Gregorian-year boundary of 1929:

      * year < 1929: local mean time, offset = 1397/180 hours
        (7 h 45 min 40 s east of UT).
      * year ≥ 1929: standard China time, offset = +8 h (120° E
        meridian).

    Args:
        date:  R.D. moment; only its Gregorian year is inspected.

    Returns:
        `location` tuple (lat_dms, lon_dms, elevation_m, offset_h).
    """
    year = gregorian_year_from_rd(floor(date))
    if year < 1929:
        return location((39,55,0),(116,25,0),Decimal(43.5), 1397/180)
    return location((39,55,0),(116,25,0),Decimal(43.5), 8)

# p308 (19.3)
def chinese_solar_longitude_on_or_after(_lambda : Decimal, t : Decimal) -> Decimal:
    """Return the first date on or after t at which the sun's ecliptic longitude is _lambda degrees."""
    sun = solar_longitude_after(_lambda, t)
    return standard_from_universal(sun, chinese_location(sun))

# p 308 (19.4)
def major_solar_term_on_or_after(date : Decimal) -> Decimal:
    """Return the first date on or after date at which the sun's ecliptic longitude is a major solar term."""
    s = solar_longitude(midnight_in_china(date))
    _lambda = (30*ceil(s / 30)) % 360
    return chinese_solar_longitude_on_or_after(_lambda, date)

# p 308 (19.5)
def current_minor_solar_term(date : Decimal) -> Decimal:
    """Return the current minor solar term for the given date."""
    s = solar_longitude(universal_from_standard(date, chinese_location(date)))
    _lambda = (3 + floor( (s -15)/ 30))
    return mod_adj(_lambda, 12)

# p 308 (19.6)
def minor_solar_term_on_or_after(date: Decimal) -> Decimal:
    s = solar_longitude(midnight_in_china(date))
    _lambda = (30 * ceil( (s -15)/ 30) + 15) % 360
    return chinese_solar_longitude_on_or_after(_lambda, date)

# p 309 (19.7)
def midnight_in_china(date: Decimal) -> Decimal:
    """Return the midnight in China for the given date."""
    return universal_from_standard(date, chinese_location(date))

# p 309 (19.8)
def chinese_winter_solstice_on_or_before(date: Decimal) -> Decimal:
    day = estimate_prior_solar_longitude(winter(), midnight_in_china(date+1)) - 1
    day = MIN(day, lambda day : winter() < solar_longitude((midnight_in_china(day+1))))
    return day

# p 309 (19.9)
def chinese_new_moon_on_or_after(date : Decimal) -> Decimal:
    t = new_moon_at_or_after(midnight_in_china(date))
    return floor(standard_from_universal(t, chinese_location(t)))

# p 309 (19.10)
def chinese_new_moon_before(date : Decimal) -> Decimal:
    t = new_moon_before(midnight_in_china(date))
    return floor(standard_from_universal(t, chinese_location(t)))

# p 313 (19.11)
def is_chinese_no_major_solar_term(date) -> bool:
    """Return True if the given date has no major solar term."""
    return current_major_solar_term(date) == current_major_solar_term(chinese_new_moon_on_or_after(date+1))
    
# p 313 (19.12)
def is_chinese_prior_leap_month(m_p, m) -> bool:
    """Return True if the given month is after the leap month."""
    if m >= m_p:
        if is_chinese_no_major_solar_term(m):
            return True
        elif is_chinese_prior_leap_month(m_p, chinese_new_moon_before(m)):
            return True
    return False

# p 315 (19.13)
def chinese_new_year_in_sui(date : Decimal) -> Decimal:
    """Return the Chinese New Year in the Sui containing the date."""
    s1 = chinese_winter_solstice_on_or_before(date)
    s2 = chinese_winter_solstice_on_or_before(date+370)
    m12 = chinese_new_moon_on_or_after(s1 + 1)
    m13 = chinese_new_moon_on_or_after(m12 + 1)
    next_m11 = chinese_new_moon_before(s2 + 1)
    if round((next_m11 - m12) / mean_synodic_month()) == 12 and (is_chinese_no_major_solar_term(m12) or is_chinese_no_major_solar_term(m13)):
        return chinese_new_moon_on_or_after(m13 + 1)
    else:
        return m13
    
# p 316 (19.14)
def chinese_new_year_on_or_before(date: Decimal) -> Decimal:
    """Return the Chinese New Year on or before the given date."""
    new_year = chinese_new_year_in_sui(date)
    if date >= new_year:
        return new_year
    else:
        return chinese_new_year_in_sui(date - 180)
    
# p 316 (19.15)  see Epoch_rd['chinese']  in CC01_Calendar_Basics.py

# p 317 (19.16)
def chinese_from_rd(date : Decimal) -> tuple[int, int, int, bool, int]:
    """Convert R.D. to a Chinese date."""
    s1 = chinese_winter_solstice_on_or_before(date)
    s2 = chinese_winter_solstice_on_or_before(s1 + 370)
    m12 = chinese_new_moon_on_or_after(s1 + 1)
    next_m11 = chinese_new_moon_before(s2 + 1)
    m = chinese_new_moon_before(date + 1)
    
    leap_year = round((next_m11 - m12) / mean_synodic_month()) == 12
    
    month = round((m - m12) / mean_synodic_month())
    if leap_year and is_chinese_prior_leap_month(m12,m):
        month -= 1
    month = mod_adj(month, 12)   
    elapsed_years = floor(Decimal(1.5) - month/12 + (date - Epoch_rd['chinese']) / mean_tropical_year())
    
    cycle = int(floor((elapsed_years - 1) / Decimal(60)) + 1)   
    year =int(mod_adj(elapsed_years, 60))
    month = int(month)
    leap_month = False
    if leap_year:
        if is_chinese_no_major_solar_term(m):
#            if not is_chinese_prior_leap_month(m12, chinese_new_moon_before(m)):
            leap_month = True
    day = int(date - m + 1)
    return cycle, year, month, leap_month, day

# p 318 (19.17)
def rd_from_chinese(cycle: Decimal, year: Decimal, month: Decimal, leap_month: bool, day: Decimal) -> Decimal:
    """Convert a Chinese date to R.D."""
    mid_year = floor(Epoch_rd['chinese'] + ((cycle -1) * 60 + year -1 + Decimal(0.5)) * mean_tropical_year())
    new_year = chinese_new_year_on_or_before(mid_year)
    p = chinese_new_moon_on_or_after(new_year + (month-1) * 29)
    d = chinese_from_rd(p)
    prior_new_moon = p if month == d[2] and leap_month == d[3] else chinese_new_moon_on_or_after(p + 1)
    return prior_new_moon + day - 1

# p 319 (19.18)
def chinese_sexagesimal_tuple(n : int) -> tuple[int,int]:
    """Return the sexagesimal name for the given index."""
    stem = mod_adj(n, 10)
    branch = mod_adj(n, 12)
    return stem, branch

# p 319 (19.19)
def chinese_name_difference(name1 : tuple[int,int], name2 : tuple[int,int]) -> int:
    """Return the difference between two sexagesimal names."""
    stem1, branch1 = name1
    stem2, branch2 = name2
    stem_diff = stem2 - stem1
    branch_diff = branch2 - branch1
    result = mod_adj(stem_diff + 25 * (branch_diff - stem_diff), 60)
    return result

# p 320 (19.20)
def chinese_year_tuple(year : int) -> str:
    return chinese_sexagesimal_tuple(year)

# p 320 (19.21)
def chinese_month_epoch() -> int:
    return 57

# p 320 (19.22)
def chinese_month_tuple(month : int, year : int) -> str:
    """Return the sexagesimal name for the given month in the given year."""
    elapsed_months = 12 * (year-1) + month -1
    return chinese_sexagesimal_tuple(elapsed_months - chinese_month_epoch())

# p 321 (19.23)
def chinese_day_epoch() -> int:
    return 45  # R.D.

# p 321 (19.24)
def chinese_day_tuple(date_rd : int) -> tuple[int,int]:
    return chinese_sexagesimal_tuple(date_rd - chinese_day_epoch())

# p 321 (19.25)
def chinese_day_tuple_on_or_before(name : tuple[int,int], date : int) -> Decimal:
    """Return the last date on or before the given date with the given sexagesimal name."""
    d = chinese_day_tuple(0)
    diff = chinese_name_difference(d, name)
    return mod_adj(diff, date - 60)