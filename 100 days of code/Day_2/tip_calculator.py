print("Welcome to the tip calculator !!")
Bill = float(input("What was the total bill ? $"))
Tip = int(input("How much tip would you like to give ? 10, 12, or 15 %?"+" "))
People = int(input("How many people to split the bill? "))
tip_percent = Tip/100
ans = (Bill + (Bill*tip_percent))/People
print(f"Each person should pay : ${ans:.2f}")