
# creates cell objects
class Cell:
    def __init__(self, x, y, alive, next, neighbors, alivecount = 0): # assign attributes to every cell to eliminate dictionary lookups and stuff
        self.x = x
        self.y = y
        self.state = alive
        self.next = next
        self.neighbors = neighbors # this is a set of objects (neighbor cells)
        self.alivecount = alivecount
        
    # counts the no. of alive cells around the given cell and adds dead cells to a set so that we can loop on it later
    def cellNext(self, filled): # emptyCells is set to 0 cuz if its set to set(), then python keeps it pointing to the same set everytime. (sometimes causes problems)(not in this case tho)
        for neighbor in self.neighbors:
            if neighbor.state == 0: # is state of neighbor is dead, increment neighbor.alivecount and decide its next
                neighbor.alivecount += 1
                alivecount = neighbor.alivecount
                if alivecount == 2:
                    filled.add(neighbor)
                    neighbor.next = 1
                elif alivecount > 2:
                    filled.discard(neighbor)
                    neighbor.next = 0
        self.next = 2 # alive cells go to dying state. dying cells die, dead cells come to life if 2 live cells surround it
        filled.discard(self)

# generates empty board and assigns neighbors to cells in advance so we only do this once
def genBoard(cols, rows, torus):
    board = { f'{h};{k}' : Cell(h, k, 0, 0, set()) for k in range(1, rows+1) for h in range(1, cols+1) } # create a dict so that we can find the neighbors using coords
    for cell in board.values():
        a, b = cell.x, cell.y # fetch values only once per cell and not in the loop
        for x, y in [(-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0)]: #cell.neighbors.add(board.get(f'{a+x};{b+y}', None))
            if torus == 1:
                X, Y = x+a, y+b
                if X > cols: X = 1
                elif X == 0: X = cols # code responsible for torus behaviour
                if Y > rows: Y = 1
                elif Y == 0: Y = rows
                cell.neighbors.add(board[f'{X};{Y}'])
            else: cell.neighbors.add(board.get(f'{x+a};{y+b}', None))
        if torus != 1: cell.neighbors.discard(None) # discard doesn't raise value not present error
        cell.neighbors = list(cell.neighbors)
    return board

# decides the next state of every cell
def boardNext(filled):
    loop = filled.copy() # we only need to loop through filled ones and not the empty ones
    for cell in loop: # we add and remove stuff from filled as cells are born and others die
        cell.cellNext(filled)

# it prints board and resets some variables
def printBoard(board, cols, cellDead, cellAlive, cellSick):
    newBoard = ''
    num = 0
    for cell in board:
        cell.state = cell.next
        num += 1
        if cell.state == 0:
            cell.alivecount = 0 # only needed if cell is either dead or alive (not dying)
            newBoard += cellDead
        elif cell.state == 1:
            cell.alivecount = 0
            newBoard += cellAlive
        elif cell.state == 2:
            cell.next = 0 # kill dying cells here cuz we dont loop on them later
            newBoard += cellSick
        if num % cols == 0: newBoard += '\n'
    return newBoard

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
    with open('./structures.txt', 'r') as structures: # all structures are from GOL and not brian's brain
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
    torus = 1 # set this to 1 to loop the board like a torus
    cellDead = ' ' # choose how dead cells look
    cellAlive = 'X' # choose how alive cells look
    cellSick = 'o' # choose how dying cells look
    worldEnd = 200000 # loop for this many generations
    structureName = 0 # index no. or name of structure to load or 'random' index is 0      (you can find structure names and indexes in structures.txt)
    randomness = 70 # if structureName == random or 0
    offX, offY = 15, 15 # structure offset: origin topleft, (right, down) = +ve (x, y)
    tickDelay = 0. # tries about this much delay
    
    
    board = genBoard(cols, rows, torus)
    board, filled = loadStructure(board, offX, offY, structureName, randomness)
    print(printBoard(board, cols, cellDead, cellAlive, cellSick)) # ('random', rarity), 'gilder', 
    start = time.time()
    for generation in range(2, worldEnd+1): #for loop is faster
        tick = time.time()
        boardNext(filled)
        #print("\u001b[H\u001b[2J") # makes screen blank but doesn't clear() (its a bit too flickery)
        delay = time.time() - tick
        if tickDelay - delay > delay: time.sleep(tickDelay - delay)
        print(printBoard(board, cols, cellDead, cellAlive, cellSick)) # takes about 0.0066 sec
        print(generation, time.time()-tick)
    print(time.time()-start)