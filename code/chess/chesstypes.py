import enum
import random
import copy


class Side(enum.Enum):
    white = 0
    black = 1

    @property
    def other(self):
        return Side.black if self == Side.white else Side.white


class PieceType(enum.Enum):
    pawn = 1
    bishop = 2
    rook = 3,
    knight = 4,
    queen = 5,
    king = 6


class Move:

    def __init__(self, piece_type, moved_from, moved_to, promoted_to=None):
        self.piece_type = piece_type
        self.moved_from = moved_from
        self.moved_to = moved_to
        self.promoted_to = promoted_to

class Board:
    def __init__(self):
        self.game_state = GameState()
        self.moves_history = []

    # def setup(self):
    #    self.game_state = GameState.create_starting_game_state()

    def print(self):
        self.game_state.print()


    def play_game(self):
        self.game_state = GameState.create_starting_game_state()
        self.moves_history = []

        while True:
            legal_moves = self.game_state.get_possible_moves(self)
            if len(legal_moves) == 0:
                if self.game_state.is_king_under_attack(self.game_state.side_to_move.other):
                    print("mate, " + ("white" if self.game_state.side_to_move == Side.black else "black") + " won")
                else:
                    print("stalemate, " + str(self.game_state.side_to_move) + " to move")
                return

            new_game_state, move = random.choice(legal_moves)

            self.game_state = new_game_state
            self.moves_history.append(move)
            self.print()

            if self.game_state.is_it_draw():
                print("draw")
                return



class GameState:
    def __init__(self):
        self.grid = []
        self.side_to_move = Side.white
        self.white_king_moved = False
        self.black_king_moved = False
        self.a1_rook_moved = False
        self.h1_rook_moved = False
        self.a8_rook_moved = False
        self.h8_rook_moved = False
        for i in range(8):
            rank = [None] * 8
            self.grid.append(rank)

    @classmethod
    def create_starting_game_state(cls):
        state = GameState()
        for i in range(8):
            state.grid[1][i] = Pawn(Side.white)
            state.grid[6][i] = Pawn(Side.black)

        state.grid[0][0] = Rook(Side.white)
        state.grid[0][1] = Knight(Side.white)
        state.grid[0][2] = Bishop(Side.white)
        state.grid[0][3] = Queen(Side.white)
        state.grid[0][4] = King(Side.white)
        state.grid[0][5] = Bishop(Side.white)
        state.grid[0][6] = Knight(Side.white)
        state.grid[0][7] = Rook(Side.white)

        state.grid[7][0] = Rook(Side.black)
        state.grid[7][1] = Knight(Side.black)
        state.grid[7][2] = Bishop(Side.black)
        state.grid[7][3] = Queen(Side.black)
        state.grid[7][4] = King(Side.black)
        state.grid[7][5] = Bishop(Side.black)
        state.grid[7][6] = Knight(Side.black)
        state.grid[7][7] = Rook(Side.black)

        return state

    def is_square_under_attack(self, attacker_side, rank_idx, file_idx):
        for i in range(8):
            for j in range(8):
                piece = self.grid[i][j]
                if piece and piece.side == attacker_side:
                    if piece.is_attacking_square(attacker_side, self, i, j, rank_idx, file_idx):
                        print(piece, i, j, rank_idx, file_idx)
                        return True

        return False

    def is_valid(self):
        return not self.is_king_under_attack(self.side_to_move)

    def is_it_draw(self):

        # insufficient material check

        # todo: for now only two kings check
        piece_counter = 0
        for i in range(8):
            for j in range(8):
                piece = self.grid[i][j]
                if piece:
                    piece_counter += 1

                if piece_counter > 2:
                    return False

        return True

    def is_king_under_attack(self, attacker_side):
        for i in range(8):
            for j in range(8):
                piece = self.grid[i][j]
                if piece and piece.side == attacker_side.other and piece.get_piece_type() == PieceType.king:
                    return self.is_square_under_attack(attacker_side, i, j)

        return False

    def get_possible_moves(self, game):
        result = []
        for i in range(8):
            for j in range(8):
                piece = self.grid[i][j]
                if piece and piece.side == self.side_to_move:
                    result += piece.get_possible_moves(game, i, j)
        return result


    @classmethod
    def is_board_position_valid(cls, rank_idx, file_idx):
        return 0 <= rank_idx < 8 and 0 <= file_idx < 8

    def print(self):
        # print from the whites point of view
        for i in range(7, -1, -1):
            rank_str = ""
            for j in range(8):
                p = self.grid[i][j]
                rank_str += str(p) if p else ' - '
            print(rank_str)
        print("========================")

