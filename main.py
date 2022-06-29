import pygame
from pygame.locals import *
import math
from functools import cache

WIDTH, HEIGHT = 800, 800
WHITE, BLACK = (235, 210, 180), (115, 85, 70)
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
START_POSITION = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
offsetX, offsetY = 0, 0
squareSize = 100
pieceList2d = []

#! Pieces
blackRook = pygame.image.load("Chess pieces/black-rook.png")
blackKnight = pygame.image.load("Chess pieces/black-knight.png")
blackBishop = pygame.image.load("Chess pieces/black-bishop.png")
blackQueen = pygame.image.load("Chess pieces/black-queen.png")
blackKing = pygame.image.load("Chess pieces/black-king.png")
blackPawn = pygame.image.load("Chess pieces/black-pawn.png")

whiteRook = pygame.image.load("Chess pieces/white-rook.png")
whiteKnight = pygame.image.load("Chess pieces/white-knight.png")
whiteBishop = pygame.image.load("Chess pieces/white-bishop.png")
whiteQueen = pygame.image.load("Chess pieces/white-queen.png")
whiteKing = pygame.image.load("Chess pieces/white-king.png")
whitePawn = pygame.image.load("Chess pieces/white-pawn.png")

def splitChar(row):
    return [char for char in row]

def resetBoard():
    drawBoard()
    drawPieces()
    pygame.display.flip()

def initialize():
    pygame.init()
    pygame.display.set_caption("Chess")

def drawBoard():
    global squareSize
    global offsetX, offsetY
    minWindowSize = min(WINDOW.get_size())
    width, height = minWindowSize, minWindowSize
    squareSize = minWindowSize / 8
    offsetX, offsetY = WINDOW.get_size()[0] - width, WINDOW.get_size()[1] - height

    for x in range(0, 8):
        for y in range(0, 8):
            if (x + y) % 2 == 0:
                pygame.draw.rect(WINDOW, WHITE, pygame.Rect(
                    offsetX/2 + x*squareSize, offsetY/2 + y*squareSize, squareSize, squareSize))
            elif (x + y) % 2 == 1:
                pygame.draw.rect(WINDOW, BLACK, pygame.Rect(
                    offsetX/2 + x*squareSize, offsetY/2 + y*squareSize, squareSize, squareSize))

def getPieceList(position, redecodePosition):
    global pieceList2d
    global settings

    if redecodePosition:
        pieceList2d, settings = makePieceList(position)

def drawPieces():
    for column, row in enumerate(pieceList2d):
        for index, piece in enumerate(row):
            if piece == " ":
                pass
            elif piece == "P":
                WINDOW.blit(pygame.transform.smoothscale(whitePawn, (squareSize, squareSize)),
                            (offsetX / 2 + index * squareSize, offsetY / 2 + column * squareSize))
            elif piece == "R":
                WINDOW.blit(pygame.transform.smoothscale(whiteRook, (squareSize, squareSize)),
                            (offsetX / 2 + index * squareSize, offsetY / 2 + column * squareSize))
            elif piece == "N":
                WINDOW.blit(pygame.transform.smoothscale(whiteKnight, (squareSize, squareSize)),
                            (offsetX / 2 + index * squareSize, offsetY / 2 + column * squareSize))
            elif piece == "B":
                WINDOW.blit(pygame.transform.smoothscale(whiteBishop, (squareSize, squareSize)),
                            (offsetX / 2 + index * squareSize, offsetY / 2 + column * squareSize))
            elif piece == "Q":
                WINDOW.blit(pygame.transform.smoothscale(whiteQueen, (squareSize, squareSize)),
                            (offsetX / 2 + index * squareSize, offsetY / 2 + column * squareSize))
            elif piece == "K":
                WINDOW.blit(pygame.transform.smoothscale(whiteKing, (squareSize, squareSize)),
                            (offsetX / 2 + index * squareSize, offsetY / 2 + column * squareSize))
            elif piece == "p":
                WINDOW.blit(pygame.transform.smoothscale(blackPawn, (squareSize, squareSize)),
                            (offsetX / 2 + index * squareSize, offsetY / 2 + column * squareSize))
            elif piece == "r":
                WINDOW.blit(pygame.transform.smoothscale(blackRook, (squareSize, squareSize)),
                            (offsetX / 2 + index * squareSize, offsetY / 2 + column * squareSize))
            elif piece == "n":
                WINDOW.blit(pygame.transform.smoothscale(blackKnight, (squareSize, squareSize)),
                            (offsetX / 2 + index * squareSize, offsetY / 2 + column * squareSize))
            elif piece == "b":
                WINDOW.blit(pygame.transform.smoothscale(blackBishop, (squareSize, squareSize)),
                            (offsetX / 2 + index * squareSize, offsetY / 2 + column * squareSize))
            elif piece == "q":
                WINDOW.blit(pygame.transform.smoothscale(blackQueen, (squareSize, squareSize)),
                            (offsetX / 2 + index * squareSize, offsetY / 2 + column * squareSize))
            elif piece == "k":
                WINDOW.blit(pygame.transform.smoothscale(blackKing, (squareSize, squareSize)),
                            (offsetX / 2 + index * squareSize, offsetY / 2 + column * squareSize))

def makePieceList(position):
    global pieceList2d
    position = position.split("/")
    position = position[0:-1] + position[-1].split(" ")
    pieceList2d = position[0:-5]
    for i, row in enumerate(pieceList2d):
        pieceList2d[i] = splitChar(row)
    for i, row in enumerate(pieceList2d):
        for j, piece in enumerate(row):
            if piece.isdigit():
                row.pop(j)
                for k in range(int(piece)):
                    row.insert(k + j, " ")
    return pieceList2d, position[-5::1]

def getMouseSquare(mousePosition):
    row = math.floor((mousePosition[0] - offsetX / 2) / (squareSize))
    column = math.floor((mousePosition[1] - offsetY / 2) / (squareSize))
    return (row, column)

def redrawSquare(square):
    if (square[0] + square[1]) % 2 == 0:
        pygame.draw.rect(WINDOW, WHITE, pygame.Rect(
            square[0] * squareSize + offsetX / 2, square[1] * squareSize + offsetY / 2, squareSize, squareSize))
    else:
        pygame.draw.rect(WINDOW, BLACK, pygame.Rect(
            square[0] * squareSize + offsetX / 2, square[1] * squareSize + offsetY / 2, squareSize, squareSize))

def main():
    global pieceList2d
    currentPosition = START_POSITION
    initialize()
    makePieceList(currentPosition)
    resetBoard()
    running = True
    verification = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.VIDEORESIZE:
                resetBoard()
            elif verification and event.type == pygame.MOUSEBUTTONDOWN:
                square1 = getMouseSquare(pygame.mouse.get_pos())
                verification = False
            elif not verification and event.type == pygame.MOUSEBUTTONUP:
                square2 = getMouseSquare(pygame.mouse.get_pos())
                if square1 != square2:
                    pieceList2d[square2[1]][square2[0]] = pieceList2d[square1[1]][square1[0]]
                    pieceList2d[square1[1]][square1[0]] = " "
                    redrawSquare(square1)
                    redrawSquare(square2)
                    drawPieces()
                    pygame.display.flip()
                verification = True

if __name__ == '__main__':
    main()