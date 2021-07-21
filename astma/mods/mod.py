

from ._utils import get_state
from ..screen import screenbuf
from ..events import event


class mod:

    label = None
    state_save = ()

    def __init__(self, label):
        self.label = label

    def __call__(self, *args):
        if self.state_save:
            state = self.state
            for attr in self.state_save:
                v = getattr(state, attr)
                if v is not None:
                    setattr(self, attr, v)
        self.render(*args)

        if self.state_save:
            state = self.state
            for attr in self.state_save:
                setattr(state, attr, getattr(self, attr))

    def render(self, buf: screenbuf, ev: event):
        pass

    @property
    def state(self):
        return get_state(self.label or str(id(self)))