class Piece:
    def __init__(self, side):
        self.side = side

    @classmethod
    def get_possible_moves(cls, game, rank_idx, file_idx):
        return []

    @classmethod
    def get_piece_type(cls):
        return None


class Pawn(Piece):
    def __init__(self, side):
        super().__init__(side)

    def __str__(self):
        return ' P ' if self.side == Side.white else '_p_'

    @classmethod
    def get_piece_type(cls):
        return PieceType.pawn


    @classmethod
    def get_possible_moves(cls, game, rank_idx, file_idx):
        game_state = game.game_state
        result = []

        # one rank move/promotion
        move_direction = 1 if game_state.side_to_move == Side.white else -1
        piece_in_front = game_state.grid[rank_idx + move_direction][file_idx]
        if piece_in_front is None:
            if (game_state.side_to_move == Side.white and rank_idx < 6) or \
                    (game_state.side_to_move == Side.black and rank_idx > 1):
                new_state = copy.deepcopy(game_state)
                new_state.grid[rank_idx + move_direction][file_idx] = new_state.grid[rank_idx][file_idx]
                new_state.grid[rank_idx][file_idx] = None
                new_state.side_to_move = game_state.side_to_move.other
                if new_state.is_valid():
                    move = Move(cls.get_piece_type(), (rank_idx, file_idx), (rank_idx + move_direction, file_idx))
                    result.append((new_state, move))
            else:
                promotion_pieces = [Queen(game_state.side_to_move),
                                    Bishop(game_state.side_to_move),
                                    Knight(game_state.side_to_move),
                                    Rook(game_state.side_to_move)]

                for piece in promotion_pieces:
                    new_state = copy.deepcopy(game_state)
                    new_state.grid[rank_idx + move_direction][file_idx] = piece
                    new_state.grid[rank_idx][file_idx] = None
                    new_state.side_to_move = game_state.side_to_move.other
                    if new_state.is_valid():
                        move = Move(cls.get_piece_type(), (rank_idx, file_idx), (rank_idx + move_direction, file_idx), piece.get_piece_type())
                        result.append((new_state, move))

        # captures
        move_direction = 1 if game_state.side_to_move == Side.white else -1
        capture_positions = [(rank_idx + move_direction, file_idx - 1), (rank_idx + move_direction, file_idx + 1)]
        for new_rank_idx, new_file_idx in capture_positions:
            if not GameState.is_board_position_valid(new_rank_idx, new_file_idx):
                continue

            piece_to_capture = game_state.grid[new_rank_idx][new_file_idx]

            if piece_to_capture and piece_to_capture.side != game_state.side_to_move:
                if (game_state.side_to_move == Side.white and rank_idx < 6) or \
                        (game_state.side_to_move == Side.black and rank_idx > 1):
                    new_state = copy.deepcopy(game_state)
                    new_state.grid[new_rank_idx][new_file_idx] = new_state.grid[rank_idx][file_idx]
                    new_state.grid[rank_idx][file_idx] = None
                    new_state.side_to_move = game_state.side_to_move.other
                    if new_state.is_valid():
                        move = Move(cls.get_piece_type(), (rank_idx, file_idx), (new_rank_idx, new_file_idx))
                        result.append((new_state, move))
                else:
                    promotion_pieces = [Queen(game_state.side_to_move),
                                        Bishop(game_state.side_to_move),
                                        Knight(game_state.side_to_move),
                                        Rook(game_state.side_to_move)]

                    for piece in promotion_pieces:
                        new_state = copy.deepcopy(game_state)
                        new_state.grid[new_rank_idx][new_file_idx] = piece
                        new_state.grid[rank_idx][file_idx] = None
                        new_state.side_to_move = game_state.side_to_move.other
                        if new_state.is_valid():
                            move = Move(cls.get_piece_type(), (rank_idx, file_idx), (new_rank_idx, new_file_idx), piece.get_piece_type())
                            result.append((new_state, move))

        # two ranks move
        if (game_state.side_to_move == Side.white and rank_idx == 1) or (game_state.side_to_move == Side.black and rank_idx == 6):
            move_direction = 1 if game_state.side_to_move == Side.white else -1
            if game_state.grid[rank_idx + move_direction][file_idx] is None and game_state.grid[rank_idx + move_direction * 2][file_idx] is None:
                new_state = copy.deepcopy(game_state)
                new_state.grid[rank_idx + move_direction * 2][file_idx] = new_state.grid[rank_idx][file_idx]
                new_state.grid[rank_idx][file_idx] = None
                new_state.side_to_move = game_state.side_to_move.other
                if new_state.is_valid():
                    move = Move(cls.get_piece_type(), (rank_idx, file_idx), (rank_idx + move_direction * 2, file_idx))
                    result.append((new_state, move))

        # en passant
        if len(game.moves_history) > 0:
            last_move = game.moves_history[-1]
            if last_move.piece_type == PieceType.pawn:
                left_and_right_positions = [(rank_idx, file_idx - 1), (rank_idx, file_idx + 1)]
                for pos in left_and_right_positions:
                    if game_state.is_board_position_valid(pos[0], pos[1]):
                        if game_state.grid[pos[0]][pos[1]] and game_state.grid[pos[0]][pos[1]].get_piece_type() == PieceType.pawn:
                            move_direction = 1 if game_state.side_to_move == Side.white else -1
                            if last_move.moved_to == (pos[0], pos[1]) and last_move.moved_from == (pos[0] + move_direction * 2, pos[1]):
                                new_state = copy.deepcopy(game_state)
                                new_state.grid[pos[0]][pos[1]] = None
                                new_state.grid[rank_idx][file_idx] = None
                                new_state.grid[pos[0] + move_direction][pos[1]] = Pawn(game_state.side_to_move)
                                new_state.side_to_move = game_state.side_to_move.other
                                if new_state.is_valid():
                                    move = Move(cls.get_piece_type(), (rank_idx, file_idx), (pos[0] + move_direction, pos[1]))
                                    result.append((new_state, move))

        return result

    @classmethod
    def is_attacking_square(cls, side, game_state, self_rank_idx, self_file_idx, square_rank_idx, square_file_idx):
        move_direction = 1 if side == Side.white else -1
        return self_rank_idx + move_direction == square_rank_idx and abs(self_file_idx - square_file_idx) == 1


