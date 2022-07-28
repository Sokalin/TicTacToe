from random import choice, shuffle
from time import sleep
from colorama import Fore


class Player:
    '''
    Used in TicTacToe class with method create_player
    '''
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
        return Fore.RESET + f'{self.name + " " if self.name != "" else ""}[{self.symbol}] '


class Cell:
    '''
    Cell's objects used in game field in TicTacToe class.
    '''
    def __init__(self):
        self.value = 0

    def __bool__(self):
        return not self.value


class TicTacToe:
    '''
    Main class for control the game.
    '''
    def __init__(self, rows=3, cols=3, win_am=3):
        if win_am > max(rows, cols):
            raise ValueError
        self.__rows = rows
        self.__cols = cols
        self.__win_am = win_am
        self.__symbols = {0: ' '}
        self.__players = []
        self.__new_field()

    def __new_field(self):
        '''
        Used for update some attributes when start new game (if called method play).
        '''
        self.__field = [[Cell() for c in range(self.__cols)] for r in range(self.__rows)]
        self.__win_list = self.__win_combs()

    def __setitem__(self, key, value):
        self.__check_ind(key)
        r, c = key
        if self.__field[r][c]:
            self.__field[r][c].value = value

    def __getitem__(self, item):
        self.__check_ind(item)
        r, c = item
        return self.__field[r][c].value

    def __bool__(self):
        '''
        If game continue (exist free Cells and nobody won) it returns True, else - returns False.
        Used in method play.
        '''
        if hasattr(self, '_win_plr'):
            delattr(self, '_win_plr')
        for plr in self.__players:
            if self.__is_player_win(plr):
                self._win_plr = plr
                return False
        return bool(self.__free_cells_indexes())

    def __check_ind(self, ind):
        '''
        Checks the indexes which player (human) add. If indexes are uncorrectable it raise IndexError.
        Used in set/get item methods.
        '''
        IE = IndexError('Uncorrectable indexes')
        if not isinstance(ind, tuple) or len(ind) != 2:
            raise IE
        r, c = ind
        if not (type(r) == type(c) == int) or min(r, c) < 0:
            raise IE
        if r >= self.__rows or c >= self.__cols:
            raise IE

    def __free_cells_indexes(self) -> list:
        '''
        :returns list[tuple]
        Any tuple in list consisted of field indexes, where nothing value in cell.

        Used for check indexes in player move or choice random indexes in computer move.
        '''
        res = []
        for r in range(self.__rows):
            for c in range(self.__cols):
                if self.__field[r][c]:
                    res.append((r, c))
        return res

    def __win_combs(self) -> list:
        '''
        :returns two-dimensional list.
        Any list in returned list consisted of Cells (Cell class objects),
        witch create combination, that player can be made for win.

        Used in _is_win(...) for check if some player won after move.
        '''
        res = []
        # -------- rows --------
        for r in self.__field:
            i = 0
            while i + self.__win_am <= len(r):
                res.append(r[i:i + self.__win_am])
                i += 1
        # -------- cols --------
        for c in range(self.__cols):
            for r in range(self.__rows):
                if r + self.__win_am > self.__rows:
                    break
                col = []
                for i in range(self.__win_am):
                    col.append(self.__field[r + i][c])
                res.append(col)
        # ------ diagonals ------
        # from right to left
        for row in range(self.__rows):
            if len(self.__field[row:]) < self.__win_am:
                break
            for c in range(self.__cols):
                if len(self.__field[0][c:]) < self.__win_am:
                    break
                dia = []
                x = c
                for n, r in enumerate(range(row, self.__rows)):
                    if n >= self.__win_am:
                        break
                    dia.append(self.__field[r][x])
                    x += 1
                res.append(dia)
        # from left to right
        for row in range(self.__rows):
            if len(self.__field[row:]) < self.__win_am:
                break
            for c in range(self.__cols - 1, -1, -1):
                if len(self.__field[0][:c + 1]) < self.__win_am:
                    break
                dia = []
                x = c
                for n, r in enumerate(range(row, self.__cols)):
                    if n >= self.__win_am:
                        break
                    dia.append(self.__field[r][x])
                    x -= 1
                res.append(dia)

        return res

    def __is_player_win(self, player: Player):
        '''
        :returns: if player made win combination returns True, else - False.
        Used in bool.
        '''
        for comb in self.__win_list:
            for cell in comb:
                if cell.value != player.id:
                    break
            else:
                return True
        return False

    def __player_go(self, player):
        '''
        Provide player move. If player is human asks indexes else choice it from free indexes.
        '''
        if player.type == 'c':
            print(str(player), end='')
            ind = choice(self.__free_cells_indexes())
            self[ind] = player.id
            sleep(0.7)
            print(*ind)
        elif player.type == 'h':
            ind = tuple(map(int, input(str(player)).split()))
            if ind in self.__free_cells_indexes():
                self.__check_ind(ind)
                self[ind] = player.id
            else:
                print('This cell is already used. Try again:')
                self.__player_go(player)

    def __str__(self):
        '''
        :returns: game field in view:
        [ ] [ ] [ ] ... [ ]
        [ ] [ ] [ ] ... [ ]
        ...................
        [ ] [ ] [ ] ... [ ]
        '''
        pole = ''
        for r in self.__field:
            for c in r:
                colors = [Fore.LIGHTWHITE_EX, Fore.RED, Fore.GREEN,
                          Fore.YELLOW, Fore.BLUE, Fore.CYAN, Fore.MAGENTA,
                          Fore.LIGHTBLACK_EX, Fore.LIGHTGREEN_EX]

                color = colors[c.value]
                pole += color + f'[{self.__symbols[c.value]}] '
            pole += f'\n'
        return pole

    def change_size(self, rows=3, cols=3, win_am=3):
        '''
        Provide size change.
        It can be called when you call more than one method play.

        For example:
        ...
        play()
        change_size(...)
        play()
        play()
        ...
        '''
        self.__rows = rows
        self.__cols = cols
        self.__win_am = win_am

    def create_player(self, symbol, plr_type, name=''):
        '''
        Creates new player with class Player.
        :param symbol: must be unique char.
        :param plr_type: 'h' - human, 'c' - computer (random moves)
        :param name: any string
        '''
        if symbol in self.__symbols.values():
            raise ValueError('Every player must had unique symbol')
        if plr_type not in ('c', 'h'):
            raise ValueError('Type must be "c" - computer or "h" - human')
        player = Player(symbol, plr_type, name)
        self.__symbols[player.id] = player.symbol
        self.__players.append(player)

    def play(self, *args):
        '''
        Used for run new game in console.
        :param args: you could enter some strings with chars of created players for begin game with there.
        If not args game will start with all created players.
        '''
        if args:
            players = []
            for x in args:
                if x not in self.__symbols.values():
                    raise ValueError('"play()" can take only players tags or no args')
                else:
                    is_app = False
                    for plr in self.__players:
                        if plr.symbol == x:
                            players.append(plr)
                            is_app = True
                            break
                    if not is_app:
                        raise ValueError(f'Player with {x} not created')
        else:
            if not self.__players:
                raise RuntimeError('You must firstly create one or more players')
            players = self.__players[:]
        self.__new_field()
        shuffle(players)
        print(self)
        for plr in players * (self.__rows * self.__cols):
            self.__player_go(plr)
            print(self)
            if not self:
                print(Fore.RESET + f'{self._win_plr}is won') if hasattr(self, '_win_plr') else print(Fore.RESET + 'Draw')
                break


# example of use:
# game = TicTacToe(5, 6, 4)
# game.create_player('!', 'h', 'Fox')
# game.create_player('+', 'c', 'XD')
# game.create_player('*', 'c')
# game.play()
# game.change_size(3, 4, 3)
# game.play('!', '+')

