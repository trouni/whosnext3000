import os
import curses
import yaml
import random
import time
import sys

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
    paragraphs = [offset_paragraph(paragraph, max_width) for paragraph in paragraphs]
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

# def main():
#     with open(CONFIG_YAML) as file:
#         config = load_config()

#     active_list = config['active_list']

#     if len(config['lists']) == 0 or active_list == '':
#         return print('No active list.')

#     students = config['lists'][active_list]
#     candidates = get_candidates()

#     if len(candidates) > 1:
#         try:
#             print(make_box_message(
#                 f'UP NEXT: {", ".join(candidates[:-1])} and {candidates[-1]}'))

#             input('Press [ENTER]')

#             stdscr = curses.initscr()
#             curses.noecho()
#             curses.cbreak()

#             draw_menu(stdscr)

#             for i in range(50):
#                 content = f'''



#                 {make_box_message(random.choice(candidates))}
#                 '''
#                 refresh_screen(content, stdscr)
#                 time.sleep(0.03 * (i // 10))
#         finally:
#             selected = random.choice(candidates)
#             refresh_screen(make_box_message(f"{selected} is up!"), stdscr)
#             while 1:
#                 c = stdscr.getch()
#                 if c == ord('n'):
#                     curses.echo()
#                     curses.nocbreak()
#                     curses.endwin()
#                     return print('No student selected...')
#                 if c == curses.KEY_ENTER or c == 10 or c == 13:
#                     increment_student(config, selected)

#                     curses.echo()
#                     curses.nocbreak()
#                     curses.endwin()
#                     return

#     else:
#         selected = candidates[0]
#         print(make_box_message(f'{selected} is the only one left...'))
#         if input('[ENTER] to confirm, [N] to cancel\n') == '':
#             config['lists'][active_list][selected] += 1
#             save_config(config)
#             return print(make_box_message(f"{selected} is up!"))
#         else:
#             return print('No student selected...')


