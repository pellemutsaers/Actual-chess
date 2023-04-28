import time
import chess, chess.polyglot
import pygame, pygame.locals
import math
from functools import cache

ENDGAME_EXAMPLE = "8/8/8/4Q3/4K2k/8/8/8 w - - 0 1"


#! If statement for cleanliness in vscode. !!!!!!GLOBALS WARNING :) !!!!!!
if True:
    pygame.init()
    window = pygame.display.set_mode([480,480])
    board = chess.Board()
    legal_moves = board.legal_moves
    legal_captures = board.generate_legal_captures()
    analyzed = 0
    analyzed_final = 0

    black = (115, 85, 70)
    white = (235, 210, 180)
    square_size = 80

    black_is_computer = True
    white_is_computer = False

    white_pawn = pygame.image.load("PNG's/white-pawn.png")
    white_rook = pygame.image.load("PNG's/white-rook.png")
    white_knight = pygame.image.load("PNG's/white-knight.png")
    white_bishop = pygame.image.load("PNG's/white-bishop.png")
    white_queen = pygame.image.load("PNG's/white-queen.png")
    white_king = pygame.image.load("PNG's/white-king.png")

    black_pawn = pygame.image.load("PNG's/black-pawn.png")
    black_rook = pygame.image.load("PNG's/black-rook.png")
    black_knight = pygame.image.load("PNG's/black-knight.png")
    black_bishop = pygame.image.load("PNG's/black-bishop.png")
    black_queen = pygame.image.load("PNG's/black-queen.png")
    black_king = pygame.image.load("PNG's/black-king.png")

def draw_board():
    global square_size
    square_size = min(window.get_size())/8
    for x in range(0,8):
        for y in range(0,8):
            if (x + y) % 2 == 0:
                color = black
            else:
                color = white
            pygame.draw.rect(window, color, pygame.Rect(x*square_size, y*square_size, square_size, square_size))
    pygame.display.flip()

def draw_pieces():
    list = create_list()
    for column, string in enumerate(list):
        for row, char in enumerate(string):
            match char:
                case ".":
                    pass
                case "r":
                    window.blit(black_rook, [row*square_size, column*square_size])
                case "n":
                    window.blit(black_knight, [row*square_size, column*square_size])
                case "b":
                    window.blit(black_bishop, [row*square_size, column*square_size])
                case "q":
                    window.blit(black_queen, [row*square_size, column*square_size])
                case "k":
                    window.blit(black_king, [row*square_size, column*square_size])
                case "p":
                    window.blit(black_pawn, [row*square_size, column*square_size])
                case "R":
                    window.blit(white_rook, [row*square_size, column*square_size])
                case "N":
                    window.blit(white_knight, [row*square_size, column*square_size])
                case "B":
                    window.blit(white_bishop, [row*square_size, column*square_size])
                case "Q":
                    window.blit(white_queen, [row*square_size, column*square_size])
                case "K":
                    window.blit(white_king, [row*square_size, column*square_size])
                case "P":
                    window.blit(white_pawn, [row*square_size, column*square_size])
    pygame.display.flip()

def create_list():
    return str(board).replace(" ", "").split("\n")

def return_mouse_square(pos):
    part1 = chr(97 + math.floor(pos[0]/60))
    part2 = str(8 - math.floor(pos[1]/60))
    return part1 + part2

#* First attempt at getting the enemy king closer to the edge of the board, for getting closer to checkmate in an endgame, idk about this.
def distance_from_center(row, column):
    distX = abs(4.5 - row)
    distY = abs(4.5 - column)
    distance = distX + distY
    return distance

@cache
def evaluate_position(_):
    if not legal_moves:
        outcome = board.outcome().result()
        if outcome == "1-0":
            return 100
        elif outcome == "0-1":
            return -100
        else:
            return 0.0

    evaluation = 0
    move_count = board.ply()

    list = create_list()
    for column, string in enumerate(list):
        for index, char in enumerate(string):
            column += 1
            index += 1
            match char:
                case "R":
                    evaluation += 50
                    if column >= 3 or column == 1:
                        evaluation += 8 - column
                    else:
                        evaluation += 10

                case "K":
                    if index <= 2 or index >= 7:
                        evaluation += 10
                    distance = distance_from_center(index, column)
                    evaluation -= distance*move_count * 0.02

                case "N":
                    evaluation += 30
                    evaluation += 8 - column
                    if index >= 3 or index <= 6:
                        evaluation += 5

                case "B":
                    evaluation += 30
                    evaluation += 8 - column

                case "Q":
                    evaluation += 90
                    if move_count > 10:
                        evaluation += 8 - column

                case "P":
                    evaluation += 10
                    evaluation += 8 - column

                case "r":
                    evaluation -= 50
                    if column <= 6 or column == 8:
                        evaluation -= column - 1
                    else:
                        evaluation -= 10

                case "k":
                    if index <= 2 or index >= 7:
                        evaluation -= 10
                    distance = distance_from_center(index, column)
                    evaluation += distance * move_count * 0.02

                case "n":
                    evaluation -= 30
                    evaluation -= column - 1
                    if index >= 3 or index <= 6:
                        evaluation -= 5

                case "b":
                    evaluation -= 30
                    evaluation -= column - 1

                case "q":
                    evaluation -= 90
                    if move_count > 10:
                        evaluation -= column - 1

                case "p":
                    evaluation -= 10
                    evaluation -= column - 1

            column -= 1
    return (evaluation * 0.1)

