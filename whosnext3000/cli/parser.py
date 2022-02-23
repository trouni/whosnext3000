import argparse
import os
from py_compile import main
from . import commands as cmd


def parse_args():
    parser = argparse.ArgumentParser(
        description="A terminal spinning wheel tool.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    commands = parser.add_subparsers(title="WHOSNEXT3000 commands")

    # Display lists
    display_lists = commands.add_parser(
        "lists",
        description="Show all the lists",
        help="Show all the lists",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    display_lists.set_defaults(cmd=cmd.display_lists)

    # Choose active list
    active = commands.add_parser(
        "active",
        description="Select the active list",
        help="Select the active list",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    active.set_defaults(cmd=cmd.change_active)

    # Create new list
    create = commands.add_parser(
        "create",
        description="Create a new list",
        help="Create a new list",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    create.set_defaults(cmd=cmd.create_list)

    # Delete list
    delete = commands.add_parser(
        "delete",
        description="Deletes a list",
        help="Deletes a list",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    delete.set_defaults(cmd=cmd.delete_list)

    # Parse and post-process args
    args = parser.parse_args()

    return args
