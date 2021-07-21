
def _lens_get(obj, names):
    for name in names:
        obj = getattr(obj, name)
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
        return lens(self.__object, self.__names + (name,))
    
    def lens_get(self):
        return _lens_get(self.__object, self.__names)
    
    def lens_set(self, value):
        if not self.__names:
            raise NotImplementedError()
        *get_names, set_name = self.__names
        setattr(_lens_get(self.__object, get_names), set_name, value)