def load_bar(iteration, total, prefix = '', suffix = '', decimals = 1, length = 50, fill = '#'):
    percent = ('{0:.' + str(decimals) + 'f}').format(100 * (iteration/float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '.' * (length - filledLength)
    print(f'\r{prefix} | {bar} | {percent}% {suffix}',end = '\r')
    if iteration == total:
        print()

#* Complicated stuff, dont trust this to actually do what it's supposed to do.
def min_max(depth, initial_depth, alpha, beta):
    global analyzed
    global analyzed_final

    if depth <= 0:
        zobrist = chess.polyglot.zobrist_hash(board)
        analyzed += 1
        return evaluate_position(zobrist)

    elif board.ply() % 2 == 0:
        max_eval = -float("inf")
        if legal_moves:
            for index, move in enumerate(legal_moves): 
                if depth == initial_depth:
                    load_bar(index + 1, legal_moves.count(), prefix = 'Progress:', suffix = 'Complete', length = 50) 
                board.push(move)
                eval = min_max(depth - 1, initial_depth, alpha, beta)
                alpha = max(alpha, eval)

                if eval > max_eval and depth != initial_depth: 
                    max_eval = eval

                elif eval > max_eval:
                    max_eval = eval
                    best_move = move

                if beta <= alpha and depth != initial_depth:
                    board.pop()
                    return max_eval
                board.pop()
        else:
            zobrist = chess.polyglot.zobrist_hash(board)
            analyzed += 1
            result = evaluate_position(zobrist)
            return result

        if depth == initial_depth:
            print("positions_ analyzed", analyzed)
            analyzed_final = analyzed
            analyzed = 0
            return (str(best_move), max_eval)

        else:
            return max_eval


    elif board.ply() % 2 == 1:
        min_eval = float("inf")
        if legal_moves: 
            for index, move in enumerate(legal_moves):
                if depth == initial_depth:
                    load_bar(index + 1, legal_moves.count(), prefix = 'Progress:', suffix = 'Complete', length = 50) 
                board.push(move)
                eval = min_max(depth - 1, initial_depth, alpha, beta)
                beta = min(beta, eval)

                if eval < min_eval and depth != initial_depth: 
                    min_eval = eval 

                elif eval < min_eval: 
                    min_eval = eval 
                    best_move = move

                if beta <= alpha and depth != initial_depth:
                    board.pop()
                    return min_eval
                board.pop() 
        else:
            zobrist = chess.polyglot.zobrist_hash(board)
            analyzed += 1
            result = evaluate_position(zobrist)
            return result

        if depth == initial_depth:
            print("positions analyzed: ", analyzed)
            analyzed_final = analyzed
            analyzed = 0
            return (str(best_move), min_eval)

        else:
            return min_eval

#* Maybe working, probably not. Issue could be here.
def compute_move(depth):

    result = min_max(depth, depth, -float("inf"), float("inf"))

    if (result[1] == float("inf") or result[1] == -float("inf")) and depth != 1:
        new_result = min_max(depth - 1, depth - 1, -float("inf"), float("inf"))
        if (new_result[1] == float("inf") or result[1] == -float("inf")) and depth != 1:
            new_result2 = min_max(depth - 2, depth - 2, -float("inf"), float("inf"))
            if (new_result2[1] == float("inf") or result[1] == -float("inf")) and depth != 1:
                new_result3 = min_max(depth - 3, depth - 3, -float("inf"), float("inf"))
                if (new_result3[1] == float("inf") or result[1] == -float("inf")) and depth != 1:
                    return new_result3
                else:
                    return new_result2
            else:
                return new_result
        else:
            return result
    else:
        return result
        
def main():
    global analyzed_final
    running = True
    waiting = False
    move_count = 0
    draw_board()
    draw_pieces()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if (not white_is_computer and move_count % 2 == 0) or (not black_is_computer and move_count % 2 == 1):
                if event.type == pygame.MOUSEBUTTONDOWN and waiting == False:
                    square1 = return_mouse_square(pygame.mouse.get_pos())
                    waiting = True
                if event.type == pygame.MOUSEBUTTONUP and waiting == True:
                    square2 = return_mouse_square(pygame.mouse.get_pos())
                    piece_at_square = str(board.piece_at(chess.parse_square(square1)))

                    if (piece_at_square == "P" and square2[1] == "8") or (piece_at_square == "p" and square2[1] == "1"):
                        move = square1 + square2 + input("Promote pawn to: (lower case)")
                        if chess.Move.from_uci(move) in legal_moves:
                            board.push_uci(move)
                            draw_board()
                            draw_pieces()
                            move_count += 1

                    elif square1 != square2:
                        move = square1 + square2
                        if chess.Move.from_uci(move) in legal_moves:
                            board.push_uci(move)
                            draw_board()
                            draw_pieces()
                            move_count += 1
                    waiting = False

            elif (white_is_computer and move_count % 2 == 0) or (black_is_computer and move_count % 2 == 1):
                start = time.perf_counter()
                if legal_moves.count() < 5:
                    calculation_result = compute_move(6)
                elif legal_moves.count() > 30:
                    calculation_result = compute_move(4)
                else:
                    calculation_result = compute_move(5)

                board.push_uci(calculation_result[0])
                print("total time taken: ", time.perf_counter() - start)
                print("positions calculated per second: ", math.floor(analyzed_final / (time.perf_counter() - start)))
                print("evaluation: ", calculation_result[1])

                draw_board()
                draw_pieces()
                move_count += 1

            if board.result() == "0-1":
                print("Black won, yay")
                input1 = input("enter anything to close game: ")
                running = True
            elif board.result() == "1-0":
                print("White won, yay")
                input2 = input("enter anything to close game: ")
                running = False
            elif board.is_stalemate():
                print("Stalemate")
                input3 = input("enter anything to close game: ")
                running = False

if __name__ == "__main__":
    main()