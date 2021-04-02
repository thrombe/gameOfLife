
from briansBrain import *

# it prints board and sets the cell.state attribute to cell.next attribute's value'
def printBoard2(board, cols, cellDead, cellAlive, cellSick):
    newBoard = ''
    num = 0
    for cell in board.values():
        cell.state = cell.next
        num += 1
        if cell.state == 0: newBoard += cellDead
        elif cell.state == 2: newBoard += cellSick
        elif cell.state == 1: newBoard += cellAlive
        if num % cols == 0: newBoard += '\n'
    return newBoard

if __name__ == '__main__':
    
    cols, rows = 83, 79 # my screen size in chars ( 67, 64 ) (83, 79)
    cellDead = ' ' # choose how dead cells look
    cellAlive = 'X' # choose how alive cells look
    cellSick = 'o' # choose how dying cells look
    worldEnd = 200000 # loop for this many generations
    structureName = 0 # index no. or name of structure to load or 'random' index is 0     (you can find structure names and indexes in structures.txt)
    randomness = 5 # if structureName == random or 0
    offX, offY = 15, 15 # structure offset: origin topleft, (right, down) = +ve (x, y)
    tickDelay = 0. # tries about this much delay
    
    import curses # idk why randomly chars keep appearing
    import time
    start = time.time()
    def screen(scr: 'curses._CursesWindow'):
        board = genBoard(cols, rows)
        scr.insstr(printBoard2(loadStructure(board, offX, offY, structureName, randomness), cols, cellDead, cellAlive, cellSick)) # ('random', rarity), 'gilder', 
        scr.refresh()
        for generation in range(worldEnd+1): #for loop is faster
            tick = time.time()
            board = decideState(board)
            #print("\u001b[H\u001b[2J") # makes screen blank but doesn't clear() (its a bit too flickery)
            scr.erase()
            scr.insstr(1, 0, printBoard2(board, cols, cellDead, cellAlive, cellSick)) # takes about 0.0066 sec
            scr.insstr(0, 0, str(generation) + ' ' + str(time.time()-tick))
            delay = time.time() - tick
            if tickDelay - delay > delay: time.sleep(tickDelay - delay)
            scr.refresh()
    curses.wrapper(screen)
    print(time.time()-start)