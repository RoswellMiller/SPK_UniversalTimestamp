from typing import Tuple
from decimal import Decimal
from .UnivDecimalLibrary import *
from .UnivSpace import psoEarth
from .CC02_Gregorian import gregorian_date_difference, gregorian_year_from_rd, gregorian_new_year

# Some general purpose functions particular to Reingold and Dershowitz
def round_(x : Decimal) -> Decimal:
    return floor(x  + Decimal(0.5))

# Converts degrees, minutes, seconds to Decimal(degrees) 
def degrees_from_dms(value : Decimal | int | float | str | tuple) -> Decimal:
    """Convert degrees, minutes, seconds to Decimal"""
    if isinstance(value, (int, float, Decimal)):
        return decimal_(value)
    elif isinstance(value, str):
        parts = value.split()
        if len(parts) == 3:
            return decimal_(parts[0]) + decimal_(parts[1]) / 60 + decimal_(parts[2]) / 3600
        elif len(parts) == 2:
            return decimal_(parts[0]) + decimal_(parts[1]) / 60
        elif len(parts) == 1:
            return decimal_(parts[0])
    elif isinstance(value, tuple):
        if len(value) == 3:
            return decimal_(value[0]) + decimal_(value[1]) / 60 + decimal_(value[2]) / 3600
        elif len(value) == 2:
            return decimal_(value[0]) + decimal_(value[1]) / 60
        elif len(value) == 1:
            return decimal_(value[0])
    raise ValueError("Invalid format for degrees")
    
def dms_from_degrees(value : Decimal) -> tuple:
    """Convert Decimal degrees to (degrees, minutes, seconds) tuple"""
    if not isinstance(value, Decimal):
        value = decimal_(value)
    degrees = int(value)
    value = abs(value - degrees) * 60
    minutes = int(value)
    seconds = (value - minutes) * 60
    seconds = seconds.quantize(Decimal('0.1'))  # Round to 1 decimal places
    return (degrees, minutes, seconds)

def hms_from_hours(value : Decimal) -> tuple:
    """Convert Decimal degrees to (degrees, minutes, seconds) tuple"""
    if not isinstance(value, Decimal):
        value = decimal_(value)
    hours = int(value)
    value = abs(value - hours) * 60
    minutes = int(value)
    seconds = (value - minutes) * 60
    seconds = seconds.quantize(Decimal('0.001'))  # Round to 1 decimal places
    return (hours, minutes, seconds)

##################################################################################################################
# p 204 (14.1-5) location class
class location:
    # __slots__
    psoe : psoEarth
    latitude : Decimal
    longitude : Decimal
    elevation : Decimal
    utc_offset : str
    name : str
    # IMMUTABLE ##################################################################################################
    __slots__ = ( 'psoe', 'latitude', 'longitude', 'elevation', 'utc_offset', 'name' )
    def __setattr__(self, name, value):
        """Prevent modification of attributes after initialization"""
        if hasattr(self, name):
            raise AttributeError(f"Cannot modify attribute '{name}' of UnivTimestamp")
        super().__setattr__(name, value)
        return

    # CONSTRUCTOR ################################################################################################
    def __init__(self, 
            latitude: int | float | Decimal | str | tuple, 
            longitude:  int | float | Decimal | str | tuple, 
            elevation: int | float | Decimal | str = Decimal(0), 
            utc_offset: float = 0,
            name: str = "UTC"
            ):
        self.latitude = degrees_from_dms(latitude)
        self.longitude = degrees_from_dms(longitude)
        self.elevation = decimal_(elevation)
        self.psoe = psoEarth(self.latitude, self.longitude, self.elevation)
        self.utc_offset = utc_offset
        self.name = name
        return
    
    # location methods ##########################################################################################
    def direction(self, loc_prime: 'location') -> Decimal:
        """Calculate the direction from this location to another location in degrees"""
        if not isinstance(loc_prime, location):
            raise TypeError("Argument must be of type 'location'")
        forward, _, _ = self.psoe.psoAzimuth_to(loc_prime.psoe)
        return Decimal(forward)
    def distance(self, loc_prime: 'location') -> Decimal:
        """Calculate the geodesic distance to another location in meters"""
        if not isinstance(loc_prime, location):
            raise TypeError("Argument must be of type 'location'")
        _, _, distance = self.psoe.psoAzimuth_to(loc_prime.psoe)
        return Decimal(distance)
    
    # FORMATTING #################################################################################################
    def __str__(self) -> str:
        """String representation of the location"""
        return f"Location(name={self.name}, utc='{self.utc_offset}',lat={self.latitude},long={self.longitude},elv={self.elevation}m)"
    def __repr__(self) -> str:
        """String representation of the location"""
        return f"Location(name={self.name}, utc='{self.utc_offset}',lat={self.latitude},long={self.longitude},elv={self.elevation}m)"
# End class location #############################################################################################
    
