import sqlite3
import os

def rare_plan():
    DATABASE = "db/swgoh_database.sqlite"  # Path to your SQLite database file

    with sqlite3.connect(DATABASE) as conn:
        conn.row_factory = sqlite3.Row  # This allows us to access columns by name
        cursor = conn.cursor()

        cursor.execute("""
WITH aggregated_platoons AS (
    SELECT 
        p.planet, 
        p.character_name, 
        GROUP_CONCAT(p.operations, ', ') AS operations, 
        p.phase, 
        COUNT(*) AS count
    FROM 
        platoons p
    WHERE 
        p.phase < 4
        AND p.planet != 'Zeffo'
    GROUP BY 
        p.planet, 
        p.character_name, 
        p.phase
)
SELECT 
    ap.planet, 
    ap.character_name, 
    ap.operations, 
    ap.phase, 
    ap.count, 
    COUNT(CASE WHEN pu.relic > ap.phase + 3 THEN 1 ELSE NULL END) AS character_count,
    GROUP_CONCAT(CASE WHEN pu.relic > ap.phase + 3 THEN pu.player_name ELSE NULL END, ', ') AS players
FROM 
    aggregated_platoons ap
LEFT JOIN 
    playerunits pu 
ON 
    ap.character_name = pu.character_name
GROUP BY 
    ap.planet, 
    ap.character_name, 
    ap.operations, 
    ap.phase, 
    ap.count
HAVING 
    COUNT(CASE WHEN pu.relic > ap.phase + 3 THEN 1 ELSE NULL END) <= ap.count
ORDER BY 
    ap.planet;
""")
        units = cursor.fetchall()

    needed_units = {'needed_units': units if units else "doable"}
    if needed_units['needed_units'] == "doable":
        return "all missions doable"

    message = "Units where needed - have = 0\n"
    planets = set()
    for unit in needed_units['needed_units']:
        relic_words = (
            "Relic 5+" if unit['phase'] == 1 else
            "Relic 6+" if unit['phase'] == 2 else
            "Relic 7+" if unit['phase'] == 3 else
            "Relic 8+" if unit['phase'] == 4 else
            "relic 9"
        )
        planets.add((unit['planet'], relic_words))

    planet_names = [
        'Mustafar', 'Corellia', 'Coruscant', 'Geonosis', 'Felucia', 'Bracca', 
        'Dathomir', 'Tatooine', 'Kashyyyk', 'Zeffo'
    ]
    order_index = {planet: index for index, planet in enumerate(planet_names)}
    sorted_planets = sorted(planets, key=lambda x: order_index[x[0]])

    for planet in sorted_planets:
        if planet[0] != "Zeffo":
            message += f'{planet[0]}\n{planet[1]}\n'
            for unit in needed_units['needed_units']:
                if unit['planet'] == planet[0]:
                    message += f"{unit['character_name']} Operations: {unit['operations']}, Players: {unit['players'] if unit['players'] else ''}\n"
            message += "\n"

    return message
