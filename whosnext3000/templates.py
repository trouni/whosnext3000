from whosnext3000.lib import load_config, center_content, add_margin, multiline_concatenate


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
