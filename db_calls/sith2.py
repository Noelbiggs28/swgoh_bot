import sqlite3
import os

def sith2_plan():
    DATABASE = "db/swgoh_database.sqlite"  # Path to your SQLite database file

    with sqlite3.connect(DATABASE) as conn:
        conn.row_factory = sqlite3.Row  # This allows us to access columns by name
        cursor = conn.cursor()

        cursor.execute("""
WITH playersunits AS (
    SELECT character_name, MAX(relic) AS maxrelic 
    FROM playerunits
    GROUP BY character_name
)
SELECT 
    p.planet, 
    p.phase, 
    p.operations, 
    GROUP_CONCAT(p.character_name) AS character_names
FROM 
    platoons p
LEFT JOIN 
    playersunits pu 
ON 
    p.character_name = pu.character_name
WHERE 
    p.phase < 5
    AND p.planet != 'Zeffo'
    AND pu.maxrelic < p.phase + 4
GROUP BY 
    p.planet, p.phase, p.operations;
""")

        units = cursor.fetchall()

    results = {'impossible_ops': units if units else "doable"}
    if results['impossible_ops'] == "doable":
        return "all missions doable"
    
    message = ""
    relics = 1
    planets = {
        'Mustafar': [], 'Corellia': [], 'Coruscant': [], 'Geonosis': [], 
        'Felucia': [], 'Bracca': [], 'Dathomir': [], 'Tatooine': [], 'Kashyyyk': [],'Haven-class Medical Station':[], 'Kessel':[], 'Lothal':[]
    } 
    
    for planet in planets.keys():
        relic_words = "Relic 5+" if relics < 4 else "Relic 6+" if relics < 7 else "Relic 7+" if relics < 8 else "Relic 8+"

        for unit in results['impossible_ops']:

            if unit[0] == planet:
                planets[planet].append([unit[2], unit[3]])
        if planets[planet]:
            message += f'{planet}\n{relic_words}\n'
            for pair in planets[planet]:
                message += f'Operation: {pair[0]} {pair[1]}\n'

        relics += 1
        message += "\n"
    return message
