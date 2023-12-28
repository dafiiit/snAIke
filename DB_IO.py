import random
import numpy as np
import sqlite3
import json

# Eingabe: direction, snake, food_list, reward


class DB_IO:
    def __init__(self, db_name="snake_game.db"):
        connection = sqlite3.connect(db_name)
        cursor = connection.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS snake_game (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                state TEXT
            )
        """
        )
        connection.commit()
        connection.close()

    def save_state(
        self, snake, food, direction, reward, game_id, db_name="snake_game.db"
    ):
        state = {}
        state["direction"] = direction  # int
        state["reward"] = reward  # int
        state["game_id"] = game_id  # int
        state["snake"] = json.dumps(snake)  # list
        state["food"] = json.dumps(food)  # list
        
        state_json = json.dumps(state)

        connection = sqlite3.connect(db_name)
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO snake_game (state) VALUES (?)
        """,
            (state_json,),
        )

        connection.commit()
        connection.close()

    def get_last_game_id(self, db_name="snake_game.db"):
        # Get the last game id from the database (one per game)
        connection = sqlite3.connect(db_name)
        cursor = connection.cursor()

        try:
            cursor.execute("SELECT state FROM snake_game WHERE id=(SELECT MAX(id)FROM snake_game)")
            last_game_id = json.loads(cursor.fetchone()[0])["game_id"]
        except:
            last_game_id = -1

        connection.close()
        
        return  last_game_id
    
    def get_last_state_id(self, db_name="snake_game.db"):
        # Get the last state id from the database (one per state)
        try:
            with sqlite3.connect(db_name) as connection:
                cursor = connection.cursor()
                cursor.execute("SELECT MAX(id) FROM snake_game")
                result = cursor.fetchone()
                last_state_id = result[0] if result is not None else None

        except sqlite3.Error as e:
            print(f"Error: {e}")
            last_state_id = None  # Handle the error as needed

        return last_state_id
    
    def get_state(self, state_id, db_name="snake_game.db"):
        connection = sqlite3.connect(db_name)
        cursor = connection.cursor()
        
        #cursor.execute("SELECT state FROM snake_game WHERE id=state_id")
        cursor.execute("SELECT state FROM snake_game WHERE id=?", (state_id,))
        state = json.loads(cursor.fetchone()[0])

        connection.close()
        return state

#frage ab ob dieser code ausgeführt werden soll
if __name__ == "__main__":
    db_io = DB_IO()
    
    print(db_io.get_last_game_id())
