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


def print_current_path(path):
    """Prints the currently selected path"""
    if len(path) == 0:
        return
    
    msg = "Current Path: "
    for c in path:
        msg = f"{msg} -> {c}"
    
    print(msg)
    print("\n")


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
                info = child.element_info if hasattr(child, "element_info") else child
                print(f"{i}: {info}")
            
            print("'B': to go back up a level")
            print("'E': to exit")

            selection = input("Select an option: ")
            if selection == "E":
                break
            elif selection == "B" and len(selected_children) > 0:
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

    except Exception as e:
        print(f"Error: Failed to connect to application: {e}")
        sys.exit(1)

if __name__ == '__main__':
    parse()
