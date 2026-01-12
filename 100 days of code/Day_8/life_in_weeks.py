from datetime import datetime,timedelta
from dateutil.relativedelta import relativedelta
print("To know how many weeks left\n" \
    "Enter Your Birth Date!! ")
Date = int(input("Enter Date (1-31) : "))
Month = int(input("Enter Month (1-12) : "))
Year = int(input("Enter Year : "))

final_years = 90
b_day = datetime(Year,Month,Date)

future_date = b_day + relativedelta(years=final_years)
curr_date = datetime.now()

ans_date = future_date - curr_date

days_left = ans_date.days
weeks_left = days_left/7
whole_weeks = days_left // 7
extra_days  = days_left % 7

print(f"Today: {curr_date:%d %b %Y}")
print(f"Days remaining: {days_left:,d}")
print(f"Weeks remaining:  ≈ {weeks_left:,.1f} weeks")
print(f"                  = {whole_weeks:,d} weeks + {extra_days} days")