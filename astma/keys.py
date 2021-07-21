import sys

C3 = 3

BACKSPACE = 8
TAB = 9
ENTER = 13
SPACE = 32
DELETE = 127

HOME = -1
INSERT = -2
END = -4
PAGEUP = -5
PAGEDOWN = -6
F0 = -10
F1 = -11
F2 = -12
F3 = -13
F4 = -14
F5 = -15
F6 = -16
F7 = -17
F8 = -18
F9 = -19
F10 = -20
F11 = -21
F12 = -22
F13 = -23
F14 = -24
F15 = -25
F16 = -26
F17 = -27
F18 = -28
F19 = -29
F20 = -30
UP = -40
DOWN = -41
RIGHT = -42
LEFT = -43

KEYNAMES = {
    C3: '^C',
    BACKSPACE: 'Backspace',
    TAB: 'Tab',
    ENTER: 'Enter',
    SPACE: 'Space',
    HOME: 'Home',
    INSERT: 'Insert',
    DELETE: 'Delete',
    END: 'End',
    PAGEUP: 'PageUp',
    PAGEDOWN: 'PageDown',
    F0: 'F0',
    F1: 'F1',
    F2: 'F2',
    F3: 'F3',
    F4: 'F4',
    F5: 'F5',
    F6: 'F6',
    F7: 'F7',
    F8: 'F8',
    F9: 'F9',
    F10: 'F10',
    F11: 'F11',
    F12: 'F12',
    F13: 'F13',
    F14: 'F14',
    F15: 'F15',
    F16: 'F16',
    F17: 'F17',
    F18: 'F18',
    F19: 'F19',
    F20: 'F20',
    UP: 'Up',
    DOWN: 'Down',
    RIGHT: 'Right',
    LEFT: 'Left',
}

MOD_SHIFT = 1
MOD_ALT = 2
MOD_CTRL = 4
MOD_META = 8

class keyinfo:
    def __init__(self, key:int, mods=0):
        "creates a new keyinfo instance"
        char = None
        if isinstance(key, str):
            if len(key) == 1:
                key = ord(key)
                char = key
            elif len(key) == 2 and key[0] == '^':
                key = ord(key[1]) - ord('@')
                if key == -1:
                    key = 127
                mods |= MOD_CTRL
            elif len(key) > 2 and key[0] == '<' and key[-1] == '>':
                orig = key
                parts = key[1:-1].split('-')
                key = get_key_by_name(parts[-1])
                for modpart in parts[:-1]:
                    if modpart not in ['C', 'A', 'S', 'M']:
                        raise ValueError(orig)
                    mods |= {
                        'C': MOD_CTRL,
                        'A': MOD_ALT,
                        'S': MOD_SHIFT,
                        'M': MOD_META
                    }[modpart]
            else:
                raise ValueError(key)
        elif isinstance(key, keyinfo):
            mods = key.mods
            key = key.key

        self.key = key
        if 32 <= key != 127:
            mods &= ~MOD_SHIFT
            self.char = chr(key)
        else:
            self.char = None


        if self.char and self.char == self.char.upper() and self.char != self.char.lower():
            mods |= MOD_SHIFT

        self.mods = mods
        self.shift = (mods & MOD_SHIFT) != 0
        self.alt = (mods & MOD_ALT) != 0
        self.ctrl = (mods & MOD_CTRL) != 0
        self.meta = (mods & MOD_META) != 0

        self._frozen = True

    def __setattr__(self, name, value):
        if getattr(self, '_frozen', False):
            raise TypeError('Can not change immutable value')
        super().__setattr__(name, value)

    def is_char(self):
        return  32 <= self.key != 127 and self.mods & (~MOD_SHIFT) == 0

    def __str__(self):
        if self.is_char():
            return self.char
        else:
            return (
                '<' +
                ('C-' if self.ctrl else '') +
                ('A-' if self.alt else '') +
                ('S-' if self.shift else '') +
                ('M-' if self.meta else '') +
                (self.char or KEYNAMES.get(self.key, '???')) + 
                '>'
            )
    def __repr__(self):
        return f"keyinfo('{self}')"

    def __hash__(self):
        return hash((self.key, self.mods))

    def __eq__(self, other):
        if isinstance(other, int):
            return self.key == other
        return self.key == other.key and self.mods == other.mods

    

def get_key_by_name(name):
    try:
        if len(name) == 1:
            return ord(name)
        return getattr(sys.modules[__name__], name.replace('-', '_').upper())
    except AttributeError:
        raise KeyError(name)

def __getitem__(self, name: str):
    return get_key_by_name(name)
    
CTRL_C = keyinfo('<C-c>')