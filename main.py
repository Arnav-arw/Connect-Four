import numpy as np

def createBoard():
    return np.zeros((6,7))

def dropPiece(board, row, col, peice):
    board[row][col] = peice

def isValidMove(board, col):
    return board[5][col] == 0

def nextOpenRow(board, col):
    for i in range(6):
        if board[i][col] == 0:
            return i

def printBoard(board):
    print(np.flip(board, 0))

game = False
# Create a board
board = createBoard()
turn = 0

while not game:
    # Player 1 turn
    if turn == 0:
        col = int(input("Player 1, choose a column: "))
        col-=1
        if col >= 0 and col <= 6:
            if isValidMove(board, col):
                row = nextOpenRow(board, col)
                dropPiece(board, row, col, 1)
                turn = 1
        else:
            print("Enter valid command!")

    else:
        col = int(input("Player 2, choose a column: "))
        col-=1
        if col >= 0 and col <= 6:
            if isValidMove(board, col):
                row = nextOpenRow(board, col)
                dropPiece(board, row, col, 2)
                turn = 1
        else:
            print("Enter valid command!")

    printBoard(board)