class Rook(Piece):
    def __init__(self, side):
        super().__init__(side)

    def __str__(self):
        return ' R ' if self.side == Side.white else ' r '

    @classmethod
    def get_piece_type(cls):
        return PieceType.rook

    @classmethod
    def get_possible_moves(cls, game, rank_idx, file_idx):
        game_state = game.game_state

        result = []

        movement_directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        for direction in movement_directions:
            new_rank_idx = rank_idx + direction[0]
            new_file_idx = file_idx + direction[1]

            while True:
                if not game_state.is_board_position_valid(new_rank_idx, new_file_idx):
                    break

                piece = game_state.grid[new_rank_idx][new_file_idx]
                if piece:
                    if piece.side == game_state.side_to_move:
                        break

                new_state = copy.deepcopy(game_state)
                new_state.grid[new_rank_idx][new_file_idx] = new_state.grid[rank_idx][file_idx]
                new_state.grid[rank_idx][file_idx] = None
                new_state.side_to_move = game_state.side_to_move.other

                if game_state.side_to_move == Side.white:
                    if rank_idx == 0 and file_idx == 0:
                        new_state.a1_rook_moved = True
                    elif rank_idx == 0 and file_idx == 7:
                        new_state.h1_rook_moved = True
                else:
                    if rank_idx == 7 and file_idx == 0:
                        new_state.a8_rook_moved = True
                    elif rank_idx == 7 and file_idx == 7:
                        new_state.h8_rook_moved = True

                if new_state.is_valid():
                    move = Move(cls.get_piece_type(), (rank_idx, file_idx), (new_rank_idx, new_file_idx))
                    result.append((new_state, move))

                if piece:
                    break

                new_rank_idx += direction[0]
                new_file_idx += direction[1]

        return result

    @classmethod
    def is_attacking_square(cls, side, game_state, self_rank_idx, self_file_idx, square_rank_idx, square_file_idx):
        if self_rank_idx == square_rank_idx:
            direction = 1 if square_file_idx > self_file_idx else -1
            for new_file_idx in range(self_file_idx + direction, square_file_idx, direction):
                piece = game_state.grid[self_rank_idx][new_file_idx]
                if piece:
                    return False

            return True

        if self_file_idx == square_file_idx:
            direction = 1 if square_rank_idx > self_rank_idx else -1
            for new_rank_idx in range(self_rank_idx + direction, square_rank_idx, direction):
                piece = game_state.grid[new_rank_idx][self_file_idx]
                if piece:
                    return False

            return True

        return False

