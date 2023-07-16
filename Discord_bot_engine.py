from __future__ import annotations

import random
import chess
import chess.pgn
import chess.svg
import discord
import svgrasterize

from dotenv import load_dotenv
from datetime import datetime
from Engine import best_move


ENGINE_NAME = "OTTOchess"
#-----------------------TOKEN-BELOW-------------------------
if True:
    token_hider = str('Token goes here')
    TOKEN = token_hider

load_dotenv()

FULLOUT_PIECES_CAP = ["Pawn", "Knight", "Bishop", "Rook", "Queen", "King"]
FULLOUT_PIECES = ["pawn", "knight", "bishop", "rook", "queen", "king"]
SHORT_PIECES_CAP = ["P", "N", "B", "R", "Q", "K"]
SHORT_PIECES = ["p", "n", "b", "r", "q", "k"]
PIECE_NAMES = FULLOUT_PIECES_CAP + FULLOUT_PIECES + SHORT_PIECES_CAP + SHORT_PIECES

ENGINE_BEST_MOVE = best_move 
board = 0
visual = True
slash_toggle = False
opponent_name = "reserved_opponent_name"


#----------------------GAME-ENCODING-----------------------

def random_move(board: chess.Board):
    new_list = list(board.legal_moves)
    idx = random.randint(0, len(new_list) - 1)
    return new_list[idx]

def retrieve_piece(move_string: str):
    for i, name in enumerate(PIECE_NAMES):
        if name in move_string:
            return (i % 6) + 1
    return 0

def truncated_move(move_challenge: str, move_truth: str):
    if move_challenge in move_truth:
        move_truth.replace(move_challenge, '')
        return move_truth
    return ''

def one_move_in(move: str, legal_moves: list):
    rest_list = []
    if move in legal_moves:
        return move

    for i in legal_moves:
        rest = truncated_move(move, i)
        if rest:
            rest_list.append(i)
    
    if len(rest_list) == 0:
        return None
    elif len(rest_list) == 1:
        return rest_list[0]
    elif len(rest_list) > 1:
        queen_promotion = [i for i in rest_list if "=Q" in i]
        if queen_promotion:
            return queen_promotion[0]
        else:
            return None

def capt_move_in_strict(move: str, legal_moves: list):
    move = move[0].upper() + move[1:]
    for i in legal_moves:
        if move == i:
            return move
    return None

def capt_move_in(move: str, legal_moves: list):
    move = move[0].upper() + move[1:]
    return one_move_in(move, legal_moves)

def WriteBoardPng(board, file_name):
    scene, idx, size = svgrasterize.svg_scene_from_str(str(chess.svg.board(board)))
    transform = svgrasterize.Transform().matrix(0, 1, 0, 1, 0, 0)
    result = scene.render(transform=transform)
    output, _convex_hull = result
    with open(f"{file_name}.png", "wb") as file:
        output.write_png(file) 

def CreateGame(players: tuple[str, str], 
               event: str = "Engine Development Match", 
               site: str = "Virtual", 
               rnd: int = 1, 
               tc: str = "unlimited", 
               elo: tuple[str, str] = ("unknown", "unknown")):
    game = chess.pgn.Game()
    date = datetime.today().strftime('%Y-%m-%d')
    game.headers["White"] = players[0]
    game.headers["Black"] = players[1]
    game.headers["Date"] = date
    game.headers["Event"] = event
    game.headers["Site"] = site
    game.headers["Round"] = rnd
    game.headers["TimeControl"] = tc
    game.headers["WhiteElo"] = elo[0]
    game.headers["BlackElo"] = elo[1]
    return game

