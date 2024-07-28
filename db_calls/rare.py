import sqlite3
import os

def rare_plan():
    DATABASE = "db/swgoh_database.sqlite"  # Path to your SQLite database file

    conn = sqlite3.connect(DATABASE)
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
        GROUP_CONCAT(DISTINCT CASE WHEN pu.relic > ap.phase + 3 THEN pu.player_name ELSE NULL END) AS players
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
    conn.close()
    
    if not units:
        return "All missions doable"
    
    result = {}
    for unit in units:
        player_names = unit[5].split(',') if unit[5] else []
        for player in player_names:
            if player not in result:
                result[player] = []
            result[player].append({
                "planet": unit[0],
                "character_name": unit[1],
                "operations": unit[2],
                "phase": unit[3],
                "count": unit[4]
            })
    
    # Sort the result dictionary by the length of the details list in descending order
    sorted_result = dict(sorted(result.items(), key=lambda item: len(item[1]), reverse=True))
    
    message = ""
    for player, details in sorted_result.items():
        message += f"Player: {player}\n"
        for detail in details:
            message += f"  {detail['planet']} - {detail['character_name']} (Phase {detail['phase']}, Operations: {detail['operations']})\n"
        message += "\n"
    
    return message

if __name__=="__main__":
    print(rare_plan())
