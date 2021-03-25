
from Conway2 import *

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
    return newBoard

if __name__ == '__main__':
    
    cols, rows = 83, 79 # my screen size in chars ( 67, 64 ) (83, 79)
    cellDead = ' ' # choose how dead cells look
    cellAlive = 'x' # choose how alive cells look
    worldEnd = 200000 # loop for this many generations
    structureName = 2 # index no. or name of structure to load or 'random' index is -1     (you can find structure names and indexes in structures.txt)
    randomness = 5 # if structureName == random
    offX, offY = 15, 15 # structure offset: origin topleft, (right, down) = +ve (x, y)
    tickDelay = 0. # tries about this much delay
    
    import curses # idk why randomly chars keep apearing
    import time
    start = time.time()
    def screen(scr: 'curses._CursesWindow'):
        board = genBoard(cols, rows)
        scr.insstr(printBoard(loadStructure(board, offX, offY, structureName, randomness), cols, cellDead, cellAlive)) # ('random', rarity), 'gilder', 
        scr.refresh()
        for generation in range(worldEnd+1): #for loop is faster
            tick = time.time()
            board = decideState(board)
            #print("\u001b[H\u001b[2J") # makes screen blank but dosent clear() (its a bit too flickery)
            scr.erase()
            scr.insstr(1, 0, printBoard(board, cols, cellDead, cellAlive)) # takes about 0.0066 sec
            scr.insstr(0, 0, str(generation) + ' ' + str(time.time()-tick))
            delay = time.time() - tick
            if tickDelay - delay > delay: time.sleep(tickDelay - delay)
            scr.refresh()
    curses.wrapper(screen)
    print(time.time()-start)