import sys
from .getkey import _readnumber, _getch
from .utils import fix_list_index

_stdout = sys.stdout
_stdin = sys.stdin

class screen:
    def __init__(self):
        self._get_size()
        _stdout.write('\x1b[2J\x1b[H') # clear the screen, and home
        self.screenbuf = screenbuf(None, self, self.rows, self.cols, focused=True)
        self.cursor_shape = CURSOR_BLINKING_BLOCK

    def _get_size(self):
        _stdout.write('\x1b[999;999H\x1b[6n')
        _stdout.flush()
        c = _getch()
        while c != '\x1b': 
            c = _getch()
        _getch() # read the '['
        self.rows, _ = _readnumber()
        self.cols, _ = _readnumber()

    def _goto_yx(self, row, col):
        _stdout.write('\x1b[{};{}H'.format(row+1, col+1))


    def put_at(self, row, col, data):
        self._goto_yx(row, col)
        assert('\x1b' not in data)
        _stdout.write(data)

    def cursor(self, pos, shape):
        self.control('\x1b[?25h\x1b[{} q'.format(shape))
        self._goto_yx(pos[0], pos[1])

    def cursor_off(self):
        self.control('\x1b[?25l')

    def control(self, data):
        _stdout.write(data)

    def flush(self):
        _stdout.flush()

CURSOR_BLINKING_BLOCK = 1
CURSOR_STEADY_BLOCK = 2
CURSOR_BLINKING_UNDERLINE = 3
CURSOR_STEADY_UNDERLINE = 4
CURSOR_BLINKING_BAR = 5
CURSOR_STEADY_BAR = 6


class screenbuf:
    def __init__(self, parent, scr: screen, height, width, row_offset=0, col_offset=0, focused=False):
        self.parent = parent
        self.scr = scr
        self.height = height
        self.width = width
        self.row_offset = row_offset
        self.col_offset = col_offset
        self.focused = focused
        self.cursor_pos = None
        self.cursor_shape = CURSOR_BLINKING_BLOCK

    def put_at(self, row, col, string, control=None):
        row = fix_list_index(row, self.height)
        col = fix_list_index(col, self.width)

        # limit string length
        string = string[:self.width - col]
        
        if control:
            self.scr.control(control)
        self.scr.put_at(row + self.row_offset, col + self.col_offset, string)
    
    def control(self, control):
        self.scr.control(control)

    def is_focused(self):
        return self.is_focused and (self.parent is None or self.parent.is_focused())

    def subbuf(self, row=0, col=0, height=None, width=None):
        
        row = fix_list_index(row, self.height)
        col = fix_list_index(col, self.width)        
        
        if height is None:
            height = self.height - row

        if width is None:
            width = self.width - col

        height = fix_list_index(height, self.height)
        width = fix_list_index(width, self.width)

        return screenbuf(self, self.scr, height, width, self.row_offset + row, self.col_offset + col)

    def focus(self, value=True):
        self.focused = value
        self._update_cursor()

        return self

    def cursor(self, row, col, shape=None):
        row = fix_list_index(row, self.height)
        col = fix_list_index(col, self.width)
        self.cursor_pos = (row, col)
        if shape is not None:
            self.cursor_shape = shape
        self._update_cursor()

    def cursor_off(self):
        self.cursor_pos = None
        self._update_cursor()
        
    def _update_cursor(self):
        if self.is_focused():
            if self.cursor_pos:    
                self.scr.cursor(
                    (self.cursor_pos[0] + self.row_offset, 
                    self.cursor_pos[1] + self.col_offset),
                    self.cursor_shape
                ),
            else:
                self.scr.cursor_off()

    def clear(self):
        ws = ' ' * self.width
        for i in range(self.height):
            self.put_at(i, 0, ws)


    def relative(self, row, col):
        row = fix_list_index(row, self.height)
        col = fix_list_index(col, self.width)
        return row + self.row_offset, col + self.col_offset

