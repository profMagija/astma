
import typing

_marker = object()


def _lens_get(obj, names):
    for at, name in names:
        name = _unlens(name)
        if at == 'attr':
            obj = getattr(obj, name)
        elif at == 'item':
            obj = obj[name]
        else:
            raise ValueError('unknown access type: ' + at)
    return obj


def _unlens(o):
    if isinstance(o, lens):
        return o.lens_get()
    else:
        return o


class lens:
    def __init__(self, obj, names=()):
        if isinstance(obj, lens):
            self.__object = obj.__object
            self.__names = obj.__names + names
        else:
            self.__object = obj
            self.__names = names

    def __getattr__(self, name):
        return lens(self.__object, self.__names + (('attr', name),))

    def __getitem__(self, name):
        return lens(self.__object, self.__names + (('item', name),))

    def __setitem__(self, name, value):
        self[name].lens_set(value)

    def __delitem__(self, name):
        del self.lens_get()[_unlens(name)]

    def __delattr__(self, name):
        delattr(self.lens_get(), _unlens(name))

    def __str__(self):
        return str(self.__object)

    def __repr__(self):
        return '<lens ' + repr(self.__object) + '>'

    def __call__(self, *args, **kwargs):
        return self.__object(*args, **kwargs)
        
    def __eq__(self, other):
        return self.lens_get().__eq__(other)

    def __ne__(self, other):
        return self.lens_get().__ne__(other)

    def lens_get(self, default=_marker):
        try:
            return _lens_get(self.__object, self.__names)
        except KeyError:
            if default is _marker:
                raise
            return default

    def lens_set(self, value):
        if not self.__names:
            raise NotImplementedError()
        *get_names, (set_type, set_name) = self.__names
        parent = _lens_get(self.__object, get_names)
        if set_type == 'attr':
            setattr(parent, _unlens(set_name), value)
        elif set_type == 'item':
            parent[_unlens(set_name)] = value
        else:
            raise ValueError('unknown access type: ' + set_type)


class constant_lens(lens):
    def lens_set(self, value):
        pass


if typing.TYPE_CHECKING:
    _orig_lens = lens
    T = typing.TypeVar('T')
    def lens(x: T) -> typing.Union[T, _orig_lens]: ...
