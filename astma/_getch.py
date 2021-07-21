try:
    from msvcrt import getch
    def getch_init():
        pass
    def getch_finalize():
        pass
except ImportError:
    import sys
    import tty
    import termios
        
    def getch_init():
        global fd, old, dbg_file
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        tty.setraw(fd)
        dbg_file = open('./getch_debug.txt', 'w')

    def getch_finalize():
        termios.tcsetattr(fd, termios.TCSADRAIN, old)
        dbg_file.close()

    def getch():
        """
        Gets a single character from STDIO.
        """
        c = sys.stdin.read(1)
        dbg_file.write(f'{ord(c):3} {repr(c)}\n')
        return c

__all__ = ['getch_init', 'getch', 'getch_finalize']