def FinalizeGame(board: chess.BoardT, 
                 final_game, 
                 players: tuple[str, str], 
                 resignation: tuple[bool, bool] = (False, True), 
                 draw_by_agreement: bool = False):
    if not (draw_by_agreement or resignation[0]):
        final_game.headers["Result"] = board.outcome().result()
        index = int(not board.outcome().winner)
    
    if draw_by_agreement:
        final_game.headers["Termination"] = "Draw by agreement"
        final_game.headers["Result"] = "1/2-1/2"
    elif resignation[0]:
        if resignation[1]:
            final_game.headers["Termination"] = f"{players[0]} wins by resignation"
            final_game.headers["Result"] = "1-0"
        else:
            final_game.headers["Termination"] = f"{players[1]} wins by resignation"
            final_game.headers["Result"] = "0-1"
    else: 
        match board.outcome().termination:
            case 1:
                final_game.headers["Termination"] = f"{players[index]} wins by checkmate"
            case 2:
                final_game.headers["Termination"] = f"draw by stalemate"
            case 3:
                final_game.headers["Termination"] = f"draw by insufficient material"
            case 5:
                final_game.headers["Termination"] = f"draw by fivefold repetition"
            case 4:
                final_game.headers["Termination"] = f"draw by seventyfive move rule"
            case 6:
                final_game.headers["Termination"] = f"draw by fifty move rule"
            case 7:
                final_game.headers["Termination"] = f"draw by threefold repetition"
    return final_game

class Game():
    def __init__(self, 
                 channel: discord.channel,
                 fen: str = None, 
                 recapture: bool = True, 
                 players: tuple[str] = ("white", "black"), 
                 engine: bool = False, 
                 trunc_messages: bool = True,
                 talkative: bool = True,
                 async_engine: bool = False
                 ) -> None:
        self.channel = channel
        self.game_done = False
        self.players = players
        self.game_node = CreateGame(self.players, "Discord match")
        self.with_engine = engine
        self.engine = ENGINE_BEST_MOVE
        self.async_engine = async_engine
        self.file_name = "board_images"
        self.recapture = recapture
        self.message_history = []
        self.trunc_messages = trunc_messages
        self.talkative = talkative
        self.board = chess.Board(fen) if fen else chess.Board()

        if engine:
            self.make_engine_move()

    def _get_legal_sans(self) -> list:
        return [self.board.san(i) for i in self.board.legal_moves]
    
    async def _engine_move(self) -> chess.Move:
        # if self.async_engine:
        #     return await self.engine(self.board)
        # else:
        return self.engine(self.board)

    def _push_pgn(self, move: chess.Move) -> None:
        self.game_node = self.game_node.add_variation(move)

    def _push(self, move: str | int) -> bool:
        if isinstance(move, str):
            move = self.board.parse_san(move)
        
        if self.board.is_legal(move):
            self.board.push(move)
            self._push_pgn(move)
            return True
        else:
            return False

    async def _check_game_done(self) -> None:
        if self.board.is_game_over():
            self.game_done = True
            self.game_node = FinalizeGame(self.board, self.game_node.game(), self.players, (False, True), False)
            await self.say_pgn()

    async def resign(self) -> None:
        await self._say(f"Game ended, {self.players[int(self.board.turn)]} resigned")
        self.game_done = True
        self.game_node = FinalizeGame(self.board, self.game_node.game(), self.players, (True, not self.board.turn), False)
        await self.say_pgn()
    
    async def _recapture(self, move: str) -> bool:
        if not self.board.move_stack:
            await self._raise("Error: no move has been made to recapture")
            return False

        past_move = self.board.pop()
        if not self.board.is_capture(past_move):
            self.board.push(past_move)
            await self._raise("Error: most recent move is not a capture")
            return False
    
        self.board.push(past_move)
        options_bb = self.board.attackers(self.board.turn, past_move.to_square)
        options = list(options_bb)

        match len(options):
            case 0:
                await self._raise("Error: no possible recaptures")
                return False
            case 1:
                new_move = self.board.find_move(chess.SQUARES[options[0]], past_move.to_square)
                self._push(new_move)
                return True
            case _:
                if (chosen_piece := retrieve_piece(move)):
                    new_options = options_bb.intersection(self.board.pieces(chosen_piece, self.board.turn)).mask
                    if new_options.bit_count() == 1:
                        piece_square = chess.BB_SQUARES[new_options]
                        new_move = self.board.find_move(piece_square, past_move.to_square)
                        self._push(new_move)
                        return True
                    else:
                        await self._raise(f"Error: recapture has {new_options.bit_count()} candidates")
        return False

    async def _say(self, message: str, forced: bool = False) -> None:
        if self.talkative or forced:
            await self.channel.send(message)

    async def _raise(self, error: str) -> None:
        await self.channel.send(error, delete_after=10)

    async def _parse_move(self, move: str) -> bool:
        if not move:
            await self._raise("Illegal move: not a move")
            return False
        
        legal_moves = self._get_legal_sans()

        # parsing forced moves
        if len(legal_moves) == 1:
            return self._push(legal_moves[0])

        # parsing move (if perfect or of by one)
        if new_move := one_move_in(move, legal_moves):
            return self._push(new_move)
        
        # parsing move (if move is all lowercase)
        if new_move := capt_move_in(move, legal_moves):
            return self._push(new_move)

        # parsing move (if recapture)
        if ('x' in move or "takes" in move) and self.recapture:
            return await self._recapture(move)
        return False

    async def make_engine_move(self) -> bool:
        engine_move, evaluation, message = await self._engine_move()
        if message:
            self._say(message)
        await self._say(f"{ENGINE_NAME}: {self.board.san(engine_move)}, eval: {evaluation}", forced=True)
        self._push(engine_move)

    async def make_move(self, move: str) -> bool:
        if self.game_done:
            await self._say("Game has completed")
            return False
        if await self._parse_move(move):
            await self._check_game_done()
            return True
        await self._raise(f"Unable to parse move '{move}' with current board state")
        return False

    async def say_pgn(self) -> None:
        await self._say(str(self.game_node.game()))

    async def show(self) -> None:
        WriteBoardPng(self.board, self.file_name)
        img_message = await self.channel.send(file=discord.File(f"{self.file_name}.png"))
        self.message_history.insert(0, img_message)
        if self.trunc_messages:
            await self.manage_messages(2)

    async def manage_messages(self, amount_allowed: int) -> None:
        while len(self.message_history) > amount_allowed:
            await self.message_history.pop().delete()


