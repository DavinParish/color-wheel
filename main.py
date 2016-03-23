from copy import deepcopy
import json
from random import randint
import bullet
import target
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

# !!!Initial setup!!!

# MAIN FILE VARIABLES
go = True  # how the program knows when to go or quit
speed = 2  # how fast to move the bullet up
points = 0
fired = False

TILE_WIDTH = 24
TILE_HEIGHT = 24
w = 24
h = 24

# make bullet
game_bullet = bullet.Bullet
# make target
game_target = target.Target

# WINDOW
screen_width = 400
screen_height = 500
screen = pygame.display.set_mode([screen_width, screen_height])

# DICTIONARY
color_dict = {
    pygame.K_r: (215, 23, 23),  # red
    pygame.K_b: (23, 23, 236),  # blue
}

# BOARD
board = []
row = []
# fill out rows
for i in range(17):
    row.append('0')
# fill out board
for i in range(23):
    board.append(row)


# !!!Functions!!!

# DRAW BOARD
def draw():
    # # TEST RECTANGLE
    for y, array in enumerate(board):
        for x, symbol in enumerate(array):
            pygame.draw.rect(screen, (128, 0, 64, 28), (x * w, y * h, w, h), 1)

    # TESTING
    # screen.fill((0, 0, 255))  # fill screen with blue

    # draw turret
    # draw bullet
    # draw target
    pygame.display.flip()


# !!!Game!!!
# MAIN GAME LOOP
while go:
    # UPDATE THE BOARD
    draw()
    print("drawing")

    # HANDLE KEY PRESSES
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                quit()
            elif event.key in color_dict:
                game_bullet.color = color_dict[event.key]
                fired = True
    # HANDLE FOR WHEN THE BULLET IS FIRED AND WHEN IT HITS
    while fired:
        print("fired")#so I know the code has been reached
        # move the bullet upwards
        game_bullet.bull[0] += 1
        # check for collision with target
        if game_bullet.bull[0] == game_target.tar[0]:
            if game_bullet.color == game_target.color:
                points += 1
                print("yay")#for debugging purposes so I know the code is reached
            else:
                points -=1
                print("dang")#for debuggin purposes so I know the code has been reached
        # update the board
