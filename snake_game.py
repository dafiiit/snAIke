import tkinter as tk
import random
import numpy as np
import sqlite3
import json
from AI import AI
from DB_IO import DB_IO
from AI_IO import AI_IO

class SnakeGame:
    # Constants
    WIDTH = 400
    HEIGHT = 400
    DELAY = 200
    CELL_SIZE = 20
    
    def __init__(self, autonomy=False, food_count=1):
        self.window = tk.Tk()
        self.window.title("Snake Game")
        self.canvas = tk.Canvas(self.window, width=self.WIDTH, height=self.HEIGHT)
        self.canvas.pack()
        self.window.bind("<Key>", self.on_key_press)
        self.food_count = food_count
        self.autonomy = autonomy
        
        # Initialize the snake
        self.snake = [(100, 100), (80, 100), (60, 100)]

        # Initialize the food
        self.food_list = []
        self.create_food_list()

        # Initialize the score
        self.score = 0
        self.direction = 8  #up=1, down=2, left=4, right=8
        self.reward = 0
        self.game_id = db_io.get_last_game_id() + 1
        print(f"game_id = {self.game_id}")
        
        # Initialize game state
        self.game_over = False

        # Start the game loop
        self.game_loop()

    def game_loop(self):
        if not self.game_over:
            if self.autonomy:
                ai_io.update_matrix(self.snake, self.food_list)
                ai_io.predict()
                self.direction = ai_io.vektor_to_number_direction(ai_io.prediction)
            self.move_snake()
            self.check_collision()
            self.update_score()
            self.draw()
            #if self.autonomy:
                #ai_io.train()
            db_io.save_state(self.snake, self.food_list, self.direction, self.reward, self.game_id)
            self.reward = 0
        self.window.after(self.DELAY, self.game_loop)

    def move_snake(self):
        head_x, head_y = self.snake[0]
        #"UP" = 1, "DOWN" = 2, "LEFT" = 4, "RIGHT" = 8
        if self.direction == 1:
            new_head = (head_x, head_y - self.CELL_SIZE)
        elif self.direction == 2:
            new_head = (head_x, head_y + self.CELL_SIZE)
        elif self.direction == 4:
            new_head = (head_x - self.CELL_SIZE, head_y)
        elif self.direction == 8:
            new_head = (head_x + self.CELL_SIZE, head_y)

        # Appear again after leaving the screen
        new_head = (new_head[0] % self.WIDTH, new_head[1] % self.HEIGHT)
        # Add head at calculated position
        self.snake.insert(0, new_head)

        if self.check_food_collision(new_head):
            self.food_list.append(self.create_food())
        else:
            self.snake.pop()

    def check_food_collision(self, new_head):
        head_x, head_y = new_head
        found_food = False
        #if self.autonomy:
            #ai_io.update_matrix(self.snake, self.food_list)
        for food in self.food_list:
            food_x, food_y = food
            if (head_x, head_y) == food:
                self.score += 1
                
                self.reward += 1
                    
                self.food_list.remove(food)
                found_food = True
        return found_food

    def check_collision(self):
        head_x, head_y = self.snake[0]
        if (
            head_x < 0
            or head_x >= self.WIDTH
            or head_y < 0
            or head_y >= self.HEIGHT
            or (head_x, head_y) in self.snake[1:]
        ):
            self.reward -= 4
            if self.autonomy:
                self.play_again()
            else:
                self.game_over = True

    def update_score(self):
        self.window.title(f"Snake Game | Score: {self.score}")

    def draw(self):
        self.canvas.delete(tk.ALL)

        # Draw the snake
        for x, y in self.snake:
            self.canvas.create_rectangle(
                x, y, x + self.CELL_SIZE, y + self.CELL_SIZE, fill="green"
            )

        # Draw the food
        for food in self.food_list:
            food_x, food_y = food
            self.canvas.create_oval(
                food_x, food_y, food_x + self.CELL_SIZE, food_y + self.CELL_SIZE, fill="red"
            )

        if self.game_over:
            self.canvas.create_text(
                self.WIDTH // 2,
                self.HEIGHT // 2,
                text="Game Over!",
                font=("Helvetica", 20),
                fill="red",
            )
            self.canvas.create_text(
                self.WIDTH // 2,
                self.HEIGHT // 2 + 30,
                text="Press Play Again to restart",
                font=("Helvetica", 14),
                fill="red",
            )

    def create_food_list(self):
        self.food_list = []
        for i in range(self.food_count):
            self.food_list.append(self.create_food())

    def create_food(self):
        while True:
            food_x = random.randint(0, self.WIDTH // self.CELL_SIZE - 1) * self.CELL_SIZE
            food_y = random.randint(0, self.HEIGHT // self.CELL_SIZE - 1) * self.CELL_SIZE
            food = (food_x, food_y)
            if food not in self.snake:
                return food

    def on_key_press(self, event):
        #up=1, down=2, left=4, right=8
        if not self.autonomy:
            if event.keysym == "Up" and self.direction != 2:
                self.direction = 1
            elif event.keysym == "Down" and self.direction != 1:
                self.direction = 2
            elif event.keysym == "Left" and self.direction != 8:
                self.direction = 4
            elif event.keysym == "Right" and self.direction != 4:
                self.direction = 8

    def play_again(self):
        self.snake = [(100, 100), (80, 100), (60, 100)]
        self.direction = 8 #right
        self.create_food_list()
        self.score = 0
        self.game_id += 1
        self.game_over = False

    def run(self):
        play_again_btn = tk.Button(
            self.window, text="Play Again", command=self.play_again
        )
        play_again_btn.pack()

        self.game_loop()
        self.window.mainloop()
        

# Create and run the game
ai = AI()
ai_io = AI_IO()
db_io = DB_IO()
game = SnakeGame(autonomy=False, food_count=35)  # Objekt "game" der Klasse SnakeGame wird erstellt

game.run()
