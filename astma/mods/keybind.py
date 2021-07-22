from .mod import mod
from ..screen import CURSOR_STEADY_BAR, screenbuf
from ..events import event, key_event
from ..lens import lens
from ..keys import BACKSPACE, DELETE, LEFT, RIGHT


class keybind(mod):

    def __init__(self, child, commands=None, modal_commands=None, mode=None, label=None):
        super().__init__(label)
        self.child = child

        self.state_save = ['queued_events', 'cur_command']
        self.queued_events = []
        self.cur_command = ''

        if modal_commands is not None:
            if mode is None:
                self._mode = '*'
                self.state_save.append('mode')
            else:
                self._mode = mode

            self._commands = modal_commands
        else:
            self._mode = '*'
            self._commands = {'*': commands}

    def _handle_key(self, ev: key_event):
        key = ev.key

        cur_mode = self._commands[self.get_mode()]
        cb = None
        if key.char and key.char in cur_mode:
            cb = cur_mode[key.char]
        elif key.key in cur_mode:
            cb = cur_mode[key.key]
        elif key in cur_mode:
            cb = cur_mode[key]
        elif str(key) in cur_mode:
            cb = cur_mode[str(key)]

        if not cb:
            return False

        res = cb(ev)

        if res is False:
            return False
        else:
            return True

    def set_mode(self, mode):
        if isinstance(self._mode, lens):
            self._mode.lens_set(mode)
        else:
            self._mode = mode

    def get_mode(self):
        if isinstance(self._mode, lens):
            return self._mode.lens_get()
        else:
            return self._mode

    def render(self, buf: screenbuf, ev: event):
        handled = False
        if buf.is_focused() and isinstance(ev, key_event):
            handled = self._handle_key(ev)

        self.child(buf, ev if not handled else None)
