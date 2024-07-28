import sqlite3
import os

def where_at(character_name):
    DATABASE = "db/swgoh_database.sqlite"  # Path to your SQLite database file

    with sqlite3.connect(DATABASE) as conn:
        conn.row_factory = sqlite3.Row  # This allows us to access columns by name
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT planet, GROUP_CONCAT(operations, ', ') AS operations
            FROM platoons 
            WHERE character_name LIKE ? AND phase < 5
            AND planet != 'Zeffo'
            GROUP BY planet
        """, (character_name,))
        
        units = cursor.fetchall()

    message = ""
    for unit in units:
        message += f"{unit['planet']} {unit['operations']}\n"
    
    return message