#--------------------------BOT------------------------------

client = discord.Client(intents = discord.Intents.all())

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    global board
    global slash_toggle
    global visual
    global opponent_name
    if message.author == client.user:
        return

    m = message.content
    s = message.channel.send

    if m.startswith('\start auto game'):
        if ENGINE_NAME in m:
            visual = False
            if m.startswith(f'\start auto game {ENGINE_NAME}'):
                opponent_name = m[17:].split(" - ")[1]
                board = Game(message.channel, engine=True, trunc_messages=True)
            else:
                opponent_name = m[17:].split(" - ")[0]
                board = Game(message.channel, engine=False, trunc_messages=True)
    # elif m.startswith('\start game'):
    #     board = Game(message.channel, engine=None)
    #     await s('Game setup in normal position!')
    #     await board.show()
    elif m.startswith('\play engine'):
        board = Game(message.channel, engine=False)
        await s('Game setup in normal position!')
        await board.show()
    elif m.startswith('\play engine white'):
        board = Game(message.channel, engine=True)
        await board.show()
    elif m.startswith('\play engine black'):
        board = Game(message.channel, engine=False)
        await board.show()
    elif m.startswith('\\end game'):
        await s('Game ended')
        board.game_done = True
        if visual:
            await board.show()
    elif m.startswith('\\toggle'):
        slash_toggle = not slash_toggle
    elif m.startswith('\\resign'):
        await board.resign()
        if visual:
            await board.show()
    elif m.startswith('\\'):
        successful = await board.make_move(message.content[1:])
        if board.with_engine != None and successful: 
            await board.make_engine_move()
        if visual:
            await board.show()
    elif m.startswith(opponent_name):
        await board.make_move(m[len(opponent_name)+2:].split(" ")[0])
    else:
        if slash_toggle:
            successful = await board.make_move(message.content)
            if board.with_engine != None and successful: 
                await board.make_engine_move()
            if visual:
                await board.show()
        

#--------------------------MAIN-----------------------------

def main():
    client.run(TOKEN)

if "__main__" in __name__:
    main()