class Knight(Piece):
    def __init__(self, side):
        super().__init__(side)

    def __str__(self):
        return ' N ' if self.side == Side.white else ' n '

    @classmethod
    def get_piece_type(cls):
        return PieceType.knight


    @classmethod
    def get_possible_moves(cls, game, rank_idx, file_idx):
        game_state = game.game_state

        new_positions = [(rank_idx + 2, file_idx - 1),
                         (rank_idx + 2, file_idx + 1),
                         (rank_idx + 1, file_idx + 2),
                         (rank_idx - 1, file_idx + 2),
                         (rank_idx - 2, file_idx + 1),
                         (rank_idx - 2, file_idx - 1),
                         (rank_idx + 1, file_idx - 2),
                         (rank_idx - 1, file_idx - 2)]

        result = []
        for new_rank_idx, new_file_idx in new_positions:
            if game_state.is_board_position_valid(new_rank_idx, new_file_idx):
                piece = game_state.grid[new_rank_idx][new_file_idx]
                if piece is None or piece.side != game_state.side_to_move:
                    new_game_state = copy.deepcopy(game_state)
                    new_game_state.side_to_move = game_state.side_to_move.other
                    new_game_state.grid[new_rank_idx][new_file_idx] = new_game_state.grid[rank_idx][file_idx]
                    new_game_state.grid[rank_idx][file_idx] = None
                    if new_game_state.is_valid():
                        move = Move(cls.get_piece_type(), (rank_idx, file_idx), (new_rank_idx, new_file_idx))
                        result.append((new_game_state, move))

        return result

    @classmethod
    def is_attacking_square(cls, side, game_state, self_rank_idx, self_file_idx, square_rank_idx, square_file_idx):
        new_positions = [(self_rank_idx + 2, self_file_idx - 1),
                         (self_rank_idx + 2, self_file_idx + 1),
                         (self_rank_idx + 1, self_file_idx + 2),
                         (self_rank_idx - 1, self_file_idx + 2),
                         (self_rank_idx - 2, self_file_idx + 1),
                         (self_rank_idx - 2, self_file_idx - 1),
                         (self_rank_idx + 1, self_file_idx - 2),
                         (self_rank_idx - 1, self_file_idx - 2)]

        return (square_rank_idx, square_file_idx) in new_positions

class Bishop(Piece):
    def __init__(self, side):
        super().__init__(side)

    def __str__(self):
        return ' B ' if self.side == Side.white else ' b '

    @classmethod
    def get_piece_type(cls):
        return PieceType.bishop

    @classmethod
    def get_possible_moves(cls, game, rank_idx, file_idx):
        game_state = game.game_state

        result = []

        movement_directions = [(1, 1), (1, -1), (-1, -1), (-1, 1)]
        for direction in movement_directions:
            new_rank_idx = rank_idx + direction[0]
            new_file_idx = file_idx + direction[1]

            while True:
                if not game_state.is_board_position_valid(new_rank_idx, new_file_idx):
                    break

                piece = game_state.grid[new_rank_idx][new_file_idx]
                if piece:
                    if piece.side == game_state.side_to_move:
                        break

                new_state = copy.deepcopy(game_state)
                new_state.grid[new_rank_idx][new_file_idx] = new_state.grid[rank_idx][file_idx]
                new_state.grid[rank_idx][file_idx] = None
                new_state.side_to_move = game_state.side_to_move.other
                if new_state.is_valid():
                    move = Move(cls.get_piece_type(), (rank_idx, file_idx), (new_rank_idx, new_file_idx))
                    result.append((new_state, move))

                if piece:
                    break

                new_rank_idx += direction[0]
                new_file_idx += direction[1]

        return result

    @classmethod
    def is_attacking_square(cls, side, game_state, self_rank_idx, self_file_idx, square_rank_idx, square_file_idx):
        if square_rank_idx == self_rank_idx or square_file_idx == self_file_idx:
            return False

        rank_direction = 1 if square_rank_idx > self_rank_idx else -1
        file_direction = 1 if square_file_idx > self_file_idx else -1

        if abs(square_rank_idx - self_rank_idx) != abs(square_file_idx - self_file_idx):
            return False

        for i in range(abs(square_rank_idx - self_rank_idx) - 1):
            new_position = (self_rank_idx + rank_direction * (i + 1), self_file_idx + file_direction * (i + 1))
            piece = game_state.grid[new_position[0]][new_position[1]]
            if piece:
                return False

        return True


