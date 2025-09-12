import sys
import json
from typing import Tuple
from decimal import Decimal

from .UnivDecimalLibrary import *
from .CC01_Calendar_Basics import *
from .CC02_Gregorian import gregorian_year_from_rd
from .CC14_Time_and_Astronomy import *

# Table_19_1 = [ 
#     #ndx.  Chinese                     Japanese    English               solar-longitude
#     #                                                                          starting-date, approximate
#     ( 1,  'Lìchun',      '立春',      'Risshun',  'Beginning of Spring', 315, 'February 4'),
#     ( 1,  'Yushuı',      '雨水',      'Usui',     'Rain Water',          330, 'February 19'),
#     ( 2,  'Jıngzhé',     '惊蛰',      'Keichitsu','Waking of Insects',   345, 'March 6'),
#     ( 2,  'Chunfen',     '春分',      'Shunbun',  'Spring Equinox',        0, 'March 21'),
#     ( 3,  'Qıngmíng',    '清明',      'Seimei',   'Pure Brightness',      15, 'April 5'),
#     ( 3,  'Guyu',        '谷雨',      'Kokuu',    'Grain Rain',           30, 'April 20'),
#     ( 4,  'Lìxià',       '立夏',      'Rikka',    'Beginning of Summer',  45, 'May 6'),
#     ( 4,  'Xiaomˇan',    '小满',      'Shoman',   'Grain Full',           60, 'May 21'),
#     ( 5,  'Mángzhòng',   '芒种',      'Boshu',    'Grain in Ear',         75, 'June 6'),
#     ( 5,  'Xiàzhì',      '夏至',      'Geshi',    'Summer Solstice',      90, 'June 21'),
#     ( 6,  'Xiaoshˇu',    '小暑',      'Shosho',   'Slight Heat',         105, 'July 7'),
#     ( 6,  'Dàshˇu',      '大暑',      'Taisho',   'Great Heat',          120, 'July 23'),
#     ( 7,  'Lìqi¯u',      '立秋',      'Rissh¯u',  'Beginning of Autumn', 135, 'August 8'),
#     ( 7,  'Chushˇu',     '处暑',      'Shosho',   'Limit of Heat',       150, 'August 23'),
#     ( 8,  'Báilù',       '白露',      'Hakuro',   'White Dew',           165, 'September 8'),
#     ( 8,  'Qiufen',      '秋分',      'Shubun',   'Autumnal Equinox',    180, 'September 23'),
#     ( 9,  'Hánlù',       '寒露',      'Kanro',    'Cold Dew',            195, 'October 8'),
#     ( 9,  'Shuangjiàng', '霜降',      'Soko',     'Descent of Frost',    210, 'October 24'),
#     ( 10, 'Lìdong',      '立冬',      'Ritto',    'Beginning of Winter', 225, 'November 8'),
#     ( 10, 'Xiaoxue',     '小雪',      'Shosetsu', 'Slight Snow',         240, 'November 22'),
#     ( 11, 'Dàxue',       '大雪',      'Taisetsu', 'Great Snow',          255, 'December 7'),
#     ( 11, 'Dongzhì',     '冬至',      'Toji',     'Winter Solstice',     270, 'December 22'),
#     ( 12, 'Xiaohán',     '小寒',      'Shokan',   'Slight Cold',         285, 'January 6'),
#     ( 12, 'Dàhán',       '大寒',      'Taikan',   'Great Cold',          300, 'January 20'),
# ]
with open('SPK_UniversalTimestamp/CC19_Table_19_1a.json', 'r', encoding='utf-8') as f:
    Table_19_1 = json.load(f)
Table_19_1_Dict = {}
for i, tu in enumerate(Table_19_1):
    if tu['month']['index'] not in Table_19_1_Dict:
        Table_19_1_Dict[tu['month']['index']] = {}
    Table_19_1_Dict[tu['month']['index']][tu['month']['leap']] = tu

