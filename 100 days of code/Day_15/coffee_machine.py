from art import logo
from resources import add_item,remove_item,show_menu,generate_report
import os
from typing import Callable
from coins import order

StateHandler = Callable[[],str]
STATE = "main"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def main_menu()->str | None:
    clear_screen()
    print(logo)
    print("""
    "What would you like?
          \n
    Type 'Menu' to check items
    Type 'Report' to see report of vending machine
    Type 'Add' to add item in machine
    Type 'Remove' to delete item from machine
    Type 'exit' to turn off machine"
""")
    choice = input("-> ").strip().lower()
    match choice:
        case "menu":
            return "menu"
        case "report":
            generate_report()
            input("\nPress enter to continue....")
            return "main"
        case "add":
            add_item()
            input("\nPress enter to continue....")
            return "main"
        case "remove":
            remove_item()
            input("\nPress enter to continue....")
            return "main"
        case "exit":
            print("Have a nice day, GoodBye !!")
            return "exit"
        case _:
            print("Invalid choice")
            input("\nPress Enter...")
            return "main"

def menu_screen()->str|None:
    clear_screen()
    show_menu()
    print("\nOptions")
    print("Type 'Order' to place an order")
    print("Type 'Back' to place an order")
    choice = input("-> ").strip().lower()
    match choice:
        case "order":
            order()
            input("\n Press Enter...")
            return "main"
        case "back":
            return "main"
        case _:
            print("Please type order or back")
            input("\n Press Enter...")
            return "menu"

HANDLERS:dict[str,StateHandler] = {
    "main":main_menu,
    "menu":menu_screen
}  

def run():
    global STATE
    STATE = "main"
    while STATE != "exit":
        handler = HANDLERS.get(STATE)
        if not handler:
            print(f"Error: Unknown state {STATE}")
            STATE = "main"
            continue
        next_state = handler()
        if next_state is not None:
            STATE = next_state

if __name__ == "__main__":
    run()