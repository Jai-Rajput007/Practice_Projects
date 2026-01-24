import os
from typing import Optional
from database import DatabaseManager
from models import Coffee, Resources
from payment import PaymentProcessor
from art import logo, coffee_logo


class CoffeeMachine:
    """Main coffee machine class that manages the entire operation."""
    
    def __init__(self, db: DatabaseManager):
        self.db = db
        self.resources = Resources(db)
        self.state = "main"
        self.running = True
    
    @staticmethod
    def clear_screen():
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_main_menu(self) -> Optional[str]:
        """Display main menu and get user choice."""
        self.clear_screen()
        print(logo)
        print("""
    "What would you like?
          \n
    Type 'Menu' to check items
    Type 'Report' to see report of vending machine
    Type 'Add' to add item in machine
    Type 'Remove' to delete item from machine
    Type 'Exit' to turn off machine"
""")
        choice = input("-> ").strip().lower()
        
        match choice:
            case "menu":
                return "menu"
            case "report":
                self._show_report()
                input("\nPress enter to continue....")
                return "main"
            case "add":
                self._add_menu()
                input("\nPress enter to continue....")
                return "main"
            case "remove":
                self._remove_menu()
                input("\nPress enter to continue....")
                return "main"
            case "exit":
                print("Have a nice day, GoodBye !!")
                self.running = False
                return "exit"
            case _:
                print("Invalid choice")
                input("\nPress Enter...")
                return "main"
    
    def display_menu_screen(self) -> Optional[str]:
        """Display menu of available coffees."""
        self.clear_screen()
        self._show_menu()
        print("\nOptions")
        print("Type 'Order' to place an order")
        print("Type 'Back' to go back")
        choice = input("-> ").strip().lower()
        
        match choice:
            case "order":
                self._process_order()
                input("\nPress Enter...")
                return "main"
            case "back":
                return "main"
            case _:
                print("Please type 'order' or 'back'")
                input("\nPress Enter...")
                return "menu"
    
    def _show_menu(self):
        """Display all available coffees."""
        coffees = self.db.get_all_coffees()
        if not coffees:
            print("No coffees available yet.")
            return
        
        print("Today these items are available!!")
        print("-" * 60)
        print(f"{'No.':<4} {'Coffee':<15} {'Water':<8} {'Coffee':<8} {'Milk':<8} {'Price':>6}")
        print("-" * 60)
        
        for i, (name, water, coffee, coffee_amt, milk, price) in enumerate(coffees, 1):
            print(f"{i:<4} {name:<15} {water:<8} {coffee_amt:<8} {milk:<8} ${price:>5.2f}")
        
        print("-" * 60)
    
    def _show_report(self):
        """Show machine resources report."""
        print("\n" + "=" * 50)
        print("COFFEE MACHINE REPORT")
        self.resources.display_report()
    
    def _process_order(self):
        """Process a coffee order."""
        order_name = input("\nWhat coffee would you like? -> ").strip()
        
        coffee_data = self.db.get_coffee(order_name)
        if coffee_data is None:
            print(f"Sorry, '{order_name}' is not available in the menu.")
            return
        
        name, water, coffee, milk, price = coffee_data
        coffee_obj = Coffee(name, water, coffee, milk, price)
        
        print(f"\nTo order {coffee_obj.name}, you need to pay ${price:.2f}")
        
        if not PaymentProcessor.process_payment(price):
            print("Order cancelled.")
            return
        
        # Check if resources are sufficient
        if not self.resources.is_sufficient(coffee_obj.get_requirements()):
            print("Sorry, not enough resources to make this coffee.")
            return
        
        # Make the coffee
        self.resources.deduct(coffee_obj.get_requirements())
        self.resources.add_money(price)
        
        print(f"\nHere is your {coffee_obj.name}!!")
        print(coffee_logo)
        print("Keep visiting us....")
    
    def _add_menu(self):
        """Menu for adding items/resources."""
        print("""
          What do you want to add?
          New coffee to menu : 'new'
          Resources : 'res'
          """)
        choice = input("->").strip().lower()
        
        if choice == "new":
            self._add_coffee()
        elif choice == "res":
            self._add_resources()
        else:
            print("Invalid choice")
    
    def _add_coffee(self):
        """Add a new coffee to the menu."""
        coffee_name = input("Coffee name : ").strip()
        water = int(input("Water required (ml) : "))
        coffee = int(input("Coffee required (g) : "))
        milk = int(input("Milk required (ml) : "))
        price = float(input("Price of coffee ($) : "))
        
        if self.db.add_coffee(coffee_name, water, coffee, milk, price):
            print(f"{coffee_name} added successfully!!")
        else:
            print(f"Error: '{coffee_name}' already exists in menu!")
    
    def _add_resources(self):
        """Add resources to the machine."""
        print("""
Which resources do you want to add?
You can write: Water, Coffee, Milk
(separated by comma or space, case doesn't matter)
        """)
        
        user_input = input("-> ").strip().lower()
        valid_map = {
            "water": "Water",
            "coffee": "Coffee",
            "milk": "Milk"
        }
        
        words = [w.strip() for w in user_input.replace(",", " ").split() if w.strip()]
        selected = {valid_map[w] for w in words if w in valid_map}
        
        if not selected:
            print("\nNo valid resource names recognized.")
            return
        
        print("\nSelected:", ", ".join(sorted(selected)))
        
        if "Water" in selected:
            try:
                amt = int(input(f"How much WATER (ml) to ADD? Current: {self.resources.water} ml → "))
                if amt > 0:
                    self.resources.add_water(amt)
                    print(f"  → Water will become: {self.resources.water} ml")
            except ValueError:
                print("Invalid number")
        
        if "Coffee" in selected:
            try:
                amt = int(input(f"How much COFFEE (g) to ADD? Current: {self.resources.coffee} g → "))
                if amt > 0:
                    self.resources.add_coffee(amt)
                    print(f"  → Coffee will become: {self.resources.coffee} g")
            except ValueError:
                print("Invalid number")
        
        if "Milk" in selected:
            try:
                amt = int(input(f"How much MILK (ml) to ADD? Current: {self.resources.milk} ml → "))
                if amt > 0:
                    self.resources.add_milk(amt)
                    print(f"  → Milk will become: {self.resources.milk} ml")
            except ValueError:
                print("Invalid number")
        
        print("\nResources updated successfully.")
    
    def _remove_menu(self):
        """Menu for removing items/resources."""
        print("""
What do you want to remove?
Remove coffee from menu  : 'coffee' or 'menu'
Remove resources         : 'res' or 'resources'
        """)
        choice = input("-> ").strip().lower()
        
        if choice in ["coffee", "menu"]:
            self._remove_coffee()
        elif choice in ["res", "resources"]:
            self._remove_resources()
        else:
            print("Invalid choice")
    
    def _remove_coffee(self):
        """Remove a coffee from the menu."""
        coffees = self.db.get_all_coffees()
        
        if not coffees:
            print("\nNo coffees in the menu yet.")
            return
        
        print("\nCurrent menu:")
        print("-" * 40)
        for i, (name, *_) in enumerate(coffees, 1):
            print(f"{i:2d}. {name}")
        print("-" * 40)
        
        to_remove = input("\nEnter the exact coffee name to remove (or 'cancel'): ").strip()
        
        if to_remove.lower() in ["cancel", "c", ""]:
            print("Operation cancelled.")
            return
        
        confirm = input(f"Are you sure you want to DELETE '{to_remove}'? (yes/no): ").strip().lower()
        if confirm in ["yes", "y"]:
            if self.db.remove_coffee(to_remove):
                print(f"\n'{to_remove}' has been removed from the menu.")
            else:
                print(f"\n'{to_remove}' not found in menu.")
        else:
            print("Deletion cancelled.")
    
    def _remove_resources(self):
        """Remove/subtract resources from the machine."""
        print("""
Which resources do you want to remove/subtract?
You can write: Water, Coffee, Milk
(separated by comma or space, case insensitive)
        """)
        
        user_input = input("-> ").strip().lower()
        valid_map = {
            "water": "Water",
            "coffee": "Coffee",
            "milk": "Milk"
        }
        
        words = [w.strip() for w in user_input.replace(",", " ").split() if w.strip()]
        selected = {valid_map[w] for w in words if w in valid_map}
        
        if not selected:
            print("\nNo valid resource names recognized.")
            return
        
        print("\nSelected:", ", ".join(sorted(selected)))
        
        if "Water" in selected:
            try:
                amt = int(input(f"How much WATER (ml) to REMOVE? Current: {self.resources.water} ml → "))
                if amt > 0 and amt <= self.resources.water:
                    self.resources.water -= amt
                    self.db.subtract_resources(water=amt)
                    print(f"  → Water will become: {self.resources.water} ml")
                else:
                    print("Invalid amount")
            except ValueError:
                print("Invalid number")
        
        if "Coffee" in selected:
            try:
                amt = int(input(f"How much COFFEE (g) to REMOVE? Current: {self.resources.coffee} g → "))
                if amt > 0 and amt <= self.resources.coffee:
                    self.resources.coffee -= amt
                    self.db.subtract_resources(coffee=amt)
                    print(f"  → Coffee will become: {self.resources.coffee} g")
                else:
                    print("Invalid amount")
            except ValueError:
                print("Invalid number")
        
        if "Milk" in selected:
            try:
                amt = int(input(f"How much MILK (ml) to REMOVE? Current: {self.resources.milk} ml → "))
                if amt > 0 and amt <= self.resources.milk:
                    self.resources.milk -= amt
                    self.db.subtract_resources(milk=amt)
                    print(f"  → Milk will become: {self.resources.milk} ml")
                else:
                    print("Invalid amount")
            except ValueError:
                print("Invalid number")
        
        print("\nResources updated successfully.")
    
    def run(self):
        """Main loop for the coffee machine."""
        self.state = "main"
        
        while self.running:
            if self.state == "main":
                self.state = self.display_main_menu()
            elif self.state == "menu":
                self.state = self.display_menu_screen()
            else:
                break
