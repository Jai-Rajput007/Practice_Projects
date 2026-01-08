import random
import string

def pass_gen():
    print("Welcome to the Password Generator!\n")
    letters = int(input("How many letters you want in your password? \n"))
    symbols = int(input("How many Symbols you want in your password? \n"))
    numbers = int(input("How many numbers you want in your password? \n"))

    letter = string.ascii_letters
    symbol = string.punctuation
    number = string.digits

    Use_letters = random.choices(letter,k=letters)
    Use_symbols = random.choices(symbol,k=symbols)
    Use_number = random.choices(number,k=numbers)
    
    all_chars = Use_letters + Use_number + Use_symbols

    random.shuffle(all_chars)
    random.shuffle(all_chars)
    passwd = "".join(all_chars)
    
    print(f"\nThis is you strong password : {passwd}\n")
    
pass_gen()