import sqlite3

# ============================================================================
# 1. USER DEFINED FUNCTION (UDF) - Currency Conversion
# ============================================================================

def py_convert_currency(amount, rate):
    
    if amount is None or rate is None:
        return None
    return round(amount * rate, 2)


# ============================================================================
# 2. USER DEFINED AGGREGATE (UDA) - Spending Gap/Volatility
# ============================================================================

class VolatilityClass:
    """
    Custom aggregate to calculate spending volatility (Max - Min).
    Methods:
        step(): Called for each row in group, accumulates min/max
        finalize(): Returns final result (spending gap)
    """
    
    def __init__(self):
        """Initialize tracking variables for min/max"""
        self.max_amount = None
        self.min_amount = None
    
    def step(self, amount):
        """
        Called for each row in a group.
        Updates min and max spending amounts.
        """
        if amount is None:
            return
        
        if self.max_amount is None:
            self.max_amount = amount
            self.min_amount = amount
        else:
            if amount > self.max_amount:
                self.max_amount = amount
            if amount < self.min_amount:
                self.min_amount = amount
    
    def finalize(self):
        """
        Called after all rows processed.
        Returns Max - Min (spending gap).
        """
        if self.max_amount is None or self.min_amount is None:
            return 0
        return round(self.max_amount - self.min_amount, 2)


# ============================================================================
# 3. SETUP FUNCTION - Register Custom Tools
# ============================================================================

def register_custom_tools(conn):
    """
    Registers UDFs and UDAs with the db_manager connection.
    
    Parameters:
        conn: SQLite db_manager connection
        
    Process:
        1. Register py_convert_currency as UDF
           - Function name in SQL: 'py_convert_currency'
           - Number of parameters: 2
        2. Register VolatilityClass as UDA
           - Function name in SQL: 'VolatilityClass'
           - Number of parameters: 1
    """
    # Register UDF for currency conversion
    conn.create_function("py_convert_currency", 2, py_convert_currency)
    
    # Register UDA for spending volatility
    conn.create_aggregate("VolatilityClass", 1, VolatilityClass)
    
    print("Custom tools registered successfully")


# ============================================================================
# 4. REPORT GENERATION - Summary with Custom Functions
# ============================================================================

def get_summary_report(conn=None):
    """
    Generates a comprehensive spending summary report.
    
    Process:
        1. Get db_manager connection
        2. Set row_factory to sqlite3.Row (enables column name access)
        3. Execute SQL query that:
           - JOINs Categories with Expenses
           - Uses SUM(amount) for total spending per category
           - Uses VolatilityClass(amount) for spending gap per category
           - Uses py_convert_currency for currency conversion (optional)
           - GROUP BY category
        4. Fetch all results
        5. Format and return results as list of Row objects
    
    Returns:
        List of Row objects with:
            - category name
            - total spending
            - spending gap (volatility)
            - other relevant metrics
    """
    # Import get_connection from db_manager module
    from db_manager import get_connection
    
    # Get connection if not provided
    if conn is None:
        conn = get_connection('data/budget.db')
    
    # Set row factory to enable column name access
    conn.row_factory = sqlite3.Row
    
    cursor = conn.cursor()
    
    # SQL Query with JOINs and custom functions
    query = """
    SELECT 
        c.id,
        c.name AS category_name,
        COUNT(e.id) AS transaction_count,
        SUM(e.amount) AS total_spending,
        ROUND(AVG(e.amount), 2) AS average_spending,
        VolatilityClass(e.amount) AS spending_gap,
        MAX(e.date) AS last_transaction_date,
        py_convert_currency(SUM(e.amount), 1.2) AS converted_amount_usd
    FROM 
        Categories c
    LEFT JOIN 
        Expenses e ON c.id = e.category_id
    GROUP BY 
        c.id, c.name
    ORDER BY 
        total_spending DESC
    """
    
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        return results
    
    except sqlite3.Error as e:
        print(f"Query failed: {e}")
        return []
    
    finally:
        conn.close()


