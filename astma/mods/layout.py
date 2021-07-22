from ..lens import lens
from typing import List
from astma.events import event
from astma.screen import screenbuf
from .mod import mod


class layout(mod):
    state_save = ('cur_focus', )

    def __init__(self, grid, widths=None, heights=None, cur_focus=None, label=None):
        super().__init__(label)
        self.grid = grid
        self.widths = widths,
        self.heights = heights
        self.cur_focus = lens(cur_focus or (0, 0))
        self._bufs = None

    def render(self, buf: screenbuf, ev: event):
        if self._bufs is None:
            self.relayout(buf)

        for row_idx, (row, buf_row) in enumerate(zip(self.grid, self._bufs)):
            for col_idx, (cell, subbuf) in enumerate(zip(row, buf_row)):
                subbuf.focus((row_idx, col_idx) == self.cur_focus)
                cell(subbuf, ev)

    def relayout(self, buf: screenbuf):
        heights = self._calculate_dims(
            buf.height, len(self.grid), self.heights)
        self._bufs = []

        cur_row = 0
        for row, h in zip(self.grid, heights):
            widths = self._calculate_dims(buf.width, len(row), None)
            cur_col = 0
            cur_buf_row = []
            for w in widths:
                subbuf = buf.subbuf(cur_row, cur_col, h, w)
                cur_buf_row.append(subbuf)
                cur_col += w
            self._bufs.append(cur_buf_row)
            cur_row += h

    def _calculate_dims(self, total_size: int, num_entries: int, dims: List[int]):
        res = []
        remaining = total_size
        for i in range(num_entries):
            if dims and len(dims) > i:
                v = dims[i]
            else:
                v = remaining // (num_entries - i)
            if v > remaining:
                return None
            res.append(v)
            remaining -= v
        return res
