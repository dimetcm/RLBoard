import enum
import copy

from collections import namedtuple

class Player(enum.Enum):
    black = 1
    white = 2

    @property
    def other(self):
        return Player.black if self == Player.white else Player.white


class Point(namedtuple('Point', 'row col')):
    def neighbors(self):
        return [
            Point(self.row - 1, self.col),
            Point(self.row + 1, self.col),
            Point(self.row, self.col - 1),
            Point(self.row, self.col + 1),
        ]

    def __deepcopy__(self, memodict={}):
        # These are very immutable.
        return self

class Move():
    """Any action a player can play on a turn.

    Exactly one of is_play, is_pass, is_resign will be set.
    """
    def __init__(self, point=None, is_pass=False, is_resign=False):
        assert (point is not None) ^ is_pass ^ is_resign
        self.point = point
        self.is_play = (self.point is not None)
        self.is_pass = is_pass
        self.is_resign = is_resign

    @classmethod
    def play(cls, point):
        """A move that places a stone on the board."""
        return Move(point=point)

    @classmethod
    def pass_turn(cls):
        return Move(is_pass=True)

    @classmethod
    def resign(cls):
        return Move(is_resign=True)

    def __str__(self):
        if self.is_pass:
            return 'pass'
        if self.is_resign:
            return 'resign'
        return '(r %d, c %d)' % (self.point.row, self.point.col)

    def __hash__(self):
        return hash((self.is_play, self.is_pass, self.is_resign, self.point))

    def __eq__(self, other):
        return (self.is_play, self.is_pass, self.is_resign, self.point) ==\
               (other.is_play, other.is_pass, other.is_resign, other.point)

class GoString:
    def __init__(self, color, stones, liberties):
        self.color = color
        self.stones = frozenset(stones)
        self.liberties = frozenset(liberties)

    def without_liberty(self, point):
        new_liberties = self.liberties - set([point])
        return GoString(self.color, self.stones, new_liberties)

    def with_liberty(self, point):
        new_liberties = self.liberties | set([point])
        return GoString(self.color, self.stones, new_liberties)

    def merged_with(self, string):
        """Return a new string containing all stones in both strings."""
        assert string.color == self.color
        combined_stones = self.stones | string.stones
        return GoString(
            self.color,
            combined_stones,
            (self.liberties | string.liberties) - combined_stones)

    @property
    def num_liberties(self):
        return len(self.liberties)

    def __eq__(self, other):
        return isinstance(other, GoString) and \
            self.color == other.color and \
            self.stones == other.stones and \
            self.liberties == other.liberties

    def __deepcopy__(self, memodict={}):
        return GoString(self.color, self.stones, copy.deepcopy(self.liberties))