class AST():
    """
    Chapter 14 - Astronomical Calendars
    Basic Functions
    """
    # point              latitude    longitude  elev  utc_offset name
    urbana = location(   40.1,       -88.2,     225,  -6,        "Urbana, IL, USA")  # Urbana, IL, USA
    greenwich = location(51.4777815, 0,         46.9,  0,        "Greenwich, UK")  # Greenwich, UK
    mecca = location(    (21,25,24), (39,49,24),298,   3,        "Mecca, Saudi Arabia")  # Mecca, Saudi Arabia (degrees, minutes, seconds))
    jerusalem = location(31.771959,  35.217018, 740,   2,        "Jerusalem")  # Jerusalem
    acre = location(     32.94,      35.09,     22,    2,        "Acre, Jordan")
    sidney = location(   -33.8688,   151.2093,  58,   10,        "Sidney, Australia")
    rio = location(      -22.9068,   -43.1729,32.9,   -3,        "Rio de Janeiro, Brazil")
    tokyo = location(    35.6895,    139.6917,  44,    9,        "Tokyo, Japan")
    moscow = location(   55.7558,    37.6173,  144,    3,        "Moscow, Russia")
    lima = location(     -12.0464,   -77.0428, 138,   -5,        "Lima, Peru")

    
# p 205 (14.6)location functions
def direction(loc : location, loc_prime : location) -> Decimal:
    """Calculate the direction from loc to loc_prime in degrees"""
    if not isinstance(loc, location) or not isinstance(loc_prime, location):
        raise TypeError("Both arguments must be of type 'location'")
    forward = loc.direction(loc_prime)
    return Decimal(forward)

# ########################################################################################
# Local time kept around the world is roughly adjusted for by offset from UTC.
# In fact, the more precise adjustment is based on the longitude of the location of the observer of the time
# Equations 14.8 - 14.14 are used to convert between local, universal, and UTC standard time.
# It does NOT account for the observence of Daylight Saving Time (DST) or other local time adjustments.

# p 208 (14.8) time zone as a fraction of a day
def zone_from_longitude(longitude: Decimal) -> Decimal:
    return longitude / Decimal(360)

# p208 (14.9) universal time from local time
def universal_from_local(moment_l : Decimal, location : location)-> Decimal:
    """Convert local time to universal time based on longitude"""
    return moment_l - zone_from_longitude(location.longitude)
# p 208 (14.10) local time from universal time
def local_from_universal(moment_u : Decimal, location : location) -> Decimal:
    """Convert universal time to local time based on longitude"""
    return moment_u + zone_from_longitude(location.longitude)

# p 208 (14.11) standard time from universal time
def standard_from_universal(moment_u : Decimal, location : location) -> Decimal:
    """Convert universal time to standard time based on UTC offset"""
    return moment_u + Decimal(location.utc_offset)/Decimal(24)
# p 208 (14.12) universal time from standard time
def universal_from_standard(moment_s : Decimal, location : location) -> Decimal:
    """Convert standard time to universal time based on UTC offset"""
    return moment_s - Decimal(location.utc_offset)/Decimal(24)

# p 208 (14.13) standard time from local
def standard_from_local(moment_l : Decimal, location : location) -> Decimal:
    """Convert local time to standard time based on UTC offset"""
    return standard_from_universal(universal_from_local(moment_l, location), location)
# p 208 (14.14) local time from standard
def local_from_standard(moment_s : Decimal, location : location) -> Decimal:
    """Convert standard time to local time based on UTC offset"""
    return local_from_universal(universal_from_standard(moment_s, location), location)

""" Astronomical calculations are typically done using Dynamical Time, with its
unchanging time units. (There are various forms of Dynamical Time,but the diferences
are too small to be of concern to us.) Solar time units, however, are not
constant through time,mainly because of the retarding effects of tides and the
atmosphere, which cause a relatively steady lengthening of the day; they contribute
what is called a “secular”(that is,steadily changing) term to its length.  This slow
down causes the mean solar day to increase in length by about 1.7milliseconds per
century.  Because Universal Time is based on the Earth’s speed of rotation,which
is slowly decreasing, the discrepancy between Universal and Dynamical Time is
growing.  It now stands at about 67 seconds and is currently increasing at about an
average of 1 second per year.  To account for the vagaries in the length of aa u.t.
day, every now and then a leap second is inserted(usually between December 31
and January 1),  there by keeping our clocks—which show Universal Time—in tune
with the gradually slowing rotation of Earth.  Because the accumulated discrepancy
is not entirely predictable and is not accurately known for the years prior to 1600,
we use the following adhoc function for this ephemeris correction """
# rd is an RD Moment 
# Calculates correction in fraction of a day
def ephemeris_correction(moment_rd: Decimal) -> Decimal:
    year = gregorian_year_from_rd(int(moment_rd))
    if year <= -500:
        return _eph_c_otherwise(year)
    elif year < 500:
        return _eph_c_0(year)
    elif year < 1600:
        return _eph_c_500(year)
    elif year < 1700:
        return _eph_c_1600(year)
    elif year < 1800:
        return _eph_c_1700(year) 
    elif year < 1900:
        eph_c = gregorian_date_difference((1900, 1, 1), (year, 7, 1)) / Decimal(36525)
        return _eph_c_1800(eph_c)
    elif year <= 1986:
        eph_c = gregorian_date_difference((1900, 1, 1), (year, 7, 1)) / Decimal(36525)
        return _eph_c_1900(eph_c)
    elif year <= 2005:
        return _eph_c_1987(year)
    elif year <= 2050:
        return _eph_c_2006(year)     
    elif year <= 2150:
        return _eph_c_2051(year)
    else:
        return _eph_c_otherwise(year)


