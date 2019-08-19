from random import randint
import curses
from pprint import pprint

# ==================== Board =================== #
class Board:
    def __init__(self,row_data=None,col_data=None,screen=None):
        self.size = 5
        self.tiles = []
        for r in range(self.size):
            self.tiles.append([])
            for c in range(self.size):
                self.tiles[r].append(Tile(self,[0,1,2,3],r,c))
        self.screen = screen
        self.h = 5
        self.w = 10
        if row_data is None and col_data is None:
            self.input_data()
        else:
            self.row_data = row_data
            self.col_data = col_data



    def __str__(self):
        string = '-'*14*5 + '\n'
        for r,row in enumerate(self.tiles):
            for cell in row:
                string += '{:^14}'.format(str(cell))
            string += (' |  {}\n'.format(self.row_data[r]))
        string += '-'*14*5 + '\n'
        string += '{:^14}{:^14}{:^14}{:^14}{:^14}\n'.format(*[str(data) for data in self.col_data])
        return(string)


    def row(self,r):
        tiles = self.tiles[r]
        return(Pane(tiles,self.row_data[r]))


    def col(self,c):
        tiles = [self.tiles[r][c] for r in range(self.size)]
        return(Pane(tiles,self.col_data[c]))


    def panes(self):
        panes = []
        for r in range(self.size):
            panes.append(self.row(r))
        for c in range(self.size):
            panes.append(self.col(c))
        return(panes)


    def tile(self,r,c):
        return(self.tiles[r][c])


    def reveal_safe(self):
        for r in range(self.size):
            for c in range(self.size):
                tile = self.tile(r,c)
                if not tile.is_shown() and tile.volt_prob() == 0:
                    self.tile(r,c).prompt(screen=self.screen)
                    return(1)
        return(0)


    def guess(self):
        # risk calculation
        risk_bins = {}
        for r in range(self.size):
            for c in range(self.size):
                tile = self.tile(r,c)
                if not tile.is_shown():
                    tile.risk = round(self.row(r).volt_prob() * self.col(c).volt_prob(),5)
                    if not tile.is_garbage():
                        risk_bins.setdefault(tile.risk, []).append(tile)  # safeley appends [r,c] in a bin

        # risk printing
        if self.screen is None:
            pprint(risk_bins)
        else:
            try:
                self.screen.addstr(self.size*(self.h+1)-1,1,'Guess')
                y = 0
                for i,bin in enumerate(sorted(risk_bins.keys())):
                    for j,tile in enumerate(risk_bins[bin]):
                        r,c = tile.r,tile.c
                        self.screen.addstr(self.size*(self.h+1)+y,1,'{},{}\t{}'.format(r,c,bin))
                        y += 1
                    y += 1
            except:  # continues until reaches end of screen
                pass

        # prompting user for value of tile
        lowest_risk = risk_bins[min(risk_bins.keys())]
        safest_tile = sorted(lowest_risk,key=lambda tile: tile.max())[0]  # tiebreak by max possible tile value
        safest_tile.prompt(self.screen)

        # clean up screen
        self.screen.clear()


    def deduce(self):
        for pane in self.panes():
            if pane.hidden.volts == 0:
                if pane.hidden.coin_v == pane.hidden.coin_c:
                    pane.update({1})
                elif pane.hidden.coin_v == pane.hidden.coin_c + 1:
                    pane.update({1,2})
                elif pane.hidden.coin_v >= pane.hidden.coin_c + 2:
                    pane.update({1,2,3})
            elif pane.hidden.count == 1:
                pane.hidden.tiles[0].update([pane.hidden.coin_v])
            else:
                if pane.hidden.coin_v == pane.hidden.coin_c:
                    pane.update({0,1})
                elif pane.hidden.coin_v == pane.hidden.coin_c + 1:
                    pane.update({0,1,2})
                elif pane.hidden.coin_v >= pane.hidden.coin_c + 2:
                    pane.update({0,1,2,3})
            # TODO: sum of max values in pane < coin_v


    def render_all(self):
        h = self.h
        w = self.w

        # renders tiles
        for r in range(self.size):
            for c in range(self.size):
                self.tile(r,c).render(self.screen)

        # renders row data
        for r in range(self.size):
            try:
                coins = str(self.row_data[r][0])
                volts = str(self.row_data[r][1])
            except:
                coins, volts = '?','?'
            self.screen.addstr(r*h+1,(w+1)*self.size,coins)
            self.screen.addstr(r*h+3,(w+1)*self.size,volts)

        # renders column data
        for c in range(self.size):
            try:
                coins = str(self.col_data[c][0])
                volts = str(self.col_data[c][1])
            except:
                coins, volts = '?','?'
            self.screen.addstr(self.size*h,c*(w+1)+2,coins)
            self.screen.addstr(self.size*h,c*(w+1)+7,volts)


    def solve(self):
        # loop to solve the board, prompts user for reveals and guesses
        while True:
            self.deduce()
            self.render_all()
            if not self.reveal_safe():
                try:
                    self.guess()
                except ValueError:
                    return()


    def input_data(self):
        self.row_data, self.col_data = [],[]

        # pane data takes input from console
        if self.screen is None:
            for r in range(self.size):
                coins = input('Input the number of coins in row {}'.format(r))
                volts = input('Input the number of voltorbs in row {}'.format(r))
                self.row_data[r] = [coins,volts]
            for c in range(self.size):
                coins = input('Input the number of coins in column {}'.format(c))
                volts = input('Input the number of voltorbs in column {}'.format(c))
                self.col_data[c] = [coins,volts]

        # takes pane data takes input from TUI
        else:
            h = self.h
            w = self.w
            self.render_all()

            # row data
            for r in range(self.size):
                y = r*h+1
                x = (w+1)*self.size

                coins = chr(self.screen.getch(y,x))
                if coins == '`':  # if ` proceeds input, accepts a two-digit number
                    coins = chr(self.screen.getch(y,x)) + chr(self.screen.getch(y,x))
                self.screen.addstr(y,x,coins)

                volts = chr(self.screen.getch(y+2,x))
                self.screen.addstr(y+2,x,volts)

                self.row_data.append([int(coins),int(volts)])

            # column data
            for c in range(self.size):
                y = self.size*h
                x = c*(w+1)+2

                coins = chr(self.screen.getch(y,x))
                if coins == '`':  # if ` proceeds input, accepts a two-digit number
                    coins = chr(self.screen.getch(y,x)) + chr(self.screen.getch(y,x))
                self.screen.addstr(y,x,coins)

                volts = chr(self.screen.getch(y,x+5))
                self.screen.addstr(y,x+5,volts)

                self.col_data.append([int(coins),int(volts)])


