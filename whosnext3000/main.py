import argparse
import curses
import time
from random import randint
from whosnext3000.lib import *
from whosnext3000.templates import welcome_screen, spin_wheel, selected_screen


def draw_menu(stdscr):
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
    while (k not in [ord('q'), 27]):
        height, width = stdscr.getmaxyx()

        keystr = "Last key pressed: {}".format(k)[:width-1]
        start_x_keystr = int(
            (width // 2) - (len(keystr) // 2) - len(keystr) % 2)

        # Turning on attributes for title
        stdscr.attron(curses.color_pair(1))

        if k in [curses.KEY_ENTER, 10, 13]:
            candidates = get_candidates()
            selected_idx = randint(0, len(candidates) - 1)
            stdscr.clear()
            if len(candidates) > 1:
                for wheel_cursor in range(50 - 50 % len(candidates) + selected_idx + 1):
                    # stdscr.addstr(0, start_x_keystr, str(selected_idx))
                    time.sleep(0.03 * (wheel_cursor // 10))
                    draw(stdscr, spin_wheel(
                        candidates, wheel_cursor), start_y, width)
            draw(stdscr, selected_screen(
                candidates, selected_idx), start_y, width)
            k = None
            while k not in [curses.KEY_ENTER, 10, 13, 127, 27, ord('q')]:
                k = stdscr.getch()
                if k in [curses.KEY_ENTER, 10, 13]:
                    increment_student(candidates[selected_idx])
            k = 0
        elif k == 0:
            stdscr.clear()
            candidates = get_candidates()
            draw(stdscr, welcome_screen(candidates), start_y, width)
            # Wait for next input
            k = stdscr.getch()
        else:
            k = stdscr.getch()


def main():
    config = load_config()
    curses.wrapper(draw_menu)


def run():
    parser = argparse.ArgumentParser(description='Manage students lists')
    parser.add_argument('names', metavar='name', type=str, nargs='*',
                        help='student name')
    parser.add_argument('--new-list', dest='new_list', action='store',
                        help='name of the list')
    parser.add_argument('--active-list', dest='active_list', action='store',
                        help='name of active list')
    parser.add_argument('--lists', action='store_true',
                        help='view lists')
    parser.add_argument('--students', action='store_true',
                        help='view students in active list')

    args = parser.parse_args()

    if args.lists:
        display_lists()
    elif args.new_list:
        display_lists()
    elif args.students:
        config = load_config()
        active_list = config['active_list']
        students = config['lists'][active_list]
        display_history(students)
    elif args.active_list:
        change_active_list(args.active_list)
    else:
        return main()


if __name__ == '__main__':
    run()
