from decimal import Decimal


# Table 1.2, p 17
Epoch_rd = {
    'julian-day-number' : Decimal(-1_721_424.5),    
    'hebrew' : -1_373_427,
    'mayan': -1_137_142,
    'hindu-kali-yuga' : -1_132_959,
    'chinese' : -963_099,
    'samaritan': -598_573,
    'egyptian': -272_787,
    'babylonian': -113_502,
    'tibetan': -46_410,
    'julian': -1,
    'gregorian': 1,         # Monday January 1, 1 Gregorian
    'ISO-8601': 1,
    'akan': 37,
    'ethiopic': 2_796,
    'coptic': 103_605,
    'armenian': 201_443,
    'persian': 226_896,
    'islamic': 227_015,
    'zoroastrian': 230_638,
    'french-revolutionary': 654_415,
    'baha-i': 673_222,
    'modified-julian-day-number': 678_576,
    'unix': 719_163
}

# Julian Day Number conversions
# p 18 (1.4)
def _moment_from_jd(jd: Decimal) -> Decimal:
    return (jd - Decimal(Epoch_rd['julian-day-number']))
# p 20 (1.13)
def rd_from_jd(jd: Decimal) -> int:
    return int(_moment_from_jd(jd))
# p 18 (1.5)
def _jd_from_moment(rd : int) -> Decimal:
    return rd + Decimal(Epoch_rd['julian-day-number'])
# p 20 (1.14)
def jd_from_rd(rd: int) -> Decimal:
    return _jd_from_moment(rd)

# Modified Julian Day Number conversions
# p 19 (1.7)
def rd_from_mjd(mjd : Decimal) -> Decimal:
    return mjd + Epoch_rd['modified-julian-day-number']
# p 19 (1.8)
def mjd_from_rd(rd : Decimal) -> Decimal:
    return rd - Epoch_rd['modified-julian-day-number']