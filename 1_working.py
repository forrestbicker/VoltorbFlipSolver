#! /Library/Frameworks/Python.framework/Versions/3.7/bin/python3
import VOLTORBAnalysis as volta


rb = volta.RandBoard()
# b = volta.Board(rb.row_data,rb.col_data)


row_data = [[3, 4], [8, 2], [1, 4], [6, 1], [7, 2]]
col_data = [[8, 1], [0, 5], [9, 1], [6, 3], [2, 3]]

print('row',row_data)
print('col',col_data)
print()

b = volta.Board(row_data,col_data)

b.tile(0,0).update({1})
print([tile.c for tile in b.row(0).total.tiles])

while True:
    b.solve()
    print(b)
    if not b.reveal_safe():
        b.guess()
print(b)
