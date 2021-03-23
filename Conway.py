
'''
possible optimisations:
    using classes to eliminate the board[key] lookup for state and alive stat and coords and using cell.alive and stuff instead
    switching between 2 dicts(global) instead of newBoard = board.copy()
    maybe try using list of tuples for the looking around a cell [ (1, 0), (-1, 1), ..... ]
    try for a way to shove dead neighbours inside cell.neighbour and loop on it in a second func inside the main (idk how to stop it from revisiting rn)
    i saw something about matrix multiplications but didnt understand it, maybe look into it later
    
what i tried:
    switching from 1,0 to bool for cell.alive - didnt notice much difference
    switching to bool in alive variable - maybe a bit speedy not sure
    
what features to add:
    a consistant board for benchmark instead of randomised
    more patterns in loadStructure()
    a better way to display cells:
        less flickery text solution
        a visual library solution
    

'''

# generates empty board
def genBoard(cols, rows):
    return { f'{h};{k}' : 0 for k in range(rows) for h in range(cols) }

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
            elif aliveCount == 3: boardNew[key] = 1 # 1) if more than 3, or less than 2 alive neighbours, then cell dies, 2) if 2 or 3 neighbours, cell lives, 3) if exactly 3 neighbours, cell comes to life
    if alive == 'yes': boardNew = decideStat(board, emptyCells, 'no', boardNew) # checking for neighbours
    #del board, key, cells, emptyCells, aliveCount, alive, # not really required
    return boardNew


def randomiser(board, rarity): # about 30 percent alive cells
    import random
    for key in board.keys():
       if random.randint(0, rarity) == 0: board[key] = 1
    return board

def loadStructure(board, structure, rarity = 5): # structure is a list of coords 'x;y', or one of the pre-defined structure name (string)
    if type(structure) == type('string'):
        if structure == 'random': return randomiser(board, rarity)
        structures = { 'glider' : ['3;2', '4;3', '2;4', '3;4', '4;4'], }
        structure = structures[structure]
    for key in structure: board[key] = 1
    return board

def printBoard(board):
    newBoard = ''
    for val in board.values():
        if val == 0: newBoard += ' '
        else: newBoard += 'x'
    print(newBoard)

def printBoard2(board, cols):
    newBoard = ''
    num = 0
    for val in board.values():
        num += 1
        if val == 0: newBoard += ' '
        else: newBoard += 'x'
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

if __name__ == '__main__': # ADJUST SIZE OF cols OR UNCOMMENT PRINTBOARD2 AND COMMENT PRINTBOARD FOR CUSTOM BOARD SIZE
    import time
    cols, rows = 67, 64 # my screen width in chars ( 67, 64 )
    board = loadStructure(genBoard(cols, rows), 'random', 5) # ('random', rarity), 'gilder', 
    printBoard(board)
    start = time.time()
    worldEnd = 200 # loop for this many generations
    for generation in range(worldEnd+1): #for loop is faster
        tick = time.time()
        #clear()
        board = decideStat(board)
        #print("\u001b[H\u001b[2J") # makes screen blank but dosent clear() (its a bit too flickery)
        #printBoard(board) #must use fixed column size (tiny bit faster)
        printBoard2(board, cols) # can use custom sizes
        print(generation, time.time()-tick)
        #print(dir()) # shows all loaded(named) objects
    print(time.time()-start)