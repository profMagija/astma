
def sgr(*args):
    return '\x1b[' + ';'.join(str(x) for x in args) + 'm'

RESET = sgr(0)

BLACK_FG = sgr(30)
RED_FG = sgr(31)
GREEN_FG = sgr(32)
YELLOW_FG = sgr(33)
BLUE_FG = sgr(34)
MAGENTA_FG = sgr(35)
CYAN_FG = sgr(36)
WHITE_FG = sgr(37)

BLACK_BG = sgr(40)
RED_BG = sgr(41)
GREEN_BG = sgr(42)
YELLOW_BG = sgr(43)
BLUE_BG = sgr(44)
MAGENTA_BG = sgr(45)
CYAN_BG = sgr(46)
WHITE_BG = sgr(47)