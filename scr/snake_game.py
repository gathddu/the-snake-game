import turtle
import tkinter as tk
import random
import time
import os
from config import GRID_WIDTH, GRID_HEIGHT, SNAKE_COLOR, FOOD_COLORS, BACKGROUND_COLOR, DELAY
from utils import read_high_score, save_high_score

#starting the game
def start_game():
    global play_again_button, quit_button

    frame.pack_forget() #hiding buttons
    if play_again_button:
        play_again_button.destroy()
        quit_button.destroy()
    wn.clear()
    wn.bgcolor(BACKGROUND_COLOR)
    start_snake_game(DELAY)

#quit forever
def quit_game():
    turtle.bye()

#game over elements
def create_game_over_elements(score, high_score):
    game_over_text = turtle.Turtle()
    game_over_text.speed(0)
    game_over_text.color("white")
    game_over_text.penup()
    game_over_text.hideturtle()
    window_width = wn.window_width()
    window_height = wn.window_height()
    x_center = 0
    y_center = 0
    game_over_text.goto(x_center, y_center)
    lines = [
        "GAME OVER",
        f"Your score is: {score}",
        f"High score is: {high_score}"
    ]
    for index, line in enumerate(lines):
        game_over_text.goto(x_center, y_center - (index * 30))
        game_over_text.write(line, align="center", font=("Courier", 18, "bold"))
    return game_over_text

#starting the snake_game
def start_snake_game(delay):
    global score, high_score, segments, head, food, scoreBoard, game_over_elements, play_again_button, quit_button

    score = 0
    high_score = read_high_score()
    segments = []

    #height and width
    wn.title("SNAKE GAME")
    wn.bgcolor(BACKGROUND_COLOR)
    wn.setup(width=GRID_WIDTH, height=GRID_HEIGHT)
    wn.tracer(0)

    #boder
    create_game_border()

    #head
    head = create_snake_head()

    #food
    food = create_food() 
    food = generate_food(food)


    #score
    scoreBoard = create_scoreboard(high_score)

    #direction
    bind_key_directions(head)

    segments = []

    #main game
    game_over_elements = []
    running = True
    while running:
        wn.update()
        if check_collision_with_border(head):
            end_game(score, high_score)
            running = False
            continue

        #collecting food
        if head.distance(food) < 20:
            score += 10
            if score > high_score:
                high_score = score
                save_high_score(high_score)
            update_score(scoreBoard, score, high_score)
            food = generate_food(food)
            add_snake_segment(segments, head)

        move_snake(segments, head)

        if check_collision_with_self(segments, head):
            end_game(score, high_score)
            running = False
            continue
        time.sleep(delay)
    turtle.done()

def create_game_border():
    border = turtle.Turtle()
    border.speed(5)
    border.pensize(4)
    border.penup()
    border.goto(-310, 250)
    border.pendown()
    border.color('white')
    for _ in range(2):
        border.forward(620)
        border.right(90)
        border.forward(500)
        border.right(90)
    border.penup()
    border.hideturtle()

def create_snake_head():
    head = turtle.Turtle()
    head.speed(0)
    head.shape("square")
    head.color(SNAKE_COLOR)
    head.penup()
    head.goto(0, 0)
    head.direction = "Stop"
    return head



def create_scoreboard(high_score):
    scoreBoard = turtle.Turtle()
    scoreBoard.speed(0)
    scoreBoard.shape("square")
    scoreBoard.color("white")
    scoreBoard.penup()
    scoreBoard.hideturtle()
    scoreBoard.goto(0, 260)
    scoreBoard.write("score: 0 high score: {}".format(high_score), align="center",
                     font=("courier", 25, "bold"))
    return scoreBoard

def bind_key_directions(head):
    def move_up():
        if head.direction != "down":
            head.direction = "up"

    def move_down():
        if head.direction != "up":
            head.direction = "down"

    def move_left():
        if head.direction != "right":
            head.direction = "left"

    def move_right():
        if head.direction != "left":
            head.direction = "right"

    wn.listen()
    wn.onkeypress(move_up, "Up")
    wn.onkeypress(move_down, "Down")
    wn.onkeypress(move_left, "Left")
    wn.onkeypress(move_right, "Right")

def check_collision_with_border(head):
    return head.xcor() > 300 or head.xcor() < -310 or head.ycor() > 240 or head.ycor() < -240

def check_collision_with_self(segments, head):
    for segment in segments:
        if segment.distance(head) < 20:
            return True
    return False

def end_game(score, high_score):
    time.sleep(1)
    wn.clear()
    wn.bgcolor(BACKGROUND_COLOR)
    create_game_over_elements(score, high_score)
    create_game_over_menu()

def create_game_over_menu():
    global play_again_button, quit_button
    play_again_button = tk.Button(canvas.master, text="Play again", command=start_game)
    play_again_button.pack()
    quit_button = tk.Button(canvas.master, text="Quit Game", command=quit_game)
    quit_button.pack()

def update_score(scoreBoard, score, high_score):
    scoreBoard.clear()
    scoreBoard.write("score: {} high score: {} ".format(score, high_score), align="center", font=("courier", 25, "bold"))

def create_food():
    food = turtle.Turtle()
    food_color = random.choice(FOOD_COLORS)
    food.speed(0)
    food.shape('circle') 
    food.color(food_color) 
    food.penup()
    food.goto(20, 20) 
    return food

def generate_food(food):
    x_cord = random.randint(-14, 14) * 20 
    y_cord = random.randint(-11, 11) * 20 
    food_color = random.choice(FOOD_COLORS) 
    food.shape('circle')
    food.color(food_color) 
    food.goto(x_cord, y_cord)
    return food



def add_snake_segment(segments, head):
    new_segment = turtle.Turtle()
    new_segment.speed(0)
    new_segment.shape("square")
    new_segment.color("white smoke")
    new_segment.penup()
    segments.append(new_segment)

def move_snake(segments, head):
    for i in range(len(segments) - 1, 0, -1):
        x = segments[i - 1].xcor()
        y = segments[i - 1].ycor()
        segments[i].goto(x, y)
    if len(segments) > 0:
        x = head.xcor()
        y = head.ycor()
        segments[0].goto(x, y)
    move(head)

def move(head):
    if head.direction == "up":
        y = head.ycor()
        head.sety(y + 20)
    if head.direction == "down":
        y = head.ycor()
        head.sety(y - 20)
    if head.direction == "left":
        x = head.xcor()
        head.setx(x - 20)
    if head.direction == "right":
        x = head.xcor()
        head.setx(x + 20)

#screen
wn = turtle.Screen()
wn.title("Snake Game Menu")
wn.bgcolor(BACKGROUND_COLOR)
wn.setup(width=GRID_WIDTH, height=GRID_HEIGHT)

#canvas from turtle scren
canvas = wn.getcanvas()

#frame for buttons
frame = tk.Frame(canvas.master)
frame.pack()

#start button
start_button = tk.Button(frame, text="Start Game", command=start_game)
start_button.pack(side=tk.LEFT)

#quit button
quit_button = tk.Button(frame, text="Quit Game", command=quit_game)
quit_button.pack(side=tk.RIGHT)

#button references
play_again_button = None
quit_button = None

#main window loop
wn.mainloop()

