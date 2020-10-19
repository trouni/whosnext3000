import curses
import os
import re
import sys
import time
import yaml

CONFIG_YAML = os.path.join(os.path.dirname(
    os.path.realpath(__file__)), 'config.yml')

# CLI


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

# APP


def block_width(block):
    return max([len(line) for line in block.split('\n')])


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


# DRAW

def add_margin(string, margin):
    return f'{string:^{margin * 2 + len(string)}}'


def multiline_concatenate(paragraphs):
    content = []
    for paragraph in paragraphs:
        for line_index, line in enumerate(paragraph.split('\n')):
            try:
                content[line_index] += line
            except IndexError:
                content.append(line)
    return '\n'.join(content)


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