class Queen(Piece):
    def __init__(self, side):
        super().__init__(side)

    def __str__(self):
        return ' Q ' if self.side == Side.white else ' q '

    @classmethod
    def get_piece_type(cls):
        return PieceType.queen


    @classmethod
    def get_possible_moves(cls, game, rank_idx, file_idx):
        game_state = game.game_state

        result = []

        movement_directions = [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (1, -1), (-1, -1), (-1, 1)]
        for direction in movement_directions:
            new_rank_idx = rank_idx + direction[0]
            new_file_idx = file_idx + direction[1]

            while True:
                if not game_state.is_board_position_valid(new_rank_idx, new_file_idx):
                    break

                piece = game_state.grid[new_rank_idx][new_file_idx]
                if piece:
                    if piece.side == game_state.side_to_move:
                        break

                new_state = copy.deepcopy(game_state)
                new_state.grid[new_rank_idx][new_file_idx] = new_state.grid[rank_idx][file_idx]
                new_state.grid[rank_idx][file_idx] = None
                new_state.side_to_move = game_state.side_to_move.other
                if new_state.is_valid():
                    move = Move(cls.get_piece_type(), (rank_idx, file_idx), (new_rank_idx, new_file_idx))
                    result.append((new_state, move))

                if piece:
                    break

                new_rank_idx += direction[0]
                new_file_idx += direction[1]

        return result

    @classmethod
    def is_attacking_square(cls, side, game_state, self_rank_idx, self_file_idx, square_rank_idx, square_file_idx):
        return Bishop.is_attacking_square(side, game_state, self_rank_idx, self_file_idx, square_rank_idx, square_file_idx)\
               or Rook.is_attacking_square(side, game_state, self_rank_idx, self_file_idx, square_rank_idx, square_file_idx)

