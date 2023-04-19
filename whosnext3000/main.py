import argparse
import curses
import time
from random import randint
from whosnext3000.lib import load_config, get_candidates, draw, increment_candidate
from whosnext3000.templates import welcome_screen, spin_wheel, selected_screen
from whosnext3000.cli.parser import parse_args


class UI:
    def __init__(self) -> None:
        # Load candidates
        self.candidates = get_candidates()
        self.draws = []

    def draw_menu(self, stdscr):
        k = 0
        cursor_x = 0
        cursor_y = 0

        # Clear and refresh the screen for a blank canvas
        stdscr.clear()
        stdscr.refresh()

        # Start colors in curses
        curses.start_color()
        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)

        # Hide cursor
        curses.curs_set(0)

        start_y = 1

        # Loop where k is the last character pressed
        while k not in [ord("q"), 27]:
            height, width = stdscr.getmaxyx()

            # # print(keystr) # To show the key codes when developing
            # keystr = "Last key pressed: {}".format(k)[: width - 1]
            # start_x_keystr = int((width // 2) - (len(keystr) // 2) - len(keystr) % 2)

            # Turning on attributes for title
            stdscr.attron(curses.color_pair(1))

            if k in [curses.KEY_ENTER, 10, 13]:
                selected_idx = randint(0, len(self.candidates) - 1)
                stdscr.clear()
                if len(self.candidates) > 1:
                    for wheel_cursor in range(
                        50 - 50 % len(self.candidates) + selected_idx + 1
                    ):
                        # stdscr.addstr(0, start_x_keystr, str(selected_idx))
                        time.sleep(0.03 * (wheel_cursor // 10))
                        print('\a')
                        draw(
                            stdscr,
                            spin_wheel(self.candidates, wheel_cursor),
                            start_y,
                            width,
                        )
                draw(
                    stdscr,
                    selected_screen(self.candidates, selected_idx),
                    start_y,
                    width,
                )
                k = None
                while k not in [curses.KEY_ENTER, 10, 13, 127, 27, ord("q")]:
                    k = stdscr.getch()
                    if k in [curses.KEY_ENTER, 10, 13]:
                        increment_candidate(self.candidates[selected_idx])
                        self.draws.append(self.candidates[selected_idx])
                        self.candidates = get_candidates()
                k = 0
            elif k == 114:  # R key to start from all candidates
                stdscr.clear()
                self.candidates = get_candidates(all=True)
                draw(
                    stdscr, welcome_screen(self.candidates, self.draws), start_y, width
                )
                # Wait for next input
                k = stdscr.getch()
            elif k == 0:
                stdscr.clear()
                draw(
                    stdscr, welcome_screen(self.candidates, self.draws), start_y, width
                )
                # Wait for next input
                k = stdscr.getch()
            else:
                k = stdscr.getch()

    def run(self):
        config = load_config()
        curses.wrapper(self.draw_menu)


def run():
    args = parse_args()

    if len(vars(args)) > 0:
        args.cmd()
    else:
        ui = UI()
        ui.run()


if __name__ == "__main__":
    run()
