# simple snake implementation. Just 1 player right now.

import time
import random
import tkinter

import numpy as np
from tkinter import *
from tkinter import ttk
import keyboard


class Snake:
    x_coord = 0
    y_coord = 0

    x = 0
    y = 0
    direction = 2  # 0 - left 1 - up 2 - right 3 - down

    def turn_left(self):

        if self.direction > 0:
            self.direction -= 1
        else:
            self.direction = 3

    def turn_right(self):

        if self.direction < 3:
            self.direction += 1
        else:
            self.direction = 0

    def move(self):

        if self.direction == 1:
            self.y_coord -= 1

        if self.direction == 2:
            self.x_coord += 1

        if self.direction == 3:
            self.y_coord += 1

        if self.direction == 0:
            self.x_coord -= 1


class Game:
    # -- some constants

    SCREEN_REFRESH_DELAY = 0.1

    x_grid_size = 15
    y_grid_size = 15
    pixel_size = 30

    WIDTH = x_grid_size * pixel_size
    HEIGHT = y_grid_size * pixel_size

    fruit = (2, 1)

    actions = [
        'LEFT',
        'RIGHT',
    ]

    # some funcs for setup
    def turn_left(self):
        self.snake.turn_left()

    def turn_right(self):
        self.snake.turn_right()

    # -- screen setup
    root = Tk()
    frm = ttk.Frame(root, padding=10)
    canvas = tkinter.Canvas(root, bg="white", height=HEIGHT, width=WIDTH)

    # -- game setup

    score = 0
    snake = Snake()
    game_over_state = False



    segments = []

    # Snake food
    segments = []

    game_grid = []

    def coord_to_point(self, x_coord, y_coord):
        return x_coord * self.pixel_size, y_coord * self.pixel_size

    def init(self):

        # 0 - blank, 1 - fruit, 2 - snake head, 3 - snake segment

        self.game_grid = [[0 for i in range(self.x_grid_size)] for j in range(self.y_grid_size)]

        self.game_grid[self.fruit[0]][self.fruit[1]] = 1

        self.snake.x_coord = int(self.x_grid_size / 2)
        self.snake.y_coord = int(self.y_grid_size / 2)

        self.snake.x, self.snake.y = self.coord_to_point(self.snake.x_coord, self.snake.y_coord)

        keyboard.add_hotkey('a', lambda: self.turn_left())
        keyboard.add_hotkey('d', lambda: self.turn_right())

    def draw(self):

        #print("Drawing...")
        self.canvas.delete("all")

        #print("SNAKEX", self.snake.x_coord)
        #print("SNAKEY", self.snake.y_coord)

        for x in range(self.x_grid_size):
            for y in range(self.y_grid_size):

                canvas_x, canvas_y = self.coord_to_point(x, y)

                if self.game_grid[x][y] == 1:
                    self.canvas.create_rectangle(canvas_x, canvas_y, canvas_x + self.pixel_size,
                                                 canvas_y + self.pixel_size,
                                                 outline="red", fill="red", width=0)

                if self.game_grid[x][y] == 2:
                    self.canvas.create_rectangle(canvas_x, canvas_y, canvas_x + self.pixel_size,
                                                 canvas_y + self.pixel_size,
                                                 outline="black", fill="black", width=0)

                if self.game_grid[x][y] == 3:
                    self.canvas.create_rectangle(canvas_x, canvas_y, canvas_x + self.pixel_size,
                                                 canvas_y + self.pixel_size,
                                                 outline="black", fill="black", width=0)

        #print("Packing and mainlooping")

        self.canvas.pack()
        self.canvas.update_idletasks()

    def game_over(self):

        #print("GAME OVER")

        time.sleep(1)

        # Clear the segments list
        self.segments.clear()

        self.snake.x_coord = int(self.x_grid_size / 2)
        self.snake.y_coord = int(self.y_grid_size / 2)

        self.snake.x, self.snake.y = self.coord_to_point(self.snake.x_coord, self.snake.y_coord)

        # Reset the score
        self.score = 0

        # Reset the delay
        self.SCREEN_REFRESH_DELAY = 0.1

        self.game_over_state = False

    def set_render(self):
        pass

    def eat_food(self):

        # Move the food to a random spot

        # Shorten the delay
        self.SCREEN_REFRESH_DELAY -= 0.001

        self.segments.append((self.snake.x_coord, self.snake.y_coord))
        self.game_grid[self.snake.x_coord][self.snake.y_coord] = 3

        self.fruit = (random.randint(0, self.x_grid_size-1), random.randint(0, self.y_grid_size-1))


        # Increase the score
        self.score += 10

    # returns an array representing the game state
    def get_observation(self):

        return self.game_grid

    def update_game_grid(self):

        for x in range(self.x_grid_size):
            for y in range(self.y_grid_size):
                self.game_grid[x][y] = 0
                self.game_grid[self.fruit[0]][self.fruit[1]] = 1
                self.game_grid[self.snake.x_coord][self.snake.y_coord] = 2

                for seg in self.segments:
                    self.game_grid[seg[0]][seg[1]] = 3

    def game_loop(self):

        self.update_game_grid()
        self.draw()
        reward = 0

        self.game_over_state = False

        # Move the end segments first in reverse order
        for index in range(len(self.segments) - 1, 0, -1):
            x = self.segments[index - 1][0]
            y = self.segments[index - 1][1]
            self.segments[index] = (x, y)

        # Move segment 0 to where the head is
        if len(self.segments) > 0:
            x = self.snake.x_coord
            y = self.snake.y_coord
            self.segments[0] = (x, y)

        self.snake.move()

        if self.snake.x_coord < 0 or self.snake.y_coord < 0:
            self.game_over()
            self.game_over_state = True
            reward = 0

        if self.snake.x_coord == self.x_grid_size or self.snake.y_coord == self.y_grid_size:
            self.game_over()
            self.game_over_state = True
            reward = 0

        for seg in self.segments:
            if self.snake.x_coord == seg[0] and self.snake.y_coord == seg[1]:
                self.game_over()
                self.game_over_state = True
                reward = 0

        if self.game_grid[self.snake.x_coord][self.snake.y_coord] == 1:
            self.eat_food()
            reward = 1

        time.sleep(self.SCREEN_REFRESH_DELAY)

        return reward


game = Game()

game.init()

while True:
    game.game_loop()
    #print(game.get_observation())
