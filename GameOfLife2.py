

# creates cell objects
class Cell:
    def __init__(self, x, y, alive, next, neighbors): # assign attributes to every cell to eliminate dictionary lookups and stuff
        self.x = x
        self.y = y
        self.state = alive
        self.next = next
        self.neighbors = neighbors # this is a set of objects (neighbor cells (walls ignored))
        
    # counts the no. of alive cells around the given cell and adds dead cells to a set so that we can loop on it later
    def countAlive(self, emptyCells = set(), aliveCount = 0):
        for cell in self.neighbors:
            if cell.state == 1: aliveCount += 1
            elif self.state == 1: emptyCells.add(cell) # only add dead cells to a set if the current cell is alive
        return aliveCount # don't have to return emptyCells as the info is stored in the objects themselves (emptyCells is just a pointer)

# generates empty board and assigns neighbors to cells in advance so we only do this once
def genBoard(cols, rows):
    board = { f'{h};{k}' : Cell(h, k, 0, 0, set()) for k in range(rows) for h in range(cols) } # create a dict so that we can find the neighbors using coords
    for cell in board.values():
        a, b = cell.x, cell.y # fetch values only once per cell and not in the loop
        for x, y in [(-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0)]: # using cached relative coords instead of the loops
            cell.neighbors.add(board.get(f'{a+x};{b+y}', None)) # returns None if cell is outside the coords ie. a wall
        cell.neighbors.discard(None) # discard doesn't raise value not present error
    return board # passing both so we can use the dict to load structures

# decides the next state of every cell
def decideState(board, emptyCells = set()):
    for cell in board.values():
        if cell.state == 1: # if cell is dead, ignore for now. we loop on en later but smartly (loop on the dead cells only if they neighbor the alive ones)
            aliveCount = cell.countAlive(emptyCells)
            if aliveCount > 3 or aliveCount < 2: cell.next = 0 # 3 conditions for the game of life (gotta play with these)
    for cell in emptyCells: # loop on dead cells
        aliveCount = cell.countAlive()
        if aliveCount == 3: cell.next = 1 # 1) if more than 3 or less than 2 alive neighbors, then cell dies, 2) if 2 or 3 neighbors, cell lives, 3) if exactly 3 neighbors, cell comes to life
    return board

# it prints board and sets the cell.state attribute to cell.next attribute's value'
def printBoard(board, cols, cellDead, cellAlive):
    newBoard = ''
    num = 0
    for cell in board.values():
        cell.state = cell.next
        num += 1
        if cell.state == 0: newBoard += cellDead
        else: newBoard += cellAlive
        if num % cols == 0: newBoard += '\n'
    print(newBoard)


# randomly assigns the state to cells (acc to rarity)
def randomiser(board, rarity):
    import random
    for cell in board.values():
       if random.randint(0, rarity) == 0: cell.state, cell.next = 1, 1
    return board

# allows you to load structures
def loadStructure(board, offX, offY, structure, rarity = 5): # structure is a list of coords 'x;y', or one of the pre-defined structure name (string)
    if structure == 'random' or structure == 0: return randomiser(board, rarity)
    with open('./structures.txt', 'r') as structures:
        import json
        if type(structure) == type('string'):
            structures = json.load(structures)
            structure = structures[structure]
        elif type(structure) == type(0): structure = list(json.load(structures).values())[structure]
    for key in structure: # set cell.state to 1 for each coord in structure
        key = key.split(';')
        key = f'{int(key[0]) + offX};{int(key[1]) + offY}' # coord offset
        cell = board[key]
        cell.state, cell.next = 1, 1
    return board



if __name__ == '__main__':
    import time
    cols, rows = 83, 77 # my screen size in chars ( 67, 64 ) (83, 77)
    cellDead = ' ' # choose how dead cells look
    cellAlive = 'x' # choose how alive cells look
    worldEnd = 200000 # loop for this many generations
    structureName = 0 # index no. or name of structure to load or 'random' index is 0      (you can find structure names and indexes in structures.txt)
    randomness = 5 # if structureName == random or 0
    offX, offY = 15, 15 # structure offset: origin topleft, (right, down) = +ve (x, y)
    tickDelay = 0. # tries about this much delay
    
    
    board = genBoard(cols, rows)
    printBoard(loadStructure(board, offX, offY, structureName, randomness), cols, cellDead, cellAlive) # ('random', rarity), 'gilder', 
    start = time.time()
    for generation in range(worldEnd+1): #for loop is faster
        tick = time.time()
        board = decideState(board)
        #print("\u001b[H\u001b[2J") # makes screen blank but doesn't clear() (its a bit too flickery)
        delay = time.time() - tick
        if tickDelay - delay > delay: time.sleep(tickDelay - delay)
        printBoard(board, cols, cellDead, cellAlive) # takes about 0.0066 sec
        print(generation, time.time()-tick)
        #print(dir()) # shows all loaded(named) objects
    print(time.time()-start)