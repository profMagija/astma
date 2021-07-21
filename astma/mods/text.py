from .mod import mod
from ..screen import CURSOR_STEADY_BAR, screenbuf
from ..events import event, key_event
from ..lens import lens
from ..keys import BACKSPACE, DELETE, LEFT, RIGHT


class text(mod):

    state_save = ('cursor', )

    def __init__(self, label, text, focus=False):
        self.label = label
        self.text = lens(text)
        self.focus = focus
        self.cursor = 0

    def _handle_key(self, ev: key_event):
        if ev.key == LEFT:
            self.cursor = max(0, self.cursor - 1)
        elif ev.key == RIGHT:
            self.cursor = min(len(self.text.lens_get()), self.cursor + 1)
        elif ev.key.is_char():
            text = self.text.lens_get()
            pre_text = text[:self.cursor]
            post_text = text[self.cursor:]
            self.text.lens_set(pre_text + ev.key.char + post_text)
            self.cursor += 1
        elif ev.key == BACKSPACE:
            if self.cursor == 0:
                return
            text = self.text.lens_get()
            pre_text = text[:self.cursor - 1]
            post_text = text[self.cursor:]
            self.text.lens_set(pre_text + post_text)
            self.cursor -= 1
        elif ev.key == DELETE:
            text = self.text.lens_get()
            if self.cursor == len(text):
                return
            pre_text = text[:self.cursor]
            post_text = text[self.cursor+1:]
            self.text.lens_set(pre_text + post_text)

    def render(self, buf: screenbuf, ev: event):
        if self.focus and isinstance(ev, key_event):
            self._handle_key(ev)

        buf.put_at(0, 0, self.text.lens_get() + ' ')
        buf.put_at(1, 0, str(ev))

        if self.focus:
            buf.cursor(0, self.cursor, CURSOR_STEADY_BAR)
