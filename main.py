import numpy as np

# Variable 
TnoColumns = 7
TnoRows = 6

# Extra
COLUMN_COUNT = TnoColumns - 1
ROW_COUNT = TnoRows
game = True

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

def winningMove(board, piece):
    # For horizontal wins
    for i in range(COLUMN_COUNT-3):
        for j in range(ROW_COUNT):  
            if board[i][j] == piece and board[i][j+1] == piece and board[i][j+2] == piece and board[i][j+3] == piece:
                return True
    
    # For vertical wins
    for i in range(COLUMN_COUNT):
        for j in range(ROW_COUNT-3):
            if board[i][j] == piece and board[i+1][j] == piece and board[i+2][j] == piece and board[i+3][j] == piece:
                return True
    
    # For this / diaganol  wins
    for i in range(COLUMN_COUNT-3):
        for j in range(ROW_COUNT-3):
            if board[i][j] == piece and board[i+1][j+1] == piece and board[i+2][j+2] == piece and board[i+3][j+3] == piece:
                return True
    
    # For this \ diaganol wins
    for i in range(COLUMN_COUNT-3):
        for j in range(3, ROW_COUNT):
            if board[i][j] == piece and board[i-1][j+1] == piece and board[i-2][j+2] == piece and board[i-3][j+3] == piece:
                return True

def printBoard(board):
    print(np.flip(board, 0))

printBoardVar = True

# Create a board
board = createBoard()
turn = 0

while game:
    # Player 1 turn
    if turn == 0:
        col = int(input("Player 1, choose a column: "))
        col-=1
        if col >= 0 and col <= 6:
            if isValidMove(board, col):
                row = nextOpenRow(board, col)
                dropPiece(board, row, col, 1)
                turn = 1
                printBoardVar = True

                if winningMove(board, 1):
                    print("Player 1 wins!")
                    game = False
                    printBoardVar = False
        else:
            print("Enter valid command!")

    else:
        col = int(input("Player 2, choose a column: "))
        col-=1
        if col >= 0 and col <= 6:
            if isValidMove(board, col):
                row = nextOpenRow(board, col)
                dropPiece(board, row, col, 2)
                turn = 0
        else:
            print("Enter valid command!")

    if printBoardVar:
        printBoard(board)
