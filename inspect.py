# Inspect a running application by window title and print control identifiers
#
# Instructions:
#   1. Run the application you want to inspect
#   2. Make sure the window you are inspecting is visible on the screen
#   3. Run the script with the window title as an argument
#
# Usage: 
# python inspect.py "<window_title>"
#   
# Example: 
# python inspect.py "Untitled - Notepad"

import sys
from pywinauto.application import Application
from pywinauto.findwindows import ElementNotFoundError, WindowAmbiguousError


def inspect(window_title):
    """Connect to a running application by window title and print control identifiers"""
    app = Application()
    
    try:
        # Connect to the application using the window title
        app.connect(name=window_title)
        
        print("==" * 20)
        print("Connected to application with window title: '{}'".format(window_title))
        print("Process ID: {}".format(app.process))
        print("Windows of this application:", app.windows())
        print("==" * 20)
        
        # Get the top window (main window) and print its control identifiers
        main_window = app.top_window()
        print("Control identifiers for window: '{}'".format(window_title))
        print("==" * 20)
        main_window.print_control_identifiers()
        print("==" * 20)
        
    except ElementNotFoundError:
        print("Error: No window found with title '{}'".format(window_title), file=sys.stderr)
        sys.exit(1)
    except WindowAmbiguousError:
        print("Error: Multiple windows found with title '{}'".format(window_title), file=sys.stderr)
        print("Please use a more specific window title.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print("Error: Failed to connect to application: {}".format(e), file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: {} <window_title>".format(sys.argv[0]), file=sys.stderr)
        print("Example: {} 'Untitled - Notepad'".format(sys.argv[0]), file=sys.stderr)
        sys.exit(1)
    
    window_title = sys.argv[1]
    inspect(window_title)
