# ! /Users/forrestbicker/miniconda3/bin/python3

import time
import curses
import VOLTORBAnalysis as volta


def main(screen):
    b = volta.Board(screen=screen)

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
