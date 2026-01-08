import sqlite3

def get_connection(file:str):
    try:
        conn = sqlite3.connect(file)
        conn.execute("PRAGMA foreign_keys = ON")
        print(f"Connection established with {file}")
        return conn
    except FileNotFoundError:
        print(f"{file} not found")
    except sqlite3.Error as e:
        print(f"Database error:{e}")

def initialize_schema():
    conn = get_connection('data/budget.db')
    cursor = conn.cursor()
    script =  """

    CREATE TABLE IF NOT EXISTS "Categories"(
    "id" INTEGER PRIMARY KEY,
    "name" TEXT UNIQUE NOT NULL
    );

    CREATE TABLE IF NOT EXISTS "Expenses"(
    "id" INTEGER PRIMARY KEY ,
    "amount" REAL NOT NULL,
    "category_id" INTEGER,
    "date" TEXT,
    FOREIGN KEY("category_id") REFERENCES "Categories"("id")
    );

    CREATE TABLE IF NOT EXISTS "Income"(
    "id" INTEGER PRIMARY KEY, 
    "amount" REAL NOT NULL
    );

        """
    cursor.executescript(script)
    conn.commit()
    conn.close()
    
def add_expense(amount,category_id,date):
    conn = get_connection('data/budget.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO 'Expenses'('amount','category_id','date') VALUES (?,?,?);",(amount,category_id,date))
    conn.commit()
    conn.close()

def bulk_insert(data):
    conn = get_connection('data/budget.db')
    cursor = conn.cursor()
    cursor.executemany("INSERT INTO 'Expenses'('amount','category_id','date') VALUES (?,?,?);",data)
    conn.commit()
    conn.close()

def transfer_funds(from_cat,to_cat,amount):
    conn = get_connection('data/budget.db')
    cursor = conn.cursor()
    conn.execute("BEGIN")
    try:
        cursor.execute(f"UPDATE 'Expenses' SET 'amount'= amount - ? WHERE 'id' = ? ",(amount,from_cat))
        cursor.execute(f"UPDATE 'Expenses' SET 'amount'= amount + ? WHERE 'id' = ? " ,(amount,to_cat))
        conn.commit()
    except sqlite3.Error as  e:
        conn.rollback()
        print(f"Transaction failed: {e}")
    finally :
        conn.close()


