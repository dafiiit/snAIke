import tkinter as tk
import random

# Constants
WIDTH = 400
HEIGHT = 400
DELAY = 200
CELL_SIZE = 20

class SnakeGame:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Snake Game")
        self.canvas = tk.Canvas(self.window, width=WIDTH, height=HEIGHT)
        self.canvas.pack()
        self.window.bind("<Key>", self.on_key_press)
        
        # Initialize the snake
        self.snake = [(100, 100), (80, 100), (60, 100)]
        self.direction = "Right"
        
        # Initialize the food
        self.food = self.create_food()
        
        # Initialize the score
        self.score = 0
        
        # Initialize game state
        self.game_over = False
        
        # Start the game loop
        self.game_loop()
        
    def game_loop(self):
        if not self.game_over:
            self.move_snake()
            self.check_collision()
            self.update_score()
            self.draw()
        self.window.after(DELAY, self.game_loop)
        
    def move_snake(self):
        head_x, head_y = self.snake[0]
        
        if self.direction == "Up":
            new_head = (head_x, head_y - CELL_SIZE)
        elif self.direction == "Down":
            new_head = (head_x, head_y + CELL_SIZE)
        elif self.direction == "Left":
            new_head = (head_x - CELL_SIZE, head_y)
        elif self.direction == "Right":
            new_head = (head_x + CELL_SIZE, head_y)
            
        # Wrap around the edges
        new_head = (new_head[0] % WIDTH, new_head[1] % HEIGHT)
        
        self.snake.insert(0, new_head)
        if new_head == self.food:
            self.score += 1
            self.food = self.create_food()
        else:
            self.snake.pop()
            
    def check_collision(self):
        head_x, head_y = self.snake[0]
        if (
            head_x < 0 or head_x >= WIDTH or
            head_y < 0 or head_y >= HEIGHT or
            (head_x, head_y) in self.snake[1:]
        ):
            self.game_over = True
            
    def update_score(self):
        self.window.title(f"Snake Game | Score: {self.score}")
        
    def draw(self):
        self.canvas.delete(tk.ALL)
        
        # Draw the snake
        for x, y in self.snake:
            self.canvas.create_rectangle(
                x, y, x + CELL_SIZE, y + CELL_SIZE, fill="green"
            )
        
        # Draw the food
        food_x, food_y = self.food
        self.canvas.create_oval(
            food_x, food_y, food_x + CELL_SIZE, food_y + CELL_SIZE, fill="red"
        )
        
        if self.game_over:
            self.canvas.create_text(
                WIDTH // 2, HEIGHT // 2,
                text="Game Over!", font=("Helvetica", 20), fill="red"
            )
            self.canvas.create_text(
                WIDTH // 2, HEIGHT // 2 + 30,
                text="Press Play Again to restart", font=("Helvetica", 14), fill="red"
            )
        
    def create_food(self):
        while True:
            food_x = random.randint(0, WIDTH // CELL_SIZE - 1) * CELL_SIZE
            food_y = random.randint(0, HEIGHT // CELL_SIZE - 1) * CELL_SIZE
            food = (food_x, food_y)
            if food not in self.snake:
                return food
            
    def on_key_press(self, event):
        if event.keysym == "Up" and self.direction != "Down":
            self.direction = "Up"
        elif event.keysym == "Down" and self.direction != "Up":
            self.direction = "Down"
        elif event.keysym == "Left" and self.direction != "Right":
            self.direction = "Left"
        elif event.keysym == "Right" and self.direction != "Left":
            self.direction = "Right"
            
    def play_again(self):
        self.snake = [(100, 100), (80, 100), (60, 100)]
        self.direction = "Right"
        self.food = self.create_food()
        self.score = 0
        self.game_over = False
        
    def run(self):
        play_again_btn = tk.Button(
            self.window, text="Play Again", command=self.play_again
        )
        play_again_btn.pack()
        
        self.game_loop()
        self.window.mainloop()

# Create and run the game
game = SnakeGame()              #Objekt "game" der Klasse SnakeGame wird erstellt
game.run()                      
