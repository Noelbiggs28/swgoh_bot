import requests
import sqlite3
import os

def update_units():
    DATABASE = "db/swgoh_database.sqlite"  # Path to your SQLite database file

    def get_ally_codes():
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT ally_code, player_name FROM players")
            ally_codes = cursor.fetchall()
        
        return [(ally_code[0], ally_code[1]) for ally_code in ally_codes] if ally_codes else "0 Players"

    def get_swgoh_player_data(ally_codes):
        all_units = []
        for code in ally_codes:
            url = f"https://swgoh.gg/api/player/{code[0]}/"
            try:
                response = requests.get(url)
                response.raise_for_status()  
                data = response.json()
                for unit in data['units']:
                    name = unit['data']['name']
                    combat_type = unit['data']['combat_type']
                    rarity = unit['data']['rarity']
                    if combat_type == 2:
                        relic = 0
                        if rarity == 7:
                            relic = 100
                        all_units.append((code[1], name, relic, rarity))
                    if combat_type == 1:
                        relic = unit['data']['relic_tier'] - 2
                        all_units.append((code[1], name, relic, rarity))
            except requests.exceptions.RequestException as e:
                print(f"Error: {e}")
                return None
        return all_units

    allies = get_ally_codes()
    all_units_list = get_swgoh_player_data(allies)

    if all_units_list:
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM PLAYERUNITS;")
            for unit in all_units_list:
                cursor.execute(
                    "INSERT INTO PLAYERUNITS (player_name, character_name, relic, rarity) VALUES (?, ?, ?, ?);",
                    (unit[0], unit[1], unit[2], unit[3])
                )
            conn.commit()

    return "complete"

if __name__ == "__main__":
    update_units()
