from .mod import mod
from ..screen import CURSOR_STEADY_BAR, screenbuf
from ..events import event, key_event
from ..lens import lens
from ..keys import DOWN, UP
from astma import ansi


def _get_key(v):
    if type(v) is tuple:
        return v[0]
    else:
        return v


def _get_text(v):
    if type(v) is tuple:
        return str(v[1])
    else:
        return str(v)


class menu(mod):

    state_save = ('row_offset', 'last_index')

    def __init__(self, values, cur_key, label=None):
        super().__init__(label)
        self.values = lens(values)
        self.cur_key = lens(cur_key)
        self.row_offset = 0
        self.last_index = 0

    def _handle_key(self, ev: key_event):
        if ev.key == UP:
            self._change_selection(-1)
        elif ev.key == DOWN:
            self._change_selection(1)

    def _change_selection(self, rel: int):
        cur_idx = None
        values = self.values.lens_get()
        if isinstance(values, dict):
            values = tuple(values)

        for i, v in enumerate(values):
            if _get_key(v) == self.cur_key.lens_get():
                cur_idx = i
                break

        if cur_idx is None:
            cur_idx = self.last_index

        if len(values) == 0:
            self.cur_key.lens_set(None)
        else:
            cur_idx += rel
            if cur_idx < 0:
                cur_idx = 0
            if cur_idx >= len(values):
                cur_idx = len(values) - 1

            self.last_index = cur_idx
            self.cur_key.lens_set(_get_key(values[cur_idx]))

    def render(self, buf: screenbuf, ev: event):
        if buf.is_focused() and isinstance(ev, key_event):
            self._handle_key(ev)

        self._change_selection(0)

        values = self.values.lens_get()
        if isinstance(values, dict):
            values = tuple(values.items())

        cur_selection = self.cur_key.lens_get()

        if self.row_offset != 0 and self.row_offset + buf.height > len(values):
            self.row_offset = len(values) - buf.height

        if self.row_offset < 0:
            self.row_offset = 0

        for row_idx in range(buf.height):
            val_idx = row_idx + self.row_offset
            if val_idx < len(values):
                value = values[val_idx]
                key, text = _get_key(value), _get_text(value)
                ctrl = ansi.INVERSE if key == cur_selection else None
                buf.put_at(
                    row_idx, 0,
                    text.ljust(buf.width),
                    control=ctrl)
            else:
                buf.put_at(row_idx, 0, ''.ljust(buf.width))

        # if buf.is_focused():
        #     buf.cursor(0, self.cursor, CURSOR_STEADY_BAR)
