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
# Optional arguments:
# <output_file>: The file to save the output to
# <max_depth>: The maximum depth of the tree to print
# <max_width>: The maximum width of the tree to print
#
# Example: 
# python inspect.py "Drake 2024 Tax Software" "output.log" 10 10

import sys
import argparse
from pywinauto.application import Application


def inspect(window_title, output_file, max_depth, max_width):
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
        window = app.window(name=selected_window.window_text(), found_index=0)
        window.dump_tree(depth=max_depth, max_width=max_width, filename=output_file)
        print("==" * 20)
        
    except Exception as e:
        print(f"Error: Failed to connect to application: {e}")
        sys.exit(1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Inspect a running application by window title and print control identifiers'
    )
    parser.add_argument(
        'window_title',
        help='The title of the window to inspect'
    )
    parser.add_argument(
        '--output-file',
        dest='output_file',
        default=None,
        help='The file to save the output to'
    )
    parser.add_argument(
        '--max-depth',
        dest='max_depth',
        type=int,
        default=None,
        help='The maximum depth of the tree to print'
    )
    parser.add_argument(
        '--max-width',
        dest='max_width',
        type=int,
        default=None,
        help='The maximum width of the tree to print'
    )

    args = parser.parse_args()
    inspect(args.window_title, args.output_file, args.max_depth, args.max_width)
