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


def inspect(window_title):
    """Connect to a running application by window title and print control identifiers"""
    app = Application()
    
    try:
        # Connect to the application using the window title
        app.connect(name=window_title)
        
        print("==" * 20)
        print("Connected to application with window title: '{}'".format(window_title))
        print("Process ID: {}".format(app.process))
        print("==" * 20)
        windows = app.windows()
        print("Please select the window you want to inspect:")
        for i, window in enumerate(windows):
            print(f"{i}: {window.window_text()}")
        selected_window_index = int(input("Enter the number of the window you want to inspect: "))
        selected_window = windows[selected_window_index]
        print("Selected window: '{}'".format(selected_window.window_text()))
        print("==" * 20)
        selected_window.print_control_identifiers()
        print("==" * 20)
        
    except Exception as e:
        print(f"Error: Failed to connect to application: {e}")
        sys.exit(1)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: {} <window_title>".format(sys.argv[0]), file=sys.stderr)
        print("Example: {} 'Untitled - Notepad'".format(sys.argv[0]), file=sys.stderr)
        sys.exit(1)
    
    window_title = sys.argv[1]
    inspect(window_title)
