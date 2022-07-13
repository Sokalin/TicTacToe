from random import choice, shuffle
from time import sleep
from colorama import Fore


class Player:
    __id = 0

    def __new__(cls, *args, **kwargs):
        cls.__id += 1
        return super().__new__(cls)

    def __init__(self, symbol, plr_type='h', name=''):
        if type(symbol) != str or len(symbol) != 1:
            raise ValueError('Uncorrectable symbol')
        self.name = name
        self.symbol = symbol
        self.type = plr_type
        self.id = self.__id

    def __str__(self):
        return f'{self.name + " " if self.name != "" else ""}[{self.symbol}] '


class Cell:
    def __init__(self):
        self.value = 0

    def __bool__(self):
        return not self.value


class TicTacToe:
    def __init__(self, rows=3, cols=3, win_am=3):
        if win_am > max(rows, cols):
            raise ValueError
        self.__rows = rows
        self.__cols = cols
        self.__win_am = win_am
        self.__symbols = {0: ' '}
        self.__players = []
        self.__new_pole()

    def __new_pole(self):
        self.__pole = [[Cell() for c in range(self.__cols)] for r in range(self.__rows)]
        self.__win_list = self.__win_combs()

    def __setitem__(self, key, value):
        self.__check_ind(key)
        r, c = key
        if self.__pole[r][c]:
            self.__pole[r][c].value = value

    def __getitem__(self, item):
        self.__check_ind(item)
        r, c = item
        return self.__pole[r][c].value

    def __bool__(self):
        if hasattr(self, '_win_plr'):
            delattr(self, '_win_plr')
        for plr in self.__players:
            if self.__is_player_win(plr):
                self._win_plr = plr
                return False
        return bool(self.__free_cells_indexes())

    def __check_ind(self, ind):
        IE = IndexError('Uncorrectable indexes')
        if not isinstance(ind, tuple) or len(ind) != 2:
            raise IE
        r, c = ind
        if not (type(r) == type(c) == int) or min(r, c) < 0:
            raise IE
        if r >= self.__rows or c >= self.__cols:
            raise IE

    def __free_cells_indexes(self) -> list:
        res = []
        for r in range(self.__rows):
            for c in range(self.__cols):
                if self.__pole[r][c]:
                    res.append((r, c))
        return res

    def __win_combs(self) -> list:
        # ==============================================================================================================
        # TODO: rewrite function
        def un():
            res = []
            for r in self.__pole:
                i = 0
                while i + self.__win_am <= len(r):
                    res.append(r[i:i + self.__win_am])
                    i += 1
            for c in range(self.__cols):
                for r in range(self.__rows):
                    if r + self.__win_am > self.__rows:
                        break
                    col = []
                    for i in range(self.__win_am):
                        col.append(self.__pole[r + i][c])
                    res.append(col)

            return res

        # ----------------------------------------------

        def three():
            res = self.__pole[:]
            for c in range(self.__cols):
                col = []
                for r in self.__pole:
                    col.append(r[c])
                res.append(col)
            res.append([self.__pole[i][i] for i in range(self.__rows)])
            res.append([self.__pole[i][-1 - i] for i in range(self.__rows)])
            return res

        # ----------------------------------------------
        if self.__cols == self.__rows == self.__win_am == 3:
            return three()
        else:
            return un()
        # ==============================================================================================================

    def __is_player_win(self, player: Player):
        for comb in self.__win_list:
            for cell in comb:
                if cell.value != player.id:
                    break
            else:
                return True
        return False

    def __player_go(self, player):
        if player.type == 'c':
            print(str(player), end='')
            ind = choice(self.__free_cells_indexes())
            self[ind] = player.id
            # sleep(0.7)
            print(*ind)
        elif player.type == 'h':
            ind = tuple(map(int, input(str(player)).split()))
            self.__check_ind(ind)
            if ind in self.__free_cells_indexes():
                self[ind] = player.id
            else:
                print('This cell is already used. Try again:')
                self.__player_go(player)

    def __str__(self):
        pole = ''
        for r in self.__pole:
            for c in r:

                colors = [Fore.LIGHTWHITE_EX, Fore.RED, Fore.GREEN,
                          Fore.YELLOW, Fore.BLUE, Fore.CYAN, Fore.MAGENTA,
                          Fore.LIGHTBLACK_EX, Fore.LIGHTGREEN_EX]

                color = colors[c.value]
                pole += color + f'[{self.__symbols[c.value]}] '
            pole += f'\n'
        return pole

    def change_size(self, rows=3, cols=3, win_am=3):
        self.__rows = rows
        self.__cols = cols
        self.__win_am = win_am

    def create_player(self, symbol, plr_type, name=''):
        if symbol in self.__symbols.values():
            raise ValueError('Every player must had unique symbol')
        if plr_type not in ('c', 'h'):
            raise ValueError('Type must be "c" - computer or "h" - human')
        player = Player(symbol, plr_type, name)
        self.__symbols[player.id] = player.symbol
        self.__players.append(player)

    def play(self, *args):
        if args:
            players = []
            for x in args:
                if x not in self.__symbols.values():
                    raise ValueError('"play()" can take only players tags or no args')
                else:
                    isapp = False
                    for plr in self.__players:
                        if plr.symbol == x:
                            players.append(plr)
                            isapp = True
                            break
                    if not isapp:
                        raise ValueError(f'Player with {x} not created')
        else:
            if not self.__players:
                raise RuntimeError('You must firstly create one or more players')
            players = self.__players[:]
        self.__new_pole()
        shuffle(players)
        print(self)
        for plr in players * (self.__rows * self.__cols):
            self.__player_go(plr)
            print(self)
            if not self:
                print(f'{self._win_plr}is won') if hasattr(self, '_win_plr') else print('Draw')
                break


game = TicTacToe()
game.create_player('!', 'h', 'Fox')
game.create_player('+', 'c', 'XD')
# game.create_player('~', 'c')
# game.create_player('X', 'c')
# game.create_player('O', 'c')
# game.create_player('#', 'c')
# game.create_player('|', 'c')
# game.create_player('*', 'c')
game.play()
