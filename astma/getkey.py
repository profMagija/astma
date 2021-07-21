
from ._getch import getch as _getch
from . import keys

def _readnumber(default=1):
    c = _getch()
    num = ''

    while c in '0123456789':
        num += c
        c = _getch()

    return int(num) if len(num) > 0 else default, c 

"""vt sequences:
<esc>[1~    - Home        <esc>[16~   -             <esc>[31~   - F17
<esc>[2~    - Insert      <esc>[17~   - F6          <esc>[32~   - F18
<esc>[3~    - Delete      <esc>[18~   - F7          <esc>[33~   - F19
<esc>[4~    - End         <esc>[19~   - F8          <esc>[34~   - F20
<esc>[5~    - PgUp        <esc>[20~   - F9          <esc>[35~   - 
<esc>[6~    - PgDn        <esc>[21~   - F10         
<esc>[7~    - Home        <esc>[22~   -             
<esc>[8~    - End         <esc>[23~   - F11         
<esc>[9~    -             <esc>[24~   - F12         
<esc>[10~   - F0          <esc>[25~   - F13         
<esc>[11~   - F1          <esc>[26~   - F14         
<esc>[12~   - F2          <esc>[27~   -             
<esc>[13~   - F3          <esc>[28~   - F15         
<esc>[14~   - F4          <esc>[29~   - F16         
<esc>[15~   - F5          <esc>[30~   -             

xterm sequences:
<esc>[A     - Up          <esc>[K     -             <esc>[U     -
<esc>[B     - Down        <esc>[L     -             <esc>[V     -
<esc>[C     - Right       <esc>[M     -             <esc>[W     -
<esc>[D     - Left        <esc>[N     -             <esc>[X     -
<esc>[E     -             <esc>[O     -             <esc>[Y     -
<esc>[F     - End         <esc>[1P    - F1          <esc>[Z     -
<esc>[G     - Keypad 5    <esc>[1Q    - F2       
<esc>[H     - Home        <esc>[1R    - F3       
<esc>[I     -             <esc>[1S    - F4       
<esc>[J     -             <esc>[T     - 
"""

_ESCAPES = {i+1 : k for i, k in enumerate([
    keys.HOME, keys.INSERT, keys.DELETE, keys.END, keys.PAGEUP,
    keys.PAGEDOWN, keys.HOME, keys.END, None, keys.F0,
    keys.F1, keys.F2, keys.F3, keys.F4, keys.F5,
    None, keys.F6, keys.F7, keys.F8, keys.F9, 
    keys.F10, None, keys.F11, keys.F12, keys.F13,
    keys.F14, None, keys.F15, keys.F16, None,
    keys.F17, keys.F18, keys.F19, keys.F20
]) if k is not None} 

_ESCAPES.update({
    'A': keys.UP,
    'B': keys.DOWN,
    'C': keys.RIGHT,
    'D': keys.LEFT,
    'F': keys.END,
    'H': keys.HOME,
    'P': keys.F1,
    'Q': keys.F2,
    'R': keys.F3,
    'S': keys.F4,
})

_FOLDS = {
    127: keys.BACKSPACE, # yes
    10: keys.ENTER
}

def getkey():
    c = _getch()

    if c == '\x1b':
        c = _getch()
        if c == '[':
            
            key, c = _readnumber()
            if key == 27:
                # xterm style
                mods, c = _readnumber()
                key, c = _readnumber()
                return keys.keyinfo(key, mods=mods-1)
            else:
                mods = 1
                if c == ';':
                    mods, c = _readnumber()
            
                if c != '~':
                    mods = key
                    key = c

            return keys.keyinfo(_ESCAPES[key], mods=mods-1)
        else:
            return keys.keyinfo(ord(c), mods=keys.MOD_ALT)
        
    else:

        c = _FOLDS.get(ord(c), ord(c))
        if 128 <= c < 256:
            mods = keys.MOD_ALT
            c = c - 128
        else:
            mods = 0
        return keys.keyinfo(c, mods=mods)
            




