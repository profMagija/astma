
from collections import defaultdict


class _obj:
    def __getattr__(self, name):
        return None

STATE_DICT = defaultdict(_obj)

def get_state(label):
    return STATE_DICT[label]

