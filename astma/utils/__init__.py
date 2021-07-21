

def fix_list_index(index, length):
    if index < -length or index > length:
        raise IndexError(index)

    if index < 0:
        index = length + index

    return index

def wrapper(fn):
    def helper(tgt):
        fn(tgt)
        return tgt

    return helper

def slack_call(f, *args):
    if f is None:
        return
    if isinstance(f, (list, tuple)):
        return [slack_call(subfun, *args) for subfun in f][-1]
    if (f.__code__.co_flags & 4) != 0:
        return f(*args)
    else:
        n = 1 if hasattr(f, '__self__') else 0
        return f(*args[:f.__code__.co_argcount - n])

def optcurry(argname):
    """optionaly curries the argument provided"""
    def wrap(fn):
        def wrapped(*args, **kwargs):
            if argname in kwargs:
                return fn(*args, **kwargs)
            else:
                return lambda tgt: fn(*args, **{**kwargs, argname: tgt})
        
        wrapped.__name__ = fn.__name__
        wrapped.__qualname__ = fn.__qualname__

        return wrapped


    return wrap