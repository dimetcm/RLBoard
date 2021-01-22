import random
import enum

MAX_SCORE = 100.0
MIN_SCORE = -100.0


class PieceType(enum.Enum):
    pawn = 1
    bishop = 2
    rook = 3,
    knight = 4,
    queen = 5,
    king = 6


class Agent:
    def __init__(self):
        pass

    def select_move(self, game):
        raise NotImplementedError()

class RandomBot(Agent):
    def select_move(self, game):
        legal_moves = game.game_state.get_possible_moves()

        if len(legal_moves) == 0:
            return None, None

        return random.choice(legal_moves)

def eval_material(game_state):
    result = 0.0
    for i in range(8):
        for j in range(8):
            piece = game_state.grid[i][j]
            piece_cost = 0.0
            if piece:
                piece_type = piece.get_piece_type()
                if piece_type == PieceType.pawn:
                    piece_cost = 1.0
                elif piece_type == PieceType.knight or piece_type == PieceType.bishop:
                    piece_cost = 3.0
                elif piece_type == PieceType.rook:
                    piece_cost = 3.0
                elif piece_type == PieceType.queen:
                    piece_cost = 9.0

                result += piece_cost * (1.0 if piece.side != game_state.side_to_move else -1.0)

    return result

def best_result(game_state, max_depth, eval_fn):
    legal_moves = game_state.get_possible_moves()
    if len(legal_moves) == 0:
        if game_state.is_king_under_attack(game_state.side_to_move.other):
            return MIN_SCORE
        else:
            return 0.0

    if max_depth == 0:
        return eval_fn(game_state)

    best_so_far = MIN_SCORE
    for next_state, candidate_move in legal_moves:
        opponents_best_result = best_result(next_state, max_depth-1, eval_fn)
        our_result = -1.0 * opponents_best_result
        if our_result > best_so_far:
            best_so_far = our_result

    return best_so_far


class DepthPruningBot(Agent):
    def select_move(self, game):
        legal_moves = game.game_state.get_possible_moves()

        if len(legal_moves) == 0:
            return None, None

        best_moves = []
        best_score = None
        for next_state, move in legal_moves:

            opponent_best_outcome = best_result(next_state, 1, eval_material)
            our_best_outcome = -1 * opponent_best_outcome
            if (not best_moves) or our_best_outcome > best_score:
                # This is the best move so far.
                best_moves = [(next_state, move)]
                best_score = our_best_outcome
            elif our_best_outcome == best_score:
                # This is as good as our previous best move.
                best_moves.append((next_state, move))

        return random.choice(best_moves)

