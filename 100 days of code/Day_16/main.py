from database import DatabaseManager
from machine import CoffeeMachine


def main():
    """Entry point for the coffee machine application."""
    # Initialize database
    db = DatabaseManager('Day_16/coffee.db')
    
    # Create and run the coffee machine
    machine = CoffeeMachine(db)
    machine.run()


if __name__ == "__main__":
    main()
