class Context:
    def __init__(self, parent=None):
        self.parent = parent
        self._context = {}

    def get(self, key):
        if key in self._context:
            return self._context[key]
        elif self.parent is not None:
            return self.parent.get(key)
        else:
            return ('error', 'No key %s' % key)

    def set(self, key, value):
        self._context[key[1]] = value
