

def drawBoard(cols, rows):
    return { f'{h};{k}' : 0 for k in range(rows) for h in range(cols) }

def printBoard(board):
    newBoard = ''
    for key in board.keys():
        newBoard += str(board[key])
        newBoard = newBoard.replace('0', ' ').replace('1', 'X')
    print(newBoard)

# goes around the square and counts how many alive
def countSurr(board, key, alive):
    aliveCount = - board[key] # cuz we'll later add it again in loop
    keyX, keyY = key.split(';')
    keyX, keyY = int(keyX), int(keyY)
    cells = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            key = f'{keyX + i};{keyY + j}'
            if board.get(key, None) == 1:
                aliveCount += 1
            elif board.get(key, 'bank') == 0: cells.append(key)
    return aliveCount, cells

# for every item, decide if it would be alive/dead
def decideStat(board, emptyCells = [], alive = 'yes', boardNew = {}): # alive = 'yes' if going through alive cells, alive = 'no' if going through dead cells
    if alive == 'no': cells = emptyCells
    else: cells, boardNew = board, board.copy()
    for key in cells:
        if board[key] == 1 or alive == 'no':
            aliveCount, cell = countSurr(board, key, alive)
            if alive == 'yes': emptyCells.extend(cell)
            if aliveCount > 3 or aliveCount < 2: boardNew[key] = 0
            elif aliveCount == 2: pass
            elif aliveCount == 3: boardNew[key] = 1
    emptyCells = set(emptyCells)
    if alive == 'yes': boardNew = decideStat(board, emptyCells, 'no', boardNew)
    return boardNew


def randomiser(board): # TEMP
    import random
    for key in board.keys():
        board[key] = random.randint(0, 2) % 2
    return board

cols = 67
rows = 65
board = randomiser(drawBoard(cols, rows))
#board = drawBoard(cols, rows)
#glider = ['3;2', '4;3', '2;4', '3;4', '4;4'] 
#for key in glider: board[key] = 1
printBoard(board)
print('\n')
while True:
    board = decideStat(board)
    printBoard(board)
    print('\n', '-'*50, '\n')
    if all( val == 0 for val in board.values()): break
    #break

