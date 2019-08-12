#! /Library/Frameworks/Python.framework/Versions/3.7/bin/python3
# ============================================== #
# =============== Voltorb Flip ================  #
# ============================================== #
# Written by Forrest Bicker
# August 2019
#


# ================ Requiremets ================  #
from pprint import pprint
import random


# ============== Board Generation =============  #
board = [
    [[],[],[],[],[]],
    [[],[],[],[],[]],
    [[],[],[],[],[]],
    [[],[],[],[],[]],
    [[],[],[],[],[]],
]

for x in range(5):
    for y in range(5):
        board[y][x] = random.randint(0,3)


# ============== Board Assessment =============  #
class Board:
    def __init__(self):
        self.contents = []
        for _ in range(5):
            self.contents.append([Tile([0,1,2,3])]*5)

    def update(self,dim,pos,val):
        if dim == 'row':
            for i in range(5):
                self.contents[pos][i] &= set(val)
        elif dim == 'col':
            for i in range(5):
                self.contents[i][pos] &= set(val)
        elif dim == 'cel':
            x,y = pos
            self.board[x,y] &= set(val)


class RowCol:
    def __init__(self,total,shown,hidden):
        self.total = total
        self.shown = shown
        self.hidden = hidden

class Tile:
    def __init__(self,memo,value,count):
        self.memo = set(memo)


# ============== Board Assessment =============  #
row_keys = [[0,0],[0,0],[0,0],[0,0],[0,0]]
col_keys = [[0,0],[0,0],[0,0],[0,0],[0,0]]
for y in range(5):
    for x in range(5):
        if board[y][x] == 0:
            row_keys[y][1] += 1
        else:
            row_keys[y][0] += board[y][x]

        if board[x][y] == 0:
            col_keys[y][1] += 1
        else:
            col_keys[y][0] += board[x][y]
print('row',row_keys)
print('column',col_keys)

# Board Printer
for row in board:
    for cell in row:
        print('{:^14}'.format(str(cell)),end='')
    print('\n')


board = Board()

for row,(t_coin_val,t_volts) in enumerate(row_keys):
    rboard = board.contents[row]
    if t_volts == 0:
        board.update('row',row,[1,2,3])
    elif t_coin_val + t_volts == 5:
        board.update('row',row,[0,1])
    h_tiles, s_coin_val = 0,0
    for cell in board.contents[row]:
        if len(cell) != 1:
            h_tiles += 1
        else:
            if cell != {0}:
                s_coin_val += list(cell)[0]
    h_coins = h_tiles - t_volts
    h_coin_val = t_coin_val - s_coin_val
    if h_coin_val < h_coins:
        board.update('row',row,[0,1])
    elif h_coin_val == h_coins:
        board.update('row',row,[1])
    elif h_coin_val == h_coins + 1:
        board.update('row',row,[0,1,2])



for col,(t_coin_val,t_volts) in enumerate(col_keys):
    if t_volts == 0:
        board.update('col',col,[1,2,3])
    elif t_coin_val + t_volts == 5:
        board.update('col',col,[0,1])






print('-'*100)
# pprint(board.contents)

for row in 1:
    for cell in row:
        print('{:^14}'.format(str(cell)),end='')
    print('\n')


# 1. 0 Voltorbs --> [1,2,3]
# 2. Volt + Coin = 5 --> [0,1]
# 3. Volt + Coin = 6 --> [0,1,2]
#
# brain cell stuff
#
# 4. Volt + Coin + OverOne(KwnTiles) = UkwnTiles --> [0,1]
#
#
# coinTiles = uTiles - nVult
# hiddenCoin = nCoin - revealCoin
# hiddenCoin < coinTiles --> [0,1]
# hiddenCoin = coinTiles --> [1]
# hiddenCoin = coinTiles + 1 --> [0,1,2]
