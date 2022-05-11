import pygame
from pygame.locals import *

WIDTH, HEIGHT = 800, 800
WHITE, BLACK = (235, 210, 180), (115, 85, 70)
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
START_POSITION = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
RANDOM_POSITION = "7r/1P2p3/3bB2N/3K2pp/4P3/5PR1/kP2pP2/8 w KQkq - 0 1"

#* Pieces
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
        global WIDTH, HEIGHT
        WIDTH, HEIGHT = min(WINDOW.get_size()), min(WINDOW.get_size())
        self.offsetX, self.offsetY = WINDOW.get_size()[0] - WIDTH, WINDOW.get_size()[1] - HEIGHT
        for x in range(0, 8):
            for y in range(0, 8):
                if (x + y) % 2 == 0: 
                    pygame.draw.rect(WINDOW, WHITE, pygame.Rect(self.offsetX/2 + x*WIDTH/8, self.offsetY/2 + y*HEIGHT/8, WIDTH/8, HEIGHT/8))
                elif (x + y) % 2 == 1:
                    pygame.draw.rect(WINDOW, BLACK, pygame.Rect(self.offsetX/2 + x*WIDTH/8, self.offsetY/2 + y*HEIGHT/8, WIDTH/8, HEIGHT/8))
        pygame.display.flip()

    def drawPieces(self, position, redecodePosition):
        global pieceList2d
        global settings
        
        if redecodePosition:
            pieceList2d, settings = self.makePieceList(position)

        for column, row in enumerate(pieceList2d):
            for index, piece in enumerate(row):
                if piece == " ":
                    pass
                elif piece == "P":
                    WINDOW.blit(pygame.transform.smoothscale(whitePawn, (WIDTH / 8, WIDTH / 8)), (self.offsetX / 2 + index * WIDTH / 8, self.offsetY / 2 + column * HEIGHT / 8))
                elif piece == "R":
                    WINDOW.blit(pygame.transform.smoothscale(whiteRook, (WIDTH / 8, WIDTH / 8)), (self.offsetX / 2 + index * WIDTH / 8, self.offsetY / 2 + column * HEIGHT / 8))
                elif piece == "N":
                    WINDOW.blit(pygame.transform.smoothscale(whiteKnight, (WIDTH / 8, WIDTH / 8)), (self.offsetX / 2 + index * WIDTH / 8, self.offsetY / 2 + column * HEIGHT / 8))
                elif piece == "B":
                    WINDOW.blit(pygame.transform.smoothscale(whiteBishop, (WIDTH / 8, WIDTH / 8)), (self.offsetX / 2 + index * WIDTH / 8, self.offsetY / 2 + column * HEIGHT / 8))
                elif piece == "Q":
                    WINDOW.blit(pygame.transform.smoothscale(whiteQueen, (WIDTH / 8, WIDTH / 8)), (self.offsetX / 2 + index * WIDTH / 8, self.offsetY / 2 + column * HEIGHT / 8))
                elif piece == "K":
                    WINDOW.blit(pygame.transform.smoothscale(whiteKing, (WIDTH / 8, WIDTH / 8)), (self.offsetX / 2 + index * WIDTH / 8, self.offsetY / 2 + column * HEIGHT / 8))
                elif piece == "p":
                    WINDOW.blit(pygame.transform.smoothscale(blackPawn, (WIDTH / 8, WIDTH / 8)), (self.offsetX / 2 + index * WIDTH / 8, self.offsetY / 2 + column * HEIGHT / 8))
                elif piece == "r":
                    WINDOW.blit(pygame.transform.smoothscale(blackRook, (WIDTH / 8, WIDTH / 8)), (self.offsetX / 2 + index * WIDTH / 8, self.offsetY / 2 + column * HEIGHT / 8))
                elif piece == "n":
                    WINDOW.blit(pygame.transform.smoothscale(blackKnight, (WIDTH / 8, WIDTH / 8)), (self.offsetX / 2 + index * WIDTH / 8, self.offsetY / 2 + column * HEIGHT / 8))
                elif piece == "b":
                    WINDOW.blit(pygame.transform.smoothscale(blackBishop, (WIDTH / 8, WIDTH / 8)), (self.offsetX / 2 + index * WIDTH / 8, self.offsetY / 2 + column * HEIGHT / 8))
                elif piece == "q":
                    WINDOW.blit(pygame.transform.smoothscale(blackQueen, (WIDTH / 8, WIDTH / 8)), (self.offsetX / 2 + index * WIDTH / 8, self.offsetY / 2 + column * HEIGHT / 8))
                elif piece == "k":
                    WINDOW.blit(pygame.transform.smoothscale(blackKing, (WIDTH / 8, WIDTH / 8)), (self.offsetX / 2 + index * WIDTH / 8, self.offsetY / 2 + column * HEIGHT / 8))

        pygame.display.flip()

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

def main():
    BOARD = Board()
    BOARD.drawBoard()
    BOARD.drawPieces(RANDOM_POSITION, True)
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.VIDEORESIZE:
                BOARD.drawBoard()
                BOARD.drawPieces(START_POSITION, False)

if __name__ == '__main__':
    main()