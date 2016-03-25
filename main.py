from copy import deepcopy
import json
from random import choice

import bullet
import target
from button import PygButton
import turret

import pygame
import os
import pygame.font
import pygame.event
import pygame.draw
import pygame.mixer
import pygame.image

pygame.display.init()
pygame.font.init()
pygame.mixer.init()
pygame.init()

# /////////////////////////////////////////////////////////////////////////////////// #


# VARIABLES //////////////////////////////////////////////////////
go = True  # how the program knows when to go or quit
speed = 10  # how fast to update the board
TILE_WIDTH = 24
TILE_HEIGHT = 24
w = 24
h = 24
# number of columns
num_columns = 15
# number of rows
num_rows = 20

# DICTIONARIES //////////////////////////////////////////////////
color_dict = {
    pygame.K_r: (215, 23, 23),  # red
    pygame.K_b: (23, 23, 236),  # blue

}

# INSTANTIATIONS ///////////////////////////////////////////////
game_bullet = bullet.Bullet()  # make bullet
game_bullet.getPos(num_columns, num_rows)  # position the bullet relative to the size of the screen
game_target = target.Target()  # make target

# WINDOW SETUP ////////////////////////////////////////////////
screen_width = TILE_WIDTH * num_columns
screen_height = TILE_HEIGHT * num_rows
screen = pygame.display.set_mode([screen_width, screen_height])

# BUILD BOARD ////////////////////////////////////////////////
board = []
row = []
for i in range(num_columns):  # make the right number of columns
    row.append('0')
for i in range(num_rows):  # make the right number of rows of those columns
    board.append(row)


# GENERAL FUNCTIONS /////////////////////////////////////////

# reset function
def reset():
    game_bullet.y = game_bullet.init_y  # reset bullets position
    game_bullet.color = (0, 0, 0, 255)  # make bullet invisible
    game_bullet.fired = False

    game_target.current_life_span = game_target.initial_life_span  # reset targets lifespan
    # change the targets color (make sure it doesn't use the same color twice in a row)
    prev_color = game_target.color
    game_target.color = color_dict[choice(list(color_dict.keys()))]  # choose a random color for the target
    while prev_color == game_target.color:
        game_target.color = color_dict[choice(list(color_dict.keys()))]  # choose a random color for the target


# function to decrement the lifespan of the target
def decrement_life():
    if game_target.current_life_span <= 0:
        reset()
        game_bullet.points -= 1  # increase game_bullet.points
        print("Too slow!!")
    else:
        game_target.current_life_span -= 1


# display text
def display_box(message, position):
    font_object = pygame.font.SysFont('Times New Roman', 18)
    if message:
        text = font_object.render(message, 1, (255, 0, 0, 255))

        screen.blit(text, position)


# POP UPS //////////////////////////////////////////////////


# DISPLAYS /////////////////////////////////////////////////
def draw_game():
    screen.fill((0, 0, 0, 255))  # fill screen with black
    for y, array in enumerate(board):  # draw grid
        for x, symbol in enumerate(array):
            pygame.draw.rect(screen, (128, 0, 64, 28), (x * w, y * h, w, h), 1)
    # draw turret
    # draw bullet
    pygame.draw.rect(screen, game_bullet.color,
                     (game_bullet.x * TILE_WIDTH, game_bullet.y * TILE_WIDTH, TILE_WIDTH, TILE_HEIGHT))
    # draw target
    pygame.draw.rect(screen, game_target.color, (
        game_target.x * TILE_WIDTH, game_target.y * TILE_WIDTH, TILE_WIDTH * num_columns, 2 * TILE_HEIGHT))

    display_box("Score: " + str(game_bullet.points), (0, 0))  # show score
    pygame.display.flip()  # flip


# MODE LOOPS //////////////////////////////////////////////


# MAIN LOOP //////////////////////////////////////////////
while go:
    # UPDATE THE BOARD
    draw_game()
    decrement_life()
    print(game_target.current_life_span)
    # HANDLE KEY PRESSES
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                quit()
            elif event.key in color_dict and not game_bullet.fired:
                game_bullet.color = color_dict[event.key]
                game_bullet.fired = True

    # HANDLE FOR WHEN THE BULLET IS FIRED AND WHEN IT HITS
    if game_bullet.fired:
        print("fired")  # so I know the code has been reached

        # MOVE THE BULLET
        game_bullet.move()
        print("moving")

        # check for collision with target
        if game_bullet.y == game_target.y:
            print("BLAARGHH!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!11")
            if game_bullet.color == game_target.color:
                game_bullet.points += 1  # increase game_bullet.points
                print("yay")  # for debugging purposes so I know the code is reached
            else:
                game_bullet.points -= 1  # increase game_bullet.points
                game_bullet.fired = False
                print("dang")  # for debugging purposes so I know the code has been reached

            reset()
    print("USER SCORE:")
    print(game_bullet.points)
    # WAIT
    game_timer = pygame.time
    game_timer.wait(int(speed))
