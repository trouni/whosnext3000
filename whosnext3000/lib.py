import curses
import os
import re
import yaml
from pathlib import Path

home_path = str(Path.home())
CONFIG_YAML = os.path.join(home_path, ".whosnext3000.yml")


def load_config():
    """
    Load config YAML file
    """
    if not os.path.exists(CONFIG_YAML):
        Path(CONFIG_YAML).touch(exist_ok=True)

    with open(CONFIG_YAML) as file:
        config = yaml.load(file, Loader=yaml.FullLoader)

    if config == None:
        config = {}
        config["lists"] = {}
        config["active_list"] = ""
    return config


def save_config(config):
    """
    Rewrite config YAML file
    """
    with open(CONFIG_YAML, "w+") as file:
        yaml.dump(config, file)


def block_width(block):
    return max([len(line) for line in block.split("\n")])


def get_start_x(content, width):
    return int((width // 2) - (block_width(content) // 2) - block_width(content) % 2)


def offset_paragraph(paragraph, width):
    start_x = get_start_x(paragraph, width)
    return "\n".join(
        [f"{' ' * start_x + line:<{width}}" for line in paragraph.split("\n")]
    )


def center_content(*paragraphs):
    paragraph_lines = [paragraph.split("\n") for paragraph in paragraphs]
    # Flattening the list of lines
    lines = [item for sublist in paragraph_lines for item in sublist]
    max_width = max([len(line) for line in lines])
    paragraphs = [offset_paragraph(paragraph, max_width) for paragraph in paragraphs]
    return paragraphs


def get_candidates(all=False):
    config = load_config()
    active_list = config["active_list"]
    candidates = config["lists"][active_list]
    if all:
        return list(candidates)
    else:
        return [
            candidate
            for candidate in candidates
            if candidates[candidate] == min(candidates.values())
        ]


def increment_candidate(candidate_name):
    config = load_config()
    active_list = config["active_list"]
    config["lists"][active_list][candidate_name] += 1
    save_config(config)


# DRAW


def add_margin(string, margin):
    return f"{string:^{margin * 2 + len(string)}}"


def multiline_concatenate(paragraphs):
    content = []
    for paragraph in paragraphs:
        for line_index, line in enumerate(paragraph.split("\n")):
            try:
                content[line_index] += line
            except IndexError:
                content.append(line)
    return "\n".join(content)


def apply_styles(stdscr, styles):
    if "bold" in styles:
        stdscr.attron(curses.A_BOLD)
    if "no-bold" in styles:
        stdscr.attroff(curses.A_BOLD)
    if "cyan" in styles:
        stdscr.attron(curses.color_pair(1))
    if "no-cyan" in styles:
        stdscr.attroff(curses.color_pair(1))
    pass


def draw(stdscr, content, start_y, width):
    start_x = int((width // 2) - (block_width(content) // 2) - block_width(content) % 2)
    for index, line in enumerate(content.split("\n")):
        try:
            match = re.match(r"<style>(.*)</style>", line)
            if match:
                styles = [style.strip() for style in match[1].split(" ")]
                apply_styles(stdscr, styles)
                line = re.sub(r"<style>(.*)</style>", "", line)

            stdscr.addstr(start_y + index, start_x, line)
        except curses.error:
            pass
    stdscr.refresh()

def batches(elements, n):
    n = max(1, n)
    return (elements[i:i+n] for i in range(0, len(elements), n))
