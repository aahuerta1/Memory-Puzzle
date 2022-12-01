import random,pygame, sys, time

from pygame import font
from pygame.locals import *  # puts a limited set of constants and functions into the global namespace of our script
from pygame.mixer import pause

### ====================================================================================================
# if I improve the game I should make it so that every time that I win a game it gets gradually harder.
### ====================================================================================================

pygame.mixer.pre_init(44100, 16, 2, 4090)  # sets up a mixer which is what python uses for sound
pygame.init()  # initializes pygame

FPS = 30  # frames per second, the general speed of the program
displayWidth = 640  # size of window's width in pixels
displayHeight = 480  # size of windows' height in pixels
box_reveal_spd = 8  # speed boxes' sliding reveals and covers
box_size = 40  # size of box height & width in pixels
gap = 10  # size of gap between boxes in pixels
tile_width = 4  # number of columns of icons 6
tile_height = 4  # number of rows of icons 5

# ----------------------- Make Game Screen -------------------------
gameDisplay = pygame.display.set_mode((displayWidth, displayHeight),
                                  pygame.FULLSCREEN)  # This represents the window that opens up (GUI)
clock = pygame.time.Clock()  # This is what helps us define time in the game

fullscreen = False
pause = False
pygame.display.set_caption('Memory Puzzle Game')  # Displays the name of the game (top right)

# ----------------------- Play Background Music --------------------
# this doesnt work
# pygame.mixer.music.load("Tokyo Daylight")  # add in the music file
# pygame.mixer.music.set_volume(0.15)  # min 0-1 max
# pygame.mixer.music.play(-1)  # the -1 means to loop endlessly

assert (tile_width * tile_height) % 2 == 0, 'Board needs to have an even number of boxes for pairs of matches.'
x_margin = int((displayWidth - (tile_width * (box_size + gap))) / 2)
y_margin = int((displayHeight - (tile_height * (box_size + gap))) / 2)

#         R    G    B
GRAY = (100, 100, 100)
DARKBLUE = (0, 0, 100)
WHITE = (255, 255, 255)
RED = (200, 0, 0)
GREEN = (0, 150, 0)
PINK = (255, 182, 193)
YELLOW = (255, 255, 0)
ORANGE = (255, 128, 0)
PURPLE = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
LIGHTBLUE = (60, 60, 100)
BLUEGREY = (27, 55, 82)
MUSTARDYELLOW = (206, 161, 8)
LIGHTYELLOW = (255, 215, 68)
PINKPEACH = (255, 197, 192)
LIGHTPEACH = (255, 141, 152)

# Button Color Effects
BRIGHTRED = (255, 0, 0)
BRIGHTGREEN = (0, 255, 0)
LIGHTGREY = (211, 211, 211)
HOTPINK = (255, 105, 180)

backgroud_color = BLUEGREY
lightBGcolor = GRAY
box_color = WHITE
highlight_color = PINK

donut = 'donut'
square = 'square'
diamond = 'diamond'
lines = 'lines'
oval = 'oval'

all_colors = (RED, GREEN, PINK, YELLOW, ORANGE, PURPLE, CYAN, PINK, WHITE, BLACK, BLUE)
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


def button(msg, x, y, w, h, inactiveColor, activeColor, fontSize, eventAction=None):
    mouse = pygame.mouse.get_pos()  # gets the position of the mouse
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:  # Causes Highlight of BUTTON
        #                                      X,   Y, Width, Height
        pygame.draw.rect(gameDisplay, activeColor, (x, y, w, h))
        if click[0] == 1 and eventAction != None:
            eventAction()
    else:
        pygame.draw.rect(gameDisplay, inactiveColor, (x, y, w, h))

    smallText = pygame.font.Font("freesansbold.ttf", fontSize)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ((x + (w / 2)), (y + (h / 2)))
    gameDisplay.blit(textSurf, textRect)


def blit_text(surface, text, pos, font,
              color=pygame.Color('black')):  # allows me to have multiple limes show up in my code.
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    max_width, max_height = surface.get_size()
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.


tutorial_text = "--- Game Tutorial: --- \n1. Click start to start the game (game will beign right away). " \
       "\n\n2. The tiles will appear and uncover 5 at a time. ( so make sure to pay attention to where you see matching pairs)" \
       "\n\n3. Click a tile and it will uncover its symbol, to find its pair click a different tile. (MUST MATCH)" \
       "\n\n4. If the player was successful in finding a pair, the images will stay exposed. If the player did not, the tiles will revert back to being covered." \
       "\n\n5. Once the player has successfully finished the puzzle a winning animation will play. However, shortly after the game will restart. " \
       "\n\nTO MOVE TO THE NEXT PAGE CLICK ANYWHERE ON THE SCREEN OR CLICK THE NEXT BUTTON " \
       "\n\n--- WARNING: No data will be saved! ---"

tutorial_text2 = "--- Game Tutorial (Continued) --- \nThere will be two buttons available during your game play one being \'Go Back\' and the other being \'Tutorial\'." \
        "\n\nClicking \'Go Back\' will take you back to the title page. YOUR PROGRESS WILL BE DELETED. " \
        "\n\nOn the other hand clicking on Tutorial will take you to the game\'s Tutorial and SAVE YOUR PROGRESS IN THE GAME" \
        "\n\nThe player also has the option of pressing the key \'P\' this will pause the GAME as well as the MUSIC, until you either click \'Unpause\' or \'Restart\'" \
        "\n\nThe player may also exit the game when they\'re in the paused screen" \

