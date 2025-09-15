import os


Table_19_1 = [ 
    #ndx.  Chinese                     Japanese    English               solar-longitude
    #                                                                          starting-date, approximate
    ( 1,  'Lìchun',      '立春',      'Risshun',  'Beginning of Spring', 315, 'February 4'),
    ( 1,  'Yushuı',      '雨水',      'Usui',     'Rain Water',          330, 'February 19'),
    ( 2,  'Jıngzhé',     '惊蛰',      'Keichitsu','Waking of Insects',   345, 'March 6'),
    ( 2,  'Chunfen',     '春分',      'Shunbun',  'Spring Equinox',        0, 'March 21'),
    ( 3,  'Qıngmíng',    '清明',      'Seimei',   'Pure Brightness',      15, 'April 5'),
    ( 3,  'Guyu',        '谷雨',      'Kokuu',    'Grain Rain',           30, 'April 20'),
    ( 4,  'Lìxià',       '立夏',      'Rikka',    'Beginning of Summer',  45, 'May 6'),
    ( 4,  'Xiaomˇan',    '小满',      'Shoman',   'Grain Full',           60, 'May 21'),
    ( 5,  'Mángzhòng',   '芒种',      'Boshu',    'Grain in Ear',         75, 'June 6'),
    ( 5,  'Xiàzhì',      '夏至',      'Geshi',    'Summer Solstice',      90, 'June 21'),
    ( 6,  'Xiaoshˇu',    '小暑',      'Shosho',   'Slight Heat',         105, 'July 7'),
    ( 6,  'Dàshˇu',      '大暑',      'Taisho',   'Great Heat',          120, 'July 23'),
    ( 7,  'Lìqi¯u',      '立秋',      'Rissh¯u',  'Beginning of Autumn', 135, 'August 8'),
    ( 7,  'Chushˇu',     '处暑',      'Shosho',   'Limit of Heat',       150, 'August 23'),
    ( 8,  'Báilù',       '白露',      'Hakuro',   'White Dew',           165, 'September 8'),
    ( 8,  'Qiufen',      '秋分',      'Shubun',   'Autumnal Equinox',    180, 'September 23'),
    ( 9,  'Hánlù',       '寒露',      'Kanro',    'Cold Dew',            195, 'October 8'),
    ( 9,  'Shuangjiàng', '霜降',      'Soko',     'Descent of Frost',    210, 'October 24'),
    ( 10, 'Lìdong',      '立冬',      'Ritto',    'Beginning of Winter', 225, 'November 8'),
    ( 10, 'Xiaoxue',     '小雪',      'Shosetsu', 'Slight Snow',         240, 'November 22'),
    ( 11, 'Dàxue',       '大雪',      'Taisetsu', 'Great Snow',          255, 'December 7'),
    ( 11, 'Dongzhì',     '冬至',      'Toji',     'Winter Solstice',     270, 'December 22'),
    ( 12, 'Xiaohán',     '小寒',      'Shokan',   'Slight Cold',         285, 'January 6'),
    ( 12, 'Dàhán',       '大寒',      'Taikan',   'Great Cold',          300, 'January 20'),
]
# Table_19_1_Dict = {}
# for i, tu in enumerate(Table_19_1):
#     if tu[0] not in Table_19_1_Dict:
#         Table_19_1_Dict[tu[0]] = {}
#     Table_19_1_Dict[tu[0]][(i % 2)==0] = tu

solar_term_columns = (
    'index',
    'chinese_name',
    'english_name',
    'traditional_alias',
    ('solar_term_1_name', 'solar_term_1_pinyin', 'solar_term_1_longitude', 'solar_term_1_date'),
    ('solar_term_2_name', 'solar_term_2_pinyin', 'solar_term_2_longitude', 'solar_term_2_date')
    )