def _eph_c_2051(year : Decimal) -> Decimal:
    """Ephemeris correction for years greater-than-or-equal 2051 on-or-before 2150"""
    y = Decimal(year - 1820) /100
    x =  -20
    x += +32*y**2
    x += +Decimal('0.5628')*(2150-year)
    return x / Decimal(86400)

def _eph_c_2006(year : Decimal) -> Decimal:
    """Ephemeris correction for years greater-than-or-equal 2006 on-or-before 2050"""
    y = year - 2000
    x = Decimal('62.92') +Decimal('0.32217')*y +Decimal('0.005589')*y**2
    return x / Decimal(86400)

def _eph_c_1987(year : Decimal) -> Decimal:
    """Ephemeris correction for years greater-than-or-equal 1987 on-or-before 2005"""
    y = year - 2000
    x = Decimal('63.86') +Decimal('0.3345')*y -Decimal('0.060374')*y**2 +Decimal('0.0017275')*y**3 +Decimal('0.000651814')*y**4 +Decimal('0.00002373599')*y**5
    return x / Decimal(86400)

def _eph_c_1900(c : Decimal) -> Decimal:
    """Ephemeris correction for years greater-than-or-equal 1900 on-or-before 1986"""
    x =  -Decimal('0.00002')
    x += +Decimal('0.000297')*c
    x += +Decimal('0.025184')*c**2
    x += -Decimal('0.181133')*c**3
    x += +Decimal('0.553040')*c**4
    x += -Decimal('0.861938')*c**5
    x += +Decimal('0.677066')*c**6
    x += -Decimal('0.212591')*c**7
    return x

def _eph_c_1800(c : Decimal) -> Decimal:
    """Ephemeris correction for years greater-than-or-equal 1800 before 1900"""
    x =  -Decimal('0.000009')
    x += +Decimal('0.003844')*c
    x += +Decimal('0.083563')*c**2
    x += +Decimal('0.865736')*c**3
    x += +Decimal('4.867575')*c**4
    x += +Decimal('15.845535')*c**5 
    x += +Decimal('31.332267')*c**6
    x += +Decimal('38.291999')*c**7
    x += +Decimal('28.316289')*c**8
    x += +Decimal('11.636204')*c**9
    x += +Decimal('2.043794')*c**10
    return x

def _eph_y_1700(year : Decimal) -> Decimal:
    return Decimal(year-1700) 
def _eph_c_1700(year : Decimal) -> Decimal:
    """Ephemeris correction for years greater-than-or-equal 1700 before 1800"""
    y = _eph_y_1700(year)
    x =   Decimal('8.118780842') -Decimal('0.005092142')*y +Decimal('0.003336121')*y**2  -Decimal('0.0000266484')*y**3
    return x / Decimal(86400)

def _eph_y_1600(year : Decimal) -> Decimal:
    return Decimal(year-1600)  
def _eph_c_1600(year : Decimal) -> Decimal:
    """Ephemeris correction for years greater-than-or-equal 1600 before 1700"""
    y = _eph_y_1600(year)
    x =  120 -Decimal('0.9808')*y  -Decimal('0.01532')*y**2 +Decimal('0.000140272128')*y**3
    return x / Decimal(86400)

def _eph_y_1000(year : Decimal) -> Decimal:
    return Decimal(year-1000) / 100  
def _eph_c_500(year : Decimal) -> Decimal:
    """Ephemeris correction for years greater-than-or-equal 500 before 1600"""
    y = _eph_y_1000(year)
    x =  +Decimal('1574.2')
    x += -Decimal('556.01')*y
    x += +Decimal('71.23472')*y**2
    x += +Decimal('0.319781')*y**3
    x += -Decimal('0.8503463')*y**4 
    x += -Decimal('0.005050998')*y**5
    x += +Decimal('0.0083572073')*y**6
    return x / Decimal(86400)

def _eph_y_0(year : Decimal) -> Decimal:
    return Decimal(year) / 100  
def _eph_c_0(year : Decimal) -> Decimal:
    """Ephemeris correction for years greater-than -500 before 500"""
    y = _eph_y_0(year)
    x =   Decimal('10583.6')
    x += -Decimal('1014.41')*y
    x += +Decimal('33.78311')*y**2
    x += -Decimal('5.952053')*y**3 
    x += -Decimal('0.1798452')*y**4 
    x += +Decimal('0.022174192')*y**5
    x += +Decimal('0.0090316521')*y**6
    return x / Decimal(86400)