tutorial_text3 = "--- Settings Page: --- \n\n1. The player can customize the music of the game (ON/OFF). " \
        "\n\n2. Once you selected what you wish to set your music to you may click the \'Go Back\' button to return to the title screen. " \
        "\n\nPlease note that when you click on the \'Music On\' button the music will play again from the beginning"\
        "\n\n--- Quit Button: --- \n\n1. Once the player does not want to play anymore, the player can click the quit button and will be exited out of the game."

pause_text = "Press \'P\' to pause the game"

font = pygame.font.Font("freesansbold.ttf", 20)


def tutorial_page():
    display_instructions = True
    instruction_page = 1

    # -------- Tutorial Page Loop -----------
    while display_instructions:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                instruction_page += 1
                if instruction_page == 4:
                    display_instructions = False

        # Set the screen background
        gameDisplay.fill(GRAY)

        if instruction_page == 1:
            # Draw instructions, page 1
            button("Next Page", 450, 410, 150, 50, GREEN, BRIGHTGREEN, 20)
            blit_text(gameDisplay, tutorial_text, (20, 20), font)

        if instruction_page == 2:
            # Draw instructions, page 2
            button("Next Page", 450, 410, 150, 50, GREEN, BRIGHTGREEN, 20)
            blit_text(gameDisplay, tutorial_text2, (20, 20), font)

        if instruction_page == 3:
            # Draw instructions, page 2
            button("Done", 450, 410, 150, 50, RED, BRIGHTRED, 20)
            blit_text(gameDisplay, tutorial_text3, (20, 20), font)

        # Go ahead and update the screen with what we've drawn.
        pygame.display.update()
        # Limit to 60 frames per second
        clock.tick(60)


def unpaused():
    global pause
    pygame.mixer.music.unpause()

    pause = False


def paused():
    pygame.mixer.music.pause()

    while pause:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gameDisplay.fill(WHITE)

        largeText = pygame.font.SysFont("comicsansms", 115)
        TextSurf, TextRect = text_objects("Paused", largeText)
        TextRect.center = ((displayWidth / 2), (displayHeight / 2))
        gameDisplay.blit(TextSurf, TextRect)

        button("Unpause", 50, 340, 100, 50, GREEN, BRIGHTGREEN, 18, unpaused)

        button("Restart", 225, 325, 200, 75, PINKPEACH, LIGHTPEACH, 40, main)

        button("Exit Game", 500, 340, 100, 50, RED, BRIGHTRED, 18, quitgame)

        pygame.display.update()
        clock.tick(15)

def music_on():
    pygame.mixer.music.play()


def music_off():
    pygame.mixer.music.stop()


def settings():
    global gameDisplay
    settings_page = True

    while settings_page:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()

        gameDisplay.fill(backgroud_color)

        button("Music On", 150, 150, 150, 50, GRAY, LIGHTGREY, 20, music_on)
        button("Music Off", 350, 150, 150, 50, GRAY, LIGHTGREY, 20, music_off)
        button("Go Back", 250, 250, 150, 50, RED, BRIGHTRED, 20, game_Intro)

        pygame.display.update()
        clock.tick(60)


def quitgame():
    pygame.quit()
    quit()


def game_Intro():
    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gameDisplay.fill(backgroud_color)
        largeText = pygame.font.Font('freesansbold.ttf', 58)
        TextSurf, TextRect = text_objects("Memory Puzzle Game", largeText)
        TextRect.center = ((displayWidth / 2), (displayHeight / 2))
        gameDisplay.blit(TextSurf, TextRect)

        # PLAY BUTTON
        button("Start!", 50, 340, 100, 50, GREEN, BRIGHTGREEN, 20, main)

        # Tutorial Button
        button("Tutorial", 225, 325, 200, 75, PINKPEACH, LIGHTPEACH, 40, tutorial_page)

        # Settings Button
        button("Settings", 500, 25, 100, 75, MUSTARDYELLOW, LIGHTYELLOW, 20, settings)

        # QUIT BUTTON
        button("Quit!", 500, 340, 100, 50, RED, BRIGHTRED, 20, quitgame)

        pygame.display.update()
        clock.tick(15)


def main():
    pygame.mixer.music.unpause()

    global clock, gameDisplay, pause

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
            if event.type == pygame.KEYDOWN:  # Pauses Game
                if event.key == pygame.K_p:
                    pause = True
                    paused()

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

        button("Instructions", 500, 25, 125, 75, PINKPEACH, HOTPINK, 20, tutorial_page)
        button("Go Back", 30, 25, 100, 75, RED, BRIGHTRED, 20, game_Intro)
        blit_text(gameDisplay, pause_text, (180, 45), font)

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
            (left + half, top), (left + box_size - 1, top + half), (left + half, top + box_size - 1),
            (left, top + half)))
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
    for coverage in range(box_size, (-box_reveal_spd) - 150, -box_reveal_spd):
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
    # Randomly reveal the boxes 5 at a time.
    coveredBoxes = generateRevealedBoxesData(False)
    boxes = []
    for x in range(tile_width):
        for y in range(tile_height):
            boxes.append((x, y))
    random.shuffle(boxes)
    boxGroups = splitIntoGroupsOf(5, boxes)

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
        pygame.time.wait(150) # Causes the Winning text to blink

        largeText = pygame.font.SysFont('comicsansms', 115)
        textSurf, textRect = text_objects("Winner!!", largeText)
        textRect.center = ((displayWidth / 2), (displayHeight / 2))
        gameDisplay.blit(textSurf, textRect)

        pygame.display.update()

        color1, color2 = color2, color1  # swap colors
        gameDisplay.fill(color1)
        drawBoard(board, coveredBoxes)

        pygame.time.wait(300)
        pygame.display.update()


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
