
from briansBrain3 import genBoard, loadStructure, boardNext, printBoard


if __name__ == '__main__':
    
    cols, rows = 151, 160 # my screen size in chars ( 67, 64 ) (83, 79)(151, 165)
    torus = 1 # set this to 1 to loop the board like a torus
    cellDead = ' ' # choose how dead cells look
    cellAlive = 'X' # choose how alive cells look
    cellSick = 'o' # choose how dying cells look
    worldEnd = 200000 # loop for this many generations
    structureName = 0 # index no. or name of structure to load or 'random' index is 0     (you can find structure names and indexes in structures.txt)
    randomness = 70 # if structureName == random or 0
    offX, offY = 15, 15 # structure offset: origin topleft, (right, down) = +ve (x, y)
    tickDelay = 0. # tries about this much delay
    
    import curses # idk why randomly chars keep appearing
    import time
    start = time.time()
    def screen(scr: 'curses._CursesWindow'):
        board = genBoard(cols, rows, torus)
        board, filled = loadStructure(board, offX, offY, structureName, randomness)
        scr.insstr(printBoard(board, cols, cellDead, cellAlive, cellSick)) # ('random', rarity), 'gilder', 
        scr.refresh()
        for generation in range(1, worldEnd): #for loop is faster
            tick = time.time()
            boardNext(filled)
            scr.erase()
            scr.insstr(1, 0, printBoard(board, cols, cellDead, cellAlive, cellSick)) # takes about 0.0066 sec
            scr.insstr(0, 0, str(generation) + ' ' + str(time.time()-tick))
            delay = time.time() - tick
            if tickDelay - delay > delay: time.sleep(tickDelay - delay)
            scr.refresh()
    curses.wrapper(screen)
    print(time.time()-start)