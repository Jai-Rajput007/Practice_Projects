from database import DatabaseManager


class Coffee:
    """Represents a coffee item on the menu."""
    
    def __init__(self, name: str, water_required: int, coffee_required: int, 
                 milk_required: int, price: float):
        self.name = name
        self.water_required = water_required
        self.coffee_required = coffee_required
        self.milk_required = milk_required
        self.price = price
    
    def __repr__(self):
        return f"Coffee({self.name}, ${self.price:.2f})"
    
    def get_requirements(self) -> dict:
        """Get resource requirements for this coffee."""
        return {
            "water": self.water_required,
            "coffee": self.coffee_required,
            "milk": self.milk_required
        }


class Resources:
    """Manages the resources of the coffee machine."""
    
    def __init__(self, db: DatabaseManager):
        self.db = db
        self._load_resources()
    
    def _load_resources(self):
        """Load current resources from database."""
        water, coffee, milk, money = self.db.get_resources()
        self.water = water
        self.coffee = coffee
        self.milk = milk
        self.money = money
    
    def is_sufficient(self, requirements: dict) -> bool:
        """Check if resources are sufficient for a coffee."""
        return (self.water >= requirements["water"] and
                self.coffee >= requirements["coffee"] and
                self.milk >= requirements["milk"])
    
    def deduct(self, requirements: dict) -> bool:
        """Deduct resources for a coffee order."""
        if not self.is_sufficient(requirements):
            return False
        
        self.water -= requirements["water"]
        self.coffee -= requirements["coffee"]
        self.milk -= requirements["milk"]
        
        self.db.subtract_resources(
            water=requirements["water"],
            coffee=requirements["coffee"],
            milk=requirements["milk"]
        )
        return True
    
    def add_water(self, amount: int):
        """Add water to resources."""
        self.water += amount
        self.db.add_resources(water=amount)
    
    def add_coffee(self, amount: int):
        """Add coffee to resources."""
        self.coffee += amount
        self.db.add_resources(coffee=amount)
    
    def add_milk(self, amount: int):
        """Add milk to resources."""
        self.milk += amount
        self.db.add_resources(milk=amount)
    
    def add_money(self, amount: float):
        """Add money to resources."""
        self.money += amount
        self.db.add_resources(money=amount)
    
    def get_status(self) -> dict:
        """Get current status of all resources."""
        return {
            "water": self.water,
            "coffee": self.coffee,
            "milk": self.milk,
            "money": self.money
        }
    
    def display_report(self):
        """Display resource report."""
        print("=" * 50)
        print("Current Resources:")
        print(f"Water : {self.water} ml")
        print(f"Coffee: {self.coffee} g")
        print(f"Milk  : {self.milk} ml")
        print(f"Money : ${self.money:.2f}")
        print("=" * 50)