solar_term_mapping = [
    (1, "正月", "First Month", "Zhengyue",
        ("立春", "lichun", 315, "Feb 4"),
        ("雨水", "yushui", 330, "Feb 19")),
    (2, "二月", "Second Month", "Eryue",
        ("驚蟄", "jingzhe", 345, "Mar 6"),
        ("春分", "chunfen", 0, "Mar 21")),
    (3, "三月", "Third Month", "Sanyue",
        ("清明", "qingming", 15, "Apr 5"),
        ("穀雨", "guyu", 30, "Apr 20")),
    (4, "四月", "Fourth Month", "Siyue",
        ("立夏", "lixia", 45, "May 5"),
        ("小滿", "xiaoman", 60, "May 21")),
    (5, "五月", "Fifth Month", "Wuyue",
        ("芒種", "mangzhong", 75, "Jun 6"),
        ("夏至", "xiazhi", 90, "Jun 21")),
    (6, "六月", "Sixth Month", "Liuyue",
        ("小暑", "xiaoshu", 105, "Jul 7"),
        ("大暑", "dashu", 120, "Jul 23")),
    (7, "七月", "Seventh Month", "Qiyue",
        ("立秋", "liqiu", 135, "Aug 7"),
        ("處暑", "chushu", 150, "Aug 23")),
    (8, "八月", "Eighth Month", "Bayue",
        ("白露", "bailu", 165, "Sep 7"),
        ("秋分", "qiufen", 180, "Sep 23")),
    (9, "九月", "Ninth Month", "Jiuyue",
        ("寒露", "hanlu", 195, "Oct 8"),
        ("霜降", "shuangjiang", 210, "Oct 23")),
    (10, "十月", "Tenth Month", "Shiyue",
        ("立冬", "lidong", 225, "Nov 7"),
        ("小雪", "xiaoxue", 240, "Nov 22")),
    (11, "十一月", "Eleventh Month", "Shiyiyue",
        ("大雪", "daxue", 255, "Dec 7"),
        ("冬至", "dongzhi", 270, "Dec 21")),
    (12, "臘月", "Twelfth Month", "Layue",
        ("小寒", "xiaohan", 285, "Jan 5"),
        ("大寒", "dahan", 300, "Jan 20"))
]
# Copilot version of the Table 19.1 above
solar_terms_2025 = [
    {"month": 1,  "pinyin": "Lìchūn",      "hanzi": "立春", "japanese": "Risshun",   "english": "Beginning of Spring",  "longitude": 315, "date": "2025-02-03", "time": "22:10"},
    {"month": 1,  "pinyin": "Yǔshuǐ",      "hanzi": "雨水", "japanese": "Usui",      "english": "Rain Water",           "longitude": 330, "date": "2025-02-18", "time": "18:07"},
    {"month": 2,  "pinyin": "Jīngzhé",     "hanzi": "惊蛰", "japanese": "Keichitsu", "english": "Awakening of Insects", "longitude": 345, "date": "2025-03-05", "time": "16:04"},
    {"month": 2,  "pinyin": "Chūnfēn",     "hanzi": "春分", "japanese": "Shunbun",   "english": "Spring Equinox",       "longitude": 0,   "date": "2025-03-20", "time": "16:57"},
    {"month": 3,  "pinyin": "Qīngmíng",    "hanzi": "清明", "japanese": "Seimei",    "english": "Pure Brightness",      "longitude": 15,  "date": "2025-04-04", "time": "20:42"},
    {"month": 3,  "pinyin": "Gǔyǔ",        "hanzi": "谷雨", "japanese": "Kokuu",     "english": "Grain Rain",           "longitude": 30,  "date": "2025-04-20", "time": "03:47"},
    {"month": 4,  "pinyin": "Lìxià",       "hanzi": "立夏", "japanese": "Rikka",     "english": "Beginning of Summer",  "longitude": 45,  "date": "2025-05-05", "time": "13:48"},
    {"month": 4,  "pinyin": "Xiǎomǎn",     "hanzi": "小满", "japanese": "Shōman",    "english": "Grain Full",           "longitude": 60,  "date": "2025-05-21", "time": "02:44"},
    {"month": 5,  "pinyin": "Mángzhòng",   "hanzi": "芒种", "japanese": "Bōshu",     "english": "Grain in Ear",         "longitude": 75,  "date": "2025-06-05", "time": "17:47"},
    {"month": 5,  "pinyin": "Xiàzhì",      "hanzi": "夏至", "japanese": "Geshi",     "english": "Summer Solstice",      "longitude": 90,  "date": "2025-06-21", "time": "10:33"},
    {"month": 6,  "pinyin": "Xiǎoshǔ",     "hanzi": "小暑", "japanese": "Shosho",    "english": "Slight Heat",          "longitude": 105, "date": "2025-07-07", "time": "03:57"},
    {"month": 6,  "pinyin": "Dàshǔ",       "hanzi": "大暑", "japanese": "Taisho",    "english": "Great Heat",           "longitude": 120, "date": "2025-07-22", "time": "21:23"},
    {"month": 7,  "pinyin": "Lìqiū",       "hanzi": "立秋", "japanese": "Risshū",    "english": "Beginning of Autumn",  "longitude": 135, "date": "2025-08-07", "time": "13:46"},
    {"month": 7,  "pinyin": "Chǔshǔ",      "hanzi": "处暑", "japanese": "Shosho",    "english": "Limit of Heat",        "longitude": 150, "date": "2025-08-23", "time": "04:31"},
    {"month": 8,  "pinyin": "Báilù",       "hanzi": "白露", "japanese": "Hakuro",    "english": "White Dew",            "longitude": 165, "date": "2025-09-07", "time": "16:49"},
    {"month": 8,  "pinyin": "Qiūfēn",      "hanzi": "秋分", "japanese": "Shūbun",    "english": "Autumnal Equinox",     "longitude": 180, "date": "2025-09-23", "time": "02:19"},
    {"month": 9,  "pinyin": "Hánlù",       "hanzi": "寒露", "japanese": "Kanro",     "english": "Cold Dew",             "longitude": 195, "date": "2025-10-08", "time": "08:39"},
    {"month": 9,  "pinyin": "Shuāngjiàng", "hanzi": "霜降", "japanese": "Sōkō",      "english": "Descent of Frost",     "longitude": 210, "date": "2025-10-23", "time": "11:51"},
    {"month": 10, "pinyin": "Lìdōng",      "hanzi": "立冬", "japanese": "Rittō",     "english": "Beginning of Winter",  "longitude": 225, "date": "2025-11-07", "time": "12:03"},
    {"month": 10, "pinyin": "Xiǎoxuě",     "hanzi": "小雪", "japanese": "Shōsetsu",  "english": "Slight Snow",          "longitude": 240, "date": "2025-11-22", "time": "09:36"},
    {"month": 11, "pinyin": "Dàxuě",       "hanzi": "大雪", "japanese": "Taisetsu",  "english": "Great Snow",           "longitude": 255, "date": "2025-12-07", "time": "05:06"},
    {"month": 11, "pinyin": "Dōngzhì",     "hanzi": "冬至", "japanese": "Tōji",      "english": "Winter Solstice",      "longitude": 270, "date": "2025-12-21", "time": "23:03"},
    {"month": 12, "pinyin": "Xiǎohán",     "hanzi": "小寒", "japanese": "Shōkan",    "english": "Slight Cold",          "longitude": 285, "date": "2026-01-05", "time": "10:31"},
    {"month": 12, "pinyin": "Dàhán",       "hanzi": "大寒", "japanese": "Taikan",    "english": "Great Cold",           "longitude": 300, "date": "2026-01-20", "time": "04:00"}
]   

def main():
    import json
    import csv
    import os

    table = []
    for i in range(24):
        old = Table_19_1[i]
        copilot = solar_terms_2025[i]
        assert old[0] == copilot['month']
        if (i % 2) == 0:
            month = {'index' : old[0]-1 if old[0]>1 else 12, 'leap': True}
        else:
            month = {'index': old[0], 'leap': False}
        entry = {
            'month': month,
            'pinyin': copilot['pinyin'],
            'hanzi': copilot['hanzi'],
            'japanese': copilot['japanese'],
            'english': copilot['english'],
            'solar_longitude': old[5],
            'approximate_starting_date': old[6],
        }
        table.append(entry)

    # Write JSON file
    json_path = os.path.join('Table_19_1_modified', 'Table_19_1a.json')
    with open(json_path, 'w', encoding='utf-8') as json_file:
        json.dump(table, json_file, ensure_ascii=False, indent=4)

        
if __name__ == "__main__":
    main()