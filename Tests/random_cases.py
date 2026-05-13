
import random
import json
from SPK_UniversalTimestamp import Calendar, UnivMomPrecision, MomPrecLevel
from decimal import Decimal
def main():

    calendars = [
        "Geological",
        "Gregorian",
        "Julian",
        "Hebrew",
        #"Islamic",
        #"Chinese",
        #"Mayan"
    ]
    cases = []
    sample_case = {'index' : -1, 'calendar': 'Gregorian', 'year': 1947, 'month': 1, 'day': 20, 'hour': None, 'minute': None, 'second': None, 'precision': MomPrecLevel[UnivMomPrecision.DAY], 'description': 'Sample case for Gregorian calendar'}
    cases.append(sample_case)
    for i in range(250):
        r = random.randint(0, len(calendars) - 1)
        calendar = calendars[r]
        if calendar == "Geological":
            eon = random.randint(0, 3)  # Randomly choose an eon
            if eon == 0:
                year = str(random.uniform(541, 5000))
                precision = UnivMomPrecision.MILLION_YEARS
                description = "Precambrian eon"
            elif eon == 1:
                year = str(random.uniform(251.9, 541.0))
                precision = UnivMomPrecision.MILLION_YEARS
                description = "Paleozoic era"
            elif eon == 2:
                year = str(random.uniform(66.0, 251.9))
                precision = UnivMomPrecision.MILLION_YEARS
                description = "Mesozoic era"
            else:
                year = str(random.uniform(0.0, 66.0))
                precision = UnivMomPrecision.MILLION_YEARS
                description = "Cenozoic era"
            level = MomPrecLevel[precision]
            month = None
            day = None
            hour = None
            minute = None
            second = None
            pass
        else:
            if calendar == "Gregorian":
                year = random.randint(-5000, 3000)
                month = random.randint(1, 12)
                day = random.randint(1, 28)
            elif calendar == "Julian":
                year = random.randint(-5000, 3000)
                month = random.randint(1, 12)
                day = random.randint(1, 28)
            elif calendar == "Hebrew":
                year = random.randint(-1, 7000)
                month = random.randint(1, 12)
                day = random.randint(1, 28)
            hour = random.randint(0, 23)
            minute = random.randint(0, 59)
            precision = random.choice(list(UnivMomPrecision))
            if MomPrecLevel[precision] > MomPrecLevel[UnivMomPrecision.YEAR]:
                precision = UnivMomPrecision.YEAR
            level = MomPrecLevel[precision]
            if level == MomPrecLevel[UnivMomPrecision.YEAR]:
                month = None
                day = None
                hour = None
                minute = None
                second = None
            elif level == MomPrecLevel[UnivMomPrecision.DAY]:
                hour = None
                minute = None
                second = None   
            elif level == MomPrecLevel[UnivMomPrecision.HOUR]:
                minute = None
                second = None
            elif level == MomPrecLevel[UnivMomPrecision.MINUTE]:
                second = None
            elif level == MomPrecLevel[UnivMomPrecision.SECOND]:
                second = str(Decimal(random.randint(0, 59)))
            elif level == MomPrecLevel[UnivMomPrecision.MILLISECOND]:
                second = str(Decimal(random.randint(0, 59_999))/ 1_000)
            elif level == MomPrecLevel[UnivMomPrecision.MICROSECOND]:
                second = str(Decimal(random.randint(0, 59_999_999))/ 1_000_000) 
            elif level == MomPrecLevel[UnivMomPrecision.NANOSECOND]:
                second = str(Decimal(random.randint(0, 59_999_999_999))/ 1_000_000_000)
            elif level == MomPrecLevel[UnivMomPrecision.PICOSECOND]:
                second = str(Decimal(random.randint(0, 59_999_999_999_999))/ 1_000_000_000_000) 
            elif level == MomPrecLevel[UnivMomPrecision.FEMTOSECOND]:
                second = str(Decimal(random.randint(0, 59_999_999_999_999_999))/ 1_000_000_000_000_000)
            elif level == MomPrecLevel[UnivMomPrecision.ATTOSECOND]:
                second = str(Decimal(random.randint(0, 59_999_999_999_999_999_999))/ 1_000_000_000_000_000_000_000)
            description = f"Random case {i+1} in {calendar} calendar"
        case = {
            'index': i,
            'calendar': calendar,
            'year': year,
            'month': month,
            'day': day,
            'hour': hour,
            'minute': minute,
            'second': second,
            'precision': level,
            'description': description
        }
        cases.append(case)
        
    print(f"Generated {len(cases)} random cases.")
    # Write to JSON file
    with open('Tests\\random_cases.json', "w") as json_file:
        json.dump(cases, json_file, indent=4)
    
    print("Cases saved to Tests\\random_cases.json")
        
            



if __name__ == "__main__":
    main()