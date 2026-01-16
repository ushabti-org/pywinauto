### Overview
This is a fork of the [pywinauto](https://github.com/pywinauto/pywinauto) library with a few very small tweaks to help while inspecting windows UI. It contains a script `inspect.py` that prints a dump of the UI tree and includes the `control_id` attribute of each element.

Note: this is the only intended use of this fork. It is not used in production.

### Windows VM Installation

if you don't have `uv`, install that first:

```
pip install uv
```

In the root of the project do the following:

- install 64-bit python version
```
uv python install cpython-3.11.14-windows-x86_64-none
```

- pin this version to the project locally:
```
 uv python pin cpython-3.11.14-windows-x86_64-none
```

- create a virtual environment
```
uv venv
```

- install dependencies
```
uv pip install -r dev-requirements.txt
uv pip install comtypes==1.3.1
```

### Usage
to dump the UI tree of a particular window, make sure your application is open and the screen you want to inspect is visible on the desktop. then:

```
uv run python inspect.py "<APPLICATION_WINDOW_TITLE>"
```

to log the output to a file

```
uv run python inspect.py "<APPLICATION_WINDOW_TITLE>" --output-file <FILE_PATH>
```

to specify a backend
```
uv run python inspect.py "<APPLICATION_WINDOW_TITLE>" --backend "win32"
```