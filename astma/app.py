from astma import utils
import sys
from astma.events import init_event, key_event, mouse_event
from ._getch import getch_init, getch_finalize
from .getkey import getkey
from .screen import screen
from .keys import CTRL_C, C3, keyinfo, mouseinfo

_intercept_ctrlc = True


def intercept_ctrlc(value):
    global _intercept_ctrlc
    _intercept_ctrlc = value


def run_app(root):

    utils.debug(' ----------------- starting astma app -----------------')
    scr = None
    try:
        getch_init()
        ev = init_event()
        scr = screen()
        root(scr.screenbuf, ev)

        while True:
            scr.flush()
            c = getkey()
            scr.cursor_off()
            if isinstance(c, keyinfo):
                ev = key_event(c)
            # elif isinstance(c, mouseinfo):
            #     ev = mouse_event(c)
            else:
                continue

            if (c == CTRL_C or c.key == C3) and _intercept_ctrlc:
                break

            root(scr.screenbuf, ev)
    except:
        et, v, tb = sys.exc_info()
        utils.debug('Exception occurred: {}: {}', et.__name__, v)
        while tb:
            utils.debug(
                '  at {}:{}',
                tb.tb_frame.f_code.co_filename, tb.tb_lineno)
            for local_name, local_v in tb.tb_frame.f_locals.items():
                utils.debug('     {} = {}', local_name, local_v)
            tb = tb.tb_next
    finally:
        if scr:
            scr.deinit()
        getch_finalize()
