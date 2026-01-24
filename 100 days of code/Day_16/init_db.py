"""
Initialize script to set up the coffee machine database with initial data.
Run this once before using the coffee machine for the first time.
"""

from database import DatabaseManager


def initialize_coffee_machine():
    """Initialize the database with some sample coffees and default resources."""
    db = DatabaseManager('Day_16/coffee.db')
    
    # Add sample coffees
    sample_coffees = [
        ("Espresso", 50, 18, 0, 1.50),
        ("Latte", 200, 24, 150, 2.50),
        ("Cappuccino", 250, 24, 100, 2.75),
        ("Americano", 250, 30, 0, 2.00),
        ("Mocha", 200, 20, 150, 3.00),
    ]
    
    print("Initializing coffee machine database...")
    print("\nAdding sample coffees:")
    
    for name, water, coffee, milk, price in sample_coffees:
        success = db.add_coffee(name, water, coffee, milk, price)
        if success:
            print(f"  ✓ {name}: ${price:.2f}")
        else:
            print(f"  - {name}: already exists")
    
    # Initialize resources
    db.update_resources(water=500, coffee=100, milk=500, money=0.0)
    
    print("\nInitializing resources:")
    print("  ✓ Water: 500 ml")
    print("  ✓ Coffee: 100 g")
    print("  ✓ Milk: 500 ml")
    print("  ✓ Money: $0.00")
    
    print("\nDatabase initialization complete!")


if __name__ == "__main__":
    initialize_coffee_machine()