def _eph_y_1820(year : Decimal) -> Decimal:
    return Decimal(year - 1820) / 100
def _eph_c_otherwise(year : Decimal) -> Decimal:
    """Ephemeris correction for years less-then-or-equal -500 after 2150"""
    return (-20 + 32 * _eph_y_1820(year) ** 2 ) / Decimal(86400)


# Universal Time and Dynamical Time
# p 212 (14.16) t is R.D. moment measured in U.T.
def dynamical_from_universal(t_utc : Decimal) -> Decimal:
    delta = ephemeris_correction(t_utc)
    return t_utc + delta
# p 212 (14.17)
def universal_from_dynamical(t_d : Decimal) -> Decimal:
    delta = ephemeris_correction(t_d)  # Approximation
    return t_d - delta

# p 212 (14.18) Julian centuries from R.D. moment
def julian_centuries(t_utc: Decimal) -> Decimal:
    """Calculate Julian centuries from R.D. moment"""
    t_dyn = dynamical_from_universal(t_utc)
    t_dyn_adj = t_dyn - _j2000()  # Adjust to gregorian 2000-01-01 12:00 origin
    return t_dyn_adj / Decimal(36525)
# p 212 (14.19)
def _j2000() -> Decimal:
    return gregorian_new_year(2000) + Decimal('0.5')  # 12 noon on January 1, 2000 in R.D. moment == 731582.5

# copilot
def rd_to_jd(t_rd : Decimal) -> Decimal:
    """Convert R.D. moment to Julian Day"""
    return t_rd + Decimal('1_721_424.5')

def jd_to_rd(t_jd : Decimal) -> Decimal:
    """Convert Julian Day to R.D. moment"""
    return t_jd - Decimal('1_721_424.5')

def jd_to_julian_centuries(t_jd : Decimal) -> Decimal:
    """Convert Julian Day to Julian centuries since J2000.0"""
    return (t_jd - Decimal('2451545.0')) / Decimal('36525')

def rd_to_julian_centuries(t_rd : Decimal) -> Decimal:
    """Convert R.D. moment to Julian centuries since J2000.0"""
    t_jd = rd_to_jd(t_rd)
    return jd_to_julian_centuries(t_jd)

# Equation of time
# p 215 (14.20) Equation of time
# Calculates the correction in fraction of day
def equation_of_time(rd_moment: Decimal) -> Decimal:
    j_centuries = rd_to_julian_centuries(rd_moment)
    _lambda = Decimal('280.46645') + Decimal('36000.76983')*j_centuries + Decimal('0.0003032')*j_centuries**2
    anomaly = Decimal('357.52910') + Decimal('35999.05030')*j_centuries - Decimal('0.0001559')*j_centuries**2 - Decimal('0.00000048')*j_centuries**3
    eccentricity = Decimal('0.016708617') - Decimal('0.000042037')*j_centuries - Decimal('0.0000001236')*j_centuries**2
    epsilon = _obliquity(j_centuries)
    y = tan(DEG2RAD * epsilon / Decimal(2))**2
    equation =    y * sin(DEG2RAD * Decimal('2') * _lambda)
    equation +=  -Decimal('2') * eccentricity * sin(DEG2RAD * anomaly)
    equation +=   Decimal('4') * eccentricity * y * sin(DEG2RAD * anomaly) * cos(DEG2RAD * Decimal('2') * _lambda)
    equation +=  -Decimal('0.5') * y**2 * sin(DEG2RAD * Decimal('4') * _lambda)
    equation +=  -Decimal('1.25') * eccentricity**2 * sin(DEG2RAD * Decimal('2') * anomaly)
    equation =   Decimal(equation / (Decimal(2) * PI))
    #from .UnivDecimalLibrary import abs as abs_decimal
    return sign(equation) * min(abs(equation), Decimal('0.5'))   # 12 hours

# p 220 (14.28) mean obliquity of the ecliptic
def _obliquity(j_centuries: Decimal) -> Decimal:
    epsilon_0  = +Decimal('23') + (Decimal('26')/Decimal('60')) + (Decimal('21.448')/Decimal('3600'))
    epsilon_0 += -Decimal('46.8150')/Decimal('3600')*j_centuries
    epsilon_0 += -Decimal('0.00059')/Decimal('3600')*j_centuries**2
    epsilon_0 += +Decimal('0.001813')/Decimal('3600')*j_centuries**3
    return epsilon_0

# p 221 (14.31-32)
def mean_tropical_year() -> Decimal:
    """Mean tropical year in days"""
    return Decimal('365.242189')  # 365 days, 5 hours, 48 minutes, 45.1296 seconds
def mean_sidereal_year() -> Decimal:
    """Mean sidereal year in days"""
    return Decimal('365.25636')  # 365 days, 6 hours, 9 minutes, 9.504 seconds