# ==================== Tile =================== #
class Tile(Board):
    def __init__(self,b,memo,r,c):
        self.memo = set(memo)
        self.r = r
        self.c = c
        self.b = b


    def __str__(self):
        return(str(self.memo))


    def is_shown(self):
        if len(self.memo) == 1:
            return(True)
        else:
            return(False)


    def is_garbage(self):
        if self.memo == {0,1}:
            return(True)
        else:
            return(False)


    def coin_v(self):
        if self.is_shown():
            return(int(list(self.memo)[0]))
        else:
            return(0)


    def volt(self):
        if self.memo == {0}:
            return(1)
        else:
            return(0)


    def volt_prob(self):
        if 0 in self.memo:
            return(1) # temp func, will be improved with maff
        else:
            return(0)


    def update(self,val):
        if not self.is_shown():
            self.memo = self.memo & set(val)


    def set(self,val):
        self.memo = set(val)


    def render(self,screen):
        h = self.b.h
        w = self.b.w
        r = self.r*h
        c = self.c*(w+1)
        screen.addstr(r,c,'┌'+'─'*(w-2)+'┐')
        for i in range(1,h-1):
            screen.addstr(r+i,c,'│')
            screen.addstr(r+i,c+w-1,'│')
        screen.addstr(r+h-1,c,'└'+'─'*(w-2)+'┘')
        screen.addstr(r+1,c+2,'0' if 0 in self.memo else ' ')
        screen.addstr(r+1,c+w-3,'1' if 1 in self.memo else ' ')
        screen.addstr(r+h-2,c+2,'2' if 2 in self.memo else ' ')
        screen.addstr(r+h-2,c+w-3,'3' if 3 in self.memo else ' ')


    def prompt(self,screen):
        if screen is None:
            user_input = input('Input contents of tile at ({},{}): '.format(self.r,self.c))
            try:
                if int(user_input) in list(self.memo):
                    self.memo = set([int(user_input)])
                else:
                    raise
            except:
                print('Invalid input, tile contents must be one of the following integers: {}'.format(self.memo))
                self.reveal()
        else:
            h = self.b.h
            w = self.b.w
            r = self.r*h
            c = self.c*(w+1)
            screen.addstr(r,c,'┌'+'─'*(w-2)+'┐',curses.A_REVERSE)
            for i in range(1,h-1):
                screen.addstr(r+i,c,'│',curses.A_REVERSE)
                screen.addstr(r+i,c+w-1,'│',curses.A_REVERSE)
            screen.addstr(r+h-1,c,'└'+'─'*(w-2)+'┘',curses.A_REVERSE)

            key = screen.getch(r,c)

            self.render(screen)

            # # if key == curses.KEY_UP:
            # #     return(self.r-1,self.c)
            # # elif key == curses.KEY_DOWN:
            # #     return((self.r+1) % self.b.size,self.c)
            # # elif key == curses.KEY_LEFT:
            # #     return(self.r,self.c-1)
            # # elif key == curses.KEY_RIGHT:
            # #     return(self.r,(self.c+1) % self.b.size)
            # else:
            self.set([int(chr(key))])
            self.render(screen)
            return([self.r,self.c])


    def max(self):
        return(max(self.memo))



