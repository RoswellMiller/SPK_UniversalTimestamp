import sys
import json
from typing import Tuple
from decimal import Decimal

from .UnivDecimalLibrary import *
from .CC01_Calendar_Basics import *
from .CC02_Gregorian import gregorian_year_from_rd
from .CC14_Time_and_Astronomy import *

# with open('SPK_UniversalTimestamp/CC19_Table_19_1a.json', 'r', encoding='utf-8') as f:
#     Table_19_1 = json.load(f)
    
Table_19_1 = [
    {
        "month": {
            "index": 12,
            "leap": True
        },
        "pinyin": "Lìchūn",
        "hanzi": "立春",
        "japanese": "Risshun",
        "english": "Beginning of Spring",
        "solar_longitude": 315,
        "approximate_starting_date": "February 4"
    },
    {
        "month": {
            "index": 1,
            "leap": False
        },
        "pinyin": "Yǔshuǐ",
        "hanzi": "雨水",
        "japanese": "Usui",
        "english": "Rain Water",
        "solar_longitude": 330,
        "approximate_starting_date": "February 19"
    },
    {
        "month": {
            "index": 1,
            "leap": True
        },
        "pinyin": "Jīngzhé",
        "hanzi": "惊蛰",
        "japanese": "Keichitsu",
        "english": "Awakening of Insects",
        "solar_longitude": 345,
        "approximate_starting_date": "March 6"
    },
    {
        "month": {
            "index": 2,
            "leap": False
        },
        "pinyin": "Chūnfēn",
        "hanzi": "春分",
        "japanese": "Shunbun",
        "english": "Spring Equinox",
        "solar_longitude": 0,
        "approximate_starting_date": "March 21"
    },
    {
        "month": {
            "index": 2,
            "leap": True
        },
        "pinyin": "Qīngmíng",
        "hanzi": "清明",
        "japanese": "Seimei",
        "english": "Pure Brightness",
        "solar_longitude": 15,
        "approximate_starting_date": "April 5"
    },
    {
        "month": {
            "index": 3,
            "leap": False
        },
        "pinyin": "Gǔyǔ",
        "hanzi": "谷雨",
        "japanese": "Kokuu",
        "english": "Grain Rain",
        "solar_longitude": 30,
        "approximate_starting_date": "April 20"
    },
    {
        "month": {
            "index": 3,
            "leap": True
        },
        "pinyin": "Lìxià",
        "hanzi": "立夏",
        "japanese": "Rikka",
        "english": "Beginning of Summer",
        "solar_longitude": 45,
        "approximate_starting_date": "May 6"
    },
    {
        "month": {
            "index": 4,
            "leap": False
        },
        "pinyin": "Xiǎomǎn",
        "hanzi": "小满",
        "japanese": "Shōman",
        "english": "Grain Full",
        "solar_longitude": 60,
        "approximate_starting_date": "May 21"
    },
    {
        "month": {
            "index": 4,
            "leap": True
        },
        "pinyin": "Mángzhòng",
        "hanzi": "芒种",
        "japanese": "Bōshu",
        "english": "Grain in Ear",
        "solar_longitude": 75,
        "approximate_starting_date": "June 6"
    },
    {
        "month": {
            "index": 5,
            "leap": False
        },
        "pinyin": "Xiàzhì",
        "hanzi": "夏至",
        "japanese": "Geshi",
        "english": "Summer Solstice",
        "solar_longitude": 90,
        "approximate_starting_date": "June 21"
    },
    {
        "month": {
            "index": 5,
            "leap": True
        },
        "pinyin": "Xiǎoshǔ",
        "hanzi": "小暑",
        "japanese": "Shosho",
        "english": "Slight Heat",
        "solar_longitude": 105,
        "approximate_starting_date": "July 7"
    },
    {
        "month": {
            "index": 6,
            "leap": False
        },
        "pinyin": "Dàshǔ",
        "hanzi": "大暑",
        "japanese": "Taisho",
        "english": "Great Heat",
        "solar_longitude": 120,
        "approximate_starting_date": "July 23"
    },
    {
        "month": {
            "index": 6,
            "leap": True
        },
        "pinyin": "Lìqiū",
        "hanzi": "立秋",
        "japanese": "Risshū",
        "english": "Beginning of Autumn",
        "solar_longitude": 135,
        "approximate_starting_date": "August 8"
    },
    {
        "month": {
            "index": 7,
            "leap": False
        },
        "pinyin": "Chǔshǔ",
        "hanzi": "处暑",
        "japanese": "Shosho",
        "english": "Limit of Heat",
        "solar_longitude": 150,
        "approximate_starting_date": "August 23"
    },
    {
        "month": {
            "index": 7,
            "leap": True
        },
        "pinyin": "Báilù",
        "hanzi": "白露",
        "japanese": "Hakuro",
        "english": "White Dew",
        "solar_longitude": 165,
        "approximate_starting_date": "September 8"
    },
    {
        "month": {
            "index": 8,
            "leap": False
        },
        "pinyin": "Qiūfēn",
        "hanzi": "秋分",
        "japanese": "Shūbun",
        "english": "Autumnal Equinox",
        "solar_longitude": 180,
        "approximate_starting_date": "September 23"
    },
    {
        "month": {
            "index": 8,
            "leap": True
        },
        "pinyin": "Hánlù",
        "hanzi": "寒露",
        "japanese": "Kanro",
        "english": "Cold Dew",
        "solar_longitude": 195,
        "approximate_starting_date": "October 8"
    },
    {
        "month": {
            "index": 9,
            "leap": False
        },
        "pinyin": "Shuāngjiàng",
        "hanzi": "霜降",
        "japanese": "Sōkō",
        "english": "Descent of Frost",
        "solar_longitude": 210,
        "approximate_starting_date": "October 24"
    },
    {
        "month": {
            "index": 9,
            "leap": True
        },
        "pinyin": "Lìdōng",
        "hanzi": "立冬",
        "japanese": "Rittō",
        "english": "Beginning of Winter",
        "solar_longitude": 225,
        "approximate_starting_date": "November 8"
    },
    {
        "month": {
            "index": 10,
            "leap": False
        },
        "pinyin": "Xiǎoxuě",
        "hanzi": "小雪",
        "japanese": "Shōsetsu",
        "english": "Slight Snow",
        "solar_longitude": 240,
        "approximate_starting_date": "November 22"
    },
    {
        "month": {
            "index": 10,
            "leap": True
        },
        "pinyin": "Dàxuě",
        "hanzi": "大雪",
        "japanese": "Taisetsu",
        "english": "Great Snow",
        "solar_longitude": 255,
        "approximate_starting_date": "December 7"
    },
    {
        "month": {
            "index": 11,
            "leap": False
        },
        "pinyin": "Dōngzhì",
        "hanzi": "冬至",
        "japanese": "Tōji",
        "english": "Winter Solstice",
        "solar_longitude": 270,
        "approximate_starting_date": "December 22"
    },
    {
        "month": {
            "index": 11,
            "leap": True
        },
        "pinyin": "Xiǎohán",
        "hanzi": "小寒",
        "japanese": "Shōkan",
        "english": "Slight Cold",
        "solar_longitude": 285,
        "approximate_starting_date": "January 6"
    },
    {
        "month": {
            "index": 12,
            "leap": False
        },
        "pinyin": "Dàhán",
        "hanzi": "大寒",
        "japanese": "Taikan",
        "english": "Great Cold",
        "solar_longitude": 300,
        "approximate_starting_date": "January 20"
    }
]    
Table_19_1_Dict = {}
for i, tu in enumerate(Table_19_1):
    if tu['month']['index'] not in Table_19_1_Dict:
        Table_19_1_Dict[tu['month']['index']] = {}
    Table_19_1_Dict[tu['month']['index']][tu['month']['leap']] = tu
    