# p 223 (14.33)
def solar_longitude(rd_moment: Decimal) -> Decimal:
    """Calculate the solar longitude in degrees from R.D. moment"""
    j_centuries = rd_to_julian_centuries(rd_moment)
    _lambda = Decimal('282.7771834') + Decimal('36000.76953744')*j_centuries
    _sum = Decimal('0')
    for x_, y_, z_ in Table_14_1:
        _sum += x_ * sin(DEG2RAD * ( y_ + z_ * j_centuries))
    _lambda += _sum * Decimal('0.000005729577951308232')
    _aberration = aberration(j_centuries)
    _nutation = nutation(j_centuries)
    result = (_lambda + _aberration + _nutation) 
    return mod(result, Decimal(360))

# p 223 (14.34)
def nutation(j_centuries: Decimal) -> Decimal:
    """Calculate the nutation in longitude in degrees from julian centuries"""
    A = Decimal('124.90') - Decimal('1934.134') * j_centuries + Decimal('0.002063') * j_centuries**2
    B = Decimal('201.11') + Decimal('72001.5377') * j_centuries + Decimal('0.00057') * j_centuries**2
    return - Decimal('0.004778') * sin(DEG2RAD * A) - Decimal('0.0003667') * sin(DEG2RAD * B)

# p 223 (14.35)
def aberration(j_centuries: Decimal) -> Decimal:
    """Calculate the aberration in longitude in degrees from julian centuries"""
    L = Decimal('0.0000974') * cos(DEG2RAD * (Decimal('177.63') + Decimal('35999.01848') * j_centuries)) - Decimal('0.005575')
    return L

# p 224 Table 14.1
Table_14_1 = [
    (403406, Decimal('270.54861'), Decimal('0.9287892')), 
    (195207, Decimal('340.19128'), Decimal('35999.1376958')), 
    (119433, Decimal('63.91854'),  Decimal('35999.4089666')),
    (112392, Decimal('331.26220'), Decimal('35998.7287385')), 
    (  3891, Decimal('317.843'),   Decimal('71998.20261')), 
    (  2819, Decimal('86.631'),    Decimal('71998.4403')), 
    (  1721, Decimal('240.052'),   Decimal('36000.35726')), 
    (   660, Decimal('310.26'),    Decimal('71997.4812')), 
    (   350, Decimal('247.23'),    Decimal('32964.4678')), 
    (   334, Decimal('260.87'),    Decimal('-19.4410')), 
    (   314, Decimal('297.82'),    Decimal('445267.1117')),
    (   268, Decimal('343.14'),    Decimal('45036.8840')), 
    (   242, Decimal('166.79'),    Decimal('3.1008')), 
    (   234, Decimal('81.53'),     Decimal('22518.4434')),
    (   158, Decimal('3.50'),      Decimal('-19.9739')), 
    (   132, Decimal('132.75'),    Decimal('65928.9345')), 
    (   129, Decimal('182.95'),    Decimal('9038.0293')), 
    
    (   114, Decimal('162.03'),    Decimal('3034.7684')), 
    (    99, Decimal('29.8'),      Decimal('33718.148')), 
    (    93, Decimal('266.4'),     Decimal('3034.448')), 
    (    86, Decimal('249.2'),     Decimal('-2280.773')), 
    (    78, Decimal('157.6'),     Decimal('29929.992')), 
    (    72, Decimal('257.8'),     Decimal('31556.493')), 
    (    68, Decimal('185.1'),     Decimal('149.588')), 
    (    64, Decimal('69.9'),      Decimal('9037.750')),
    
    (    46, Decimal('8'),         Decimal('107997.405')),
    (    38, Decimal('197.1'),     Decimal('-4444.176')),
    (    37, Decimal('250.4'),     Decimal('151.771')),
    (    32, Decimal('65.3'),      Decimal('67555.316')),
    (    29, Decimal('162.7'),     Decimal('31556.080')),
    (    28, Decimal('341.5'),     Decimal('-4561.540')),
    (    27, Decimal('291.6'),     Decimal('107996.706')),
    (    27, Decimal('98.5'),      Decimal('1221.655')),
    (    25, Decimal('146.7'),     Decimal('62894.167')),
    (    24, Decimal('110'),       Decimal('31437.369')),
    (    21, Decimal('5.2'),       Decimal('14578.298')),
    (    21, Decimal('342.6'),     Decimal('-31931.757')),
    (    20, Decimal('230.9'),     Decimal('34777.243')),
    
    (    18, Decimal('256.1'),     Decimal('1221.999')),
    (    17, Decimal('45.3'),      Decimal('62894.511')),
    (    14, Decimal('242.9'),     Decimal('-4442.039')),
    (    13, Decimal('115.2'),     Decimal('107997.909')),
    (    13, Decimal('151.8'),     Decimal('119.066')),
    (    13, Decimal('285.3'),     Decimal('16859.071')),
    (    12, Decimal('53.3'),      Decimal('-4.578')),
    (    10, Decimal('126.6'),     Decimal('26895.292')),
    (    10, Decimal('205.7'),     Decimal('-39.127')),
    (    10, Decimal('85.9'),      Decimal('12297.536')),
    (    10, Decimal('146.1'),     Decimal('90073.778'))
    ]