# ============================================================================
# 5. ADDITIONAL ANALYTICS FUNCTIONS
# ============================================================================

def get_category_breakdown(category_id, conn=None):
    """
    Get detailed breakdown for a specific category.
    
    Parameters:
        category_id: ID of the category
        conn: Db_manager connection
    
    Returns:
        List of expenses for that category with volatility
    """
    from db_manager import get_connection
    
    if conn is None:
        conn = get_connection('data/budget.db')
    
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    query = """
    SELECT 
        e.id,
        e.amount,
        e.date,
        py_convert_currency(e.amount, 1.2) AS converted_amount
    FROM 
        Expenses e
    WHERE 
        e.category_id = ?
    ORDER BY 
        e.date DESC
    """
    
    try:
        cursor.execute(query, (category_id,))
        return cursor.fetchall()
    
    except sqlite3.Error as e:
        print(f"Query failed: {e}")
        return []
    
    finally:
        conn.close()


def get_spending_trends(conn=None):
    """
    Get spending trends across all categories.
    Shows which categories have highest volatility.
    
    Parameters:
        conn: Db_manager connection
    
    Returns:
        List of categories with spending gaps, ordered by volatility
    """
    from db_manager import get_connection
    
    if conn is None:
        conn = get_connection('data/budget.db')
    
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    query = """
    SELECT 
        c.name,
        VolatilityClass(e.amount) AS spending_volatility,
        SUM(e.amount) AS total_amount,
        COUNT(e.id) AS num_transactions
    FROM 
        Categories c
    LEFT JOIN 
        Expenses e ON c.id = e.category_id
    GROUP BY 
        c.id, c.name
    HAVING 
        VolatilityClass(e.amount) > 0
    ORDER BY 
        spending_volatility DESC
    """
    
    try:
        cursor.execute(query)
        return cursor.fetchall()
    
    except sqlite3.Error as e:
        print(f"Query failed: {e}")
        return []
    
    finally:
        conn.close()


# ============================================================================
# 6. USAGE EXAMPLE (Main Block)
# ============================================================================

if __name__ == "__main__":
    # Import db_manager functions
    from db_manager import get_connection
    
    # Step 1: Get connection
    conn = get_connection('data/budget.db')
    
    # Step 2: Register custom tools
    register_custom_tools(conn)
    
    # Step 3: Generate and display summary report
    print("\n" + "="*80)
    print("SPENDING SUMMARY REPORT")
    print("="*80)
    report = get_summary_report(conn)
    
    if report:
        for row in report:
            print(f"\nCategory: {row['category_name']}")
            print(f"  Total Spending: ${row['total_spending']:.2f}" if row['total_spending'] else "  Total Spending: $0.00")
            print(f"  Transactions: {row['transaction_count']}")
            print(f"  Average Spending: ${row['average_spending']:.2f}" if row['average_spending'] else "  Average Spending: $0.00")
            print(f"  Spending Gap (Volatility): ${row['spending_gap']:.2f}")
            print(f"  Converted Amount (USD): ${row['converted_amount_usd']:.2f}" if row['converted_amount_usd'] else "  Converted Amount (USD): $0.00")
            print(f"  Last Transaction: {row['last_transaction_date']}")
    else:
        print("No data available")
    
    # Step 4: Display spending trends
    print("\n" + "="*80)
    print("SPENDING TRENDS (By Volatility)")
    print("="*80)
    trends = get_spending_trends(conn)
    
    if trends:
        for row in trends:
            print(f"\n{row['name']}: Volatility ${row['spending_volatility']:.2f}")
            print(f"  Total: ${row['total_amount']:.2f}" if row['total_amount'] else "  Total: $0.00")
            print(f"  Transactions: {row['num_transactions']}")
    else:
        print("No trend data available")