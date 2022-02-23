from whosnext3000.cli.colors import bcolors

from whosnext3000.lib import (
    load_config,
    center_content,
    add_margin,
    multiline_concatenate,
)


def logo():
    config = load_config()
    active_list = config["active_list"]
    subtitle = f"{active_list} Edition"
    return f"""
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
"""


def box(message):
    width = len(message)
    return f"""
╓{'─' * width}╖
║{' ':^{width}}║
║{message}║
║{' ':^{width}}║
╙{'─' * width}╜
"""


def no_box(message):
    width = len(message)
    return f"""
 {' ' * width} 
 {' ':^{width}} 
 {message} 
 {' ':^{width}} 
 {' ' * width} 
"""


def candidate_list(candidates, selected_index=None):
    candidates = [add_margin(candidate, 2) for candidate in candidates]
    candidates = [
        f"{box(candidate) if candidate_index == selected_index else no_box(candidate)}"
        for candidate_index, candidate in enumerate(candidates)
    ]
    return multiline_concatenate(candidates)


def welcome_screen(candidates, draws=[]):
    header = logo()
    icon = ""
    prompt = "Up next:"
    content = candidate_list(candidates)
    footer = "\n\n[R] to include all candidates"
    if len(draws) > 0:
        footer_2 = "\n\nPrevious draws:"
        footer_3 = ", ".join(draws)
    else:
        footer_2, footer_3 = "", ""

    return "\n".join(
        center_content(header, icon, prompt, content, footer, footer_2, footer_3)
    )


def spin_wheel(candidates, wheel_index):
    header = logo()
    icon = "🎯"
    prompt = "Picking candidate..."
    content = candidate_list(candidates, wheel_index % len(candidates))
    return "\n".join(center_content(header, icon, prompt, content))


def selected_screen(candidates, index):
    header = logo()
    icon = "🎉"
    prompt = f"Congratulations, {candidates[index]}!"
    content = candidate_list(candidates, index % len(candidates))
    footer = "\n\n[ENTER] to confirm | [DELETE] to cancel"
    return "\n".join(center_content(header, icon, prompt, content, footer))
