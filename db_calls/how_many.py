import sqlite3
import os

def get_number(character_name):
    DATABASE = "db/swgoh_database.sqlite"  # Path to your SQLite database file
    
    with sqlite3.connect(DATABASE) as conn:
        conn.row_factory = sqlite3.Row  # This allows us to access columns by name
        cursor = conn.cursor()
        
        # Using LOWER for case-insensitive comparison
        cursor.execute("SELECT player_name, relic, rarity FROM playerunits WHERE LOWER(character_name) = LOWER(?) ORDER BY relic DESC, rarity DESC", (character_name,))
        
        units = cursor.fetchall()
    
    message = ""
    for unit in units:
        message += f"{unit['player_name']}: relic {unit['relic']}, stars {unit['rarity']}\n"
    
    return message
