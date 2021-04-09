
# generates empty board
def genBoard(cols, rows):
    board = {}
    for k in range(rows):
        for h in range(cols):
            cell = Cell(h, k)
            board[f'{h};{k}'] = cell
    return board

class Cell:
    def __init__(self, x, y, alive = False):
        self.x = x
        self.y = y
        self.alive = alive
        self.next = False
        self.neighbours = None

# goes around the square and counts how many alive and keeps track of dead neighbours
def countSurr(board, cell, alive, emptyCells):
    if cell.alive == True: aliveCount = -1
    else: aliveCount = 0 # cuz we'll later add it again in loop
    x, y = cell.x, cell.y
    for i in range(-1, 2):
        for j in range(-1, 2): # counting alive neighbours
            key = f'{x + i};{y + j}'
            cell = board.get(key, Cell(None, None, None)) # .get() allows to check for non-existing keys, and return None on them (essentially counting them as a hard dead cell)
            if cell.alive == True: aliveCount += 1
            elif cell.alive == False and alive == True: emptyCells.add(cell) # add dead neighbours to a set(iff we are checking alive ones) so that we can loop on em later
    return aliveCount, emptyCells

# for every item, decide if it would be alive/dead
def decideStat(board, emptyCells = set(), alive = True, boardNew = {}): # alive = 'yes' if going through alive cells, alive = 'no' if going through dead cells
    if alive == False:
        cells = emptyCells.copy() # has to be a copy cuz we gonna loop on cells later
        for cell in cells: # cells is board when we check alive ones only, and later it is neighbours of previously alive ones
            aliveCount, emptyCells = countSurr(board, cell, alive, emptyCells)
            if aliveCount == 3: cell.next = True # 1) if more than 3, or less than 2 alive neighbours, then cell dies, 2) if 2 or 3 neighbours, cell lives, 3) if exactly 3 neighbours, cell comes to life
    else:
        #cells, boardNew = board, board.copy() # when alive == 'yes', we only check for the alive ones and if its 'no', then we check for its(dead) neighbours
        for cell in board.values(): # cells is board when we check alive ones only, and later it is neighbours of previously alive ones
            cell.alive = cell.next
            if cell.alive == True: # loop only if checking either alive ones or their neighbours
                aliveCount, emptyCells = countSurr(board, cell, alive, emptyCells)
                if aliveCount > 3 or aliveCount < 2: cell.next = False # these 3 are the conditions for the game of life (gotta play with these)
                decideStat(board, emptyCells, False, boardNew) # checking for neighbours
    #for cell in board.values():
        #if cell.next != None: cell.alive = cell.next
    return board


def randomiser(board, rarity): # about 30 percent alive cells
    import random
    for key, cell in board.items():
       if random.randint(0, rarity) == 0: cell.alive = True
    return board

def loadStructure(board, structure, rarity = 5): # structure is a list of coords 'x;y', or one of the pre-defined structure name (string)
    if type(structure) == type('string'):
        if structure == 'random': return randomiser(board, rarity)
        structures = { 'glider' : ['3;2', '4;3', '2;4', '3;4', '4;4'], }
        structure = structures[structure]
    for key in structure:
        board[key].next = True
        board[key].alive = True
    return board

def printBoard(board):
    newBoard = ''
    for cell in board.values():
        if cell.next == False: newBoard += ' '
        elif cell.next == True: newBoard += 'x'
    print(newBoard)

def printBoard2(board, cols):
    newBoard = ''
    num = 0
    for cell in board.values():
        num += 1
        if cell.next == False: newBoard += ' '
        elif cell.next == True: newBoard += 'x'
        if num % cols == 0: newBoard += '\n'
    print(newBoard)

''' # to clear screen (sloooow)
from os import system, name 
def clear(): 
    # for windows 
    if name == 'nt':  _ = system('cls') 
    # for mac and linux(here, os.name is 'posix') 
    else:  _ = system('clear') 
'''

if __name__ == '__main__': # ADJUST SIZE OF cols OR UNCOMMENT PRINTBOARD2 AND COMMENT PRINTBOARD
    cols = 20 # my screen width in chars ( 67, 64 )
    rows = 20
    board = loadStructure(genBoard(cols, rows), 'glider', 5) # ('random', rarity), 'gilder', 
    import time
    num = 0
    strat = time.time()
    printBoard2(board, cols)
    while True:
        num += 1
        start = time.time()
        #clear()
        board = decideStat(board)
        #print("\u001b[H\u001b[2J")
        #printBoard(board) #must use fixed column size (tiny bit faster)
        printBoard2(board, cols) # can use custom sizes
        print(time.time()-start)
        print(num)
        if num == 200:
            print(time.time()-strat)
            exit()
        #print(dir()) # shows all loaded(named) objects
        exit()