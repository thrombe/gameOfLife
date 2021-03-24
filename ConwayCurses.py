
from Conway import *

def printBoard2(board, cols):
    newBoard = ''
    num = 0
    for val in board.values():
        num += 1
        if val == 0: newBoard += ' '
        else: newBoard += 'x'
        if num % cols == 0: newBoard += '\n'
    return newBoard


import curses # idk why randomly chars keep apearing
import time
start = time.time()
def curse(scr: 'curses._CursesWindow'):
    cols, rows = 83, 77 # my screen width in chars ( 67, 64 ) (83, 77)
    board = loadStructure(genBoard(cols, rows), 'random', 5) # ('random', rarity), 'gilder', 
    scr.insstr(printBoard2(board, cols))
    scr.refresh()
    worldEnd = 200 # loop for this many generations
    for generation in range(worldEnd+1): #for loop is faster
        tick = time.time()
        board = decideStat(board)
        #scr.insstr(printBoard(board)) #must use fixed column size (tiny bit faster)
        #scr.clear()
        #scr.insstr(' '*1000)
        scr.erase()
        scr.insstr(1, 0, printBoard2(board, cols)) # can use custom sizes
        scr.insstr(0, 0, str(generation) + ' ' + str(time.time()-tick))
        scr.refresh()

curses.wrapper(curse)
print(str(time.time()-start))