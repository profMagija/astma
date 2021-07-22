# `astma` - A Simple Text Mode Application library

`astma` is an attempt to make a very simplified library for making text mode apps. Largely inspired by web frameworks and declarative GUI libraries.

## Usage example

In this usage example we will create a simple TODO app, which allows us to create and delete TODOs.

First we will import all the required modules. `astma.mods` contains all the display modules we will use later.

```py
import sys
from astma import app
from astma.lens import lens
from astma.mods import *
```

Next, we will declare our view model data, and wrap it in a `lens`. Lenses allow us to scope into parts of the data later. `values` will be all our TODOs, and `cur_value` will be the key of the currently selected one. `statusline` is used by the statusl line mod we will explain later.

```py
class ViewData:
    values = {}
    cur_value = 0
    statusline = None

DATA = lens(ViewData())
```

Next we will declare some operations on our TODOs. We can use `DATA` like its a regular `ViewData` instance, since `lens`es are mostly transparent.

For creating a new TODO, we ask our user for a title, using `mods.statusline.ask` function which acceprs a callback.

For killing a TODO, we just use the regular `del` operator.

For exiting from the app, we just use `sys.exit()`.

```py
def _create_new_todo(_):
    STATUSLINE.ask('title? ', callback=_create_new_todo_2)

_cur_index = 1
def _create_new_todo_2(ok, value):
    global _cur_index
    if not ok:
        return
    DATA.values[_cur_index] = value
    _cur_index += 1

def _kill_todo(_):
    # cur_value is None, if nothing is selected (e.g. our list is empty)
    if DATA.cur_value is not None:
        del DATA.values[DATA.cur_value]

def _exit_app(_):
    sys.exit()
```

Next, we will define our commands. We can use string key identifiers to define our keybindings, and the values are callbacks (accepting a single argument, the event that triggered it).

```py
COMMANDS = {
    '<C-N>': _create_new_todo,
    '<C-X>': _kill_todo,
    '<C-C>': _exit_app
}
```

Next, we define our layout, using the `mods.layout` mod. It takes a grid (as a list of lists) of elements. We also define which cell is currently focused, and override the height of the first row.

```py
LAYOUT = layout([
    [text('Use Ctrl-N to create new task, and Ctrl-X to delete a task.')],
    [
        menu(DATA.values, DATA.cur_value),
        text(DATA.values[DATA.cur_value], prefix="Current value: ")
    ],
], cur_focus=(1, 0), heights=[1])
```

Then we define the supporting elements, the statusline (which provides a vim-like statusline and prompt box), and the keybind mod (which provides keybinds which we defined in the `COMMANDS` dict).

```py
STATUSLINE = statusline(
    keybind(LAYOUT, commands=COMMANDS),
    DATA.statusline
)
```

Lastly, we turn off Ctlr-C intercept (as we handle the app exit ourselves), and run the app with the topmost element as the root (in our case, the statusline).

```py
app.intercept_ctrlc(False)
app.run_app(STATUSLINE)
```