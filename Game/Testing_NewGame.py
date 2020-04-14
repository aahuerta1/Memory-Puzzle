import random, pygame, sys, time
from pygame.locals import *  # puts a limited set of constants and functions into the global namespace of our script

pygame.init() # initializes pygame

FPS = 30  # frames per second, the general speed of the program
displayWidth = 640  # size of window's width in pixels
displayHeight = 480  # size of windows' height in pixels
box_reveal_spd = 8  # speed boxes' sliding reveals and covers
box_size = 40  # size of box height & width in pixels
gap = 10  # size of gap between boxes in pixels
tile_width = 6  # number of columns of icons
tile_height = 5  # number of rows of icons
assert (tile_width * tile_height) % 2 == 0, 'Board needs to have an even number of boxes for pairs of matches.'
x_margin = int((displayWidth - (tile_width * (box_size + gap))) / 2)
y_margin = int((displayHeight - (tile_height * (box_size + gap))) / 2)

#            R    G    B
GRAY = (100, 100, 100)
NAVYBLUE = (60, 60, 100)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 128, 0)
PURPLE = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

backgroud_color = NAVYBLUE
lightBGcolor = GRAY
box_color = WHITE
highlight_color = BLUE

donut = 'donut'
square = 'square'
diamond = 'diamond'
lines = 'lines'
oval = 'oval'

all_colors = (RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, CYAN)
all_shapes = (donut, square, diamond, lines, oval)
assert len(all_colors) * len(all_shapes) * 2 >= tile_width * tile_height, \
    "Board is too big for the number of shapes/colors defined."
gameDisplay = pygame.display.set_mode((displayWidth, displayHeight))


def text_objects(text, font):
    textSurface = font.render(text, True, BLACK)
    return textSurface, textSurface.get_rect()


def messageDisimport random, pygame, sys, time
from pygame.locals import *  # puts a limited set of constants and functions into the global namespace of our script

pygame.init() # initializes pygame

FPS = 30  # frames per second, the general speed of the program
displayWidth = 640  # size of window's width in pixels
displayHeight = 480  # size of windows' height in pixels
box_reveal_spd = 8  # speed boxes' sliding reveals and covers
box_size = 40  # size of box height & width in pixels
gap = 10  # size of gap between boxes in pixels
tile_width = 6  # number of columns of icons
tile_height = 5  # number of rows of icons

gameDisplay = pygame.display.set_mode((displayWidth, displayHeight)) # This represents the window that opens up (GUI)
clock = pygame.time.Clock() # This is what helps us define time in the game

pygame.display.set_caption('Memory Puzzle Game') # Displays the name of the game (top right)

assert (tile_width * tile_height) % 2 == 0, 'Board needs to have an even number of boxes for pairs of matches.'
x_margin = int((displayWidth - (tile_width * (box_size + gap))) / 2)
y_margin = int((displayHeight - (tile_height * (box_size + gap))) / 2)

#                R    G    B
GRAY        = (100, 100, 100)
DARKBLUE    = (  0,   0, 100)
WHITE       = (255, 255, 255)
RED         = (200,   0,   0)
GREEN       = (  0, 150,   0)
PINK        = (255, 182, 193)
YELLOW      = (255, 255,   0)
ORANGE      = (255, 128,   0)
PURPLE      = (255,   0, 255)
CYAN        = (  0, 255, 255)
BLACK       = (  0,   0,   0)
WHITE       = (255, 255, 255)
BLUE        = (  0,   0, 255)

# Button Color Effects
BRIGHTRED   = (255,   0,   0)
BRIGHTGREEN = (  0, 255,   0)

backgroud_color = DARKBLUE
lightBGcolor = GRAY
box_color = WHITE
highlight_color = PINK

donut = 'donut'
square = 'square'
diamond = 'diamond'
lines = 'lines'
oval = 'oval'

