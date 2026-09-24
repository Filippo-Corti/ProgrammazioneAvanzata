# The Calendar Module
import calendar

# 3)
CURR_YEAR = 2026
print(next(
    year
    for year in range(CURR_YEAR, CURR_YEAR+8)
    if calendar.isleap(year)
))

# 4)
START_YEAR = 2000
END_YEAR = 2050
print(calendar.leapdays(START_YEAR, END_YEAR + 1))

# 5)
DATE = '2016-07-29'
dateaslist = [int(n) for n in DATE.split('-')]
print(calendar.day_name[
    calendar.weekday(dateaslist[0], dateaslist[1], dateaslist[2])
])