#p 83 (3.18-21)  relocated from Chapter 3
def spring()-> Decimal: return 0
def summer()-> Decimal: return 90
def autumn()-> Decimal: return 180
def winter()-> Decimal: return 270

# p224 (14.36) mean synodic month
def circular_distance(to_angle : Decimal, from_angle : Decimal) -> Tuple[Decimal,str]:
    """Calculate the circular distance between two angles in degrees"""
    diff = mod(to_angle - from_angle, Decimal(360))
    if diff == 0:
        return diff, "same"
    elif diff <= 180:
        return diff, "clockwise"
    else:
        return diff, "counterclockwise"

def solar_longitude_after(_lambda, t: Decimal) -> Decimal:
    rate = mean_tropical_year() / 360
    diff, _ = circular_distance(_lambda, solar_longitude(t))
    t_delta =  rate * diff
    tau = int(t + t_delta)
    lower_bound = max(t, tau-5)
    upper_bound = tau + 5
    x = lower_bound
    delta = Decimal(1)
    direction = 'clockwise'
    switch = 2
    while x < upper_bound:
        sl = solar_longitude(x)
        diff, new_direction = circular_distance(_lambda, sl)
        #if first_after and new_direction != direction:
        #    return x
        if new_direction=='same' or (switch<=0 and direction == 'clockwise' and direction != new_direction): # and abs(diff) < abs(delta/Decimal(2))):
            return x
        if direction != new_direction:
            delta /= -10
            direction = new_direction
            x += delta
            switch -= 1
        else:
            x += delta

    return None

# p 224 (14.37)
def season_in_gregorian(season, g_year):
    return solar_longitude_after(season, gregorian_new_year(g_year))

# p 226 (14.42)
def estimate_prior_solar_longitude(_lambda, t: Decimal) -> Decimal:
    rate = mean_tropical_year() / 360
    diff, _ = circular_distance(solar_longitude(t), _lambda)
    tau = t - rate * diff
    delta, _ = circular_distance(solar_longitude(tau), _lambda)
    delta = mod_interval(delta, -180, 180)
    return min(t, tau - rate*delta)

# p 227 (14.44)
def mean_synodic_month() -> Decimal:
    """Mean synodic month in days"""
    return Decimal('29.530588861')  # 29 days, 12 hours, 44 minutes

# p 231 Table 14.3
Table_14_3 = [
    (Decimal('-0.40720'), 0,  0, 1,  0), 
    (Decimal('0.17241'),  1,  1, 0,  0), 
    (Decimal('0.01608'),  0,  0, 2,  0), 
    (Decimal('0.01039'),  0,  0, 0,  2), 
    (Decimal('0.00739'),  1, -1, 1,  0), 
    (Decimal('-0.00514'), 1,  1, 1,  0), 
    (Decimal('0.00208'),  2,  2, 0,  0), 
    (Decimal('-0.00111'), 0,  0, 1, -2), 
    (Decimal('-0.00057'), 0,  0, 1,  2), 
    (Decimal('0.00056'),  1,  1, 2,  0), 
    (Decimal('-0.00042'), 0,  0, 3,  0), 
    (Decimal('0.00042'),  1,  1, 0,  2), 
    (Decimal('0.00038'),  1,  1, 0, -2),
    (Decimal('-0.00024'), 1, -1, 2,  0),
    (Decimal('-0.00007'), 0,  2, 1,  0),
    (Decimal('0.00004'),  0,  0, 2, -2),
    (Decimal('0.00004'),  0,  3, 0,  0),
    (Decimal('0.00003'),  0,  1, 1, -2),
    (Decimal('0.00003'),  0,  0, 2,  2),
    (Decimal('-0.00003'), 0,  1, 1,  2),
    (Decimal('0.00003'),  0, -1, 1,  2),    
    (Decimal('-0.00002'), 0, -1, 1, -2),
    (Decimal('-0.00002'), 0,  1, 3,  0),
    (Decimal('0.00002'),  0,  0, 4,  0)
    ]
# p 231 Table 14.4
Table_14_4 = [
    (Decimal('251.88'), Decimal('0.016321'),  Decimal('0.000165')), 
    (Decimal('251.83'), Decimal('26.651886'), Decimal('0.000164')), 
    (Decimal('349.42'), Decimal('36.412478'), Decimal('0.000126')), 
    (Decimal('84.66'),  Decimal('18.206239'), Decimal('0.000110')), 
    (Decimal('141.74'), Decimal('53.303771'), Decimal('0.000062')), 
    (Decimal('207.14'), Decimal('2.453732'),  Decimal('0.000060')),
    (Decimal('154.84'), Decimal('7.306860'),  Decimal('0.000056')),
    (Decimal('34.52'),  Decimal('27.261239'), Decimal('0.000047')),                                            
    (Decimal('207.19'), Decimal('0.121824'),  Decimal('0.000042')),                                            
    (Decimal('291.34'), Decimal('1.844379'),  Decimal('0.000040')),                                            
    (Decimal('161.72'), Decimal('24.198154'), Decimal('0.000037')),                                   
    (Decimal('239.56'), Decimal('25.513099'), Decimal('0.000035')),                                            
    (Decimal('331.55'), Decimal('3.592518'),  Decimal('0.000023'))
    ]