all_colors = (RED, GREEN, PINK, YELLOW, ORANGE, PURPLE, CYAN, DARKBLUE, WHITE, BLACK, BLUE)
all_shapes = (donut, square, diamond, lines, oval)
assert len(all_colors) * len(all_shapes) * 2 >= tile_width * tile_height, \
    "Board is too big for the number of shapes/colors defined."

def text_objects(text, font):
    textSurface = font.render(text, True, BLACK)
    return textSurface, textSurface.get_rect()


def messageDisplay(text):
    largeText = pygame.font.Font('freesansbold.ttf', 115)
    textSurf, textRect = text_objects("Memory Puzzle Game", largeText)
    textRect.center = ((displayWidth / 2), (displayHeight / 2))
    gameDisplay.blit(textSurf, textRect)

    pygame.display.update()  # updates texts on our display

    time.sleep(2)

    main()

def game_Intro():

    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gameDisplay.fill(backgroud_color)
        largeText = pygame.font.Font('freesansbold.ttf', 50)
        TextSurf, TextRect = text_objects("Memory Puzzle Game", largeText)
        TextRect.center = ((displayWidth / 2), (displayHeight / 2))
        gameDisplay.blit(TextSurf, TextRect)

        mouse = pygame.mouse.get_pos() # gets the position of the mouse

        #PLAY BUTTON
        if 50 + 100 > mouse[0] > 50 and 350 + 50 > mouse[1] > 350:
            #                                      X,   Y, Width, Height
            pygame.draw.rect(gameDisplay, BRIGHTGREEN, (50, 350, 100, 50))
        else:
            pygame.draw.rect(gameDisplay, GREEN, (50, 350, 100, 50))

              # QUIT BUTTON
        if 500 + 100 > mouse[0] > 500 and 350 + 50 > mouse[1] > 350:
        #                                      X,   Y, Width, Height
            pygame.draw.rect(gameDisplay, BRIGHTRED, (500, 350, 100, 50))
        else:
            pygame.draw.rect(gameDisplay, RED, (500, 350, 100, 50))

        pygame.display.update()
        clock.tick(15)

def main():
    global clock, gameDisplay

    mousex = 0  # used to store x coordinate of mouse event
    mousey = 0  # used to store y coordinate of mouse event

    mainBoard = getRandomizedBoard()
    revealedBoxes = generateRevealedBoxesData(False)

    firstSelection = None  # stores the (x, y) of the first box clicked.

    gameDisplay.fill(backgroud_color)
    startGameAnimation(mainBoard)

    while True:  # main game loop
        mouseClicked = False

        gameDisplay.fill(backgroud_color)  # drawing the window
        drawBoard(mainBoard, revealedBoxes)

        for event in pygame.event.get():  # event handling loop
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True

        boxx, boxy = getBoxAtPixel(mousex, mousey)
        if boxx != None and boxy != None:
            # The mouse is currently over a box.
            if not revealedBoxes[boxx][boxy]:
                drawHighlightBox(boxx, boxy)
            if not revealedBoxes[boxx][boxy] and mouseClicked:
                revealBoxesAnimation(mainBoard, [(boxx, boxy)])
                revealedBoxes[boxx][boxy] = True  # set the box as "revealed"
                if firstSelection == None:  # the current box was the first box clicked
                    firstSelection = (boxx, boxy)
                else:  # the current box was the second box clicked
                    # Check if there is a match between the two icons.
                    icon1shape, icon1color = getShapeAndColor(mainBoard, firstSelection[0], firstSelection[1])
                    icon2shape, icon2color = getShapeAndColor(mainBoard, boxx, boxy)

                    if icon1shape != icon2shape or icon1color != icon2color:
                        # Icons don't match. Re-cover up both selections.
                        pygame.time.wait(1000)  # 1000 milliseconds = 1 sec
                        coverBoxesAnimation(mainBoard, [(firstSelection[0], firstSelection[1]), (boxx, boxy)])
                        revealedBoxes[firstSelection[0]][firstSelection[1]] = False
                        revealedBoxes[boxx][boxy] = False
                    elif wonGame(revealedBoxes):  # check if all pairs found
                        winningAnimation(mainBoard)
                        pygame.time.wait(2000)

                        # Reset the board
                        mainBoard = getRandomizedBoard()
                        revealedBoxes = generateRevealedBoxesData(False)

                        # Show the fully unrevealed board for a second.
                        drawBoard(mainBoard, revealedBoxes)
                        pygame.display.update()
                        pygame.time.wait(1000)

                        # Replay the start game animation.
                        startGameAnimation(mainBoard)
                    firstSelection = None  # reset firstSelection variable

        # Redraw the screen and wait a clock tick.
        pygame.display.update()
        clock.tick(FPS)