class King(Piece):
    def __init__(self, side):
        super().__init__(side)

    def __str__(self):
        return ' K ' if self.side == Side.white else ' k '

    @classmethod
    def get_piece_type(cls):
        return PieceType.king

    @classmethod
    def __is_king_moved__(cls, game_state):
        if game_state.side_to_move == Side.white:
            return game_state.white_king_moved
        else:
            return game_state.black_king_moved

    @classmethod
    def __is_queens_rook_available_for_castling__(cls, game_state):
        if game_state.side_to_move == Side.white:
            if game_state.a1_rook_moved:
                return True
            piece = game_state.grid[0][0]
            if piece and piece.side == Side.white:
                assert (piece.get_piece_type() == PieceType.rook)
                return False
            else:
                # rook captured
                return True
        else:
            if game_state.a8_rook_moved:
                return True
            piece = game_state.grid[7][0]
            if piece and piece.side == Side.black:
                assert (piece.get_piece_type() == PieceType.rook)
                return False
            else:
                # rook captured
                return True

    @classmethod
    def __is_kings_rook_available_for_castling__(cls, game_state):
        if game_state.side_to_move == Side.white:
            if game_state.h1_rook_moved:
                return True
            piece = game_state.grid[0][7]
            if piece and piece.side == Side.white:
                assert (piece.get_piece_type() == PieceType.rook)
                return False
            else:
                # rook captured
                return True
        else:
            if game_state.h8_rook_moved:
                return True
            piece = game_state.grid[7][7]
            if piece and piece.side == Side.black:
                assert (piece.get_piece_type() == PieceType.rook)
                return False
            else:
                # rook captured
                return True

    @classmethod
    def __get_castling_moves__(cls, game_state):
        result = []

        rank_idx = 0 if game_state.side_to_move == Side.white else 7
        file_idx = 4

        if not cls.__is_king_moved__(game_state):
            # queen side castling
            if not cls.__is_queens_rook_available_for_castling__(game_state):

                assert (game_state.grid[rank_idx][4].get_piece_type() == PieceType.king)
                assert (game_state.grid[rank_idx][0].get_piece_type() == PieceType.rook)

                squares_between_king_and_rook_are_empty = True

                for file in range(1, 4):
                    if game_state.grid[rank_idx][file]:
                        squares_between_king_and_rook_are_empty = False
                        break

                if squares_between_king_and_rook_are_empty:
                    king_or_squares_are_in_check = False
                    for file in range(1, 5):
                        if game_state.is_square_under_attack(Side.black, rank_idx, file):
                            king_or_squares_are_in_check = True
                            break

                    if not king_or_squares_are_in_check:
                        new_state = copy.deepcopy(game_state)
                        new_state.grid[rank_idx][2] = new_state.grid[rank_idx][4]  # move king
                        new_state.grid[rank_idx][4] = None
                        new_state.grid[rank_idx][3] = new_state.grid[rank_idx][0]  # move rook
                        new_state.grid[rank_idx][0] = None

                        new_state.white_king_moved = True
                        new_state.a1_rook_moved = True

                        move = Move(cls.get_piece_type(), (rank_idx, 4), (rank_idx, 2))
                        result.append((new_state, move))

            # king side castling
            if not cls.__is_kings_rook_available_for_castling__(game_state):

                assert (game_state.grid[rank_idx][4].get_piece_type() == PieceType.king)
                assert (game_state.grid[rank_idx][7].get_piece_type() == PieceType.rook)

                squares_between_king_and_rook_are_empty = True

                for file in range(5, 8):
                    if game_state.grid[rank_idx][file]:
                        squares_between_king_and_rook_are_empty = False
                        break

                if squares_between_king_and_rook_are_empty:
                    king_or_squares_are_in_check = False
                    for file in range(4, 8):
                        if game_state.is_square_under_attack(Side.black, rank_idx, file):
                            king_or_squares_are_in_check = True
                            break

                    if not king_or_squares_are_in_check:
                        new_state = copy.deepcopy(game_state)
                        new_state.grid[rank_idx][6] = new_state.grid[rank_idx][4]  # move king
                        new_state.grid[rank_idx][4] = None
                        new_state.grid[rank_idx][7] = new_state.grid[rank_idx][5]  # move rook
                        new_state.grid[rank_idx][7] = None

                        new_state.white_king_moved = True
                        new_state.h1_rook_moved = True

                        move = Move(cls.get_piece_type(), (rank_idx, 4), (rank_idx, 6))
                        result.append((new_state, move))
        return result

    @classmethod
    def get_possible_moves(cls, game, rank_idx, file_idx):
        game_state = game.game_state
        side = game_state.side_to_move
        result = []
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for i, j in directions:
            new_rank_idx = rank_idx + i
            new_file_idx = file_idx + j
            if game_state.is_board_position_valid(new_rank_idx, new_file_idx):
                piece = game_state.grid[new_rank_idx][new_file_idx]
                if piece and side == piece.side:
                    continue
                new_state = copy.deepcopy(game_state)
                new_state.grid[new_rank_idx][new_file_idx] = new_state.grid[rank_idx][file_idx]
                new_state.grid[rank_idx][file_idx] = None
                new_state.side_to_move = side.other
                if side == Side.white:
                    new_state.white_king_moved = True
                else:
                    new_state.black_king_moved = True

                if new_state.is_valid():
                    move = Move(cls.get_piece_type(), (rank_idx, file_idx), (new_rank_idx, new_file_idx))
                    result.append((new_state, move))

        # castling
        result += cls.__get_castling_moves__(game_state)
        return result

    @classmethod
    def is_attacking_square(cls, side, game_state, self_rank_idx, self_file_idx, square_rank_idx, square_file_idx):
        return abs(self_rank_idx - square_rank_idx) <= 1 and abs(self_file_idx - square_file_idx) <= 1


board = Board()
board.play_game()
