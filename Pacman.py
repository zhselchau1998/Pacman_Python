from random import randint
from KeyListener import KeyListener
from GUI import GUI
from time import sleep

#CONSTANTS
BOARD_WIDTH = 20
BOARD_HEIGHT = 20
INITIAL_LENGTH = 3
UP = 3
DOWN = 1
LEFT = 2
RIGHT = 0
EMPTY = 0
PLAYER = 1
GHOST = 5 
PINKY = 5
ROCKY = 6
POGO = 7
RINGO = 8
POWERUP = 4
POWERUPTIME = 20
CHERRY = 3
WALL = 2
INITIAL_GHOST = (10,10)
MAPS = ["Map1.txt", "Map2.txt"]

#VARIABLES
board = [[] for i in range(0,BOARD_WIDTH)]    # A list of lists, BOARD_WIDTH
snacks = [[] for i in range(0,BOARD_WIDTH)]   # A list of 1s and 0s representing what tiles pacman has visited
powerUps = []   # A list of duples representing the coords of powerups
ghosts = [(0,0) for i in range(0,4)]  # A list of duples representing the coords of ghosts

def initPacman(map):

    for row in board: row.clear()
    for snack in snacks: snack.clear()
    powerUps.clear()
    ghosts.clear()
    for i in range(0,4): ghosts.append((0,0))

    for i in range(len(ghosts)):
        ghosts[i]=INITIAL_GHOST
    
    pacman = (10,12)
    score = 0
    
    with open(map, "r") as map:
        mapText = map.readlines()
        if len(mapText) != BOARD_HEIGHT:
            return False
        for i in range(BOARD_HEIGHT):
            for value in mapText[i].strip().split(","):
                board[i].append(int(value))
    
    for x, row in enumerate(board):
        for y, value in enumerate(row):
            if value == 0: snacks[x].append(1)
            else: snacks[x].append(0)
            if value == 4: powerUps.append((x,y))
    
    board[pacman[0]][pacman[1]] = PLAYER
    for i,ghost in enumerate(ghosts):
        board[ghost[0]][ghost[1]] = GHOST + i

    return (pacman[0], pacman[1]), score

def generateApple():
    appleX = randint(0,BOARD_WIDTH-1)
    appleY = randint(0,BOARD_HEIGHT-1)
    while board[appleX][appleY] != 0:
        appleX = randint(0,BOARD_WIDTH-1)
        appleY = randint(0,BOARD_HEIGHT-1)
    board[appleX][appleY] = CHERRY
    return (appleX, appleY)
    
def gameOverCheck(pacman, snackCount, powerUpCount):
    if powerUpCount != 0: return snackCount == 0
    return pacman in ghosts or snackCount == 0

def removeSnack(pacman, snackCount, score):
    if snacks[pacman[0]][pacman[1]] == 1:
        snackCount -= 1
        snacks[pacman[0]][pacman[1]] = 0
        score += 5
    
    return snackCount, score

def moveEntity(direction, pos, TYPE):
    board[pos[0]][pos[1]] = EMPTY
    newEntity = (pos[0],pos[1])

    if direction == UP and board[pos[0]][roundPosition(pos[1] + 1)] != WALL: 
        newEntity = (pos[0], roundPosition(pos[1] + 1))
    if direction == DOWN and board[pos[0]][roundPosition(pos[1] - 1)] != WALL:
        newEntity = (pos[0], roundPosition(pos[1] - 1))
    if direction == LEFT and board[roundPosition(pos[0] - 1)][pos[1]] != WALL:
        newEntity = (roundPosition(pos[0] - 1), pos[1])
    if direction == RIGHT and board[roundPosition(pos[0] + 1)][pos[1]] != WALL:
        newEntity = (roundPosition(pos[0] + 1), pos[1])

    board[newEntity[0]][newEntity[1]] = TYPE
    
    return newEntity, pos[0] != newEntity[0] or pos[1] != newEntity[1]

def roundPosition(position):
    while position >= BOARD_HEIGHT:
        position -= BOARD_HEIGHT
    while position < 0:
        position += BOARD_HEIGHT
    return position

def setDirection(key, dir, pos):
    if key == 'w':
        return DOWN
    if key == 's':
        return UP
    if key == 'a':
        return LEFT
    if key == 'd':
        return RIGHT
    return dir

def distanceFunction(currentPos, targetPos):
    return abs(currentPos[0] - targetPos[0]) + abs(currentPos[1] - targetPos[1])

def depthFirstSearch(currentPos, targetPos, depth=0, maxDepth=5, path=[]):
    if currentPos == targetPos: return UP, 0
    if board[currentPos[0]][currentPos[1]] == WALL: return UP, BOARD_HEIGHT + BOARD_WIDTH
    if currentPos in path: return DOWN, BOARD_HEIGHT + BOARD_WIDTH
    if maxDepth == depth: return UP, distanceFunction(currentPos, targetPos)

    path.append(currentPos)
    directions = [RIGHT, DOWN, LEFT, UP]

    tmp, directions[RIGHT] = depthFirstSearch((roundPosition(currentPos[0]+1), currentPos[1]), targetPos, depth=depth+1, path=path)
    tmp, directions[LEFT] = depthFirstSearch((roundPosition(currentPos[0]-1), currentPos[1]), targetPos, depth=depth+1, path=path)
    tmp, directions[UP] = depthFirstSearch((currentPos[0], roundPosition(currentPos[1]+1)), targetPos, depth=depth+1, path=path)
    tmp, directions[DOWN] = depthFirstSearch((currentPos[0], roundPosition(currentPos[1])-1), targetPos, depth=depth+1, path=path)

    bestDir = UP
    minValue = BOARD_HEIGHT + BOARD_WIDTH + 1

    for dir, val in enumerate(directions):
        if minValue > val:
            bestDir = dir
            minValue = val
    
    return bestDir, minValue