def generateRevealedBoxesData(val):
    revealedBoxes = []
    for i in range(tile_width):
        revealedBoxes.append([val] * tile_height)
    return revealedBoxes


def getRandomizedBoard():
    # Get a list of every possible shape in every possible color.
    icons = []
    for color in all_colors:
        for shape in all_shapes:
            icons.append((shape, color))

    random.shuffle(icons)  # randomize the order of the icons list
    numIconsUsed = int(tile_width * tile_height / 2)  # calculate how many icons are needed
    icons = icons[:numIconsUsed] * 2  # make two of each
    random.shuffle(icons)

    # Create the board data structure, with randomly placed icons.
    board = []
    for x in range(tile_width):
        column = []
        for y in range(tile_height):
            column.append(icons[0])
            del icons[0]  # remove the icons as we assign them
        board.append(column)
    return board


def splitIntoGroupsOf(groupSize, theList):
    # splits a list into a list of lists, where the inner lists have at
    # most groupSize number of items.
    result = []
    for i in range(0, len(theList), groupSize):
        result.append(theList[i:i + groupSize])
    return result


def leftTopCoordsOfBox(boxx, boxy):
    # Convert board coordinates to pixel coordinates
    left = boxx * (box_size + gap) + x_margin
    top = boxy * (box_size + gap) + y_margin
    return (left, top)


def getBoxAtPixel(x, y):
    for boxx in range(tile_width):
        for boxy in range(tile_height):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            boxRect = pygame.Rect(left, top, box_size, box_size)
            if boxRect.collidepoint(x, y):
                return (boxx, boxy)
    return (None, None)


def drawIcon(shape, color, boxx, boxy):
    quarter = int(box_size * 0.25)  # syntactic sugar
    half = int(box_size * 0.5)  # syntactic sugar

    left, top = leftTopCoordsOfBox(boxx, boxy)  # get pixel coords from board coords
    # Draw the shapes
    if shape == donut:
        pygame.draw.circle(gameDisplay, color, (left + half, top + half), half - 5)
        pygame.draw.circle(gameDisplay, backgroud_color, (left + half, top + half), quarter - 5)
    elif shape == square:
        pygame.draw.rect(gameDisplay, color, (left + quarter, top + quarter, box_size - half, box_size - half))
    elif shape == diamond:
        pygame.draw.polygon(gameDisplay, color, (
        (left + half, top), (left + box_size - 1, top + half), (left + half, top + box_size - 1), (left, top + half)))
    elif shape == lines:
        for i in range(0, box_size, 4):
            pygame.draw.line(gameDisplay, color, (left, top + i), (left + i, top))
            pygame.draw.line(gameDisplay, color, (left + i, top + box_size - 1), (left + box_size - 1, top + i))
    elif shape == oval:
        pygame.draw.ellipse(gameDisplay, color, (left, top + quarter, box_size, half))


def getShapeAndColor(board, boxx, boxy):
    # shape value for x, y spot is stored in board[x][y][0]
    # color value for x, y spot is stored in board[x][y][1]
    return board[boxx][boxy][0], board[boxx][boxy][1]


