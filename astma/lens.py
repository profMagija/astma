
import typing


def _lens_get(obj, names):
    for at, name in names:
        if type(name) is lens:
            name = name.lens_get()
        if at == 'attr':
            obj = getattr(obj, name)
        elif at == 'item':
            obj = obj[name]
        else:
            raise ValueError('unknown access type: ' + at)
    return obj


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

    def lens_get(self):
        return _lens_get(self.__object, self.__names)

    def lens_set(self, value):
        if not self.__names:
            raise NotImplementedError()
        *get_names, (set_type, set_name) = self.__names
        if set_type == 'attr':
            setattr(_lens_get(self.__object, get_names), set_name, value)
        elif set_type == 'item':
            _lens_get(self.__object, get_names)[set_name] = value
        else:
            raise ValueError('unknown access type: ' + set_type)


if typing.TYPE_CHECKING:
    _orig_lens = lens
    T = typing.TypeVar('T')
    def lens(x: T) -> typing.Union[T, _orig_lens]: ...
