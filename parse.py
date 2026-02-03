# Prarse is an interactive parser that lets you navigate the UI tree of a running application
# It is used for UI heavy applications where the UI is very complex and the UI tree is very large.
# Use this script when it is typically not feasible to parse the UI tree statically using a tool like inspect.py (app crashes)
#
# Instructions:
#   1. Run the application you want to inspect
#   2. Make sure the window you are inspecting is visible on the screen
#   3. Run the script with the window title as an argument
#
# Usage: 
# python parse.py
#
# Example: 
# python parse.py

import re
import sys
from releases.pywinauto069.pywinauto.application import Application


## Update this regex to match the window title of the application you want to parse
APPLICATION_TITLE = re.compile(r".*SOMETHING_TO_MATCH_ON_THE_WINDOW_TITLE.*")
APPLICATION_ENGINE = "win32"
STR_LIMIT = 20


def shorthand(value: str) -> str:
    if value is None:
        return "unset"
    if len(value) <= STR_LIMIT:
        return value
    return value[:STR_LIMIT] + "..."


def get_element_info(element, index: int | None = None) -> str:
    if not hasattr(element, "element_info"):
        return str(element)
    info = element.element_info
    num_children = len(element.children())
    class_name = shorthand(info.class_name)
    control_type = shorthand(info.control_type)
    control_id = shorthand(info.automation_id)
    name = shorthand(info.name)
    index_str = f"{index}:" if index is not None else ""

    return f"""{index_str:<4} {class_name:<{STR_LIMIT}} {control_type:<{STR_LIMIT}} {control_id:<{STR_LIMIT}} {name:<{STR_LIMIT}} ({num_children})"""


def print_current_path(path) -> None:
    if len(path) == 0:
        return
    msg = "CURRENT PATH"
    print("==" * 20)
    spaces = 0
    for c in path:
        spaces_str = " " * spaces
        info_str = get_element_info(c)
        print(f"{spaces_str}{info_str}")
        spaces = spaces + 2
    print("==" * 20)


def parse():
    """Connect to a running application by window title and print control identifiers"""
    app = Application(backend=APPLICATION_ENGINE)
    
    try:
        # Connect to the application using the window title
        app.connect(title_re=APPLICATION_TITLE)
        
        print("==" * 20)
        print("Connected to application")
        print("Engine: '{}'".format(APPLICATION_ENGINE))
        print("Process ID: {}".format(app.process))
        print("==" * 20)
        windows = app.windows()
        selected_children = []
        options = windows

        while True:
            print_current_path(selected_children)
            print("Please select the element you want to parse:")
            for i, child in enumerate(options):
                print(get_element_info(child, i))
            
            print("==" * 20)
            print("'B':    Back")
            print("'E':    Exit")

            selection = input("> ")
            if selection.upper() == "E":
                break
            elif selection.upper() == "B" and len(selected_children) > 0:
                selected_children = selected_children[:-1]
                if len(selected_children) > 0:
                    options = selected_children[-1].children()
                else:
                    options = windows
            else:
                selected_index = int(selection)
                selected_children.append(options[selected_index])
                options = options[selected_index].children()
            print("==" * 20)
            print("\n\n")

    except Exception as e:
        print(f"Error: Failed to connect to application: {e}")
        sys.exit(1)

if __name__ == '__main__':
    parse()
