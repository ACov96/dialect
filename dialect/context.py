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

    def check(self, identifier):
        if identifier[1] in self._context or (self.parent is not None and self.parent.check(identifier)):
            return ('bool', True)
        return ('bool', False)

    def delete(self, identifier):
        if identifier[1] in self._context:
            del self._context[identifier[1]]
        elif self.parent is not None and self.parent.check(identifier):
            self.parent.delete(identifier)
