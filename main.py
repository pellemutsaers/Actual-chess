import time
import chess
import pygame, pygame.locals
import math

#* If statement for cleanliness in vscode
if True:
    pygame.init()
    window = pygame.display.set_mode([480,480])
    board = chess.Board()
    legal_moves = board.legal_moves
    analyzed = 0
    analyzed_final = 0

    black = (115, 85, 70)
    white = (235, 210, 180)
    square_size = 80

    black_is_computer = True
    white_is_computer = True

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
    list = str(board).replace(" ", "").split("\n")
    return list

def return_mouse_square(pos):
    part1 = chr(97 + math.floor(pos[0]/60))
    part2 = str(8 - math.floor(pos[1]/60))
    return part1 + part2

#* First attempt at getting the enemy king closer to the edge of the board, for getting closer to checkmate in an endgame.
def distanceFromCenter(row, column):
    row -= 1
    distX = abs(4 - row)
    distY = abs(4 - column)
    distance = distX + distY
    return distance

#* Is speeding this up possible, intelligence should be easily extendible.
def evaluate_position(move_count):
    if board.is_checkmate():
        if move_count % 2 == 0:
            return -float("inf")
        if move_count % 2 == 1:
            return float("inf")
    if board.is_stalemate():
        return 0.0

    global analyzed
    global analyzed_final
    evaluation = 0

    list = create_list()
    for column, string in enumerate(list):
        for index, char in enumerate(string):
            match char:
                case "R":
                    evaluation += 5
                    if column <= 4:
                        evaluation += 0.9 - 0.1*(column+1)

                case "K":
                    if index < 3 or index > 6:
                        evaluation += 1
                    distance = distanceFromCenter(index, column)
                    evaluation -= distance / 8

                case "N":
                    evaluation += 3
                    evaluation += 0.9 - 0.1*(column+1)
                    if index >= 3 or index <= 6:
                        evaluation += 0.5

                case "B":
                    evaluation += 3
                    evaluation += 0.9 - 0.1*(column+1)

                case "Q":
                    evaluation += 9
                    if move_count > 10:
                        evaluation += 0.9 - 0.1*(column+1)

                case "P":
                    evaluation += 1
                    evaluation += 0.9 - 0.1*(column + 1)

                case "r":
                    evaluation -= 5
                    if column >= 3:
                        evaluation -= 0.1*(column+1)

                case "k":
                    if index < 3 or index > 6:
                        evaluation -= 1
                    distance = distanceFromCenter(index, column)
                    evaluation += distance / 8

                case "n":
                    evaluation -= 3
                    evaluation -= 0.1*(column+1)
                    if index >= 3 or index <= 6:
                        evaluation -= 0.5
                
                case "b":
                    evaluation -= 3
                    evaluation -= 0.1*(column+1)                

                case "q":
                    evaluation -= 9
                    if move_count > 10:
                        evaluation -= 0.1*(column+1)        

                case "p":
                    evaluation -= 1
                    evaluation -= 0.1*(column + 1)
    analyzed += 1
    return evaluation

def load_bar(iteration, total, prefix = '', suffix = '', decimals = 1, length = 50, fill = '#'):
    percent = ('{0:.' + str(decimals) + 'f}').format(100 * (iteration/float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '.' * (length - filledLength)
    print(f'\r{prefix} | {bar} | {percent} % {suffix}',end = '\r')
    if iteration == total:
        print()

#* Maybe important to get crital moves evaluiated first, to speed up the pruning in the min_max function.
def get_legal_moves_sorted():
    list = []
    for move in legal_moves:
        if board.is_capture(move):
            list.append(str(move))
    for move in legal_moves:
        if not board.is_capture(move):
            list.append(str(move))
    return list

#* Complicated stuff, dont trust this to actually do what it's supposed to do.
def min_max(depth, initial_depth, move_count, alpha, beta):
    global analyzed
    global analyzed_final
    if depth == 0:
        return evaluate_position(move_count)

    elif move_count % 2 == 0:
        max_eval = -float("inf") 
        if legal_moves.count() != 0:
            legal_moves_alt = get_legal_moves_sorted()
            for index, move in enumerate(legal_moves_alt): 
                if depth == initial_depth:
                    load_bar(index + 1, len(legal_moves_alt), prefix = 'Progress:', suffix = 'Complete', length = 50) 
                move = str(move)
                board.push_san(move)
                eval = min_max(depth - 1, initial_depth, move_count + 1, alpha, beta)
                alpha = max(alpha, eval)

                if eval > max_eval and depth != initial_depth: 
                    max_eval = eval

                elif eval > max_eval and depth == initial_depth:
                    max_eval = eval
                    best_move = move

                if beta <= alpha:
                    board.pop()
                    return max_eval
                board.pop()
        else:
            return evaluate_position(move_count)

        if depth == initial_depth:
            print("positions_ analyzed", analyzed)
            analyzed_final = analyzed
            analyzed = 0
            try:
                return (best_move, max_eval)
            except:
                return (move, max_eval)
        else: 
            return max_eval

    elif move_count % 2 == 1:
        min_eval = float("inf")
        if legal_moves.count() != 0: 
            legal_moves_alt = get_legal_moves_sorted()
            for index, move in enumerate(legal_moves_alt):
                if depth == initial_depth:
                    load_bar(index + 1, len(legal_moves_alt), prefix = 'Progress:', suffix = 'Complete', length = 50) 
                move = str(move)
                board.push_san(move)
                eval = min_max(depth - 1, initial_depth, move_count + 1, alpha, beta)
                beta = min(beta, eval)

                if eval < min_eval and depth != initial_depth: 
                    min_eval = eval 

                elif eval < min_eval and depth == initial_depth: 
                    min_eval = eval 
                    best_move = move

                if beta <= alpha:
                    board.pop()
                    return min_eval
                board.pop() 
        else: 
            return evaluate_position(move_count)

        if depth == initial_depth:
            print("positions analyzed: ", analyzed)
            analyzed_final = analyzed
            analyzed = 0
            try:
                return (best_move, min_eval)
            except:
                return (move, min_eval)

        else:
            return min_eval

#* Recursively finding the fastest way to a checkmate if thats necessairy, because otherwise it might find itself in an infinite loop in the endgame.
def compute_move(move_count, depth, last_result):

    result = min_max(depth, depth, move_count, -float("inf"), float("inf"))

    if result[1] == float("inf") or result[1] == -float("inf"):
        compute_move(move_count, depth - 1, result)

    if not last_result:
        return result
    else:
        return last_result

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
                        move = square1 + square2 + input("Promote pawn to: ")
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
                start = time.time()
                if legal_moves.count() < 5:
                    calculation_result = compute_move(move_count, 4, False)
                else:
                    calculation_result = compute_move(move_count, 5, False)
                board.push_uci(calculation_result[0])
                print("total time taken: ", time.time() - start)
                print("positions calculated per second: ", math.floor(analyzed_final / (time.time() - start)))
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