# ==================== Pane =================== #
class Pane:
    def __init__(self,tiles,data):
        self.data = data

        hidden_tiles = [tile for tile in tiles if not tile.is_shown()]
        shown_tiles = [tile for tile in tiles if tile.is_shown()]
        total_coins = data[0]
        total_volts = data[1]
        self.total = PaneProp(tiles,total_coins,total_volts)
        shown_coin_v = sum([tile.coin_v() for tile in self.total.tiles])
        shown_volts = sum([tile.volt() for tile in self.total.tiles])
        hidden_coins = total_coins - shown_coin_v
        hidden_volts = total_volts - shown_volts
        self.shown = PaneProp(shown_tiles,shown_coin_v,shown_volts)
        self.hidden = PaneProp(hidden_tiles,hidden_coins,hidden_volts)


    def __str__(self):
        return(str([tile for tile in self.tiles]))


    def tile(self,i):
        return(self.tiles[i])


    def update(self,val):
        for tile in self.total.tiles:
            tile.update(val)


    def volt_prob(self):
        if self.hidden.count == 0:
            return(0)
        else:
            return(self.hidden.volts/self.hidden.count)



# =============== Pane Properties ============== #
class PaneProp:
    def __init__(self,tiles,coins,volts):
        self.tiles = tiles
        self.count = len(tiles)
        self.coin_v = coins
        self.coin_c = self.count - volts
        self.volts = volts



# =========== Random Board Properties ========== #
class RandBoard:
    def __init__(self,min=0,max=3):
        self.size = 5
        self.tiles = []
        for r in range(self.size):
            self.tiles.append([])
            for c in range(self.size):
                self.tiles[r].append(Tile(self,{randint(min,max)},r,c))

        row_data = [[0,0],[0,0],[0,0],[0,0],[0,0]]
        col_data = [[0,0],[0,0],[0,0],[0,0],[0,0]]

        for r in range(5):
            for c in range(5):
                if self.tiles[r][c].coin_v() == 0:
                    row_data[r][1] += 1
                else:
                    row_data[r][0] += self.tiles[r][c].coin_v()

                if self.tiles[c][r].coin_v() == 0:
                    col_data[c][1] += 1
                else:
                    col_data[c][0] += self.tiles[r][c].coin_v()

        self.row_data = row_data
        self.col_data = col_data


    def __str__(self):
        string = ''
        for row in self.tiles:
            for tile in row:
                string += '{:^14}'.format(str(tile))
            string += ('\n')
        return(string)
