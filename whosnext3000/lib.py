import argparse
import curses
import os
import random
import re
import sys
import time
import yaml
from random import randint

CONFIG_YAML = os.path.join(os.path.dirname(
    os.path.realpath(__file__)), 'config.yml')


def make_box_message(message):
    """
    Puts message in box for display
    """
    width = max([len(message) + 10, 50])
    return f'''
╓{'─' * width}╖
║{' ':^{width}}║
║{message:^{width}}║
║{' ':^{width}}║
╙{'─' * width}╜
'''


def block_width(block):
    return max([len(line) for line in block.split('\n')])


def display_block(start_y, start_x, block, stdscr):
    for index, line in enumerate(block.split('\n')):
        stdscr.addstr(start_y + index, start_x, line)


def get_start_x(content, width):
    return int((width // 2) - (block_width(content) // 2) - block_width(content) % 2)


def offset_paragraph(paragraph, width):
    start_x = get_start_x(paragraph, width)
    return '\n'.join([f"{' ' * start_x + line:<{width}}" for line in paragraph.split('\n')])


def center_content(*paragraphs):
    paragraph_lines = [paragraph.split('\n') for paragraph in paragraphs]
    # Flattening the list of lines
    lines = [item for sublist in paragraph_lines for item in sublist]
    max_width = max([len(line) for line in lines])
    paragraphs = [offset_paragraph(paragraph, max_width)
                  for paragraph in paragraphs]
    return paragraphs


def refresh_screen(content, stdscr):
    """
    Display box message
    """
    for index, line in enumerate(content.split('\n')):
        stdscr.addstr(index, 0, line)

    stdscr.refresh()


def display_history(students):
    """
    Displays history of selected students
    """
    sorted_students = {student: count for student, count in sorted(
        students.items(), key=lambda item: item[1])}
    print()
    for student, count in sorted_students.items():
        print(f'{student:<15} | {count:^11} |')
    print()


def load_config():
    """
    Load config YAML file
    """
    if not os.path.exists(CONFIG_YAML):
        print('reset')
        with open(CONFIG_YAML, 'w+'):
            pass

    with open(CONFIG_YAML) as file:
        config = yaml.load(file, Loader=yaml.FullLoader)

    if config == None:
        config = {}
        config['lists'] = {}
        config['active_list'] = ""
    return config


def save_config(config):
    """
    Rewrite config YAML file
    """
    with open(CONFIG_YAML, 'w+') as file:
        yaml.dump(config, file)


def create_students_list(list_name, students):
    """
    Creates list of students in config file
    """
    config = load_config()
    config['lists'][list_name] = {student: 0 for student in sorted(students)}
    config['active_list'] = list_name
    save_config(config)


def change_active_list(list_name):
    """
    Change active list
    """
    config = load_config()
    config['active_list'] = list_name
    save_config(config)


def display_lists():
    """
    Display existing list names
    """
    config = load_config()
    print('\n'.join(
        [f"{list}{'*' if list == config['active_list'] else ''}" for list in config['lists'].keys()]))


def get_candidates():
    config = load_config()
    active_list = config['active_list']
    students = config['lists'][active_list]
    return [student for student in students if students[student] == min(students.values())]


def increment_student(student_name):
    config = load_config()
    active_list = config['active_list']
    config['lists'][active_list][student_name] += 1
    save_config(config)


# =========================================

def logo():
    config = load_config()
    active_list = config['active_list']
    subtitle = f'{active_list} Edition'
    return f'''
<style>no-cyan bold</style>
 __       __  __                 __                                              __     ____  
/  |  _  /  |/  |               /  |                                            /  |   /    \ 
$$ | / \ $$ |$$ |____    ______ $$/_______        _______    ______   __    __ _$$ |_ /$$$$  |
$$ |/$  \$$ |$$      \  /      \$//       |      /       \  /      \ /  \  /  / $$   |$$  $$ |
$$ /$$$  $$ |$$$$$$$  |/$$$$$$  |/$$$$$$$/       $$$$$$$  |/$$$$$$  |$$  \/$$/$$$$$$/    /$$/ 
$$ $$/$$ $$ |$$ |  $$ |$$ |  $$ |$$      \       $$ |  $$ |$$    $$ | $$  $$<   $$ | __ /$$/  
$$$$/  $$$$ |$$ |  $$ |$$ \__$$ | $$$$$$  |      $$ |  $$ |$$$$$$$$/  /$$$$  \  $$ |/  |$$/   
$$$/    $$$ |$$ |  $$ |$$    $$/ /     $$/       $$ |  $$ |$$       |/$$/ $$  | $$  $$/ /  |  
$$/      $$/ $$/   $$/  $$$$$$/  $$$$$$$/        $$/   $$/  $$$$$$$/ $$/   $$/   $$$$/  $$/ 

                                                            @@@@@@   @@@@@@   @@@@@@   @@@@@@  
                                                                @@! @@!  @@@ @@!  @@@ @@!  @@@ 
                                                             @!!!:  @!@  !@! @!@  !@! @!@  !@!
{subtitle:^64}!!: !!:  !!! !!:  !!! !!:  !!!  
                                                            ::: ::   : : ::   : : ::   : : ::
<style>cyan no-bold</style>
'''
    # start_x = int((width // 2) - (block_width(logo) // 2) - block_width(logo) % 2)
    # for index, line in enumerate(logo.split('\n')):
    #     stdscr.addstr(index, start_x, line)
    # return logo


def add_margin(string, margin):
    return f'{string:^{margin * 2 + len(string)}}'


def box(message):
    width = len(message)
    return f'''
╓{'─' * width}╖
║{' ':^{width}}║
║{message}║
║{' ':^{width}}║
╙{'─' * width}╜
'''


def no_box(message):
    width = len(message)
    return f'''
 {' ' * width} 
 {' ':^{width}} 
 {message} 
 {' ':^{width}} 
 {' ' * width} 
'''


def multiline_concatenate(paragraphs):
    content = []
    for paragraph in paragraphs:
        for line_index, line in enumerate(paragraph.split('\n')):
            try:
                content[line_index] += line
            except IndexError:
                content.append(line)
    return '\n'.join(content)


def student_list(candidates, selected_index=None):
    students = [add_margin(student, 2) for student in candidates]
    students = [f"{box(student) if student_index == selected_index else no_box(student)}" for student_index,
                student in enumerate(students)]
    return multiline_concatenate(students)


def welcome_screen(candidates):
    header = logo()
    icon = ""
    prompt = "Up next:"
    content = student_list(candidates)
    return '\n'.join(center_content(header, icon, prompt, content))


def spin_wheel(candidates, wheel_index):
    header = logo()
    icon = "🎯"
    prompt = "Picking student..."
    content = student_list(candidates, wheel_index % len(candidates))
    return '\n'.join(center_content(header, icon, prompt, content))


def selected_screen(candidates, index):
    header = logo()
    icon = "🎉"
    prompt = f"Congratulations, {candidates[index]}!"
    content = student_list(candidates, index % len(candidates))
    footer = "[ENTER] to confirm | [DELETE] to cancel"
    return '\n'.join(center_content(header, icon, prompt, content, footer))

# =========================================


def apply_styles(stdscr, styles):
    if 'bold' in styles:
        stdscr.attron(curses.A_BOLD)
    if 'no-bold' in styles:
        stdscr.attroff(curses.A_BOLD)
    if 'cyan' in styles:
        stdscr.attron(curses.color_pair(1))
    if 'no-cyan' in styles:
        stdscr.attroff(curses.color_pair(1))
    pass


def draw(stdscr, content, start_y, width):
    start_x = int((width // 2) - (block_width(content) // 2) -
                  block_width(content) % 2)
    for index, line in enumerate(content.split('\n')):
        try:
            match = re.match(r'<style>(.*)</style>', line)
            if match:
                styles = [style.strip() for style in match[1].split(' ')]
                apply_styles(stdscr, styles)
                line = re.sub(r'<style>(.*)</style>', '', line)

            stdscr.addstr(start_y + index, start_x, line)
        except curses.error:
            pass
    stdscr.refresh()


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

        # Initialization
        # stdscr.clear()

        # if k == curses.KEY_DOWN:
        #     cursor_y = cursor_y + 1
        # elif k == curses.KEY_UP:
        #     cursor_y = cursor_y - 1
        # elif k == curses.KEY_RIGHT:
        #     cursor_x = cursor_x + 1
        # elif k == curses.KEY_LEFT:
        #     cursor_x = cursor_x - 1

        # cursor_x = max(0, cursor_x)
        # cursor_x = min(width-1, cursor_x)

        # cursor_y = max(0, cursor_y)
        # cursor_y = min(height-1, cursor_y)

        # Declaration of strings
        # logo = templates.logo("# 5 0 9   E d i t i o n")
        # print(block_width(logo))
        # title = "Curses example"[:width-1]
        # prompt = "UP NEXT"[:width-1]
        # candidates = ['Yann', 'Doug', 'Trouni']
        # content = '   '.join([f"{student:^{len(student) + 4}}" for student in candidates])
        # statusbarstr = "Press 'q' to exit | STATUS BAR | Pos: {}, {}".format(cursor_x, cursor_y)

        # Centering calculations

        # start_x_title = int((width // 2) - (len(title) // 2) - len(title) % 2)
        # start_x_prompt = int((width // 2) - (len(prompt) // 2) - len(prompt) % 2)

        # Turning on attributes for title
        stdscr.attron(curses.color_pair(1))
        # stdscr.attron(curses.A_BOLD)

        # Rendering title
        # display_block(start_y, start_x_logo, logo, stdscr)
        # stdscr.addstr(start_y, start_x_title, title)

        # Turning off attributes for title
        # stdscr.attroff(curses.color_pair(2))
        # stdscr.attroff(curses.A_BOLD)

        # Print rest of text
        # stdscr.addstr(start_y + len(logo.split('\n')) + 1, start_x_prompt, prompt))
        # stdscr.addstr(0, start_x_keystr, keystr)

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
