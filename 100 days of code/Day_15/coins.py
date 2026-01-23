import sqlite3
from art import coffee_logo
coins = {
    "Penny" : 0.01,
    "Dime": 0.10,
    "Nickel":0.05,
    "Quarter":0.25
}

def order():
    conn = sqlite3.connect('Day_15/coffee.db')
    cursor = conn.cursor()
    print("What you wanna order??")
    order = input("->").strip()
    try:
        cursor.execute("SELECT coffee_name, price FROM coffee WHERE coffee_name = ?",(order,))
        row = cursor.fetchone()
        if row is None:
            print(f"Sorry, '{order}' is not available in the menu.")
            input("\nPress Enter to continue.....")
            return "menu"
        name, price = row        
        print(f"To place order of {name} you need to pay {price}")
        decision = transact(price)
        if decision:
            cursor.execute("UPDATE resources SET money = money + ? WHERE rowid = 1",(price,))
            conn.commit()
            print(f"Here is your {name} !!")
            print(coffee_logo)
            print("Keep visiting us....")                 
        else:
            print("Payment issues \n Try again.....")

    except sqlite3.Error as e:
            print("Database error:", e)
        
    finally:
        conn.close()
        input("\nPress Enter to continue...")
        return "main"

def transact(price: float) -> bool:
    print("You can pay with: Penny (0.01), Dime (0.10), Nickel (0.05), Quarter (0.25)")
    
    try:
        pennies  = int(input("How many pennies?   → ") or 0)
        dimes    = int(input("How many dimes?     → ") or 0)
        nickels  = int(input("How many nickels?   → ") or 0)
        quarters = int(input("How many quarters?  → ") or 0)
    except ValueError:
        print("Invalid input — payment cancelled.")
        return False

    total_paid = (
        pennies  * 0.01 +
        dimes    * 0.10 +
        nickels  * 0.05 +
        quarters * 0.25
    )
    
    if total_paid < price:
        shortfall = price - total_paid
        print(f"You paid ${total_paid:.2f} — ${shortfall:.2f} short.")
        return False
    
    elif total_paid > price:
        change = total_paid - price
        print(f"Here is your change: ${change:.2f}")
    
    print("Payment accepted. Order completed.")
    return True
    
