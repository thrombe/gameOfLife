
# creates cell objects
class Cell:
    def __init__(self, x, y, alive, next, neighbors, alivecount = 0): # assign attributes to every cell to eliminate dictionary lookups and stuff
        self.x = x
        self.y = y
        self.state = alive
        self.next = next
        self.neighbors = neighbors # this is a set of objects (neighbor cells (walls ignored))
        self.alivecount = alivecount
        
    # counts the no. of alive cells around the given cell and adds dead cells to a set so that we can loop on it later
    def countAlive(self, filled, aliveCount = 0): # emptyCells is set to 0 cuz if its set to set(), then python keeps it pointing to the same set everytime. (sometimes causes problems)(not in this case tho)
        for neighbor in self.neighbors:
            if neighbor.state == 1: aliveCount += 1
            else: # is state of neighbor is dead, increment neighbor.alivecount and decide its next
                neighbor.alivecount += 1
                alivecount = neighbor.alivecount
                if alivecount == 3:
                    filled.add(neighbor)
                    neighbor.next = 1
                elif alivecount > 3:
                    filled.discard(neighbor)
                    neighbor.next = 0
        return aliveCount # don't have to return emptyCells as the info is stored in the objects themselves (emptyCells is just a pointer)

# generates empty board and assigns neighbors to cells in advance so we only do this once
def genBoard(cols, rows):
    board = { f'{h};{k}' : Cell(h, k, 0, 0, set()) for k in range(rows) for h in range(cols) } # create a dict so that we can find the neighbors using coords
    for cell in board.values():
        a, b = cell.x, cell.y # fetch values only once per cell and not in the loop
        for x, y in [(-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0)]: # using cached relative coords instead of the loops
            cell.neighbors.add(board.get(f'{a+x};{b+y}', None)) # returns None if cell is outside the coords ie. a wall
        cell.neighbors.discard(None) # discard doesn't raise value not present error
        cell.neighbors = list(cell.neighbors)
    return board # passing both so we can use the dict to load structures

# decides the next state of every cell
def decideState(filled):
    loop = filled.copy() # we only need to loop through filled ones and not the empty ones
    for cell in loop: # we add and remove stuff from filled as cells are born and others die
        aliveCount = cell.countAlive(filled)
        if aliveCount > 3 or aliveCount < 2:
            filled.discard(cell)
            cell.next = 0 # 3 conditions for the game of life (gotta play with these)
    return filled

# it prints board and sets the cell.state attribute to cell.next attribute's value'
def printBoard(board, cols, cellDead, cellAlive):
    newBoard = ''
    num = 0
    for cell in board:
        cell.state = cell.next
        num += 1
        if cell.state == 0:
            cell.alivecount = 0
            newBoard += cellDead
        else: newBoard += cellAlive
        if num % cols == 0: newBoard += '\n'
    print(newBoard)

# randomly assigns the state to cells (acc to rarity)
def randomiser(board, rarity):
    import random
    newBoard = []
    filled = set()
    for cell in board.values():
        if random.randint(0, rarity) == 0:
            cell.state, cell.next = 1, 1
            filled.add(cell)
        newBoard.append(cell)
    return newBoard, filled

# allows you to load structures
def loadStructure(board, offX, offY, structure, rarity): # structure is a list of coords 'x;y', or one of the pre-defined structure name (string)
    if structure == 'random' or structure == 0: return randomiser(board, rarity)
    with open('./structures.txt', 'r') as structures:
        import json
        if type(structure) == type('string'):
            structures = json.load(structures)
            structure = structures[structure]
        elif type(structure) == type(0): structure = list(json.load(structures).values())[structure]
    filled = set()
    for key in structure: # set cell.state to 1 for each coord in structure
        key = key.split(';')
        key = f'{int(key[0]) + offX};{int(key[1]) + offY}' # coord offset
        cell = board[key]
        cell.state, cell.next = 1, 1
        filled.add(cell)
    return [cell for cell in board.values()], filled



if __name__ == '__main__':
    import time
    cols, rows = 151, 160 # my screen size in chars ( 67, 64 ) (83, 77)
    cellDead = ' ' # choose how dead cells look
    cellAlive = 'x' # choose how alive cells look
    worldEnd = 200 # loop for this many generations
    structureName = 0 # index no. or name of structure to load or 'random' index is 0      (you can find structure names and indexes in structures.txt)
    randomness = 5 # if structureName == random or 0
    offX, offY = 15, 15 # structure offset: origin topleft, (right, down) = +ve (x, y)
    tickDelay = 0. # tries about this much delay
    
    
    board = genBoard(cols, rows)
    board, filled = loadStructure(board, offX, offY, structureName, randomness)
    printBoard(board, cols, cellDead, cellAlive) # ('random', rarity), 'gilder', 
    start = time.time()
    for generation in range(2, worldEnd+1): #for loop is faster
        tick = time.time()
        filled = decideState(filled)
        #print("\u001b[H\u001b[2J") # makes screen blank but doesn't clear() (its a bit too flickery)
        delay = time.time() - tick
        if tickDelay - delay > delay: time.sleep(tickDelay - delay)
        printBoard(board, cols, cellDead, cellAlive) # takes about 0.0066 sec
        print(generation, time.time()-tick)
        #print(dir()) # shows all loaded(named) objects
    print(time.time()-start)