# ==================== Board =================== #
class Board:
    def __init__(self):
        self.size = 5
        self.tiles = []
        for i in range(self.size):
            self.tiles.append([])
            for _ in range(self.size):
                self.tiles[i].append(Tile([0,1,2,3]))

    def update(self,dim,pos,val):
        if dim == 'row':
            for i in range(self.size):
                self.tiles[pos][i].intersect(val)
        elif dim == 'col':
            for i in range(self.size):
                self.tiles[i][pos].intersect(val)
        elif dim == 'cel':
            x,y = pos
            self.tiles[y][x].intersect(val)

    def row(self,r):
        tiles = self.tiles[r]
        shown = sum([tile.is_shown() for tile in tiles])
        return(Pane(tiles,shown,row_data[r]))

    def col(self,c):
        tiles = [self.tiles[r][c] for r in range(self.size)]
        shown = sum([tile.is_shown() for tile in tiles])
        return(Pane(tiles,shown,col_data[c]))

    def tile(self,x,y):
        return(self.tiles[y][x])

    def __str__(self):
        string = ''
        for row in self.tiles:
            for cell in row:
                string += '{:^14}'.format(str(cell))
            string += ('\n')
        return(string)

# ==================== Tile =================== #
class Tile:
    def __init__(self,memo):
        self.memo = set(memo)

    def __str__(self):
        return(str(self.memo))

    def is_shown(self):
        if len(self.memo) == 1:
            return(True)
        else:
            return(False)

    def coin(self):
        if len(self.memo) == 1:
            return(int(list(self.memo)[0]))
        else:
            return(0)

    def volt(self):
        if self.memo == {0}:
            return(1)
        else:
            return(0)

    def intersect(self,val):
        self.memo = self.memo & set(val)


# ==================== Pane =================== #
class Pane:
    def __init__(self,tiles,shown,data):
        self.data = data
        self.tiles = tiles
        total_coins = data[0]
        total_volts = data[1]
        shown_coins = sum([tile.coin() for tile in self.tiles])
        shown_volts = sum([tile.volt() for tile in self.tiles])
        hidden_coins = data[0]-shown_coins
        hidden_volts = data[1]-shown_volts
        self.total = PaneProp(5,total_coins,total_volts)
        self.shown = PaneProp(shown,shown_coins,shown_volts)
        self.hidden = PaneProp(5-shown,hidden_coins,hidden_volts)

    def tile(self,i):
        return(self.tiles[i])


# =============== Pane Properties ============== #
class PaneProp:
    def __init__(self,count,coins,volts):
        self.count = count
        self.coins = coins
        self.volts = volts
