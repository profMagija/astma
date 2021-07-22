from typing import Callable
from astma.mods.text import text
from .mod import mod
from ..screen import CURSOR_STEADY_BAR, screenbuf
from ..events import event, key_event
from ..lens import lens
from ..keys import BACKSPACE, DELETE, LEFT, RIGHT
from astma import keys

class _statusline_state: 
    __slots__ = ('editing', 'content', 'entry', 'callback', 'old_content')

class statusline(mod):
    def __init__(self, child, status, label=None):
        super().__init__(label)
        
        self.status = lens(status)
        
        if self.status.lens_get() is None:
            self.status.lens_set(_statusline_state())
        
        self.status.editing.lens_set(False)
        self.status.content.lens_set('')
        self.status.entry.lens_set('')

        text_label = None if label is None else label + '$text'

        self._child = child
        self._text = text(
            text=self.status.entry,
            prefix=self.status.content,
            label=text_label)

        self._child_buf = None

    def relayout(self, buf: screenbuf):
        self._child_buf = buf.subbuf(0, 0, -2, None)
        self._status_buf = buf.subbuf(-1, 0, 1, None)

    def ask(self, question: str, value: str = '', callback: Callable[[bool, str], None] = None):
        self.status.old_content.lens_set(self.status.content.lens_get())
        self.status.content.lens_set(question)
        self.status.entry.lens_set(value)
        self.status.editing.lens_set(True)
        self.status.callback.lens_set(callback)

    def _handle_key(self, ev: key_event):
        if ev.key.key not in (keys.ENTER, keys.CTRL_C):
            return False

        cur_entry = self.status.entry.lens_get()
        self.status.editing.lens_set(False)
        self.status.entry.lens_set('')
        self.status.content.lens_set(self.status.old_content.lens_get())
        
        cb = self.status.callback.lens_get()
        
        if cb:
            cb(ev.key.key == keys.ENTER, cur_entry)

    def render(self, buf: screenbuf, ev: event):
        if self._child_buf is None:
            self.relayout(buf)

        editing = bool(self.status.editing.lens_get())
        if editing and isinstance(ev, key_event):
            if self._handle_key(ev):
                ev = None

        self._status_buf.focus(editing)
        self._child_buf.focus(not editing)

        self._child(self._child_buf, ev if not editing else None)
        self._text(self._status_buf, ev if editing else None)
