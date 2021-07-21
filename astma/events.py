

from astma.keys import keyinfo, mouseinfo


class event:
    def __init__(self, event_type):
        self.event_type = event_type


class init_event(event):
    def __init__(self):
        super().__init__('init')


class key_event(event):
    def __init__(self, key: keyinfo):
        super().__init__('key')
        self.key = key

    def __str__(self):
        return f'key_event({self.key!r})'


class mouse_event(event):
    def __init__(self, mouse: mouseinfo):
        self.mouse = mouse

    def __str__(self):
        return f'mouse_event({self.mouse!r})'