def drawBoxCovers(board, boxes, coverage):
    # Draws boxes being covered/revealed. "boxes" is a list
    # of two-item lists, which have the x & y spot of the box.
    for box in boxes:
        left, top = leftTopCoordsOfBox(box[0], box[1])
        pygame.draw.rect(gameDisplay, backgroud_color, (left, top, box_size, box_size))
        shape, color = getShapeAndColor(board, box[0], box[1])
        drawIcon(shape, color, box[0], box[1])
        if coverage > 0:  # only draw the cover if there is an coverage
            pygame.draw.rect(gameDisplay, box_color, (left, top, coverage, box_size))
    pygame.display.update()
    clock.tick(FPS)


def revealBoxesAnimation(board, boxesToReveal):
    # Do the "box reveal" animation.
    for coverage in range(box_size, (-box_reveal_spd) - 1, -box_reveal_spd):
        drawBoxCovers(board, boxesToReveal, coverage)


def coverBoxesAnimation(board, boxesToCover):
    # Do the "box cover" animation.
    for coverage in range(0, box_size + box_reveal_spd, box_reveal_spd):
        drawBoxCovers(board, boxesToCover, coverage)


def drawBoard(board, revealed):
    # Draws all of the boxes in their covered or revealed state.
    for boxx in range(tile_width):
        for boxy in range(tile_height):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            if not revealed[boxx][boxy]:
                # Draw a covered box.
                pygame.draw.rect(gameDisplay, box_color, (left, top, box_size, box_size))
            else:
                # Draw the (revealed) icon.
                shape, color = getShapeAndColor(board, boxx, boxy)
                drawIcon(shape, color, boxx, boxy)


def drawHighlightBox(boxx, boxy):
    left, top = leftTopCoordsOfBox(boxx, boxy)
    pygame.draw.rect(gameDisplay, highlight_color, (left - 5, top - 5, box_size + 10, box_size + 10), 4)


def startGameAnimation(board):
    # Randomly reveal the boxes 10 at a time.
    coveredBoxes = generateRevealedBoxesData(False)
    boxes = []
    for x in range(tile_width):
        for y in range(tile_height):
            boxes.append((x, y))
    random.shuffle(boxes)
    boxGroups = splitIntoGroupsOf(2, boxes)

    drawBoard(board, coveredBoxes)
    for boxGroup in boxGroups:
        revealBoxesAnimation(board, boxGroup)
        coverBoxesAnimation(board, boxGroup)


def winningAnimation(board):
    # flash the background color when the player has won
    coveredBoxes = generateRevealedBoxesData(True)
    color1 = lightBGcolor
    color2 = backgroud_color

    for i in range(13):
        color1, color2 = color2, color1  # swap colors
        gameDisplay.fill(color1)
        drawBoard(board, coveredBoxes)
        pygame.display.update()
        pygame.time.wait(300)


def wonGame(revealedBoxes):
    # Returns True if all the boxes have been revealed, otherwise False
    for i in revealedBoxes:
        if False in i:
            return False  # return False if any boxes are covered.
    return True


game_Intro()
main()
pygame.quit()
quit()
play(text):
    largeText = pygame.font.Font('freesansbold.ttf', 115)
    TextSurf, TextRect = text_objects("Memory Puzzle Game", largeText)
    TextRect.center = ((displayWidth / 2), (displayHeight / 2))
    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update()  # updates texts on our display

    time.sleep(2)


def game_Intro():

    intro = True

    while intro:
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gameDisplay.fill(backgroud_color)
        largeText = pygame.font.Font('freesansbold.ttf', 115)
        TextSurf, TextRect = text_objects("Memory Puzzle Game", largeText)
        TextRect.center = ((displayWidth / 2), (displayHeight / 2))
        gameDisplay.blit(TextSurf, TextRect)
        pygame.display.update()


game_Intro()
pygame.quit()
quit()
