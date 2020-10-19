from lib import *

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
    students = [f"{box(student) if student_index == selected_index else no_box(student)}" for student_index, student in enumerate(students)]
    return multiline_concatenate(students)

def welcome_screen(candidates):
    header = logo()
    prompt = "Up next:\n"
    content = student_list(candidates)
    header, prompt, content = center_content(header, prompt, content)
    return '\n'.join([header, prompt, content])

def spin_wheel(candidates, wheel_index):
    header = logo()
    prompt = "🎯\nPicking student..."
    content = student_list(candidates, wheel_index % len(candidates))
    # import ipdb; ipdb.set_trace()
    header, prompt, content = center_content(header, prompt, content)
    return '\n'.join([header, prompt, content])

def selected_screen(candidates, index):
    header = logo()
    prompt = f"🎉\nCongratulations, {candidates[index]}!"
    content = student_list(candidates, index % len(candidates))
    footer = "[ENTER] to confirm | [DELETE] to cancel"
    # import ipdb; ipdb.set_trace()
    header, prompt, content, footer = center_content(header, prompt, content, footer)
    return '\n'.join([header, prompt, content, footer])