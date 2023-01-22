# Free for personal or classroom use; see 'LICENSE.md' for details.
# https://github.com/squillero/computational-intelligence

import numpy as np
from abc import abstractmethod
import copy


class Player(object):

    def __init__(self, quarto) -> None:
        self.__quarto = quarto

    @abstractmethod
    def choose_piece(self) -> int:
        pass

    @abstractmethod
    def place_piece(self) -> tuple[int, int]:
        pass

    def get_game(self):
        return self.__quarto


class Piece(object):

    def __init__(self, high: bool, coloured: bool, solid: bool, square: bool) -> None:
        self.HIGH = high
        self.COLOURED = coloured
        self.SOLID = solid
        self.SQUARE = square
        self.binary = [int(high), int(coloured), int(solid), int(square)]


class Quarto(object):

    MAX_PLAYERS = 2
    BOARD_SIDE = 4

    def __init__(self) -> None:
        self.__players = ()
        self.reset()

    def reset(self):
        self._board = np.ones(
            shape=(self.BOARD_SIDE, self.BOARD_SIDE), dtype=int) * -1
        self.__binary_board = np.full(
            shape=(self.BOARD_SIDE, self.BOARD_SIDE, 4), fill_value=np.nan)
        self.__pieces = []
        self.__pieces.append(Piece(False, False, False, False))  # 0
        self.__pieces.append(Piece(False, False, False, True))  # 1
        self.__pieces.append(Piece(False, False, True, False))  # 2
        self.__pieces.append(Piece(False, False, True, True))  # 3
        self.__pieces.append(Piece(False, True, False, False))  # 4
        self.__pieces.append(Piece(False, True, False, True))  # 5
        self.__pieces.append(Piece(False, True, True, False))  # 6
        self.__pieces.append(Piece(False, True, True, True))  # 7
        self.__pieces.append(Piece(True, False, False, False))  # 8
        self.__pieces.append(Piece(True, False, False, True))  # 9
        self.__pieces.append(Piece(True, False, True, False))  # 10
        self.__pieces.append(Piece(True, False, True, True))  # 11
        self.__pieces.append(Piece(True, True, False, False))  # 12
        self.__pieces.append(Piece(True, True, False, True))  # 13
        self.__pieces.append(Piece(True, True, True, False))  # 14
        self.__pieces.append(Piece(True, True, True, True))  # 15
        self._current_player = 0
        self.__selected_piece_index = -1

    def set_players(self, players: tuple[Player, Player]):
        self.__players = players

    def get_current_player(self) -> int:
        '''
        Gets the current player
        '''
        return self._current_player

    def select(self, pieceIndex: int) -> bool:
        '''
        select a piece. Returns True on success
        '''
        if pieceIndex not in self._board:
            self.__selected_piece_index = pieceIndex
            return True
        return False

    def place(self, x: int, y: int) -> bool:
        '''
        Place piece in coordinates (x, y). Returns true on success
        '''
        if self.__placeable(x, y):
            self._board[y, x] = self.__selected_piece_index
            self.__binary_board[y,
                                x][:] = self.__pieces[self.__selected_piece_index].binary
            return True
        return False

    def __placeable(self, x: int, y: int) -> bool:
        return not (y < 0 or x < 0 or x > 3 or y > 3 or self._board[y, x] >= 0)

    def print(self):
        '''
        Print the board
        '''
        for row in self._board:
            print("\n -------------------")
            print("|", end="")
            for element in row:
                print(f" {element: >2}", end=" |")
        print("\n -------------------\n")
        print(f"Selected piece: {self.__selected_piece_index}\n")

    def get_piece_charachteristics(self, index: int) -> Piece:
        '''
        Gets charachteristics of a piece (index-based)
        '''
        return copy.deepcopy(self.__pieces[index])

    def get_board_status(self) -> np.ndarray:
        '''
        Get the current board status (pieces are represented by index)
        '''
        return copy.deepcopy(self._board)

    def get_selected_piece(self) -> int:
        '''
        Get index of selected piece
        '''
        return copy.deepcopy(self.__selected_piece_index)

    def __check_horizontal(self) -> int:
        hsum = np.sum(self.__binary_board, axis=1)

        if self.BOARD_SIDE in hsum or 0 in hsum:
            return self._current_player
        else:
            return -1

    def __check_vertical(self):
        vsum = np.sum(self.__binary_board, axis=0)

        if self.BOARD_SIDE in vsum or 0 in vsum:
            return self._current_player
        else:
            return -1

    def __check_diagonal(self):
        dsum1 = np.trace(self.__binary_board, axis1=0, axis2=1)
        dsum2 = np.trace(np.fliplr(self.__binary_board), axis1=0, axis2=1)

        if self.BOARD_SIDE in dsum1 or self.BOARD_SIDE in dsum2 or 0 in dsum1 or 0 in dsum2:
            return self._current_player
        else:
            return -1

    def check_winner(self) -> int:
        '''
        Check who is the winner
        '''
        l = [self.__check_horizontal(), self.__check_vertical(),
             self.__check_diagonal()]
        for elem in l:
            if elem >= 0:
                return elem
        return -1

    def check_finished(self) -> bool:
        '''
        Check who is the loser
        '''
        for row in self._board:
            for elem in row:
                if elem == -1:
                    return False
        return True

    def run(self) -> int:
        '''
        Run the game (with output for every move)
        '''
        winner = -1
        while winner < 0 and not self.check_finished():
            #self.print()
            piece_ok = False
            while not piece_ok:
                piece_ok = self.select(
                    self.__players[self._current_player].choose_piece())
            piece_ok = False
            self._current_player = (
                self._current_player + 1) % self.MAX_PLAYERS
            #self.print()
            while not piece_ok:
                x, y = self.__players[self._current_player].place_piece()
                piece_ok = self.place(x, y)
            winner = self.check_winner()
        #self.print()
        return winner