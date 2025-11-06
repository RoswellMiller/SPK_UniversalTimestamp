"""
Comprehensive tests for the UnivTimestamp class.
"""
import os
import sys
import json
from decimal import Decimal, ROUND_FLOOR
#from datetime import datetime
#import matplotlib.pyplot as plt
#import numpy as np

#from SPK_UniversalTimestamp.UnivDecimalLibrary import location, direction
from SPK_UniversalTimestamp.CC02_Gregorian import gregorian_from_rd
from SPK_UniversalTimestamp.CC14_Time_and_Astronomy import ephemeris_correction, equation_of_time, dynamical_from_universal
from SPK_UniversalTimestamp.CC14_Time_and_Astronomy import solar_longitude, solar_longitude_after, dms_from_degrees
from SPK_UniversalTimestamp.CC14_Time_and_Astronomy import hms_from_hours, universal_from_local, round_, degrees_from_dms
from SPK_UniversalTimestamp.CC14_Time_and_Astronomy import AST, standard_from_local, location, direction
#from .PolynomialRegression import polynomial_regression

from SPK_UniversalTimestamp.UnivGREGORIAN import UnivGREGORIAN

class TestUniversalTimestamp:
    def setup_method(self):
        """Setup for each test method."""
        cwd = os.getcwd()
        print(f"Current working directory: {cwd}")
        with open("Tests\\RandD_Appendix_C.json", "r") as f:
            self.dates_table = json.load(f)
        with open("Tests\\RandD_Appendix_C_Lunisolar_table.json", "r") as f:
            self.lunisolar_table = json.load(f)
            
    def test_round_(self):
        n = Decimal('12.345')
        n_r = round_(n)
        #print(f"Original(n): {n}, round_(n): {n_r}")
        assert n_r == Decimal('12'), "Round function failed"
        
        n = Decimal('12.545')
        n_r = round_(n)
        #print(f"Original(n): {n}, round_(n): {n_r}")
        assert n_r == Decimal('13'), "Round function failed"
        return
    
    def test_degrees_from_dms(self):
        dms = Decimal('12.234')
        degrees = degrees_from_dms(dms)
        print(f"DMS: {dms}, Degrees: {degrees}")
        assert degrees == Decimal('12.234'), "Degrees from DMS conversion failed"
        
        dms = (Decimal(12))
        degrees = degrees_from_dms(dms)
        print(f"DMS: {dms}, Degrees: {degrees}")
        assert degrees == Decimal('12'), "Degrees from DMS conversion failed"
        
        dms = (Decimal(12), Decimal(30))
        degrees = degrees_from_dms(dms)
        print(f"DMS: {dms}, Degrees: {degrees}")
        assert degrees == Decimal('12.5'), "Degrees from DMS conversion failed"
        
        dms = (Decimal(12), Decimal(30), Decimal('45.6'))
        degrees = degrees_from_dms(dms)
        print(f"DMS: {dms}, Degrees: {degrees}")
        ans = Decimal(12) + Decimal(30)/Decimal(60) + Decimal('45.6')/Decimal(3600)
        assert degrees == ans, "Degrees from DMS conversion failed"
        return
        
    def test_constructors(self):
        # Run a simple test series
        print(f"Testing on Python {sys.version} location and direction functions...")
        print(AST.greenwich)
        print(AST.mecca)
        print("#" * 10)
        return            
            
    def test_direction(self):    
        #print("Direction from greenwich to mecca:", direction(AST.greenwich, AST.mecca))   
        #print("Direction from mecca to greenwich:", direction(AST.mecca, AST.greenwich))
        print("Direction from urbana to greenwich:", direction(AST.urbana, AST.greenwich))
        print("Direction from greenwich to urbana:", direction(AST.greenwich, AST.urbana))
        #print("Direction from urbana to mecca:", direction(AST.urbana, AST.mecca))
        #print("Direction from mecca to urbana:", direction(AST.mecca, AST.urbana)) 
        d = direction(AST.greenwich, AST.mecca)
        print("Qibla for greenwich ", d, "\u00B0", 'East' if d>0 and d<180 else 'West' if d<0 and d>-180 else 'North' if d==0 else 'South')
        d = direction(AST.urbana, AST.mecca)  
        print("Qibla for urbana ", d, "\u00B0", 'East' if d>0 and d<180 else 'West' if d<0 and d>-180 else 'North' if d==0 else 'South')
        rio = location(-22.9068, -43.1729, 2, -3, "Rio de Janeiro, Brazil")
        d = direction(rio, AST.mecca)
        print("Qibla for Rio de Janeiro ", d, "\u00B0", 'East' if d>0 and d<180 else 'West' if d<0 and d>-180 else 'North' if d==0 else 'South')
        sidney = location(-33.8688, 151.2093, 58, 10, "Sidney, Australia")
        d = direction(sidney, AST.mecca)
        print("Qibla for Sidney ", d, "\u00B0", 'East' if d>0 and d<180 else 'West' if d<0 and d>-180 else 'North' if d==0 else 'South')
        npole = location(90,0,0,0,"North Pole")
        d = direction(npole, AST.mecca)
        print("Qibla for North Pole ", d, "\u00B0", 'East' if d>0 and d<180 else 'West' if d<0 and d>-180 else 'North' if d==0 else 'South')
        spole = location(-90,0,0,0,"South Pole")
        d = direction(spole, AST.mecca)
        print("Qibla for South Pole ", d, "\u00B0", 'East' if d>0 and d<180 else 'West' if d<0 and d>-180 else 'North' if d==0 else 'South')  
        d = direction(npole, spole)
        print("Direction from North Pole to South Pole:", d, "\u00B0", 'East' if d>0 and d<180 else 'West' if d<0 and d>-180 else 'North' if d==0 else 'South')
        d = direction(spole, npole)
        print("Direction from South Pole to North Pole:", d, "\u00B0", 'East' if d>0 and d<180 else 'West' if d<0 and d>-180 else 'North' if d==0 else 'South')
        return
    
    def test_universal_from_local(self):
        print("Testing universal_from_local and standard_from_local functions...")
        test_times = [
            (Decimal(8.75), AST.jerusalem),
            (Decimal(12), AST.urbana),
            (Decimal(14.5), AST.greenwich),
            (Decimal(10.25), AST.mecca),
            (Decimal(9.5), AST.acre),
            (Decimal(16), AST.sidney),
            (Decimal(3), AST.rio),
            (Decimal(23), AST.tokyo),
            (Decimal(18), AST.moscow),
            (Decimal(11.5), AST.lima)
        ]
        print("Greenwich     long:", dms_from_degrees(AST.greenwich.longitude))
        for hr_local, loc in test_times:
            print(f"{loc.name}  longitude:", dms_from_degrees(loc.longitude))
            print(f"{loc.name} utc-offset:", loc.utc_offset)
            print(f"{loc.name} local time:", hms_from_hours(hr_local))
            hr_universal = universal_from_local(hr_local, loc)
            hr_standard = standard_from_local(hr_local, loc)
            print(f"-----> Universal time: {hms_from_hours(hr_universal)}")
            print(f"-----> UTC Standard  : {hms_from_hours(hr_standard)}")
        
        return

    def test_RandD_Appendix_C_ephemeris(self):
        for entry in self.lunisolar_table:
            entry['EphemerisCorrection'] = Decimal(entry['EphemerisCorrection'])
        print("Testing ephemeris correction values from Reingold & Dershowitz, 'Calendrical Calculations', 4th Ed., Appendix C Lunisolar Table")
        errors = 0
        for entry in self.lunisolar_table:
            rd = entry['RD']
            expected = entry['EphemerisCorrection']
            calculated = ephemeris_correction(rd).quantize(Decimal('0.000_000_01'), rounding=ROUND_FLOOR)
            error = abs(calculated - expected)
            print(f"RD: {rd:9d} calculated: {calculated:.8f}")
            print(f"    {' ':9} expected:   {expected:.6f}, error: {error:.6f}")
            if error <= Decimal('0.000_001'):
                print ("    ✅ Test passed")
            else:
                print ("    ❌ Test failed")
                errors += 1
                
        
        assert errors==0, f"❌ Ephemeris correction test failed. {errors} errors found."
        return
    
    def test_ephemeris(self, plot_manager):
        print("Testing ephemeris functions...")
        # Test the ephemeris function with a known date
        years = []
        corrections = []
        for year in range(-600, 2200, 1):
            test_date = UnivGREGORIAN(year, 1, 1)
            years.append(year)
            corrections.append(float(ephemeris_correction(test_date.rd))*86400)
        ex_years = []
        ex_corrections = []
        for i, entry in enumerate(self.lunisolar_table):
            year = self.dates_table['Gregorian-year'][i]
            expected = float(entry['EphemerisCorrection'])*86400 -1 # from fraction of day to seconds - ε
            ex_years.append(year)
            ex_corrections.append(expected)
        
        
        plot_manager.figure(figsize=(12, 6))
        # Plot the expected values
        plot_manager.plot(ex_years, ex_corrections, 'r.', linewidth=1, label='Appendix C values - ε')
        # Plot the calculated values
        plot_manager.plot(years, corrections, 'b-', linewidth=1, label='Calculated values')
        # Create proxy for transition years in legend
        plot_manager.plot([0,0], [0,0], 'g--', linewidth=1, label='Calculation transition years')
        # Highlight transition years
        transition_years = [-500, 500, 1600, 1700, 1800, 1900, 1986, 2005, 2050, 2150]
        for year in transition_years:
            plot_manager.vertical_line(year, color='g', linestyle='--')
        plot_manager.xlabel('Gregorian Year')
        plot_manager.ylabel('ΔT (atomic seconds)')
        plot_manager.grid(True)
        plot_manager.title(
            'Figure 14.3 Ephemeris Correction (ΔT) Over Time.',
            'See Reingold & Dershowitz, "Calendrical Calculations", 4th Ed., p. 213'
        )
        
        plot_manager.legend()
        plot_manager.show('Figure_14_3_Ephemeris_Correction.png')
        return
    
    def test_RandD_Appendix_C_equation_of_time(self):
        for entry in self.lunisolar_table:
            entry['EquationOfTime'] = Decimal(entry['EquationOfTime'])
        print("Testing Equation of Time values from Reingold & Dershowitz, 'Calendrical Calculations', 4th Ed., Appendix C Lunisolar Table")
        errors = 0
        for entry in self.lunisolar_table:
            rd = entry['RD']
            expected = entry['EquationOfTime']
            calculated = equation_of_time(rd).quantize(Decimal('0.000_001'), rounding=ROUND_FLOOR)
            error = abs(calculated - expected)
            print(f"RD: {rd:9d} calculated: {calculated:.6f}")
            print(f"    {' ':9} expected:   {expected:.6f}, error: {error:.6f}")
            if error < Decimal('0.000_100'):
                print ("    ✅ Test passed")
            else:
                print ("    ❌ Test failed")
                errors += 1
                
        
        assert errors==0, f"❌ Equation of Time test failed. {errors} errors found."
        return
    
    def test_equation_of_time(self, plot_manager):
        """Test the equation of time calculations"""
        days = []
        eot_values = []
        x_ticks = []
        test_date = UnivGREGORIAN(2000, 1, 1)
        start_rd = test_date.rd
        current_month = 1
        for day in range(0, 366, 1):
            eot = equation_of_time(start_rd + day)
            _, month, _ = gregorian_from_rd(start_rd + day)
            if month != current_month:
                current_month = month
                x_ticks.append(day)
            days.append(day)
            eot_values.append(float(eot)*24*60)  # from fraction of day to minutes   
            
        plot_manager.figure(figsize=(12, 6))
        plot_manager.plot(days, eot_values, 'b-', linewidth=1)
        plot_manager.xlabel('Day of Year 2000')
        plot_manager.xticks(x_ticks)
        plot_manager.ylabel('ΔT (minutes)')
        plot_manager.grid(True)
        plot_manager.title(
            'Figure 14.5 Equation of Time for Year 2000.',
            'See Reingold & Dershowitz, "Calendrical Calculations", 4th Ed., p. 216'
        )
            
        plot_manager.show('Figure_14_5_Equation_of_Time.png')
        return
    
    # def test_equation_of_time_continuity(self, plot_manager):
    #     x = []
    #     y = []
    #     z = []
        
    #     for year in range(1500, 5000):
    #         first_of_year = rd_from_gregorian(year, 1, 1)
    #         days_in_year = 366 if is_gregorian_leap_year(year) else 365
    #         for month in range(1,14):
    #             if month > 12:
    #                 first_of_month = rd_from_gregorian(year + 1, 1, 1)
    #             else:
    #                 first_of_month = rd_from_gregorian(year, month, 1)
    #             day_of_year = first_of_month - first_of_year 
    #             day_degree = (day_of_year / days_in_year) * 360
    #             eot = float(equation_of_time(first_of_month))* 24*60 + 20
    #             x_d = round(eot * math.sin(float(DEG2RAD) * day_degree), 1)
    #             y_d = round(eot * math.cos(float(DEG2RAD) * day_degree), 1)
    #             z_d = year
    #             x.append(x_d)
    #             y.append(y_d)
    #             z.append(z_d)
    #             #print(f"X: {x_d:5.1f}, Y: {y_d:5.1f}, Z: {z_d:4d}, m:{month:2d}, d:{day_of_year:4d} dg:{day_degree:6.2f} EoT:{eot:6.2f}")
            
    #     # Fit polynomial model
    #     model_info = polynomial_regression(x, y, z, degree=2)
    #     print(f"Polynomial formula: {model_info['formula']}")
    #     print(f"R² score: {model_info['r2_score']:.4f}")

    #     x_range = sorted(set(x))
    #     y_range = sorted(set(y))
    #     # Create surface using the model
    #     plot_manager.figure(figsize=(12, 6))
    #     plot_manager.plot_surface(x_range, y_range, model_info['predict'], linewidth=0)
    #     plot_manager.xlabel('EOT * sin(day_degree)')
    #     plot_manager.ylabel('EOT * cos(day_degree)')
    #     #plot_manager.zlabel('Year')
    #     plot_manager.title(
    #         'Figure 14.6 Equation of Time Model using Polynomial Regression',
    #         # 'See Reingold & Dershowitz, "Calendrical Calculations", 4th Ed., p. 216',
    #         f"{model_info['formula']}  R²={model_info['r2_score']:.4f}")
    #     plot_manager.show('Figure_14_6_Equation_of_Time_Polynomial_Model.png')        
    #     plot_manager.xlabel('Month')
    #     return     # def test_nasa_reference_values(self):
    #     """Test against NASA's published delta-T values"""
    #     # Historical test cases
    #     test_cases = [
    #         # (year, expected_delta_T_in_seconds)
    #         (500,  5700),    # Approximate values
    #         (1000, 3900),
    #         (1600, 170),
    #         (1750, 13),
    #         (1900, -3),
    #         (2000, 64),
    #     ]
        
    #     for year, expected_seconds in test_cases:
    #         stamp = UnivGREGORIAN(year, 1, 1)
    #         #print(f"Testing year {year} with rd={stamp.rd}")
    #         calculated = ephemeris_correction(stamp.rd) * 86400  # Convert from days to seconds
    #         error = abs(calculated - Decimal(expected_seconds))
    #         if error <= max(Decimal('10'), abs(Decimal(expected_seconds) * Decimal('0.05'))):
    #             result = "✅"
    #         else:
    #             result = "❌"
    #         print(f"{result} Test Year {year}: calculated={calculated:.6f}s, expected={expected_seconds:.6f}s, error={error:.6f}s, 5% = {abs(Decimal(expected_seconds) * Decimal('0.05')):.6f}s")
            
    def test_continuous_function(self):
        """Test that the function is reasonably continuous across transition points"""
        transition_years = [-499, 500, 1600, 1700, 1800, 1900, 1986, 2005, 2050, 2150]
        #                    <    <    <     <     <     <     <     <     <     <
        for year in transition_years:
            # Test just before and after the transition
            before = UnivGREGORIAN(year-1, 12, 31)
            after = UnivGREGORIAN(year, 1, 1)
            
            before_correction = ephemeris_correction(before.rd)*86400
            after_correction = ephemeris_correction(after.rd)*86400
            # The difference should be small at transition points
            diff = abs(before_correction - after_correction)
            
            # Print the values for inspection
            if diff < Decimal(15):
                result = "✅"
            else:
                result = "❌"
            print(f"{result} Transition at {year}: before={before_correction:.6f}sec, after={after_correction:.6f}sec, diff={diff:.6f}sec")
            #assert diff < Decimal(170)  # ~170 seconds is a reasonable threshold for continuity
            
    def test_dynamic_vs_universal(self, plot_manager):
        """Test dynamic vs universal time corrections"""
        years = []
        diffs = []
        eph_cs = []
        
        for year in range(1600, 2050, 1):
            test_date = UnivGREGORIAN(year, 1, 1)
            years.append(year)
            u_time = universal_from_local(test_date.rd, AST.greenwich)
            d_time = dynamical_from_universal(u_time)
            eph_c = float(ephemeris_correction(test_date.rd))*86400 - 1 # from fraction of day to seconds
            diff = (d_time - u_time)*86400
            diffs.append(diff)
            eph_cs.append(eph_c)
        
        plot_manager.figure(figsize=(12, 6))
        plot_manager.axes_limits(1600, 2050)
        plot_manager.plot(years, diffs, 'b-', linewidth=1, label='Dynamic Time - Universal Time')
        plot_manager.plot(years, eph_cs, 'r--', linewidth=1, label='Ephemeris Correction (ΔT) - ε')
        plot_manager.xlabel('Gregorian Year')
        plot_manager.ylabel('ΔT (atomic seconds)')
        plot_manager.grid(True)
        plot_manager.title(
            'Figure 14.4 Difference between Dynamic (terrestrial) vs Universal Time',
            'See Reingold & Dershowitz, "Calendrical Calculations", 4th Ed., p. 214'
        )
        
        # Add legend
        plot_manager.legend()
        
        # Highlight transition years
        transition_years = [-500, 500, 1600, 1700, 1800, 1900, 1986, 2005, 2050, 2150]
        for year in transition_years:
            plot_manager.vertical_line(year)
        
        plot_manager.show('Figure_14_4_Dynamic_vs_Universal_Ephemeris_Corrections.png')
        return

    # def test_March_21_2000(self):
    #     """Test solar longitude on March 21, 2000"""
    #     print("Testing solar longitude on March 21, 2000...")
    #     test_date = UnivGREGORIAN(2000, 3, 21)
    #     expected_longitude = Decimal('0.0')
    #     calculated_longitude = solar_longitude(test_date.rd).quantize(Decimal('0.000_001'), rounding=ROUND_FLOOR)
    #     error = abs(calculated_longitude - expected_longitude) % Decimal('360')
    #     print(f"Calculated Solar Longitude: {calculated_longitude:.6f}°")
    #     print(f"                  Expected: {expected_longitude:.6f}°, Error: {error:.1f}°")
    #     assert error < Decimal('1.0'), "Solar Longitude test for March 21, 2000 failed"
    #     return
    
    def test_RandD_Appendix_C_solar_longitude(self):
        for entry in self.lunisolar_table:
            entry['SolarLongitude'] = Decimal(entry['SolarLongitude'])
        print("Testing Solar Longitude values from Reingold & Dershowitz, 'Calendrical Calculations', 4th Ed., Appendix C Lunisolar Table")
        errors = 0
        for entry in self.lunisolar_table:
            rd = entry['RD']
            expected = entry['SolarLongitude']
            calculated = solar_longitude(rd).quantize(Decimal('0.000_001'), rounding=ROUND_FLOOR)
            error = abs(calculated - expected) % Decimal('360')
            print(f"RD: {rd:9d} calculated: {calculated:.6f}")
            print(f"    {' ':9} expected:   {expected:.6f}, error: {error:.3f}")
            if error < Decimal('1.0'):
                print ("    ✅ Test passed")
            else:
                print ("    ❌ Test failed")
                errors += 1
                
        
        assert errors==0, f"❌ Solar Longitude test failed. {errors} errors found."
        return
    
    def test_RandD_Appendix_C_solar_longitude_after(self):
        for entry in self.lunisolar_table:
            entry['Next-Season-rd'] = Decimal(entry['Next-Season-rd'])
        print("Testing Next-Season-rd values from Reingold & Dershowitz, 'Calendrical Calculations', 4th Ed., Appendix C Lunisolar Table")
        errors = 0
        for entry in self.lunisolar_table:
            rd = entry['RD']
            expected = entry['Next-Season-rd']
            sl_rd = solar_longitude(rd).quantize(Decimal('0.000_001'), rounding=ROUND_FLOOR)
            next_season = ((1 + sl_rd // Decimal('90'))*90) % Decimal('360') 
            calculated = solar_longitude_after(next_season, rd)
            error = abs(calculated - expected) % Decimal('360')
            print(f"RD: {rd:9d} calculated: {calculated:.6f} for next season {next_season:.0f} after solar longitude {sl_rd:.6f}")
            print(f"    {' ':9} expected:   {expected:.6f}, error: {error:.3f}")
            if error < Decimal('1.0'):
                print ("    ✅ Test passed")
            else:
                print ("    ❌ Test failed")
                errors += 1
                
        
        assert errors==0, f"❌ solar_longitude_after test failed. {errors} errors found."
        return
    
