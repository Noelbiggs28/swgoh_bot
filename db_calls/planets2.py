import sqlite3
import os

def planets_check2(planet1, planet2, all):
    DATABASE = "db/swgoh_database.sqlite"  # Path to your SQLite database file

    with sqlite3.connect(DATABASE) as conn:
        conn.row_factory = sqlite3.Row  # This allows us to access columns by name
        cursor = conn.cursor()

        cursor.execute("""
WITH aggregated_platoons AS (
    SELECT 
        p.character_name, 
        p.phase, 
        COUNT(*) AS needed
    FROM 
        platoons p
    WHERE 
        LOWER(p.planet) = LOWER(?)
    OR
        LOWER(p.planet) = LOWER(?)
    GROUP BY 
        p.character_name, 
        p.phase  
)
SELECT 
    ap.character_name, 
    ap.needed, 
    COUNT(CASE WHEN pu.relic > ap.phase + 3 THEN 1 ELSE NULL END) AS character_count
FROM 
    aggregated_platoons ap
LEFT JOIN 
    playerunits pu ON ap.character_name = pu.character_name
GROUP BY 
    ap.character_name, 
    ap.needed
ORDER BY ap.needed;
""", (planet1, planet2,))
        units = cursor.fetchall()
    
    planet_info = {'units': units if units else "No one's home..."}

    message = '\nThe units for the whole planet\nunit, how many we have, how many we need\n'

    for unit in planet_info['units']:
        if not all:
            if int(unit['character_count']) < int(unit['needed']):
                message += f'{unit["character_name"]}, {unit["character_count"]}, {unit["needed"]}\n'
        else:
            message += f'{unit["character_name"]}, {unit["character_count"]}, {unit["needed"]}\n'

    return message
