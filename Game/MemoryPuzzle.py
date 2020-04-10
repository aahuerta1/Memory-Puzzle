#PuzzleWithin Inc: Memory Puzzle
#Creators: Alan Huerta, Besty Andrade, Monseratt Moreno
#Class: CIS 260
import random
import pygame
import sys

FPS = 30 # frames per second, the general speed of the program
window_width = 640 # size of window's width in pixels
window_height = 480 # size of windows' height in pixels
box_reveal_spd = 8 # speed boxes' sliding reveals and covers
box_size = 40 # size of box height and width in pixels
gap = 10 # size of gap between boxes in pixels
board_width = 10 # number of columns of icons
board_height = 7 # number of rows of icons

X_margin = int((board_width - (board_width * (box_size + gap))) / 2)
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

allColors = (RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, CYAN)
allShapes = (donut, square, diamond, lines, oval)
assert len(Colors) * len(Shapes) * 2 >= board_width * board_height, \
"Board is too big for the number of shapes/colors defined."

def main():
    global FPSCLOCK, ShowSurface
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    ShowSurface = pygame.display.set_mode((window_width, window_height))

    xx = 0 # used to store x coordinate of mouse event
    yy = 0 # used to store y coordinate of mouse event
    pygame.display.set_caption('Memory Game')

    mainBoard = getRandomizedBoard()
    revealedBoxes = revealedBoxData(False)

    firstSelection = None # stores the (x, y) of the first box clicked.

    ShowSurface.fill(BGCOLOR)
    startGameAnimation(mainBoard)

    while True:  # main game loop
        mouseClicked = False

        ShowSurface.fill(BGCOLOR)  # drawing the window
        drawBoard(mainBoard, revealedBoxes)

        for event in pygame.event.get(): # event handling loop
            if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEMOTION:
                xx, yy = event.pos
            elif event.type == pygame.MOUSEBUTTONUP:
                xx, yy = event.pos
                mouseClicked = True

        boxX, boxY = getBoxAtPixel(xx, yy)
        if boxX is not None and boxY is not None: # Was like this -- if boxX != None and boxY != None: --

            # The mouse is currently over a box.
            if not revealedBoxes[boxX][boxY]:
                drawHighlightBox(boxX, boxY)

            if not revealedBoxes[boxX][boxY] and mouseClicked:
                revealBoxesAnimation(mainBoard, [(boxX, boxY)])
                revealedBoxes[boxX][boxY] = True # set the box as "revealed"
                if firstSelection == None: # the current box was the first box clicked
                    firstSelection = (boxX, boxY)

                else:
                    # the current box was the second box clicked
                    # Check if there is a match between the two icons. (!!!Basically check if the answer is right!!!)
                    icon1shape, icon1color = getShapeAndColor(mainBoard, firstSelection[0], firstSelection[1])
                    icon2shape, icon2color = getShapeAndColor(mainBoard, boxX, boxY)

                    if icon1shape != icon2shape or icon1color != icon2color:
                        # If icons don't match. Re-cover up both selections.
                        pygame.time.wait(1000) # 1000 milliseconds = 1 sec
                        coverBoxesAnimation(mainBoard, [(firstSelection[0], firstSelection[1]), (boxX, boxY)])
                        revealedBoxes[firstSelection[0]][firstSelection [1]] = False
                        revealedBoxes[boxX][boxY] = False
                    elif FinishedGame(revealedBoxes): # check if all pairs found
                        WinningAnimation(mainBoard)
                        pygame.time.wait(2000)

                        # Reset the Game Board
                        mainBoard = getRandomizedBoard()
                        revealedBoxes = revealedBoxData(False)

                        # Show the fully unrevealed board for a second.
                        drawBoard(mainBoard, revealedBoxes)
                        pygame.display.update()
                        pygame.time.wait(1000)

                        # Replay the start game animation.
                        startGameAnimation(mainBoard)

                        firstSelection = None # reset firstSelection variable

        #Redraw the screen and wait a clock tick.
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def revealedBoxData(val):
    revealedBoxes = []
    for i in range(board_width):
        revealedBoxes.append([val] * board_height)
    return revealedBoxes

def getRandomizedBoard():
    # Get a list of every possible shape in every possible color.
    icons = []
    for color in allColors:
        for shape in allShapes:
            icons.append((shape, color))

    random.shuffle(icons) # randomize the order of the icons list
    totalIconsUsed = int(board_width * board_height / 2) # calculate how many icons are needed
    icons = icons[:totalIconsUsed] * 2 # make two of each
    random.shuffle(icons)

    #Create the board data structure, with randomly placed icons.
    board = []
    for x in range(board_width):
        column = []
        for y in range(board_height):
            column.append(icons[0])
            del icons[0] # remove the icons as we assign them
        board.append(column)
    return board

def splitIntoGroupsOf(groupSize, theList):
    # splits a list into a list of lists, where the inner lists have at
    # most groupSize number of items.
    result = []
    for i in range(0, len(theList), groupSize):
        result.append(theList[i:i + groupSize])
    return result

def leftTopCoordsOfBox(boxX, boxY):
    # Convert board coordinates to pixel coordinates
    left = boxX * (box_size + gap) + X_margin
    top = boxY * (box_size + gap) + Y_margin
    return (left, top)

