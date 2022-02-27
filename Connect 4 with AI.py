import numpy as np
import pygame
import sys
import math
import random

# Colours codes
BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

# Variables
ROW_COUNT = 6
COLUMN_COUNT = 7

PLAYER = 0
AI = 1

PLAYER_PIECE = 1
AI_PIECE = 2

def createBoard():
	board = np.zeros((ROW_COUNT,COLUMN_COUNT))
	return board

def dropPiece(board, row, col, piece):
	board[row][col] = piece

def isPlaceValid(board, col):
	return board[ROW_COUNT-1][col] == 0

def GetNextRow(board, col):
	for r in range(ROW_COUNT):
		if board[r][col] == 0:
			return r

def printBoard(board):
	print(np.flip(board, 0))

def winningMove(board, piece):
	# Check horizontal locations for win
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT):
			if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
				return True

	# Check vertical locations for win
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT-3):
			if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
				return True

	# Check positively sloped diaganols
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT-3):
			if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
				return True

	# Check negatively sloped diaganols
	for c in range(COLUMN_COUNT-3):
		for r in range(3, ROW_COUNT):
			if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
				return True

def scoringScorePosition(selectedGroup, piece):
	score = 0
	opponentPeice = PLAYER_PIECE
	if piece == PLAYER_PIECE:
		opponentPeice = AI_PIECE

	if selectedGroup.count(piece) == 4:
		score += 100
	if selectedGroup.count(piece) == 3 and selectedGroup.count(0) == 1:
		score += 10
	if selectedGroup.count(piece) == 2 and selectedGroup.count(0) == 2:
		score += 5

	if selectedGroup.count(opponentPeice) == 3 and selectedGroup.count(0) == 1:
		score -= 80

	return score

def scorePosition(board, piece):
	score = 0

	# Score center column
	# centerArray = [int(i) for i in list(board[:, COLUMN_COUNT//2])]
	# centerCount = centerArray.count(piece)
	# score += 6 * centerCount

	# Horizontal check
	for r in range(ROW_COUNT):
		rowArray = [int(i) for i in board[r,:]]
		for c in range(COLUMN_COUNT-3):
			selectedGroup = rowArray[c:c+4]
			scoringScorePosition(selectedGroup, piece)
	
	# Vertical check
	for c in range(COLUMN_COUNT):
		colArray = [int(i) for i in board[:,c]]
		for r in range(ROW_COUNT-3):
			selectedGroup = colArray[r:r+4]
			scoringScorePosition(selectedGroup, piece)
	
	# "/" Diagonal check
	for r in range(ROW_COUNT-3):
		for c in range(COLUMN_COUNT-3):
			selectedGroup = [board[r+i][c+i] for i in range(4)]
			scoringScorePosition(selectedGroup, piece)
	
	# "\" Diagonal check
	for r in range(ROW_COUNT-3):
		for c in range(COLUMN_COUNT-3):
			selectedGroup = [board[r+3-i][c+i] for i in range(4)]
			scoringScorePosition(selectedGroup, piece)

	return score

def getValidLocations(board):
	validLocations = []
	for col in range(COLUMN_COUNT):
		if isPlaceValid(board, col):
			validLocations.append(col)
	return validLocations

def bestMoveForAI(board, peice):
	validLocations = getValidLocations(board)
	bestScore = -10000
	bestMove = random.choice(validLocations)
	for col in range(COLUMN_COUNT):
		row = GetNextRow(board, col)
		tempBoard = board.copy() 	# Create a copy of the board because we are going to change it
		dropPiece(tempBoard, row, col, peice)
		score = scorePosition(tempBoard, peice)
		if score > bestScore:
			bestScore = score
			bestMove = col
	return bestMove

def drawBoard(board):
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):
			pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
			pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
	
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):		
			if board[r][c] == PLAYER_PIECE:
				pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
			elif board[r][c] == AI_PIECE: 
				pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
	pygame.display.update()


board = createBoard()
printBoard(board)
isGameOver = False

pygame.init()

SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE/2 - 5)

screen = pygame.display.set_mode(size)
drawBoard(board)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 75)

turn = random.randint(PLAYER, AI)

while not isGameOver:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		if event.type == pygame.MOUSEMOTION:
			pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
			posx = event.pos[0]
			if turn == 0:
				pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
			# else: 
			# 	pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)
		pygame.display.update()

		if event.type == pygame.MOUSEBUTTONDOWN:
			pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
			# Ask for Player 1 Input
			if turn == PLAYER:
				posx = event.pos[0]
				col = int(math.floor(posx/SQUARESIZE))

				if isPlaceValid(board, col):
					row = GetNextRow(board, col)
					dropPiece(board, row, col, PLAYER_PIECE)

					if winningMove(board, PLAYER_PIECE):
						label = myfont.render("Player 1 wins!", 1, RED)
						screen.blit(label, (40,10))
						isGameOver = True
				
					turn += 1
					turn = turn % 2

					printBoard(board)
					drawBoard(board)

	if turn == AI and not isGameOver:				
		col = bestMoveForAI(board, AI_PIECE)
		if isPlaceValid(board, col):
			pygame.time.wait(500)
			row = GetNextRow(board, col)
			dropPiece(board, row, col, AI_PIECE )

			if winningMove(board, AI_PIECE):
				label = myfont.render("Player 2 wins!", 1, YELLOW)
				screen.blit(label, (40,10))
				isGameOver = True

			printBoard(board)
			drawBoard(board)

			turn += 1
			turn = turn % 2

	if isGameOver:
		pygame.time.wait(10000)