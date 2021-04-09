
'''
possible optimisations:
    #  done  #    using classes to eliminate the board[key] lookup for state and alive stat and coords and using cell.alive and stuff instead
    #  not needed  #      switching between 2 dicts(global) instead of newBoard = board.copy()
    #  done   #      maybe try using list of tuples for the looking around a cell [ (1, 0), (-1, 1), ..... ]
    #  done   #        try for a way to shove dead neighbours inside cell.neighbour and loop on it in a second func inside the main (idk how to stop it from revisiting rn)
    i saw something about matrix multiplications but didnt understand it, maybe look into it later
    #  not needed  #      use cell objects as keys. cell.up as upper cell and stuff. we precalculate this (just once) to increase fetch time
        #  not needed  #      also use tuples for coords instead of '2;34' 
    
what i tried:
    switching from 1,0 to bool for cell.state - didnt notice much difference
    #  not needed  #     switching to bool in alive variable - maybe a bit speedy not sure
    
what features to add:
    . a consistant board for benchmark instead of randomised
    . more patterns in loadStructure()
    . offset for structures (so we can place them anywhere)
    . a better way to display cells:
        less flickery text solution(curses kinda works)
        a visual library solution
    . some kinda interactive play
    . ability to slow dows the tick rate (something like wait(200ms - start))
    
smol optimisations (maybe will have to try):
    . when checking dead cells,(countAlive()) do not add cells to set (optimisation) (maybe)
    . try converting board to a list(or set. its faster ig). the dictionary part of it isnt really used anywhere
    
'''

# creates cell objects
class Cell:
    def __init__(self, x, y, alive, next, neighbours): # assign attributes to every cell to eliminate dictionary lookups and stuff
        self.x = x
        self.y = y
        self.state = alive
        self.next = next
        self.neighbours = neighbours # this is a set of objects (neighbour cells (walls ignored))
        
    # counts the no. of alive cells around the given cell and adds dead cells to a set so that we can loop on it later
    def countAlive(self, emptyCells = set()):
        aliveCount = 0
        for cell in self.neighbours:
            if cell.state == 1: aliveCount += 1
            else: emptyCells.add(cell)
        return aliveCount # dont have to return emptyCells as the info is stored in the objects themselves (emptyCells is just a pointer)

# generates empty board and assigns neighbours to cells in advance so we only do this once
def genBoard(cols, rows):
    board = {}
    assign = { f'{h};{k}' : Cell(h, k, 0, 0, set()) for k in range(rows) for h in range(cols) } # create a dict so that we can find the neighbours using coords
    for cell in assign.values():
        a, b = cell.x, cell.y # fetch values only once per cell and not in the loop
        for x, y in [(-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0)]: # using cached relative coords instead of the loops
            cell.neighbours.add(assign.get(f'{a+x};{b+y}', None)) # returns None if cell is outside the coords ie. a wall
        cell.neighbours.discard(None) # discard dosent raise value not present error
        board[cell] = (a, b)
    return board, assign # passing both so we can use the dict to load structures

# decides the next state of every cell
def decideState(board, emptyCells = set()):
    for cell in board.keys():
        if cell.state == 1: # if cell is dead, ignore for now. we loop on en later but smartly (loop on the dead cells only if they neighbour the alive ones)
            aliveCount = cell.countAlive(emptyCells)
            if aliveCount > 3 or aliveCount < 2: cell.next = 0 # 3 conditions for the game of life (gotta play with these)
    for cell in emptyCells: # loop on dead cells
        aliveCount = cell.countAlive()
        if aliveCount == 3: cell.next = 1 # 1) if more than 3 or less than 2 alive neighbours, then cell dies, 2) if 2 or 3 neighbours, cell lives, 3) if exactly 3 neighbours, cell comes to life
    return board

# it prints board and sets the cell.state attribute to cell.next attribute's value'
def printBoard(board, cols):
    newBoard = ''
    num = 0
    for cell in board.keys():
        cell.state = cell.next
        num += 1
        if cell.state == 0: newBoard += ' '
        else: newBoard += 'x'
        if num % cols == 0: newBoard += '\n'
    print(newBoard)


# randomly assigns the state to cells (acc to rarity)
def randomiser(board, rarity):
    import random
    for cell in board.keys():
       if random.randint(0, rarity) == 0: cell.state, cell.next = 1, 1
    return board

# allows you to load structures
def loadStructure(board, assign, structure, rarity = 5): # structure is a list of coords 'x;y', or one of the pre-defined structure name (string)
    if type(structure) == type('string'):
        if structure == 'random': return randomiser(board, rarity)
        structures = { 'glider' : ['3;2', '4;3', '2;4', '3;4', '4;4'], }
        structure = structures[structure]
    for key in structure:
        cell = assign[key]
        cell.state, cell.next = 1, 1
    return board



if __name__ == '__main__':
    import time
    cols, rows = 83, 77 # my screen size in chars ( 67, 64 ) (83, 77)
    board, assign = genBoard(cols, rows)
    board = loadStructure(board, assign , 'random', 5) # ('random', rarity), 'gilder', 
    printBoard(board, cols)
    start = time.time()
    worldEnd = 200 # loop for this many generations
    for generation in range(worldEnd+1): #for loop is faster
        tick = time.time()
        board = decideState(board)
        #print("\u001b[H\u001b[2J") # makes screen blank but dosent clear() (its a bit too flickery)
        printBoard(board, cols)
        print(generation, time.time()-tick)
        #print(dir()) # shows all loaded(named) objects
    print(time.time()-start)