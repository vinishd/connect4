import numpy as np
import pygame
import sys
import math

BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)
ROWCOUNT = 6
COLCOUNT = 7

def createBoard():
    board = np.zeros((ROWCOUNT,COLCOUNT))
    return board

def dropPiece(board, row, col, piece):
    board[row][col] = piece

def isValidLocation(board, col):
    return board[ROWCOUNT - 1][col] == 0


def getNextOpenRow(board, col):
    for r in range(ROWCOUNT):
        if board[r][col] == 0:
            return r

def printBoard(board):
    print(np.flip(board, axis=0))

def winningMove(board, piece):
    for c in range(COLCOUNT - 3):
        for r in range(ROWCOUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True
    for c in range(COLCOUNT):
        for r in range(ROWCOUNT - 3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True
    for c in range(COLCOUNT - 3):
        for r in range(ROWCOUNT - 3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True
    for c in range(COLCOUNT - 3):
        for r in range(3, ROWCOUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True


def drawBoard(board):
    for c in range(COLCOUNT):
        for r in range(ROWCOUNT):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE + SQUARESIZE /2), int(r* SQUARESIZE + SQUARESIZE+SQUARESIZE/2)), RADIUS)

    for c in range(COLCOUNT):
        for r in range(ROWCOUNT):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c*SQUARESIZE + SQUARESIZE /2), height - int(r* SQUARESIZE+SQUARESIZE/2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE + SQUARESIZE /2), height - int(r* SQUARESIZE+SQUARESIZE/2)), RADIUS)
    pygame.display.update()


board = createBoard()
print(printBoard(board))
gameOver = False
turn = 0
pygame.init()

SQUARESIZE = 100
width = COLCOUNT * SQUARESIZE
height = (ROWCOUNT + 1)  * SQUARESIZE
RADIUS = int(SQUARESIZE / 2 - 5)
size = (width, height)
screen = pygame.display.set_mode(size)
drawBoard(board)
pygame.display.update()
myFont = pygame.font.SysFont("monospace", 75)

while not gameOver:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
            posx = event.pos[0]
            if turn == 0:
                pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
            else:
                pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
            # print(event.pos)
            # Ask p1 input
            if turn == 0:
                posx = event.pos[0]
                col = int(math.floor(posx /SQUARESIZE))

                if isValidLocation(board, col):
                    row = getNextOpenRow(board, col)
                    dropPiece(board, row, col, 1)
                    if winningMove(board, 1):
                        label = myFont.render("Player 1 Wins!!", 1, RED)
                        screen.blit(label, (40,10))
                        gameOver = True
            # #ask p2 input
            else:
                posx = event.pos[0]
                col = int(math.floor(posx /SQUARESIZE))
                if isValidLocation(board, col):
                    row = getNextOpenRow(board, col)
                    dropPiece(board, row, col, 2)
                    if winningMove(board, 2):
                        label = myFont.render("Player 2 Wins!!", 1, YELLOW)
                        screen.blit(label, (40,10))
                        gameOver = True

                    turn += 1
                    turn = turn % 2
            if gameOver:
                pygame.time.wait(3000)