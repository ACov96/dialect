from macro import Macro

class Context:
    def __init__(self, parent=None, __path__=None):
        self.parent = parent
        self._context = {}
        self.ret_val = None
        self.__path__ = __path__ 
        self.macro = Macro()

    def get(self, key):
        if key in self._context:
            return self._context[key]
        elif self.parent is not None:
            return self.parent.get(key)
        else:
            return ('error', 'No key %s' % key)

    def set(self, key, value):
        self._context[key[1]] = value

    def flag_return(self, val):
        self.ret_val = val
