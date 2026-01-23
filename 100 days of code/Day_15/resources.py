import sqlite3

def add_item():
    
    print("""
          What do you want to add?
          New coffee to menu : 'new'
          Resources : 'res'
          """)
    choice = input("->").strip().lower()
    conn = sqlite3.connect('Day_15/coffee.db')
    cursor = conn.cursor()
    
    match choice:
        case "new":
            coffee_name = input("Coffee name : ")
            water = int(input("Water required (ml) : "))
            coffee = int(input("coffee required (g) : "))
            milk =  int(input("milk required (ml) : "))
            price = float(input("Price of coffee ($) : "))
            try:
                cursor.execute("INSERT INTO coffee (coffee_name,water_required,coffee_required,milk_required,price) VALUES (?,?,?,?,?)",(coffee_name,water,coffee,milk,price))
                conn.commit()
                print(f"{coffee_name} added successfully !!")
            except sqlite3.IntegrityError:
                print(f"Error: '{coffee_name}' already exists in menu!")
            except sqlite3.DataError as e:
                print("Database error:",e)
            finally:
                conn.close()
            input("\nPress Enter to continue...")
            return "menu"
        
        case "res":
            print("""
What resources do you want to add?
You can write: Water, Coffee, Milk
(separated by comma or space, case doesn't matter)
            """)
            
            user_input = input("-> ").strip().lower()
            
            valid_map = {
                "water":  "Water",
                "coffee": "Coffee",
                "milk":   "Milk"
            }

            # Normalize input: replace comma with space, split, clean
            words = [w.strip() for w in user_input.replace(",", " ").split() if w.strip()]
            
            selected = set()
            for w in words:
                if w in valid_map:
                    selected.add(valid_map[w])

            if not selected:
                print("\nNo valid resource names recognized.")
                input("\nPress Enter to continue...")
                return "main"   # or "menu" — decide what feels better

            print("\nSelected:", ", ".join(sorted(selected)))


            updated = False

            try:
                # Check how many rows exist
                cursor.execute("SELECT COUNT(*) FROM resources")
                count = cursor.fetchone()[0]

                if count == 0:
                    print("Resources table is empty → creating initial row with zeros")
                    cursor.execute("INSERT INTO resources DEFAULT VALUES")
                    conn.commit()
                    count = 1

                if count > 1:
                    print("WARNING: Multiple rows found in resources table!")
                    print("         Only the first row will be updated.")
                    print("         This should be fixed in the database design.\n")

                # Get current values (take the "first" row)
                cursor.execute("""
                    SELECT water, coffee, milk 
                    FROM resources 
                    ORDER BY rowid 
                    LIMIT 1
                """)
                row = cursor.fetchone()

                if row is None:
                    print("Unexpected error: could not read resources row")
                else:
                    curr_water, curr_coffee, curr_milk = row

                    updates = []
                    params = []

                    if "Water" in selected:
                        try:
                            amt = int(input(f"How much WATER (ml) to ADD? Current: {curr_water} ml → "))
                            if amt < 0:
                                print("Negative amounts are not allowed → skipped")
                            elif amt == 0:
                                print("Zero amount → skipped")
                            else:
                                updates.append("water = water + ?")
                                params.append(amt)
                                print(f"  → Water will become: {curr_water + amt} ml")
                                updated = True
                        except ValueError:
                            print("Invalid number → water not updated")

                    if "Coffee" in selected:
                        try:
                            amt = int(input(f"How much COFFEE (g) to ADD? Current: {curr_coffee} g → "))
                            if amt < 0:
                                print("Negative amounts are not allowed → skipped")
                            elif amt == 0:
                                print("Zero amount → skipped")
                            else:
                                updates.append("coffee = coffee + ?")
                                params.append(amt)
                                print(f"  → Coffee will become: {curr_coffee + amt} g")
                                updated = True
                        except ValueError:
                            print("Invalid number → coffee not updated")

                    if "Milk" in selected:
                        try:
                            amt = int(input(f"How much MILK (ml) to ADD? Current: {curr_milk} ml → "))
                            if amt < 0:
                                print("Negative amounts are not allowed → skipped")
                            elif amt == 0:
                                print("Zero amount → skipped")
                            else:
                                updates.append("milk = milk + ?")
                                params.append(amt)
                                print(f"  → Milk will become: {curr_milk + amt} ml")
                                updated = True
                        except ValueError:
                            print("Invalid number → milk not updated")

                    if updates:
                        # Build dynamic UPDATE query
                        set_clause = ", ".join(updates)
                        query = f"""
                            UPDATE resources
                            SET {set_clause}
                            WHERE rowid = (
                                SELECT rowid FROM resources ORDER BY rowid LIMIT 1
                            )
                        """
                        cursor.execute(query, params)
                        conn.commit()
                        print("\nResources updated successfully.")
                    else:
                        print("\nNo valid amounts entered → no changes were made.")

            except sqlite3.Error as e:
                print("Database error:", e)
                conn.rollback()
            finally:
                conn.close()

            input("\nPress Enter to continue...")
            return "main"   # or "menu" — your choice      

def remove_item():
    pass

def show_menu():
    conn = sqlite3.connect('Day_15/coffee.db')
    cursor = conn.cursor()
    try:
        cursor.execute("""
SELECT coffee_name,water_required,coffee_required,milk_required,price FROM coffee
""")
        coffees = cursor.fetchall()
        if not coffees:
            print("No coffees available yet.")
            return
        print("Today this things are available !!")
        print("-" * 50)
        print(f"{'No.':<4} {'Coffee':<15} {'Water':<8} {'Coffee':<8} {'Milk':<8} {'Price':>6}")
        print("-" * 50)
        for i,row in enumerate(coffees,1):
            name,water,coffee_amt,milk,price = row
            print(f"{i:<4} {name:<15} {water:<8} {coffee_amt:<8} {milk:<8} ${price:>5.2f}")
        print("-" * 50)
    except sqlite3.Error as e:
        print("Database error:",e)
    finally:
        conn.close()

def generate_report():
    conn = sqlite3.connect('Day_15/coffee.db')
    cursor = conn.cursor()
    try:
        cursor.execute("""
    SELECT water,coffee,milk,money FROM resources LIMIT 1
""")
        resources = cursor.fetchone()
        print("Today this things are available !!")
        print("-" * 50)
        if resources:
            water,coffee,milk,money = resources
            print("\nCurrent Resources:")
            print(f"Water : {water} ml")
            print(f"Coffee: {coffee} g")
            print(f"Milk  : {milk} ml")
            print(f"Money : ${money:.2f}")
            print("-" * 50)
        else:
            print("No resources data found.")
    except sqlite3.Error as e:
        print("Database error:",e)
    finally:
        conn.close()
