

def drawBoard(cols, rows):
    return { f'{h};{k}' : 0 for k in range(rows) for h in range(cols) }

def printBoard(board):
    newBoard = ''
    for val in board.values():
        if val == 0: newBoard += ' '
        else: newBoard += 'X'
        #newBoard += str(board[key])
        #newBoard = newBoard.replace('0', ' ').replace('1', 'X')
    print(newBoard)

# goes around the square and counts how many alive and keeps track of dead neighbours
def countSurr(board, key, alive, emptyCells):
    aliveCount = - board[key] # cuz we'll later add it again in loop
    keyX, keyY = key.split(';')
    keyX, keyY = int(keyX), int(keyY)
    for i in range(-1, 2):
        for j in range(-1, 2): # counting alive neighbours
            key = f'{keyX + i};{keyY + j}'
            val = board.get(key, None) # .get() allows to check for non-existing keys, and return None on them (essentially counting them as a hard dead cell)
            if val == 1: aliveCount += 1
            elif val == 0 and alive == 'yes': emptyCells.add(key) # add dead neighbours to a set(iff we are checking alive ones) so that we can loop on em later
    return aliveCount, emptyCells

# for every item, decide if it would be alive/dead
def decideStat(board, emptyCells = set(), alive = 'yes', boardNew = {}): # alive = 'yes' if going through alive cells, alive = 'no' if going through dead cells
    if alive == 'no': cells = emptyCells.copy() # has to be a copy cuz we gonna loop on cells later
    else: cells, boardNew = board, board.copy() # when alive == 'yes', we only check for the alive ones and if its 'no', then we check for its(dead) neighbours
    for key in cells: # cells is board when we check alive ones only, and later it is neighbours of previously alive ones
        if alive == 'no' or board[key] == 1: # loop only if checking either alive ones or their neighbours
            aliveCount, emptyCells = countSurr(board, key, alive, emptyCells)
            if aliveCount > 3 or aliveCount < 2: boardNew[key] = 0 # these 3 are the conditions for the game of life (gotta play with these)
            elif aliveCount == 2: pass
            elif aliveCount == 3: boardNew[key] = 1 # 1) if more than 3, or less than 2 alive neighbours, then cell dies, 2) if 2 or 3 neighbours, cell lives, 3) if exactly 3 neighbours, cell comes to life
    if alive == 'yes': boardNew = decideStat(board, emptyCells, 'no', boardNew) # checking for neighbours
    #del board, key, cells, emptyCells, aliveCount, alive, # not really required
    return boardNew


def randomiser(board): # TEMP # about 30 percent alive cells
    import random
    for key in board.keys():
        board[key] = random.randint(0, 2) % 2
    return board

''' # to clear screen (sloooow)
from os import system, name 
def clear(): 
    # for windows 
    if name == 'nt':  _ = system('cls') 
    # for mac and linux(here, os.name is 'posix') 
    else:  _ = system('clear') 
'''


cols = 67
rows = 64
board = randomiser(drawBoard(cols, rows))
#board = drawBoard(cols, rows) # creates a glider at about the top left of screen
#glider = ['3;2', '4;3', '2;4', '3;4', '4;4'] 
#for key in glider: board[key] = 1
import time
while True:
    start = time.time()
    #clear()
    printBoard(board)
    print(str(time.time()-start))
    board = decideStat(board)
    #print(dir()) # shows all loaded(named) objects