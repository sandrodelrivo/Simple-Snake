# simple snake implementation. Just 1 player right now.

import time
import random
import turtle

class Snake:
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

        if self.direction == 2:
            self.y += 20

        if self.direction == 3:
            self.y -= 20

        if self.direction == 0:
            self.x -= 20

        if self.direction == 1:
            self.x += 20


class Game:
    # -- some constants

    WIDTH = 800
    HEIGHT = 600
    SCREEN_REFRESH_DELAY = 0.1

    # -- screen setup
    wn = turtle.Screen()

    # -- game setup

    score = 0
    snake = Snake()

    segments = []

    # -- visuals setup

    # Snake head
    snake_head = turtle.Turtle()

    # Snake food
    point = turtle.Turtle()
    pen = turtle.Turtle()


    segments = []

    def turn_left(self):
        print("TUUURN")

    def init(self):

        self.wn.title("Snake")
        self.wn.bgcolor("white")
        self.wn.setup(width=self.WIDTH, height=self.HEIGHT)
        self.wn.tracer(0)  # Turns off the screen updates

        self.snake_head.shape("square")
        self.snake_head.color("black")

        self.point.speed(0)
        self.point.shape("square")
        self.point.color("red")

        self.pen.speed(0)
        self.pen.shape("square")
        self.pen.color("black")
        self.pen.penup()
        self.pen.hideturtle()
        self.pen.goto(0, 260)
        self.pen.write("Score: 0", align="center", font=("Courier", 24, "normal"))

        # -- bindings
        self.wn.listen()
        self.wn.onkeypress(self.snake.turn_left(), "a")
        self.wn.onkeypress(self.snake.turn_right(), "d")

        self.snake_head.speed(0)
        self.snake_head.penup()
        self.snake_head.goto(0, 0)
        self.snake_head.direction = "stop"

        self.point.penup()
        self.point.goto(0, 100)

    def game_over(self):

        print("GAME OVER")

        time.sleep(1)

        self.snake.x = 0
        self.snake.y = 0
        self.snake_head.direction = "stop"

        # Hide the segments
        for segment in self.segments:
            segment.goto(1000, 1000)

        # Clear the segments list
        self.segments.clear()

        # Reset the score
        self.score = 0

        # Reset the delay
        self.SCREEN_REFRESH_DELAY = 0.1

        self.pen.clear()
        self.pen.write("Score: {}".format(self.score), align="center", font=("Courier", 24, "normal"))

    def eat_food(self):
        # Move the food to a random spot
        x = random.randint(-290, 290)
        y = random.randint(-290, 290)
        self.point.goto(x, y)

        # Add a segment
        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape("square")
        new_segment.color("grey")
        new_segment.penup()
        self.segments.append(new_segment)

        # Shorten the delay
        self.SCREEN_REFRESH_DELAY -= 0.001

        # Increase the score
        self.score += 10

        self.pen.clear()
        self.pen.write("Score: {}".format(self.score), align="center", font=("Courier", 24, "normal"))

    def game_loop(self):

        self.wn.update()

        if self.snake_head.distance(self.point) < 20:
            self.eat_food()

        for segment in self.segments:
            if segment.distance(self.snake_head) < 20:
                self.game_over()

        if self.snake.x < (-1 * (self.WIDTH / 2)) or self.snake.x > (self.WIDTH / 2) or self.snake.y < (
                -1 * (self.HEIGHT / 2)) or self.snake.y > (self.HEIGHT / 2):
            self.game_over()

        # Move the end segments first in reverse order
        for index in range(len(self.segments) - 1, 0, -1):
            x = self.segments[index - 1].x
            y = self.segments[index - 1].y
            self.segments[index].goto(x, y)

        # Move segment 0 to where the head is
        if len(self.segments) > 0:
            x = self.snake.x
            y = self.snake.y
            self.segments[0].goto(x, y)

        self.snake.move()
        self.snake_head.goto(self.snake.x, self.snake.y)

        time.sleep(self.SCREEN_REFRESH_DELAY)


game = Game()

game.init()

while True:
    game.game_loop()