# p 229 (14.45) mean synodic month
def nth_new_moon(n : Decimal) -> Decimal:
    n0 = 24724
    k = n-n0
    c = k / Decimal('1236.85')
    approx = _j2000() 
    approx += Decimal('5.09766')
    approx += mean_synodic_month() * Decimal('1236.85')*c
    approx += Decimal('0.00015437')*c**2
    approx += -Decimal('0.000000150')*c**3
    approx += Decimal('0.00000000073')*c**4
    E = 1
    E += -Decimal('0.002516')*c
    E += -Decimal('0.0000074')*c**2
    solar_anomaly = Decimal('2.5534')
    solar_anomaly += Decimal('1236.85')*Decimal('29.10535670')*c
    solar_anomaly += -Decimal('0.0000014')*c**2
    solar_anomaly += -Decimal('0.00000011')*c**3
    lunar_anomaly = Decimal('201.5643')
    lunar_anomaly += Decimal('385.81693528')*Decimal('1236.85')*c
    lunar_anomaly += Decimal('0.0107582')*c**2
    lunar_anomaly += Decimal('0.00001238')*c**3
    lunar_anomaly += -Decimal('0.000000058')*c**4
    moon_argument = Decimal('160.7108')
    moon_argument += Decimal('390.67050284')*Decimal('1236.85')*c
    moon_argument += -Decimal('0.0016118')*c**2
    moon_argument += -Decimal('0.00000227')*c**3
    moon_argument += Decimal('0.000000011')*c**4
    sigma = Decimal('124.7746')
    sigma += -Decimal('1.56375588')*Decimal('1236.85')*c
    sigma += Decimal('0.0020672')*c**2
    sigma += Decimal('0.00000215')*c**3
    correction = -Decimal('0.00017')*sin(DEG2RAD*sigma)
    for v_, w_, x_, y_, z_ in Table_14_3:
        correction += v_ * E**w_ * sin(DEG2RAD * (x_ * solar_anomaly + y_ * lunar_anomaly + z_ * moon_argument))
    extra =  Decimal('0.000325')*sin(Decimal(299.77)+Decimal('132.8475848')*c)
    extra += -Decimal('0.009173')*c**2
    additional = 0
    for i_, j_, l_ in Table_14_4:
        additional += l_*sin(DEG2RAD*(i_+j_*k))
    return universal_from_dynamical(approx + correction + extra + additional)
    
# p 227 (14.44)
def mean_synodic_month() -> Decimal:
    """Calculate the mean synodic month in days"""
    return Decimal('29.530588861')  # Mean synodic month in days
    
# p 230 (14.46)
def new_moon_before(t : Decimal) -> Decimal:
    t0 = nth_new_moon(0)
    psi = lunar_phase(t)
    n = round_((t - t0)/mean_synodic_month() - psi / 360)
    n_x = MAX(n-1, lambda k: nth_new_moon(k) < t)
    x = nth_new_moon(n_x)
    return x

# p 230 (14.47)
def new_moon_at_or_after(t : Decimal) -> Decimal:
    t0 = nth_new_moon(0)
    psi = lunar_phase(t)
    n = round_((t - t0)/mean_synodic_month() - psi / 360)
    x = nth_new_moon(MIN(n, lambda k: nth_new_moon(k) >= t))
    return x
    
# p232 (14.48)
def lunar_longitude(t : Decimal) -> Decimal:
    """Calculate the lunar longitude at time t in degrees"""
    c = julian_centuries(t)
    L_p = mean_lunar_longitude(c)
    D = lunar_elongation(c)
    M = solar_anomaly(c)
    M_p = lunar_anomaly(c)
    F = moon_node(c)
    E = Decimal('1') + Decimal('0.00251')*c - Decimal('0.0000074')*c**2
    correction = 0
    for v_, w_, x_, y_, z_ in Table_14_5:
        correction += v_ * E**abs(x_) * sin(DEG2RAD * (w_*D + x_ * M + y_ * M_p + z_ * F))
    venus = Decimal(3958) * sin(DEG2RAD*Decimal('119.75') + c*Decimal('131.849')) / 1_000_000  
    jupiter = Decimal(318) * sin(DEG2RAD*Decimal('53.09') + c*Decimal('479264.29')) / 1_000_000
    flat_earth = Decimal(1962) * sin(DEG2RAD*(L_p - F)) / 1_000_000
    return  mod(L_p + correction + venus + jupiter + flat_earth, Decimal(360))