def getBoxAtPixel(x, y):
    for boxX in range(board_width):
        for boxY in range(board_height):
            left, top = leftTopCoordsOfBox(boxX, boxY)
            boxRect = pygame.Rect(left, top, box_size, box_size)
            if boxRect.collidepoint(x, y):
                return (boxX, boxY)
    return (None, None)

def drawIcon(shape, color, boxX, boxY):
    quarter = int(box_size * 0.25) # syntactic sugar
    half = int(box_size * 0.5)  # syntactic sugar
    left, top = leftTopCoordsOfBox(boxX, boxY) # get pixel coordinates from board coordinates

    # Draw the shapes
    if shape == donut:
        pygame.draw.circle(ShowSurface, color, (left + half, top + half), half - 5)
        pygame.draw.circle(ShowSurface, BGCOLOR, (left + half, top + half), quarter - 5)

    elif shape == square:
        pygame.draw.rect(ShowSurface, color, (left + quarter, top + quarter, box_size - half, box_size - half))

    elif shape == diamond:
        pygame.draw.polygon(ShowSurface, color, ((left + half, top), (left + box_size - 1, top + half)
                                                 , (left + half, top + box_size - 1), (left, top + half)))

    elif shape == lines:
        for i in range(0, box_size, 4):
            pygame.draw.line(ShowSurface, color, (left, top + i), (left + i, top))
            pygame.draw.line(ShowSurface, color, (left + i, top + box_size - 1), (left + box_size - 1, top + i))

    elif shape == oval:
        pygame.draw.ellipse(ShowSurface, color, (left, top + quarter, box_size, half))


def getShapeAndColor(board, boxX, boxY):
    # shape value for x, y spot is stored in board[x][y][0]
    # color value for x, y spot is stored in board[x][y][1]
    return board[boxX][boxY][0], board[boxX][boxY][1]

def drawBoxCovers(board, boxes, coverage):
    # Draws boxes being covered/revealed. "boxes" is a list
    # of two-item lists, which have the x & y spot of the box.
    for box in boxes:
        left, top = leftTopCoordsOfBox(box[0], box[1])
        pygame.draw.rect(ShowSurface, BGCOLOR, (left, top, box_size, box_size))
        shape, color = getShapeAndColor(board, box[0], box[1])
        drawIcon(shape, color, box[0], box[1])
        if coverage > 0:  # only draw the cover if there is an coverage
            pygame.draw.rect(ShowSurface, BOXCOLOR, (left, top, coverage, box_size))
    pygame.display.update()
    FPSCLOCK.tick(FPS)

def revealBoxesAnimation(board, boxesToReveal):
    # Do the "box reveal" animation.
    for coverage in range(box_size, (-box_reveal_spd) - 1, - box_reveal_spd):
        drawBoxCovers(board, boxesToReveal, coverage)

def coverBoxesAnimation(board, boxesToCover):
    # Do the "box cover" animation.
    for coverage in range(0, box_size + box_reveal_spd, box_reveal_spd):
        drawBoxCovers(board, boxesToCover, coverage)


def drawBoard(board, revealed):
    # Draws all of the boxes in their covered or revealed state.
    for boxX in range(board_width):
        for boxY in range(board_height):
            left, top = leftTopCoordsOfBox(boxX, boxY)
            if not revealed[boxX][boxY]:
                # Draw a covered box.
                pygame.draw.rect(ShowSurface, BOXCOLOR, (left, top, box_size, box_size))
            else:
                # Draw the (revealed) icon.
                shape, color = getShapeAndColor(board, boxX, boxY)
                drawIcon(shape, color, boxX, boxY)

def drawHighlightBox(boxX, boxY):
    left, top = leftTopCoordsOfBox(boxX, boxY)
    pygame.draw.rect(ShowSurface, HIGHLIGHTCOLOR, (left - 5, top - 5, box_size + 10, box_size + 10), 4)

def startGameAnimation(board):
    # Randomly reveal the boxes 8 at a time.
    coveredBoxes = revealedBoxData(False)
    boxes = []
    for x in range(board_width):
        for y in range(board_height):
            boxes.append((x, y))
    random.shuffle(boxes)
    boxGroups = splitIntoGroupsOf(8, boxes)

    drawBoard(board, coveredBoxes)
    for boxGroup in boxGroups:
        revealBoxesAnimation(board, boxGroup)
        coverBoxesAnimation(board, boxGroup)

def WinningAnimation(board):
    # flash the background color when the player has won
    coveredBoxes = revealedBoxData(True)
    color1 = LIGHTBGCOLOR
    color2 = BGCOLOR
    for i in range(13):
        color1, color2 = color2, color1  # swap colors
        ShowSurface.fill(color1)
        drawBoard(board, coveredBoxes)
        pygame.display.update()
        pygame.time.wait(300)


def FinishedGame(revealedBoxes):
    # Returns True if all the boxes have been revealed, otherwise False
    for i in revealedBoxes:
        if False in i:
            return False  # return False if any boxes are covered.
    return True


if __name__ == '__main__':
    main()
