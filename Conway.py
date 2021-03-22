

def drawBoard(cols, rows):
    return { f'{h};{k}' : 0 for k in range(rows) for h in range(cols) }

def printBoard(board):
    newBoard = ''
    for key in board.keys():
        if board[key] == 0: newBoard += ' '
        else: newBoard += 'X'
        #newBoard += str(board[key])
        #newBoard = newBoard.replace('0', ' ').replace('1', 'X')
    print(newBoard)

# goes around the square and counts how many alive
def countSurr(board, key, alive, emptyCells):
    aliveCount = - board[key] # cuz we'll later add it again in loop
    keyX, keyY = key.split(';')
    keyX, keyY = int(keyX), int(keyY)
    for i in range(-1, 2):
        for j in range(-1, 2):
            key = f'{keyX + i};{keyY + j}'
            val = board.get(key, None)
            if val == 1: aliveCount += 1
            elif val == 0 and alive == 'yes': emptyCells.add(key)
    return aliveCount, emptyCells

# for every item, decide if it would be alive/dead
def decideStat(board, emptyCells = set(), alive = 'yes', boardNew = {}): # alive = 'yes' if going through alive cells, alive = 'no' if going through dead cells
    if alive == 'no': cells = emptyCells.copy()
    else: cells, boardNew = board, board.copy()
    for key in cells:
        if alive == 'no' or board[key] == 1:
            aliveCount, emptyCells = countSurr(board, key, alive, emptyCells)
            if aliveCount > 3 or aliveCount < 2: boardNew[key] = 0
            elif aliveCount == 2: pass
            elif aliveCount == 3: boardNew[key] = 1
    if alive == 'yes': boardNew = decideStat(board, emptyCells, 'no', boardNew)
    #del board, key, cells, emptyCells, aliveCount, alive, 
    return boardNew


def randomiser(board): # TEMP
    import random
    for key in board.keys():
        board[key] = random.randint(0, 2) % 2
    return board

'''
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
#board = drawBoard(cols, rows)
#glider = ['3;2', '4;3', '2;4', '3;4', '4;4'] 
#for key in glider: board[key] = 1
printBoard(board)
print('\n')
import time
while True:
    start = time.time()
    board = decideStat(board)
    #clear()
    printBoard(board)
    print(str(time.time()-start))
    #print(dir()) # shows all loaded(named) objects