import random
import numpy as np
from AI import AI
from DB_IO import DB_IO
import json

#Eingabe: direction, snake, food_list, reward
#Ausgabe: ruft prediction und train auf

class AI_IO:
    def __init__(self):
        self.ai_direction = "up"
        self.recent_matrix_index = 0
        self.matrix = np.zeros(( 20, 20), dtype=int)
        self.move = np.zeros((3), dtype=int)
        self.recent_move_index = 0
        self.last_reward = 0
        self.prediction = np.zeros((3), dtype=int)

    def update_matrix(self, snake, food_list):
        # setze neustes Feld auf 0
        self.matrix = np.zeros((20, 20), dtype=int)

        # Kopf in neustem Feld auf 2 setzen
        x_head, y_head = snake[0]
        self.matrix[x_head // 20][y_head // 20] = 2

        # Körper auf 1 setzen
        for x, y in snake[1:]:
            self.matrix[x // 20][y // 20] = 1
        
        # food auf 3 setzen
        for food in food_list:
            self.matrix[food[0] // 20][food[1] // 20] += 3
            
        self.recent_matrix_index += 1
        if self.recent_matrix_index > 4:
            self.recent_matrix_index = 0
    
    """        
    def string_to_number_direction(self, direction):
        #up=1, down=2, left=4, right=8
        direction_mapping = {
            1: {"right": 8, "left": 4, "up": 1},
            2: {"right": 4, "left": 8, "up": 2},
            4: {"right": 1, "left": 2, "up": 4},
            8: {"right": 2, "left": 1, "up": 8},
        }
        return direction_mapping[direction][self.ai_direction]          
    """
    def number_to_vektor_direction(self, direction, last_move):
        #Eingebe: direction, last_move als int
        #Ausgabe: direction_vektor als np.array der Größe 3
        direction_vector = np.zeros(3)
        direction_mapping = {
            #up=1, down=2, left=4, right=8
            1: {8: "right", 4: "left", 1: "up", 2: "up"},
            2: {8: "left", 4: "right", 1: "up", 2: "up"},
            4: {8: "up", 4: "up", 1: "right", 2: "left"},
            8: {8: "up", 4: "up", 1: "left", 2: "right"},
        }
        direction_to_vector_mapping = ["up", "left", "right"]
        for i in range(3):
            if (
                direction_mapping[direction][last_move]
                == direction_to_vector_mapping[i]
            ):
                direction_vector[i] = 1
        return direction_vector

    def vektor_to_number_direction(self, direction_vektor, last_direction):
        #Eingabe: direction_vektor als np.array der Größe 3 und last_move als int
        #Ausgabe: direction als int
        direction_vector_four = np.zeros(4)
        if last_direction == 1:
            direction_vector_four[0] = 1
            
    
    def vektor_to_number_direction(self, direction_vektor):
        #Eingabe: direction_vektor als np.array der Größe 3
        #Ausgabe: direction als int
        for i in direction_vektor:
            if direction_vektor[i] == 1:
                direction += 2**i
        return direction

    def number_to_vektor_direction(self, number):
        direction_vektor = np.zeros(3)
        for i in range(3):
            if number % 2 == 1:
                direction_vektor[i] = 1
            number = number // 2
        return direction_vektor
    
    def predict(self):
        #funktioniert wahrscheinlich noch nicht
        input_data = self.get_matrix()[0]
        input_data = input_data.reshape(1,400)
        
        self.prediction = neural_net.predict(input_data)
        direction_mapping = ["up", "left", "right"]
        for i in range(3):
            if prediction[i]==1:
                self.ai_direction=direction_mapping[i]
        
        #self.move[self.recent_move_index] = self.prediction
        self.recent_move_index += 1
        if self.recent_move_index > 4:
            self.recent_move_index = 0
            
    def train(self, train_whole_db = False):
        last_game_id = db_io.get_last_game_id()
        
        if train_whole_db:
            for i in range(db_io.get_last_state_id()):                        
                entire_state = db_io.get_state(str(db_io.get_last_state_id()-i))    
                self.train_one_state(entire_state)  
                if last_game_id != db_io.get_last_game_id():
                    self.last_reward = 0                             
        else: 
            i = 0
            while last_game_id == db_io.get_last_game_id():
                entire_state = db_io.get_state(db_io.get_last_state_id()-i)
                self.train_one_state(entire_state)
            else:
                self.last_reward = 0
                        
    
    def train_one_state(self, entire_state):   
        snake = json.loads(entire_state["snake"])
        food_list = json.loads(entire_state["food"])
        direction = entire_state["direction"]
        #move = entire_state["move"]
        reward = int(entire_state["reward"]) + (self.last_reward/2)
        self.last_reward = reward
        self.update_matrix(snake, food_list)
        input_data = self.matrix
        #output_data = self.number_to_vektor_direction(direction, move)

        ai.train(input_data, output_data, reward)
    
    
if __name__ == "__main__":
    #erstelle Objekte
    ai_io = AI_IO()
    ai = AI()
    db_io = DB_IO()

    ai_io.train(train_whole_db = True)