from astma.events import init_event, key_event
from ._getch import getch_init, getch_finalize
from .getkey import getkey
from .screen import screen
from .keys import CTRL_C, C3

_intercept_ctrlc = True

def intercept_ctrlc(value):
    global _intercept_ctrlc
    _intercept_ctrlc = value

def run_app(root):

    getch_init()
    ev = init_event()
    scr = screen()
    scr.control('\x1b[>4;2m')
    root(scr.screenbuf, ev)

    try:
        while True:
            scr.flush()
            c = getkey()
            ev = key_event(c)

            if (c == CTRL_C or c.key == C3) and _intercept_ctrlc:
                break

            root(scr.screenbuf, ev)
    finally:
        scr.control('\x1b[>4m')
        getch_finalize()