import os
from pathlib import Path
from simple_term_menu import TerminalMenu
from whosnext3000.lib import load_config, save_config
from whosnext3000.cli.colors import bcolors

home_path = str(Path.home())
CONFIG_YAML = os.path.join(home_path, ".whosnext3000.yml")


def display_history(candidates):
    """
    Displays history of selected candidates
    """
    sorted_candidates = {
        candidate: count
        for candidate, count in sorted(candidates.items(), key=lambda item: item[1])
    }
    print()
    for candidate, count in sorted_candidates.items():
        print(f"{candidate:<15} | {count:^11} |")
    print()


def create_list():
    """
    Creates list of candidates in config file
    """
    list_name = input("Name of the list > ")
    print(
        "Please enter the name of the candidates in the list.\nLeave the name empty and press [ENTER] to finish creating the list."
    )
    candidates = []

    i = 0
    candidate_name = None
    while candidate_name != "":
        i += 1
        candidate_name = input(f"Name of candidate #{i} > ")
        if candidate_name != "":
            candidates.append(candidate_name)

    if len(candidates) > 0:
        config = load_config()
        config["lists"][list_name] = {candidate: 0 for candidate in sorted(candidates)}
        config["active_list"] = list_name
        save_config(config)


def change_active():
    """
    Change active list
    """
    config = load_config()
    print("Please choose the list you'd like to use:")
    terminal_menu = TerminalMenu(
        [
            f"{list} (current)" if list == config["active_list"] else list
            for list in config["lists"].keys()
        ]
    )
    choice_index = terminal_menu.show()
    config["active_list"] = list(config["lists"])[choice_index]
    print(f"'{config['active_list']}' is  now the active list.")
    save_config(config)


def display_lists():
    """
    Display existing list names
    """
    config = load_config()
    print(
        "\n".join(
            [
                f"{bcolors.OKGREEN}{bcolors.BOLD}> {list}{bcolors.ENDC}"
                if list == config["active_list"]
                else f"  {list}"
                for list in config["lists"].keys()
            ]
        )
    )


def delete_list():
    """
    Deletes list of candidates in config file
    """
    config = load_config()
    print("Please choose the list you'd like to delete:")
    terminal_menu = TerminalMenu(config["lists"].keys())
    choice_index = terminal_menu.show()
    delete_list_name = list(config["lists"])[choice_index]
    del config["lists"][delete_list_name]
    if config["active_list"] == delete_list_name:
        config["active_list"] = (
            list(config["lists"])[0] if len(config["lists"]) > 0 else ""
        )
    save_config(config)
    print(f"'{delete_list_name}' has been deleted.")
