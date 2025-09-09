
import inspect
from SPK_UniversalTimestamp.UnivDecimalLibrary import to_roman_numeral

from SPK_UniversalTimestamp.CC01_Calendar_Basics import *
from SPK_UniversalTimestamp.CC02_Gregorian import *
from SPK_UniversalTimestamp.CC03_Julian import *
from SPK_UniversalTimestamp.CC19_Chinese_1645 import *

from SPK_UniversalTimestamp import *
from SPK_UniversalTimestamp.UnivGREGORIAN import *
from SPK_UniversalTimestamp.UnivCHINESE import *

class TestUniversalTimestamp:
    """Test cases for UnivTimestamp class."""
    def setup_class(cls):
        # Set font for Chinese characters before creating figure
        import matplotlib.font_manager as fm
        import matplotlib as mpl
        
        # Try to use a font that supports Chinese characters
        # Priority list of fonts that support CJK characters
        cjk_fonts = ['SimHei', 'Microsoft YaHei', 'SimSun', 'NSimSun', 'FangSong', 
                    'KaiTi', 'Arial Unicode MS', 'Noto Sans CJK JP', 'Noto Sans CJK SC']
        
        # Find the first available font
        font_found = False
        for font in cjk_fonts:
            if any(font.lower() in f.name.lower() for f in fm.fontManager.ttflist):
                mpl.rcParams['font.family'] = font
                print(f"Using font: {font}")
                font_found = True
                break
        
        if not font_found:
            print("Warning: No CJK-compatible font found. Chinese characters may not display correctly.")
        # Reingold & Dershowitz p 310
        cls.rds_1989_12_22_new_moons_expected = [726464,726494,726523,726553,726582,726611,726641,726670,726699,726729,726758,726788,726818]
        return
    
    def test_chinese_epoch(self):
        """Test Chnese calendar conversion."""
        # Reingold & Derhowitz p 316
        chinese_epoch = rd_from_gregorian(-2636, 2, 15)
        univ_chinese_epoch = Epoch_rd['chinese']
        assert chinese_epoch == univ_chinese_epoch  # R.D. 
        chinese_epoch = rd_from_julian(-2637, 3, 8)
        assert chinese_epoch == univ_chinese_epoch  # R.D. for 1st day of Chinese calendar
        
    def test_chinese_terms(self, plot_manager):        
        """Test Chinese calendar terms."""
        # Reingold & Dershowitz p 307
        cell_data = []
        for term in Table_19_1:
            term_cells = []
            
            term_cells.append(f"{term['month']['index']:2d}{'L' if term['month']['leap'] else ' '}")
            term_cells.append(f"{term['pinyin']}({term['hanzi']})")
            term_cells.append(f"{term['japanese']}")
            term_cells.append(f"{term['english']}")
            term_cells.append(f"{term['solar_longitude']:3d}°")
            term_cells.append(f"{term['approximate_starting_date']}")
            # for i in range(len(term)):
            #     if i==2:
            #         term_cells[-1] += f"({term[i]})"
            #     else:
            #         term_cells.append(term[i])
            cell_data.append(term_cells)
        col_labels = ["Ndx", "Chinese", "Japanese", "English", "Solar Longitude", "approx. Start Date"]
        col_widths = [0.05, 0.20, 0.20, 0.20, 0.20, 0.15]
        plot_manager.figure(figsize=(16, 8.5))
        plot_manager.create_table(cell_data, col_labels, col_widths, fontsize=10, bbox=[0.05,0.05,0.9,0.85])
        plot_manager.title(
            "Table 19.1 Solar Terms of Chinese year",
            'See Reingold & Dershowitz, "Calendrical Calculations", 4th Ed., p. 307'
            )
        for i in range(len(cell_data)+1):
            for j in range(len(col_labels)):
                text_props = {'va': 'center' }
                if (i % 2) == 0:
                    text_props['fontweight'] = 'bold'
                if j == 1:
                    text_props['fontsize'] = 12
                if j in [1,2,3,5]:
                    text_props['ha'] = 'left'
                else:
                    text_props['ha'] = 'right'    
                plot_manager.style_table_cell(i, j, text_props=text_props)
                
        plot_manager.show("Table_19_1_Chinese_solar_terms.png")

    def test_chinese_new_moons(self):
        # Reingold & Dershowitz p 310
        winter_solstice_1989_12_22 = rd_from_gregorian(1989, 12, 22)
        day = winter_solstice_1989_12_22
        index = 0
        TestUniversalTimestamp.rds_1989_12_22_new_moons_found = []
        while day <= winter_solstice_1989_12_22 + 360:
            new_moon = int(chinese_new_moon_on_or_after(day))
            new_moon_expected = self.rds_1989_12_22_new_moons_expected[index]
            assert new_moon == new_moon_expected, f"Expected {new_moon_expected} but got {new_moon} for index {index}"
            index += 1
            g_year, g_month, g_day = gregorian_from_rd(new_moon)
            ts = UnivGREGORIAN(g_year, g_month, g_day, description=f"New Moon {index:2d}")
            print(f"New Moon {f'({to_roman_numeral(index)})':6}: RD={new_moon:5d} => {ts.strftime('%B %d, %Y')}")
            TestUniversalTimestamp.rds_1989_12_22_new_moons_found.append((index, to_roman_numeral(index), new_moon, ts))
            day = new_moon + 1
            
        return
  
    def test_solar_longitude(self):
        ts = UnivGREGORIAN(1990, 12, 22, description="Winter Solstice 1990-12-22")
        for day in range(ts.rd, ts.rd + 365, 5):
            long = solar_longitude(day)
            g_year, g_month, g_day = gregorian_from_rd(day)
            print (f"Day {day:5d} => {g_year}-{g_month:02d}-{g_day:02d} => Solar Longitude = {long:7.3f}°")
        
        winter_solstice = int(season_in_gregorian(winter(), 1989))
        g_year, g_month, g_day = gregorian_from_rd(winter_solstice)
        long = solar_longitude(winter_solstice)
        print (f"Winter solstice R.D.{winter_solstice:9,d} => {g_year}-{g_month:02d}-{g_day:02d} => Solar Longitude = {long:7.3f}°")
        
        vernal_equinox = int(season_in_gregorian(spring(), 1990))
        g_year, g_month, g_day = gregorian_from_rd(vernal_equinox)
        long = solar_longitude(vernal_equinox)
        print (f"Vernal equinox  R.D.{vernal_equinox:9,d} => {g_year}-{g_month:02d}-{g_day:02d} => Solar Longitude = {long:7.3f}°")
        
        summer_solstice = int(season_in_gregorian(summer(), 1990))
        g_year, g_month, g_day = gregorian_from_rd(summer_solstice)
        long = solar_longitude(summer_solstice)
        print (f"Summer solstice R.D.{summer_solstice:9,d} => {g_year}-{g_month:02d}-{g_day:02d} => Solar Longitude = {long:7.3f}°")
        
        autumnal_equinox = int(season_in_gregorian(autumn(), 1990))
        g_year, g_month, g_day = gregorian_from_rd(autumnal_equinox)
        long = solar_longitude(autumnal_equinox)
        print (f"Autumnal equinox R.D.{autumnal_equinox:9,d} => {g_year}-{g_month:02d}-{g_day:02d} => Solar Longitude = {long:7.3f}°")
        
        winter_solstice = int(season_in_gregorian(winter(), 1990))
        g_year, g_month, g_day = gregorian_from_rd(winter_solstice)
        long = solar_longitude(winter_solstice)
        print (f"Winter solstice  R.D.{winter_solstice:9,d} => {g_year}-{g_month:02d}-{g_day:02d} => Solar Longitude = {long:7.3f}°")
        return

    ###############################################################################################
    def display_sui(self, year :int, print_sui:bool=False):
        winter_begin = int(season_in_gregorian(winter(), year-1))
        g_year, g_month, g_day = gregorian_from_rd(winter_begin)
        long = solar_longitude(winter_begin)
        if print_sui:
            print (f"\nBegin Winter  R.D.{winter_begin:9,d} => {g_year}-{g_month:02d}-{g_day:02d} => Solar Longitude = {long:7.3f}°")
        
        winter_end = int(season_in_gregorian(winter(), year))
        g_year, g_month, g_day = gregorian_from_rd(winter_end)
        long = solar_longitude(winter_end)
        if print_sui:
            print (f"End   Winter  R.D.{winter_end:9,d} => {g_year}-{g_month:02d}-{g_day:02d} => Solar Longitude = {long:7.3f}°")
        
        # Add the new moons between the winter solstices
        day = winter_begin
        index = 0
        new_calendar = []
        last_new_moon_elm = None
        last_new_moon_moment = None
        # Add the new moons to the calendar
        while day < winter_end:
            new_moon = chinese_new_moon_on_or_after(day)
            if last_new_moon_elm:
                last_new_moon_elm['days_in_month'] = int(round(new_moon - last_new_moon_moment))
            index += 1
            g_year, g_month, g_day = gregorian_from_rd(new_moon)
            g_ts = UnivGREGORIAN(g_year, g_month, g_day, description=f"New Moon {index:2d}")
            last_new_moon_elm = {
                'moon_ndx' : to_roman_numeral(index),
                'days_in_month' : None,
                'month_no' : None, 
                'ch_name' : None,
                'leap_month': None, 
                'def_sl': None,
                'english': None,
                'actual_sl': None,
                'approximate_start': None,
                'RD' : g_ts.rd,
                'g_ts' : g_ts
                }
            new_calendar.append(last_new_moon_elm)
            last_new_moon_moment = new_moon
            #print(f"{' ':4} {to_roman_numeral(index):20} R.D. {g_ts.rd:9,d} ({g_ts.strftime('%B %d, %Y')})")
            day = new_moon + 1
        # Assign new moons 1 to 12,13
        # Collect the major solar terms 
        principal_solar_terms = []
        leap_solar_terms = [] 
        for i in range(len(Table_19_1)):
            term = Table_19_1[i]    
            m_index = term['month']['index']
            m_leap = term['month']['leap']
            m_ch_name = term['pinyin']
            m_ch_writing = term['hanzi']
            m_japan = term['japanese']
            m_english = term['english']
            m_def_sl = term['solar_longitude']
            m_start = term['approximate_starting_date'] 
            rd = solar_longitude_after(m_def_sl, winter_begin+1) + Decimal(8)/Decimal(24)
            actual_sl = solar_longitude(rd)
            g_year, g_month, g_day = gregorian_from_rd(int(rd))
            g_ts = UnivGREGORIAN(g_year, g_month, g_day, description=f"{m_ch_name} ({m_english})")
            term ={
                'month_no' : f"{m_index}{'L' if m_leap else ' '}",
                'ch_name' : m_ch_name, 
                'ch_writing' : m_ch_writing,
                'english' : m_english,
                'RD' : rd, 
                'def_sl' : m_def_sl,
                'actual_sl' : actual_sl,
                'g_ts' :g_ts,
                'approximate_start' : m_start
                }
            if i % 2 == 1:
                principal_solar_terms.append(term)
                term['leap_month'] = False
            else:
                leap_solar_terms.append(term)
                term['leap_month'] = True
                #term['month_no'] = f"{m_no - 1 if m_no > 1 else 12}L"
            #print(f"{m_no:4d} {m_ch_name:20} R.D. {int(rd):9,d} {m_def_sl:4d}° ({g_ts.strftime('%B %d, %Y')})")

        # Assign Names to the new moons
        term_i = 11
        for i in range(0, len(new_calendar)-1):
            new_moon = new_calendar[i]
            if i < len(new_calendar)-1:
                upper_bound = new_calendar[i+1]['RD']
            else:
                upper_bound = new_moon['RD']+30
            mst_date = principal_solar_terms[term_i]['RD']
            if mst_date >= new_moon['RD'] and mst_date < upper_bound:
                term = principal_solar_terms[term_i]
                term_i = (term_i + 1) % 12
            else:
                term = leap_solar_terms[term_i]
            new_moon['month_no'] = term['month_no']
            new_moon['leap_month'] = term['leap_month']
            new_moon['ch_name'] = term['ch_name']
            new_moon['def_sl'] = term['def_sl']
            new_moon['english'] = term['english']
            new_moon['actual_sl'] = term['actual_sl']
            new_moon['approximate_start'] = term['approximate_start']
        
        if print_sui:  
            print(f"Sui {year-1}-{year} Calendar:")
            print(f"{' ':6} {'Month':5} {'Lp':2} {'Days'} {'Chinese Name':20} {'Def.SL':6} {'SL':>7} {'Approx. Start':15} {'English':<20} {'RD':>9} {'Start Date':20}")
            for month in new_calendar:
                month_no = month['month_no'] if month['month_no'] is not None else ""
                days_in_month = str(month['days_in_month']) if month['days_in_month'] is not None else ""
                leap_month = 't' if month['leap_month'] else ''
                m_ch_name = month['ch_name'] if month['ch_name'] is not None else ""
                def_sl = month['def_sl'] if month['def_sl'] is not None else ""
                sl = f"{month['actual_sl']:7.2f}" if month['actual_sl'] is not None else ""
                appx_start = month['approximate_start'] if month['approximate_start'] is not None else ""
                english = month['english'] if month['english'] is not None else ""
                
                print(f"{month['moon_ndx']:>6} {month_no:5} {leap_month:>2} {days_in_month:4} {m_ch_name:20} {def_sl:>6} {sl:>7} {appx_start:<15} {english:<20} {month['RD']:9,d} {month['g_ts'].strftime('%B %d, %Y'):20}")
        
        return

    def test_chinese_from_rd_against_RnD(self):    
        # Reingold & Dershowitz p 315
        self.display_sui(1990)
        rd = rd_from_gregorian(1990, 1, 20)
        cycle, year, month, leap_month, day = chinese_from_rd(rd)        
        assert cycle == 78
        assert year == 6
        assert month == 12
        assert leap_month is False
        assert day == 24
        rd = rd_from_gregorian(1990, 1, 27)
        cycle, year, month, leap_month, day = chinese_from_rd(rd)        
        assert cycle == 78
        assert year == 7
        assert month == 1
        assert leap_month is False
        assert day == 1
        rd = rd_from_gregorian(1990, 5, 24)
        cycle, year, month, leap_month, day = chinese_from_rd(rd)        
        assert cycle == 78
        assert year == 7
        assert month == 5
        assert leap_month is False
        assert day == 1
        rd = rd_from_gregorian(1990, 6, 23)
        cycle, year, month, leap_month, day = chinese_from_rd(rd)        
        assert cycle == 78
        assert year == 7
        assert month == 5
        assert leap_month is True
        assert day == 1
        rd = rd_from_gregorian(1990, 7, 1)
        cycle, year, month, leap_month, day = chinese_from_rd(rd)        
        assert cycle == 78
        assert year == 7
        assert month == 5
        assert leap_month is True
        assert day == 9
        rd = rd_from_gregorian(1990, 7, 22)
        cycle, year, month, leap_month, day = chinese_from_rd(rd)        
        assert cycle == 78
        assert year == 7
        assert month == 6
        assert leap_month is False
        assert day == 1
        rd = rd_from_gregorian(1990, 12, 21)
        cycle, year, month, leap_month, day = chinese_from_rd(rd)        
        assert cycle == 78
        assert year == 7
        assert month == 11
        assert leap_month is False
        assert day == 5
        rd = rd_from_gregorian(1990, 1, 1)
        rd_new_year = chinese_new_year_in_sui(rd)
        cycle, year, month, leap_month, day = chinese_from_rd(rd_new_year)        
        assert cycle == 78
        assert year == 7
        assert month == 1
        assert leap_month is False
        assert day == 1
        g_year, g_month, g_day = gregorian_from_rd(rd_new_year)
        assert g_year == 1990
        assert g_month == 1 
        assert g_day == 27
        return
    
    def test_rd_from_chinese(self):
        rd_from_greg = rd_from_gregorian(1990, 4, 25)
        cycle, year, month, leap, day = chinese_from_rd(rd_from_greg)
        rd = rd_from_chinese(cycle, year, month, leap, day)
        if rd != rd_from_greg:
            print(f"Expected {rd_from_greg} but got {rd}")
        
        rd_from_greg = rd_from_gregorian(1990, 6, 22)
        cycle, year, month, leap, day = chinese_from_rd(rd_from_greg)
        rd = rd_from_chinese(cycle, year, month, leap, day)
        if rd != rd_from_greg:
            print(f"Expected {rd_from_greg} but got {rd}")
        
        rd_from_greg = rd_from_gregorian(1990, 7, 1)
        cycle, year, month, leap, day = chinese_from_rd(rd_from_greg)
        rd = rd_from_chinese(cycle, year, month, leap, day)
        if rd != rd_from_greg:
            print(f"Expected {rd_from_greg} but got {rd}")
            
        rd_from_greg = rd_from_gregorian(1990, 7, 22)
        cycle, year, month, leap, day = chinese_from_rd(rd_from_greg)
        rd = rd_from_chinese(cycle, year, month, leap, day)
        if rd != rd_from_greg:
            print(f"Expected {rd_from_greg} but got {rd}")
        
        rd_from_greg = rd_from_gregorian(1096, 5, 24)
        cycle, year, month, leap, day = chinese_from_rd(rd_from_greg)
        rd = rd_from_chinese(cycle, year, month, leap, day)
        if rd != rd_from_greg:
            print(f"Expected {rd_from_greg} but got {rd}")
            
        rd_from_greg = rd_from_gregorian(1648, 6, 10)
        cycle, year, month, leap, day = chinese_from_rd(rd_from_greg)
        rd = rd_from_chinese(cycle, year, month, leap, day)
        if rd != rd_from_greg:
            print(f"Expected {rd_from_greg} but got {rd}")
            
    def test_chinese_from_rd_against_2023(self):    
        # 12 new moons between winter solstices
        self.display_sui(2015)
        rd = rd_from_gregorian(2015, 1, 20)
        cycle, year, month, leap_month, day = chinese_from_rd(rd)        
        assert cycle == 78
        assert year == 31
        assert month == 12
        assert leap_month is False
        assert day == 1
        rd = rd_from_gregorian(2015, 2, 19)
        cycle, year, month, leap_month, day = chinese_from_rd(rd)        
        assert cycle == 78
        assert year == 32
        assert month == 1
        assert leap_month is False
        assert day == 1
        rd = rd_from_gregorian(2015, 5, 24)
        cycle, year, month, leap_month, day = chinese_from_rd(rd)        
        assert cycle == 78
        assert year == 32
        assert month == 4
        assert leap_month is False
        assert day == 7
        rd = rd_from_gregorian(2016, 1, 9)
        cycle, year, month, leap_month, day = chinese_from_rd(rd)        
        assert cycle == 78
        assert year == 32
        assert month == 11
        assert leap_month is False
        assert day == 30
        return
    
    def test_chinese_from_rd_against_1941(self):
        self.display_sui(1941)
        rd = rd_from_gregorian(1941, 9, 29)
        cycle, year, month, leap_month, day = chinese_from_rd(rd)        
        assert cycle == 77
        assert year == 18
        assert month == 8
        assert leap_month is False
        assert day == 9
        
    def test_chinese_from_rd_against_470(self):
        self.display_sui(470)
        rd = rd_from_gregorian(470, 1, 8)
        cycle, year, month, leap_month, day = chinese_from_rd(rd)        
        assert cycle == 52
        assert year == 46
        assert month == 11
        assert leap_month is False
        assert day == 22
        
    def test_chinese_from_rd_against_2025(self):
        self.display_sui(2025)
        rd = rd_from_gregorian(2025, 8, 17)
        cycle, year, month, leap_month, day = chinese_from_rd(rd)        
        assert cycle == 78
        assert year == 42
        assert month == 6
        assert leap_month is True
        assert day == 24
        return
    
    def test_chinese_timestamp(self):    
        timestamp = UnivCHINESE(
            63, 13, 4, 25,  
            description="p 451 Reingold & Dershowitz"
        )      
        rd = timestamp.rd
        need_rd = 400085
        signature = timestamp.format_signature()
        _str = timestamp.__str__()
        _repr = timestamp.__repr__()
        assert timestamp.calendar == Calendar.CHINESE
        assert timestamp.year == 3732
        assert timestamp.month == 4
        assert timestamp.day == 25
        assert timestamp.precision == Precision.DAY
        assert rd == need_rd
        assert signature == "3732-04-25 CC"
        assert _str == "3732-04-25 CC"
        assert _repr == "{'class':'UnivCHINESE','ca':'CHINESE','yr':3732,'mo':4,'da':25,'hr':None,'mi':None,'sc':None,'pr':'DAY','tz':'UTC','fo':0,'ac':None,'de':'p 451 Reingold & Dershowitz'}"
        timestamp = UnivCHINESE(
            72, 25, (4,True), 20,  
            timezone='Asia/Shanghai',
            accuracy=Decimal('0.01'),
            description="p 451 Reingold & Dershowitz"
        )      
        rd = timestamp.rd
        need_rd = 601716
        signature = timestamp.format_signature(include_precision=True)
        _str = timestamp.__str__()
        _repr = timestamp.__repr__()
        assert timestamp.calendar == Calendar.CHINESE
        assert timestamp.year == 4284
        assert timestamp.month[0] == 4
        assert timestamp.month[1] is True
        assert timestamp.day == 20
        assert timestamp.precision == Precision.DAY
        assert rd == need_rd
        assert signature == "4284-04L-20 CC day±1.0%"
        assert _str == "4284-04L-20 CC"
        assert _repr == "{'class':'UnivCHINESE','ca':'CHINESE','yr':4284,'mo':(4, True),'da':20,'hr':None,'mi':None,'sc':None,'pr':'DAY','tz':'Asia/Shanghai','fo':0,'ac':'0.01','de':'p 451 Reingold & Dershowitz'}"
        return

    def test_string__str__(self):
        """Test string representations."""
        timestamp = UnivCHINESE(
            72, 25, (4,True), 20,  
            description="Test timestamp"
        )
        
        # Test __str__
        str_repr = str(timestamp)
        assert "4284-04L-20 CC" == str_repr
        print(f"✅ SUCCESS: {inspect.currentframe().f_code.co_name}")
        return

    def test_string__repr__(self):
        timestamp = UnivCHINESE(
            72, 25, (4,True), 20, 8, 45, 15,
            timezone='Asia/Shanghai',
            description="Test timestamp"
        )      
        need_str = "{'class':'UnivCHINESE','ca':'CHINESE','yr':4284,'mo':(4, True),'da':20,'hr':8,'mi':45,'sc':15,'pr':'SECOND','tz':'Asia/Shanghai','fo':0,'ac':None,'de':'Test timestamp'}" 
        # Test __repr__
        repr_str = repr(timestamp)
        assert repr_str == need_str, "Repr string mismatch!" 
        
        ts_repro = UnivTimestampFactory.parse_repr(repr_str)
        assert ts_repro == timestamp, "Timestamp mismatch after reconstruction"
        repr_str = repr(ts_repro)
        assert repr_str ==  need_str, "Repr string mismatch after reconstruction"
        
        print(f"✅ SUCCESS: {inspect.currentframe().f_code.co_name}")
        return