# with open('SPK_UniversalTimestamp/CC19_Sexagesimal_Names.json', 'r', encoding='utf-8') as f:
#     Sexagesimal_Names = json.load(f)
Sexagesimal_Names = {
    "stem": [
        {"index": 1, "pinyin": "Jiˇa", "hanzi": "甲", "japanese": "Kō", "english": "First"},
        {"index": 2, "pinyin": "Yˇı", "hanzi": "乙", "japanese": "Otsu", "english": "Second"},
        {"index": 3, "pinyin": "Bˇıng", "hanzi": "丙", "japanese": "Hei", "english": "Third"},
        {"index": 4, "pinyin": "D¯ıng", "hanzi": "丁", "japanese": "Tei", "english": "Fourth"},
        {"index": 5, "pinyin": "Wù", "hanzi": "戊", "japanese": "Bo", "english": "Fifth"},
        {"index": 6, "pinyin": "Jˇı", "hanzi": "己", "japanese": "Ki", "english": "Sixth"},
        {"index": 7, "pinyin": "G¯eng", "hanzi": "庚", "japanese": "Kō", "english": "Seventh"},
        {"index": 8, "pinyin": "X¯ın", "hanzi": "辛", "japanese": "Shin", "english": "Eighth"},
        {"index": 9, "pinyin": "Rén", "hanzi": "壬", "japanese": "Jin", "english": "Ninth"},
        {"index":10, "pinyin": "Guˇı", "hanzi": "癸", "japanese": "Ki", "english": "Tenth"}
    ],
    "branch": [
        {"index": 1, "pinyin": "Z¯ı", "hanzi": "子", "japanese": "Shi", "english": "Rat"},
        {"index": 2, "pinyin": "Ch¯ou", "hanzi": "丑", "japanese": "Ushi", "english": "Ox"},
        {"index": 3, "pinyin": "Yín", "hanzi": "寅", "japanese": "Tora", "english": "Tiger"},
        {"index": 4, "pinyin": "Mˇao", "hanzi": "卯", "japanese": "U", "english": "Rabbit"},
        {"index": 5, "pinyin": "Chén", "hanzi": "辰", "japanese": "Tatsu", "english": "Dragon"},
        {"index": 6, "pinyin": "S¯ı", "hanzi": "巳", "japanese": "Mi", "english": "Snake"},
        {"index": 7, "pinyin": "W¯u", "hanzi": "午", "japanese": "Uma", "english": "Horse"},
        {"index": 8, "pinyin": "Wèi", "hanzi": "未", "japanese": "Hitsuji", "english": "Goat"},
        {"index": 9, "pinyin": "Sh¯en", "hanzi": "申", "japanese": "Saru", "english": "Monkey"},
        {"index": 10, "pinyin": "Yóu", 	"hanzi":	"酉",	"japanese":"Tori","english":"Rooster"},
        {"index": 11, "pinyin":"X¯u","hanzi":"戌","japanese":"Inu","english":"Dog"},
        {"index": 12, "pinyin":"Hài","hanzi":"亥","japanese":"I","english":"Pig"}
    ]
}