# 233 Table 14.5
Table_14_5 = [
    (6288774, 0, 0,  1,  0), 
    (1274027, 2, 0, -1,  0), 
    ( 658314, 2, 0,  0,  0), 
    ( 213618, 0, 0,  2,  0),
    (-185116, 0, 1,  0,  0), 
    (-114332, 0, 0,  0,  2), 
    (  58793, 2, 0, -2,  0), 
    (  57066, 2,-1, -1,  0), 
    (  53322, 2, 0,  1,  0), 
    (  45758, 2,-1,  0,  0), 
    ( -40923, 0, 1, -1,  0), 
    ( -34720, 1, 0,  0,  0), 
    ( -30383, 0, 1,  1,  0), 
    (  15327, 2, 0,  0, -2), 
    ( -12528, 0, 0,  1,  2), 
    (  10980, 0, 0,  1, -2), 
    (  10675, 4, 0, -1,  0), 
    (  10034, 0, 0,  3,  0), 
    (   8548, 4, 0, -2,  0), 
    (  -7888, 2, 1, -1,  0),
    (  -6766, 2, 1,  0,  0), 
    (  -5163, 1, 0, -1,  0), 
    (   4987, 1, 1,  0,  0), 
    (   4036, 2,-1,  1,  0), 
    (   3994, 2, 0,  2,  0), 
    (   3861, 4, 0,  0,  0), 
    (   3665, 2, 0, -3,  0),
    (  -2689, 0, 1, -2,  0), 
    (  -2602, 2, 0, -1,  2), 
    (   2390, 2,-1, -2,  0),
    (  -2348, 1, 0,  1,  0),
    (   2236, 2,-2,  0,  0),
    (  -2120, 0, 1,  2,  0),
    (  -2069, 0, 2,  0,  0),
    (   2048, 2,-2, -1,  0),
    (  -1773, 2, 0,  1, -2),
    (  -1595, 2, 0,  0,  2),
    (   1215, 4,-1, -1,  0),
    (  -1110, 0, 0,  2,  2),
    (   -892, 3, 0, -1,  0),
    (   -810, 2, 1,  1,  0),
    (    759, 4,-1, -2,  0),
    (   -713, 0, 2, -1,  0),
    (   -700, 2, 2, -1,  0),
    (    691, 2, 1, -2,  0),
    (    596, 2,-1,  0, -2),
    (    549, 4, 0,  1,  0),
    (    537, 0, 0,  4,  0),
    (    520, 4,-1,  0,  0),
    (   -487, 1, 0, -2,  0),
    (   -399, 2, 1,  0, -2),
    (   -381, 0, 0,  2, -2),
    (    351, 1, 1,  1,  0),
    (   -340, 3, 0, -2,  0),
    (    330, 4, 0, -3,  0),
    (    327, 2,-1,  2,  0),
    (   -323, 0, 2,  1,  0),
    (    299, 1, 1, -1,  0),
    (    294, 2, 0,  3,  0)
    ]

# 233 (14.49)
def mean_lunar_longitude(c : Decimal) -> Decimal:
    """Calculate the mean lunar longitude at time c in degrees"""
    L_0 = Decimal('218.3164477') + Decimal('481267.88123421')*c - Decimal('0.0015786')*c**2 + (1 / Decimal(538_841))*c**3 -(1/Decimal(65_194_00))*c**4
    return mod(L_0, Decimal(360))

# p 234 (14.50)
def lunar_elongation(c : Decimal) -> Decimal:
    L_0 = Decimal('297.8501921') + Decimal('445267.1114034')*c - Decimal('0.0018819')*c**2 + (1 / Decimal(545_868))*c**3 -(1/Decimal(113_065_000))*c**4
    return mod(L_0,  Decimal(360))

# p 234 (14.51)
def solar_anomaly(c : Decimal) -> Decimal:
    M = Decimal('357.5291092') + Decimal('35999.0502909')*c - Decimal('0.0001536')*c**2 + (1 / Decimal(24_490_000))*c**3
    return mod(M, Decimal(360))

# p 234 (14.52)
def lunar_anomaly(c : Decimal) -> Decimal:
    M_p = Decimal('134.9633964') + Decimal('477198.8675055')*c + Decimal('0.0087414')*c**2 + (1 / Decimal(69_699))*c**3 -(1/Decimal(14_712_000))*c**4
    return mod(M_p, Decimal(360))

# p 234 (14.53)
def moon_node(c : Decimal) -> Decimal:
    F = Decimal('93.2720950') + Decimal('483202.0175233')*c - Decimal('0.0036539')*c**2 - (1 / Decimal(3_526_000))*c**3 +(1/Decimal(863_310_000))*c**4
    return mod(F , Decimal(360))

# p 235 (14.56)
def lunar_phase(t : Decimal) -> Decimal:
    phi = mod(lunar_longitude(t) - solar_longitude(t), Decimal(360))
    t0 = nth_new_moon(0)
    n = round_( (t - t0) / mean_synodic_month())
    phi_p = Decimal(360) * mod((t - nth_new_moon(n))/mean_synodic_month() , 1 )
    if abs(phi - phi_p) > Decimal(180):
        return phi_p
    else:
        return phi