def eatGhostCheck(pacman, ghost, isEating, score):
    if pacman == ghost and isEating: return INITIAL_GHOST, score+200
    return ghost, score

def ghostDir(ghost, position, pacman, powerUpCount):
    if powerUpCount != 0:
        return randint(0,4)
    if ghost == PINKY:
        options = []
        if board[roundPosition(position[0]+1)][position[1]] != WALL: options.append(RIGHT)
        if board[roundPosition(position[0]-1)][position[1]] != WALL: options.append(LEFT)
        if board[position[0]][roundPosition(position[1]+1)] != WALL: options.append(UP)
        if board[position[0]][roundPosition(position[1]-1)] != WALL: options.append(DOWN)
        return options[randint(0,len(options)-1)]
    if ghost == ROCKY:
        options = []
        if pacman[0] > position[0]: options.append(RIGHT)
        if pacman[0] < position[0]: options.append(LEFT)
        if pacman[1] > position[1]: options.append(UP)
        if pacman[1] < position[1]: options.append(DOWN)
        if len(options) == 0: return 0
        return options[randint(0,len(options)-1)]
    if ghost == POGO:
        options = []
        if pacman[0] > position[0] and board[roundPosition(position[0]+1)][position[1]] != WALL: options.append(RIGHT)
        if pacman[0] < position[0] and board[roundPosition(position[0]-1)][position[1]] != WALL: options.append(LEFT)
        if pacman[1] > position[1] and board[position[0]][roundPosition(position[1]+1)] != WALL: options.append(UP)
        if pacman[1] < position[1] and board[position[0]][roundPosition(position[1]-1)] != WALL: options.append(DOWN)
        if len(options) == 0: return 0
        return options[randint(0,len(options)-1)]
    if ghost == RINGO:
        direction, distance = depthFirstSearch(position, pacman, path = [])
        return direction
    return randint(0,4)

def printBoard():
    print("\n\n\n")
    for column in board:
        line = ""
        for cell in column:
            if cell == EMPTY:
                line+='. '
            if cell == WALL:
                line+='# '
            if cell == PLAYER:
                line+='@ '
            if cell == CHERRY:
                line+='O '
            if cell >= GHOST:
                line+='W '
        print(line)

def gameLoop(player, gui, score):
    direction = [DOWN,UP,UP,UP,UP]  # player, pinky, rocky, pogo, ringo
    keyListener = KeyListener()
    inGame = True
    apple = generateApple()
    snackCount = 0
    moved = [True, False, False, False, False]  #player, pinky, rocky, pogo, ringo
    beatLevel = False
    pacman = (player[0], player[1])
    powerUpCount = 0
    for row in snacks: snackCount += sum(row)

    while inGame:
        key = keyListener.nextKey()
        direction[0] = setDirection(key, direction[0], pacman)

        pacman, moved[0] = moveEntity(direction[0], pacman, PLAYER)
        snackCount, score = removeSnack(pacman, snackCount, score)
        if powerUpCount > 0: 
            powerUpCount -= 1
        if pacman in powerUps:
            powerUps.remove(pacman)
            powerUpCount += POWERUPTIME

        for i, ghost in enumerate(ghosts):
            ghost, score = eatGhostCheck(pacman, ghost, powerUpCount > 0, score)
            direction[i+1] = ghostDir(i+GHOST, ghost, pacman, powerUpCount)
            ghosts[i],moved[i+1] = moveEntity(direction[i+1], ghost, GHOST+i)
        
        
        inGame = not gameOverCheck(pacman, snackCount, powerUpCount)
        if snackCount == 0:
            beatLevel = True
        
        # Apple Check
        if pacman[0] == apple[0] and pacman[1] == apple[1]:
            apple = generateApple()
            score += 100
        if board[apple[0]][apple[1]] == EMPTY:
            apple = generateApple()
        
        for i in range(5):
            gui.update(board,snacks, powerUps, direction,i, moved, ghosts, pacman, powerUpCount, score)
            sleep(0.05)
    
    return beatLevel, score
        
        

def runPacman():
    # Initialization
    gui = GUI()
    gui.titlePage()
    sleep(3)
    for level,map in enumerate(MAPS):
        gui.levelPage(level+1)
        pacman, score = initPacman(map)
        sleep(5)
        # Starting Game
        won, score = gameLoop(pacman, gui, score)
        if not won: break
    if won: print(f"YOU WON! Your Score: {score}")
    else: print(f"YOU LOST... Your Score: {score}")

if __name__ == "__main__":
    runPacman()