# page 306 (19.1)
def current_major_solar_term(date : Decimal) -> int:
    """ Calculate the index of the last major solar term on or before a given date

    Args:
        date (Decimal): _description_

    Returns:
        int: _description_
    """
    s = solar_longitude(universal_from_standard(date, chinese_location(date)))
    return mod_adj(2 + floor(s / Decimal(30)), 12)

# page 306 (19.2)
def chinese_location(date: Decimal) -> Decimal:
    """ The location, Beijing, used for Chinese calendar calculations
        year < 1929 uses Beijing lat,long, altitude with UT +7hr 45min 40sec = 1397/180
        otherwie    ........                        with UT +8hr = 120 meridian

    Args:
        date (Decimal): _description_

    Returns:
        Decimal: _description_
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
def minor_soloar_term_on_or_after(date: Decimal) -> Decimal:
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
    if round_((next_m11 - m12) / mean_synodic_month()) == 12 and (is_chinese_no_major_solar_term(m12) or is_chinese_no_major_solar_term(m13)):
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
def chinese_from_rd(date : Decimal) -> Tuple[int, int, int, bool, int]:
    """Convert R.D. to a Chinese date."""
    s1 = chinese_winter_solstice_on_or_before(date)
    s2 = chinese_winter_solstice_on_or_before(s1 + 370)
    m12 = chinese_new_moon_on_or_after(s1 + 1)
    next_m11 = chinese_new_moon_before(s2 + 1)
    m = chinese_new_moon_before(date + 1)
    
    leap_year = round_((next_m11 - m12) / mean_synodic_month()) == 12
    
    month = round_((m - m12) / mean_synodic_month())
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
def chinese_sexagesimal_tuple(n : int) -> Tuple[int,int]:
    """Return the sexagesimal name for the given index."""
    stem = mod_adj(n, 10)
    branch = mod_adj(n, 12)
    return stem, branch

# p 319 (19.19)
def chinese_name_difference(name1 : Tuple[int,int], name2 : Tuple[int,int]) -> int:
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
def chinese_day_tuple(date_rd : int) -> Tuple[int,int]:
    return chinese_sexagesimal_tuple(date_rd - chinese_day_epoch())

# p 321 (19.25)
def chinese_day_tuple_on_or_before(name : Tuple[int,int], date : int) -> Decimal:
    """Return the last date on or before the given date with the given sexagesimal name."""
    d = chinese_day_tuple(0)
    diff = chinese_name_difference(d, name)
    return mod_adj(diff, date - 60)