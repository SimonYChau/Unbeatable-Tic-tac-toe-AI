import time
import random

def makeBoard():
    return [' ' for _ in range(9)]

def printBoard(board):
    print("-------------------")
    for i in range(3):
        for row in [board[3 * i: 3 * i + 3]]:
            print('|  ' + '  |  '.join(row) + '  |')
            print("-------------------")

def insertInBoard(board, position, entry):
    board[position] = entry

def undoInsert(board, position):
    board[position] = ' '

def isBoardEmpty(board):
    for entry in board:
        if entry == ' ':
            return False
    return True

def validLocations(board):
    valid = []
    for i, entry in enumerate(board):
        if entry == ' ':
            valid.append(i)
    return valid

def hasWon(board, player):
    # horizontal
    for i in range(3):
        for row in [board[3 * i: 3 * i + 3]]:
            if all([entry == player for entry in row]):
                return True
    # vertical
    for i in range(3):
        col = [board[i], board[i + 3], board[i + 6]]
        if all([entry == player for entry in col]):
            return True
    # positive sloping diagonal
    diagonalPos = [board[0], board[4], board[8]]
    if all([entry == player for entry in diagonalPos]):
        return True
    # negatively sloping diagonal
    diagonalNeg = [board[2], board[4], board[6]]
    if all([entry == player for entry in diagonalNeg]):
        return True
    return False

def getPlayerMove(board, player):
    playerMove = -1
    while playerMove - 1 not in validLocations(board):
        playerMove = int(input('Select your move [1 - 9]: '))
        if playerMove - 1 in validLocations(board):
            insertInBoard(board, playerMove - 1, player)
            printBoard(board)
            if hasWon(board, player):
                print(player, " has won!")
                exit() 
            return
        else:
            print('Invalid choice\n')

def getComputerMove(board, computer, computerAI):
    print('Computer has played . . . ')
    time.sleep(0.5)
    computerMove = bestMove(board, computer) if computerAI else random.choice(validLocations(board))
    insertInBoard(board, computerMove, computer)
    printBoard(board)
    if hasWon(board, computer):
        print(computer, " has won!")
        exit()

def bestMove(board, entry):
    bestScore = float('-inf')
    for move in validLocations(board):
        insertInBoard(board, move, entry)
        score = minimax(board, entry, float('-inf'), float('inf'), False)
        undoInsert(board, move)
        if score > bestScore:
            bestScore = score
            bestMove = move
    return bestMove

def minimax(board, maximizingPlayer, alpha, beta, maximizing):
    minimizingPlayer = 'O' if maximizingPlayer == 'X' else 'X'

    # check if we have a win or draw
    if hasWon(board, maximizingPlayer):
        return +1 * (len(validLocations(board)) + 1)
    elif hasWon(board, minimizingPlayer):
        return -1 * (len(validLocations(board)) + 1)
    elif len(validLocations(board)) == 0:
        return 0
    
    if maximizing:
        value = float('-inf')
        for move in validLocations(board):
            insertInBoard(board, move, maximizingPlayer)
            value = max(value, minimax(board, maximizingPlayer, alpha, beta, False))
            undoInsert(board, move)
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return value
    else:
        value = float('inf')
        for move in validLocations(board):
            insertInBoard(board, move, minimizingPlayer)
            value = min(value, minimax(board, maximizingPlayer, alpha, beta, True))
            undoInsert(board, move)
            beta = min(beta, value)
            if beta <= alpha:
                break
        return value

def main():
    board = makeBoard()
    printBoard(board)

    player = ''
    while player != 'O' and player != 'X':
        player = input('Select X or O: ').upper()
        if player != 'O' and player != 'X':
            print('Invalid choice\n')

    computer = 'X' if player == 'O' else 'O'

    computerAI = ''
    while computerAI != 'y' and computerAI != 'n':
        computerAI = input('Do you want to play the AI? [ y / n ]: ').lower()
        if computerAI != 'y' and computerAI != 'n':
            print('Invalid choice\n')
    computerAI = True if computerAI == 'y' else False

    firstMove = ''
    while firstMove != 'y' and firstMove != 'n':
        firstMove = input('Do you want to start first? [ y / n ]: ').lower()
        if firstMove != 'y' and firstMove != 'n':
            print('Invalid choice\n')

    while not isBoardEmpty(board):
        if firstMove == 'y':
            printBoard(board)
            getPlayerMove(board, player)
            firstMove = ''
        getComputerMove(board, computer, computerAI)
        if isBoardEmpty(board):
            break
        getPlayerMove(board, player)
    print("Game has ended in a draw")

if __name__ == '__main__':
    main()