# solar_term_columns = (
#     'index',
#     'chinese_name',
#     'english_name',
#     'traditional_alias',
#     ('solar_term_1_name', 'solar_term_1_pinyin', 'solar_term_1_longitude', 'solar_term_1_date'),
#     ('solar_term_2_name', 'solar_term_2_pinyin', 'solar_term_2_longitude', 'solar_term_2_date')
#     )

# solar_term_mapping = [
#     (1, "正月", "First Month", "Zhengyue",
#         ("立春", "lichun", 315, "Feb 4"),
#         ("雨水", "yushui", 330, "Feb 19")),
#     (2, "二月", "Second Month", "Eryue",
#         ("驚蟄", "jingzhe", 345, "Mar 6"),
#         ("春分", "chunfen", 0, "Mar 21")),
#     (3, "三月", "Third Month", "Sanyue",
#         ("清明", "qingming", 15, "Apr 5"),
#         ("穀雨", "guyu", 30, "Apr 20")),
#     (4, "四月", "Fourth Month", "Siyue",
#         ("立夏", "lixia", 45, "May 5"),
#         ("小滿", "xiaoman", 60, "May 21")),
#     (5, "五月", "Fifth Month", "Wuyue",
#         ("芒種", "mangzhong", 75, "Jun 6"),
#         ("夏至", "xiazhi", 90, "Jun 21")),
#     (6, "六月", "Sixth Month", "Liuyue",
#         ("小暑", "xiaoshu", 105, "Jul 7"),
#         ("大暑", "dashu", 120, "Jul 23")),
#     (7, "七月", "Seventh Month", "Qiyue",
#         ("立秋", "liqiu", 135, "Aug 7"),
#         ("處暑", "chushu", 150, "Aug 23")),
#     (8, "八月", "Eighth Month", "Bayue",
#         ("白露", "bailu", 165, "Sep 7"),
#         ("秋分", "qiufen", 180, "Sep 23")),
#     (9, "九月", "Ninth Month", "Jiuyue",
#         ("寒露", "hanlu", 195, "Oct 8"),
#         ("霜降", "shuangjiang", 210, "Oct 23")),
#     (10, "十月", "Tenth Month", "Shiyue",
#         ("立冬", "lidong", 225, "Nov 7"),
#         ("小雪", "xiaoxue", 240, "Nov 22")),
#     (11, "十一月", "Eleventh Month", "Shiyiyue",
#         ("大雪", "daxue", 255, "Dec 7"),
#         ("冬至", "dongzhi", 270, "Dec 21")),
#     (12, "臘月", "Twelfth Month", "Layue",
#         ("小寒", "xiaohan", 285, "Jan 5"),
#         ("大寒", "dahan", 300, "Jan 20"))
# ]
# # Copilot version of the Table 19.1 above
# solar_terms_2025 = [
#     {"month": 1,  "pinyin": "Lìchūn",      "hanzi": "立春", "japanese": "Risshun",   "english": "Beginning of Spring",  "longitude": 315, "date": "2025-02-03", "time": "22:10"},
#     {"month": 1,  "pinyin": "Yǔshuǐ",      "hanzi": "雨水", "japanese": "Usui",      "english": "Rain Water",           "longitude": 330, "date": "2025-02-18", "time": "18:07"},
#     {"month": 2,  "pinyin": "Jīngzhé",     "hanzi": "惊蛰", "japanese": "Keichitsu", "english": "Awakening of Insects", "longitude": 345, "date": "2025-03-05", "time": "16:04"},
#     {"month": 2,  "pinyin": "Chūnfēn",     "hanzi": "春分", "japanese": "Shunbun",   "english": "Spring Equinox",       "longitude": 0,   "date": "2025-03-20", "time": "16:57"},
#     {"month": 3,  "pinyin": "Qīngmíng",    "hanzi": "清明", "japanese": "Seimei",    "english": "Pure Brightness",      "longitude": 15,  "date": "2025-04-04", "time": "20:42"},
#     {"month": 3,  "pinyin": "Gǔyǔ",        "hanzi": "谷雨", "japanese": "Kokuu",     "english": "Grain Rain",           "longitude": 30,  "date": "2025-04-20", "time": "03:47"},
#     {"month": 4,  "pinyin": "Lìxià",       "hanzi": "立夏", "japanese": "Rikka",     "english": "Beginning of Summer",  "longitude": 45,  "date": "2025-05-05", "time": "13:48"},
#     {"month": 4,  "pinyin": "Xiǎomǎn",     "hanzi": "小满", "japanese": "Shōman",    "english": "Grain Full",           "longitude": 60,  "date": "2025-05-21", "time": "02:44"},
#     {"month": 5,  "pinyin": "Mángzhòng",   "hanzi": "芒种", "japanese": "Bōshu",     "english": "Grain in Ear",         "longitude": 75,  "date": "2025-06-05", "time": "17:47"},
#     {"month": 5,  "pinyin": "Xiàzhì",      "hanzi": "夏至", "japanese": "Geshi",     "english": "Summer Solstice",      "longitude": 90,  "date": "2025-06-21", "time": "10:33"},
#     {"month": 6,  "pinyin": "Xiǎoshǔ",     "hanzi": "小暑", "japanese": "Shosho",    "english": "Slight Heat",          "longitude": 105, "date": "2025-07-07", "time": "03:57"},
#     {"month": 6,  "pinyin": "Dàshǔ",       "hanzi": "大暑", "japanese": "Taisho",    "english": "Great Heat",           "longitude": 120, "date": "2025-07-22", "time": "21:23"},
#     {"month": 7,  "pinyin": "Lìqiū",       "hanzi": "立秋", "japanese": "Risshū",    "english": "Beginning of Autumn",  "longitude": 135, "date": "2025-08-07", "time": "13:46"},
#     {"month": 7,  "pinyin": "Chǔshǔ",      "hanzi": "处暑", "japanese": "Shosho",    "english": "Limit of Heat",        "longitude": 150, "date": "2025-08-23", "time": "04:31"},
#     {"month": 8,  "pinyin": "Báilù",       "hanzi": "白露", "japanese": "Hakuro",    "english": "White Dew",            "longitude": 165, "date": "2025-09-07", "time": "16:49"},
#     {"month": 8,  "pinyin": "Qiūfēn",      "hanzi": "秋分", "japanese": "Shūbun",    "english": "Autumnal Equinox",     "longitude": 180, "date": "2025-09-23", "time": "02:19"},
#     {"month": 9,  "pinyin": "Hánlù",       "hanzi": "寒露", "japanese": "Kanro",     "english": "Cold Dew",             "longitude": 195, "date": "2025-10-08", "time": "08:39"},
#     {"month": 9,  "pinyin": "Shuāngjiàng", "hanzi": "霜降", "japanese": "Sōkō",      "english": "Descent of Frost",     "longitude": 210, "date": "2025-10-23", "time": "11:51"},
#     {"month": 10, "pinyin": "Lìdōng",      "hanzi": "立冬", "japanese": "Rittō",     "english": "Beginning of Winter",  "longitude": 225, "date": "2025-11-07", "time": "12:03"},
#     {"month": 10, "pinyin": "Xiǎoxuě",     "hanzi": "小雪", "japanese": "Shōsetsu",  "english": "Slight Snow",          "longitude": 240, "date": "2025-11-22", "time": "09:36"},
#     {"month": 11, "pinyin": "Dàxuě",       "hanzi": "大雪", "japanese": "Taisetsu",  "english": "Great Snow",           "longitude": 255, "date": "2025-12-07", "time": "05:06"},
#     {"month": 11, "pinyin": "Dōngzhì",     "hanzi": "冬至", "japanese": "Tōji",      "english": "Winter Solstice",      "longitude": 270, "date": "2025-12-21", "time": "23:03"},
#     {"month": 12, "pinyin": "Xiǎohán",     "hanzi": "小寒", "japanese": "Shōkan",    "english": "Slight Cold",          "longitude": 285, "date": "2026-01-05", "time": "10:31"},
#     {"month": 12, "pinyin": "Dàhán",       "hanzi": "大寒", "japanese": "Taikan",    "english": "Great Cold",           "longitude": 300, "date": "2026-01-20", "time": "04:00"}
# ]   

    
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