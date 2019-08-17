#! /Library/Frameworks/Python.framework/Versions/3.7/bin/python3
import time
import curses
import VOLTORBAnalysis as volta



def main(screen):
    rb = volta.RandBoard()
    b = volta.Board(rb.row_data,rb.col_data,screen=screen)

    row_data = [[3, 4], [8, 2], [1, 4], [6, 1], [7, 2]]
    col_data = [[8, 1], [0, 5], [9, 1], [6, 3], [2, 3]]
    b = volta.Board(row_data,col_data,screen=screen)

    b.render_all()

    while True:
        b.deduce()
        b.render_all()
        if not b.reveal_safe():
            try:
                b.guess()
            except ValueError:
                pass


if __name__ == '__main__':
    curses.wrapper(main)
