import sqlite3
import os

DB_PATH = os.getenv("DATABASE_PATH", "/app/sqlitedb/Game_Data.db")

# Ensure the directory exists
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

def initialize():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Use 'IF NOT EXISTS' to make the script idempotent
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS game_data (
            name_of_table VARCHAR(100) PRIMARY KEY,
            in_1 INTEGER,
            in_2 INTEGER,
            in_3 INTEGER,
            in_4 INTEGER,
            in_5 INTEGER,
            in_6 INTEGER,
            in_7 INTEGER, 
            in_8 INTEGER,
            in_9 INTEGER,
            in_10 INTEGER      
            )"""
        )
    
    conn.commit()
    conn.close()
    print(f"Database initialized at {DB_PATH}")

if __name__ == "__main__":
    initialize()