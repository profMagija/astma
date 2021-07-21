from typing import List
from astma.events import event
from astma.screen import screenbuf
from .mod import mod


class layout(mod):
    state_save = ('cur_focus', )

    def __init__(self, grid, widths=None, heights=None):
        self.grid = grid
        self.widths = widths,
        self.heights = heights
        self.cur_focus = (0, 0)

    def render(self, buf: screenbuf, ev: event):
        heights = self._calculate_dims(
            buf.height, len(self.grid), self.heights)

        cur_row = 0
        for row_idx, (row, h) in enumerate(zip(self.grid, heights)):
            widths = self._calculate_dims(buf.width, len(row), None)
            cur_col = 0
            for col_idx, (cell, w) in enumerate(zip(row, widths)):
                subbuf = buf.subbuf(
                    cur_row, cur_col, h, w,
                    focused=(row_idx, col_idx) == self.cur_focus
                )
                cell(subbuf, ev)
                cur_col += w
            cur_row += h

    def _calculate_dims(self, total_size: int, num_entries: int, dims: List[int]):
        res = []
        remaining = total_size
        for i in range(num_entries):
            res.append(remaining // (num_entries - i))
        return res
