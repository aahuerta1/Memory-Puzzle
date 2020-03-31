#PuzzleWithin Inc: Memory Puzzle
#Creators: Alan Huerta, Besty Andrade, Monseratt Moreno
#Class: CIS 260
import random, pygame, sys

FPS = 30 # frames per second, the general speed of the program
window_with = 640 # size of window's width in pixels
window_height = 480 # size of windows' height in pixels
box_reveal_spd = 8 # speed boxes' sliding reveals and covers
box_size = 40 # size of box height and width in pixels
gap = 10 # size of gap between boxes in pixels
board_with = 10 # number of columns of icons
board_height = 7 # number of rows of icons

X_margin = int((window_with - (board_with * (box_size + gap))) / 2)
Y_margin = int((window_height - (board_height * (box_size + gap))) / 2)

#            R    G    B
GRAY     = (100, 100, 100)
LIGHTBLUE= ( 60,  60, 100)
WHITE    = (255, 255, 255)
RED      = (255,   0,   0)
GREEN    = (  0, 255,   0)
BLUE     = (  0,   0, 255)
YELLOW   = (255, 255,   0)
ORANGE   = (255, 128,   0)
PURPLE   = (255,   0, 255)
CYAN     = (  0, 255, 255)

BGCOLOR = LIGHTBLUE
LIGHTBGCOLOR = GRAY
BOXCOLOR = WHITE
HIGHLIGHTCOLOR = BLUE

donut = 'donut'
square = 'square'
diamond = 'diamond'
lines = 'lines'
oval = 'oval'

Colors = (RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, CYAN)
Shapes = (donut, square, diamond, lines, oval)

assert len(Colors) * len(Shapes) * 2 >= board_with * board_height, \
 "Board is too big for the number of shapes/colors defined."
