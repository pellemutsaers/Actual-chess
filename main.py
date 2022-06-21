import pygame
from pygame.locals import *
import math
from functools import cache

WIDTH, HEIGHT = 800, 800
WHITE, BLACK, SELECTED = (235, 210, 180), (115, 85, 70), (0, 120, 100)
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
START_POSITION = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
RANDOM_POSITION = "7r/1P2p3/3bB2N/3K2pp/4P3/5PR1/kP2pP2/8 w KQkq - 0 1"

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

class Board:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Chess")
    
    def drawBoard(self):
        global squareSize
        global WIDTH, HEIGHT
        minWindowSize = min(WINDOW.get_size())
        WIDTH, HEIGHT = minWindowSize, minWindowSize
        squareSize = WIDTH / 8
        self.offsetX, self.offsetY = WINDOW.get_size()[0] - WIDTH, WINDOW.get_size()[1] - HEIGHT 

        for x in range(0, 8):
            for y in range(0, 8):
                if (x + y) % 2 == 0: 
                    pygame.draw.rect(WINDOW, WHITE, pygame.Rect(self.offsetX/2 + x*squareSize, self.offsetY/2 + y*squareSize, squareSize, squareSize))
                elif (x + y) % 2 == 1:
                    pygame.draw.rect(WINDOW, BLACK, pygame.Rect(self.offsetX/2 + x*squareSize, self.offsetY/2 + y*squareSize, squareSize, squareSize))
        pygame.display.flip()

    def getPieceList(self, position, redecodePosition):
        global pieceList2d
        global settings
        
        if redecodePosition:
            pieceList2d, settings = self.makePieceList(position)

    def drawPieces(self):
        global pieceList2d
        for column, row in enumerate(pieceList2d):
            for index, piece in enumerate(row):
                if piece == " ":
                    pass
                self.drawThePiece(piece, index, column)
        pygame.display.flip()

    @cache
    def drawThePiece(self, piece, index, column):
        if piece == "P":
            WINDOW.blit(pygame.transform.smoothscale(whitePawn, (squareSize, squareSize)), (self.offsetX / 2 + index * squareSize, self.offsetY / 2 + column * HEIGHT / 8))
        elif piece == "R":
            WINDOW.blit(pygame.transform.smoothscale(whiteRook, (squareSize, squareSize)), (self.offsetX / 2 + index * squareSize, self.offsetY / 2 + column * HEIGHT / 8))
        elif piece == "N":
            WINDOW.blit(pygame.transform.smoothscale(whiteKnight, (squareSize, squareSize)), (self.offsetX / 2 + index * squareSize, self.offsetY / 2 + column * HEIGHT / 8))
        elif piece == "B":
            WINDOW.blit(pygame.transform.smoothscale(whiteBishop, (squareSize, squareSize)), (self.offsetX / 2 + index * squareSize, self.offsetY / 2 + column * HEIGHT / 8))
        elif piece == "Q":
            WINDOW.blit(pygame.transform.smoothscale(whiteQueen, (squareSize, squareSize)), (self.offsetX / 2 + index * squareSize, self.offsetY / 2 + column * HEIGHT / 8))
        elif piece == "K":
            WINDOW.blit(pygame.transform.smoothscale(whiteKing, (squareSize, squareSize)), (self.offsetX / 2 + index * squareSize, self.offsetY / 2 + column * HEIGHT / 8))
        elif piece == "p":
            WINDOW.blit(pygame.transform.smoothscale(blackPawn, (squareSize, squareSize)), (self.offsetX / 2 + index * squareSize, self.offsetY / 2 + column * HEIGHT / 8))
        elif piece == "r":
            WINDOW.blit(pygame.transform.smoothscale(blackRook, (squareSize, squareSize)), (self.offsetX / 2 + index * squareSize, self.offsetY / 2 + column * HEIGHT / 8))
        elif piece == "n":
            WINDOW.blit(pygame.transform.smoothscale(blackKnight, (squareSize, squareSize)), (self.offsetX / 2 + index * squareSize, self.offsetY / 2 + column * HEIGHT / 8))
        elif piece == "b":
            WINDOW.blit(pygame.transform.smoothscale(blackBishop, (squareSize, squareSize)), (self.offsetX / 2 + index * squareSize, self.offsetY / 2 + column * HEIGHT / 8))
        elif piece == "q":
            WINDOW.blit(pygame.transform.smoothscale(blackQueen, (squareSize, squareSize)), (self.offsetX / 2 + index * squareSize, self.offsetY / 2 + column * HEIGHT / 8))
        elif piece == "k":
            WINDOW.blit(pygame.transform.smoothscale(blackKing, (squareSize, squareSize)), (self.offsetX / 2 + index * squareSize, self.offsetY / 2 + column * HEIGHT / 8))

    def makePieceList(self, position):
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

    def getMouseSquare(self, mousePosition):
        row = math.floor((mousePosition[0] - self.offsetX / 2) / (squareSize))
        column = math.floor((mousePosition[1] - self.offsetY / 2) / (squareSize))
        return (row, column)
    
    def redrawSquare(self, square1, square2):
        if (square1[0] + square1[1]) % 2 == 0:    
            pygame.draw.rect(WINDOW, WHITE, pygame.Rect(square1[0] * squareSize + self.offsetX / 2, square1[1] * squareSize + self.offsetY / 2, squareSize, squareSize))
        else:
            pygame.draw.rect(WINDOW, BLACK, pygame.Rect(square1[0] * squareSize + self.offsetX / 2, square1[1] * squareSize + self.offsetY / 2, squareSize, squareSize))
        if (square2[0] + square2[1]) % 2 == 0:    
            pygame.draw.rect(WINDOW, WHITE, pygame.Rect(square2[0] * squareSize + self.offsetX / 2, square2[1] * squareSize + self.offsetY / 2, squareSize, squareSize))
        else:
            pygame.draw.rect(WINDOW, BLACK, pygame.Rect(square2[0] * squareSize + self.offsetX / 2, square2[1] * squareSize + self.offsetY / 2, squareSize, squareSize))


def main():
    global pieceList2d
    currentPosition = START_POSITION
    BOARD = Board()
    BOARD.drawBoard()
    BOARD.makePieceList(currentPosition)
    BOARD.drawPieces()
    running = True
    v = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.VIDEORESIZE:
                BOARD.drawBoard()
                BOARD.drawPieces()
            elif v and event.type == pygame.MOUSEBUTTONDOWN:
                square1 = BOARD.getMouseSquare(pygame.mouse.get_pos())
                v = False
            if not v and event.type == pygame.MOUSEBUTTONUP:
                square2 = BOARD.getMouseSquare(pygame.mouse.get_pos())
                if square1 != square2:
                    v = True
                    pieceList2d[square2[1]][square2[0]] = pieceList2d[square1[1]][square1[0]]
                    pieceList2d[square1[1]][square1[0]] = " "
                    BOARD.redrawSquare(square1, square2)
                    BOARD.drawPieces()
            
if __name__ == '__main__':
    main()