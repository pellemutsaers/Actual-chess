import pygame
from pygame.locals import *

WIDTH, HEIGHT = 800, 800
WHITE, BLACK = (235, 210, 180), (115, 85, 70)
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

class Board:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Chess")
    
    def drawBoard(self):
        WIDTH, HEIGHT = min(WINDOW.get_size()), min(WINDOW.get_size())
        offsetX, offsetY = WINDOW.get_size()[0] - WIDTH, WINDOW.get_size()[1] - HEIGHT
        for x in range(0, 8):
            for y in range(0, 8):
                if (x + y) % 2 == 0: 
                    pygame.draw.rect(WINDOW, WHITE, pygame.Rect(offsetX/2 + x*WIDTH/8, offsetY/2 + y*HEIGHT/8, WIDTH/8, HEIGHT/8))
                elif (x + y) % 2 == 1:
                    pygame.draw.rect(WINDOW, BLACK, pygame.Rect(offsetX/2 + x*WIDTH/8, offsetY/2 + y*HEIGHT/8, WIDTH/8, HEIGHT/8))
        pygame.display.flip()


def main():
    BOARD = Board()
    BOARD.drawBoard()
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

if __name__ == '__main__':
    main()