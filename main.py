import tkinter as tk
import random
from tkinter import simpledialog, messagebox

class Snake(tk.Canvas):
    def __init__(self):
        super().__init__(width=800, height=800, background="blue", highlightthickness=0)
        self.shape_type = 1  # 1 for ovals, 2 for rectangles, 3 for triangles
        self.speed = 100  # default speed
        self.snake_color = "green"
        self.food_color = "red"
        self.canvas_color = "blue"
        self.grid_color = "black"
        self.border_color = "black"
        self.food_count = 1
        self.welcome_screen()

    def set_new_food_positions(self):
        food_positions = []
        for _ in range(self.food_count):
            while True:
                x_position = random.randint(3, 28)*20
                y_position = random.randint(5,28)*20
                food_position = (x_position, y_position)

                if food_position not in self.snake_positions and food_position not in food_positions:
                    food_positions.append(food_position)
                    break
        return food_positions

    def start_game(self):
        self.delete(tk.ALL)  # Clear the canvas before starting a new game
        self.draw_grid()
        self.draw_border()
        self.snake_positions = [(100, 100), (80, 100), (60, 100)]
        self.food_positions = self.set_new_food_positions()
        self.score = 0
        self.direction = "Right"
        self.bind_all("<Key>", self.on_key_press)
        self.update_game()

    def on_key_press(self, e):
        new_direction = e.keysym

        all_directions = ["Up", "Down", "Left", "Right"]
        opposites = [["Up", "Down"], ["Left", "Right"]]

        if (new_direction in all_directions and
            [new_direction, self.direction] not in opposites):
            self.direction = new_direction

    def move_snake(self):
        head_x_position, head_y_position = self.snake_positions[0]

        if self.direction == "Left":
            new_head_position = (head_x_position - 20, head_y_position)
        elif self.direction == "Right":
            new_head_position = (head_x_position + 20, head_y_position)
        elif self.direction == "Down":
            new_head_position = (head_x_position, head_y_position + 20)
        elif self.direction == "Up":
            new_head_position = (head_x_position, head_y_position - 20)

        return new_head_position

    def update_game(self):
        self.delete('snake')  # Remove old snake from canvas
        self.delete('food')  # Remove old food from canvas

        new_head_position = self.move_snake()

        if (new_head_position in self.snake_positions or
            new_head_position[0] in (0, 600) or
            new_head_position[1] in (0, 600)):
            self.game_over()
        else:
            self.snake_positions = [new_head_position] + self.snake_positions[:-1]

            if new_head_position in self.food_positions:
                self.score += 1
                self.snake_positions.append(self.snake_positions[-1])
                self.food_positions.remove(new_head_position)
                self.food_positions.append(self.set_new_food_positions()[0])

            # Draw snake
            for position in self.snake_positions:
                if self.shape_type == 1:
                    self.create_oval(position[0], position[1], position[0]+20, position[1]+20, fill=self.snake_color, tags='snake')
                elif self.shape_type == 2:
                    self.create_rectangle(position[0], position[1], position[0]+20, position[1]+20, fill=self.snake_color, tags='snake')
                elif self.shape_type == 3:
                    self.create_polygon([position[0], position[1], position[0]+20, position[1], position[0]+10, position[1]+20], fill=self.snake_color, tags='snake')

            # Draw food
            for food_position in self.food_positions:
                if self.shape_type == 1:
                    self.create_oval(food_position[0], food_position[1], food_position[0]+20, food_position[1]+20, fill=self.food_color, tags='food')
                elif self.shape_type == 2:
                    self.create_rectangle(food_position[0], food_position[1], food_position[0]+20, food_position[1]+20, fill=self.food_color, tags='food')
                elif self.shape_type == 3:
                    self.create_polygon([food_position[0], food_position[1], food_position[0]+20, food_position[1], food_position[0]+10, food_position[1]+20], fill=self.food_color, tags='food')

            self.after(self.speed, self.update_game)

    def game_over(self):
        self.delete(tk.ALL)
        self.create_text(
            self.winfo_width() / 2,
            self.winfo_height() / 2,
            text=f"Game Over! You scored {self.score}!",
            fill="white",
            font=("", 8)
        )

        button = tk.Button(root, text="Play Again", command=self.start_game)
        button_window = self.create_window(self.winfo_width() / 2, self.winfo_height() / 2 + 30, window=button)

        shape_button = tk.Button(root, text="Change Shape", command=self.change_shape)
        shape_button_window = self.create_window(self.winfo_width() / 2, self.winfo_height() / 2 + 60, window=shape_button)

        speed_button = tk.Button(root, text="Change Speed", command=self.change_speed)
        speed_button_window = self.create_window(self.winfo_width() / 2, self.winfo_height() / 2 + 90, window=speed_button)

        color_button = tk.Button(root, text="Change Colors", command=self.change_colors)
        color_button_window = self.create_window(self.winfo_width() / 2, self.winfo_height() / 2 + 120, window=color_button)

        grid_color_button = tk.Button(root, text="Change Grid Color", command=self.change_grid_color)
        grid_color_button_window = self.create_window(self.winfo_width() / 2, self.winfo_height() / 2 + 150, window=grid_color_button)

        food_count_button = tk.Button(root, text="Change Food Count", command=self.change_food_count)
        food_count_button_window = self.create_window(self.winfo_width() / 2, self.winfo_height() / 2 + 180, window=food_count_button)

        # Display chosen options
        chosen_options = tk.Label(root, text=f"Chosen options: \nShape: {'oval' if self.shape_type == 1 else 'rectangle' if self.shape_type == 2 else 'triangle'}\nSpeed: {self.speed}\nSnake color: {self.snake_color}\nFood color: {self.food_color}\nCanvas color: {self.canvas_color}\nGrid color: {self.grid_color}\nFood count: {self.food_count}", bg="white", justify="left")
        chosen_options_window = self.create_window(10, 10, anchor="nw", window=chosen_options)

    def welcome_screen(self):
        self.delete(tk.ALL)
        self.create_text(
            self.winfo_width() / 2+350,
            self.winfo_height() / 2+180,
            text="Welcome to the Snake Game!",
            fill="white",
            font=("", 8)
        )

        button = tk.Button(root, text="Start Game", command=self.start_game)
        button_window = self.create_window(self.winfo_width() / 2+350, self.winfo_height() / 2 + 30+200, window=button)

        shape_button = tk.Button(root, text="Change Shape", command=self.change_shape)
        shape_button_window = self.create_window(self.winfo_width() / 2+350, self.winfo_height() / 2+60+200, window=shape_button)

        speed_button = tk.Button(root, text="Change Speed", command=self.change_speed)
        speed_button_window = self.create_window(self.winfo_width() / 2+350, self.winfo_height() / 2 + 90+200, window=speed_button)

        color_button = tk.Button(root, text="Change Colors", command=self.change_colors)
        color_button_window = self.create_window(self.winfo_width() / 2+350, self.winfo_height() / 2 + 120+200, window=color_button)

        grid_color_button = tk.Button(root, text="Change Grid Color", command=self.change_grid_color)
        grid_color_button_window = self.create_window(self.winfo_width() / 2+350, self.winfo_height() / 2 + 150+200, window=grid_color_button)

        food_count_button = tk.Button(root, text="Change Food Count", command=self.change_food_count)
        food_count_button_window = self.create_window(self.winfo_width() / 2+350, self.winfo_height() / 2 + 180+200, window=food_count_button)

        # Display chosen options
        chosen_options = tk.Label(root, text=f"Chosen options: \nShape: {'oval' if self.shape_type == 1 else 'rectangle' if self.shape_type == 2 else 'triangle'}\nSpeed: {self.speed}\nSnake color: {self.snake_color}\nFood color: {self.food_color}\nCanvas color: {self.canvas_color}\nGrid color: {self.grid_color}\nFood count: {self.food_count}", bg="white", justify="left")
        chosen_options_window = self.create_window(5, 5, anchor="nw", window=chosen_options)

    def change_shape(self):
        self.shape_type = simpledialog.askinteger("Input", "Enter shape type (1 for oval, 2 for rectangle, 3 for triangle)", parent=root, minvalue=1, maxvalue=3)

    def change_speed(self):
        self.speed = simpledialog.askinteger("Input", "Enter speed (10 for fast, 300 for slow)", parent=root, minvalue=10, maxvalue=300)

    def change_colors(self):
        self.snake_color = simpledialog.askstring("Input", "Enter snake color", parent=root)
        self.food_color = simpledialog.askstring("Input", "Enter food color", parent=root)
        self.canvas_color = simpledialog.askstring("Input", "Enter canvas color", parent=root)
        self.config(bg=self.canvas_color)

    def change_grid_color(self):
        self.grid_color = simpledialog.askstring("Input", "Enter grid color", parent=root)

    def change_food_count(self):
        self.food_count = simpledialog.askinteger("Input", "Enter food count (1 to 100)", parent=root, minvalue=1, maxvalue=400)

    def draw_grid(self):
        for i in range(20, 600, 20):
            self.create_line([(i, 20), (i, 600)], tag='grid', fill=self.grid_color)
            self.create_line([(20, i), (600, i)], tag='grid', fill=self.grid_color)

    def draw_border(self):
        self.create_line([(10, 10), (590, 10), (590, 590), (10, 590), (10, 10)], tag='border', fill=self.border_color, width=10)

root = tk.Tk()
root.title("Snake Game")
root.resizable(False, False)
root.tk.call("tk", "scaling", 4.0)

board = Snake()
board.pack()

root.mainloop()
