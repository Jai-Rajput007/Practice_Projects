import sqlite3
from typing import List, Optional, Tuple


class DatabaseManager:
    """Manages all database operations for the coffee machine."""
    
    def __init__(self, db_path: str = 'Day_16/coffee.db'):
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """Initialize database with required tables if they don't exist."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Create coffee table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS coffee (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                coffee_name TEXT UNIQUE NOT NULL,
                water_required INTEGER NOT NULL,
                coffee_required INTEGER NOT NULL,
                milk_required INTEGER NOT NULL,
                price REAL NOT NULL
            )
        """)
        
        # Create resources table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS resources (
                id INTEGER PRIMARY KEY,
                water INTEGER DEFAULT 0,
                coffee INTEGER DEFAULT 0,
                milk INTEGER DEFAULT 0,
                money REAL DEFAULT 0.0
            )
        """)
        
        # Ensure at least one resources row exists
        cursor.execute("SELECT COUNT(*) FROM resources")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO resources (water, coffee, milk, money) VALUES (0, 0, 0, 0.0)")
        
        conn.commit()
        conn.close()
    
    def get_connection(self):
        """Get a database connection."""
        return sqlite3.connect(self.db_path)
    
    # Coffee operations
    def add_coffee(self, name: str, water: int, coffee: int, milk: int, price: float) -> bool:
        """Add a new coffee to the menu."""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO coffee (coffee_name, water_required, coffee_required, milk_required, price) VALUES (?, ?, ?, ?, ?)",
                (name, water, coffee, milk, price)
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()
    
    def remove_coffee(self, name: str) -> bool:
        """Remove a coffee from the menu."""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM coffee WHERE coffee_name = ?", (name,))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()
    
    def get_all_coffees(self) -> List[Tuple]:
        """Get all coffees from the menu."""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT coffee_name, water_required, coffee_required, milk_required, price FROM coffee ORDER BY coffee_name")
            return cursor.fetchall()
        finally:
            conn.close()
    
    def get_coffee(self, name: str) -> Optional[Tuple]:
        """Get a specific coffee by name."""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT coffee_name, water_required, coffee_required, milk_required, price FROM coffee WHERE coffee_name = ?", (name,))
            return cursor.fetchone()
        finally:
            conn.close()
    
    # Resources operations
    def get_resources(self) -> Tuple[int, int, int, float]:
        """Get current resources (water, coffee, milk, money)."""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT water, coffee, milk, money FROM resources LIMIT 1")
            row = cursor.fetchone()
            return row if row else (0, 0, 0, 0.0)
        finally:
            conn.close()
    
    def update_resources(self, water: int = None, coffee: int = None, milk: int = None, money: float = None) -> bool:
        """Update resources. Use None to skip updating a field."""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            updates = []
            params = []
            
            if water is not None:
                updates.append("water = ?")
                params.append(water)
            if coffee is not None:
                updates.append("coffee = ?")
                params.append(coffee)
            if milk is not None:
                updates.append("milk = ?")
                params.append(milk)
            if money is not None:
                updates.append("money = ?")
                params.append(money)
            
            if not updates:
                return True
            
            query = f"UPDATE resources SET {', '.join(updates)} WHERE id = 1"
            cursor.execute(query, params)
            conn.commit()
            return True
        finally:
            conn.close()
    
    def add_resources(self, water: int = 0, coffee: int = 0, milk: int = 0, money: float = 0.0) -> bool:
        """Add (increment) resources."""
        curr_water, curr_coffee, curr_milk, curr_money = self.get_resources()
        return self.update_resources(
            water=curr_water + water,
            coffee=curr_coffee + coffee,
            milk=curr_milk + milk,
            money=curr_money + money
        )
    
    def subtract_resources(self, water: int = 0, coffee: int = 0, milk: int = 0) -> bool:
        """Subtract (decrement) resources."""
        curr_water, curr_coffee, curr_milk, curr_money = self.get_resources()
        return self.update_resources(
            water=curr_water - water,
            coffee=curr_coffee - coffee,
            milk=curr_milk - milk
        )
