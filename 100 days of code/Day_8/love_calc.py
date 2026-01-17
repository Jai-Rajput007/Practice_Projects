print("*"*40)
print("Welcome to Love calculator !!")
name_1 = list(input("Enter first Person's name : ").upper().strip())
name_2 = list(input("Enter second Person's name : ").upper().strip())

true = ['T','R','U','E']
love = ['L','O','V','E']
print(name_1)
count_1 = 0
count_2 = 0
name_1.extend(name_2)
combine_name = name_1

for i in range(len(combine_name)):
    if combine_name[i] in true:
        count_1 += 1

for i in range(len(combine_name)):
    if combine_name[i] in love:
        count_2 += 1

print(f"Your love score is : {count_1}{count_2}")
print("*"*40)