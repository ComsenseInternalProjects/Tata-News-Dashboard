import sqlite3

def display_table_names():
    conn = sqlite3.connect('src/tata_news.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    print("Tables in the database:")
    for table in tables:
        print(table[0])
    
    conn.close()

def display_table_contents(table_name):
    conn = sqlite3.connect('src/tata_news.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    
    # Get column names
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [description[1] for description in cursor.fetchall()]
    
    print(f"\nContents of {table_name} table:")
    print(", ".join(columns))
    for row in rows:
        print(row)
    
    conn.close()

if __name__ == "__main__":
    display_table_names()
    
    try:
        display_table_contents('bulk_news')
    except sqlite3.OperationalError as e:
        print(f"Error: {e}")
    
    # try:
    #     display_table_contents('automobile_industry')
    # except sqlite3.OperationalError as e:
    #     print(f"Error: {e}")
