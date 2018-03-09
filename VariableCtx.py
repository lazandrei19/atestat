class VariableCTX:
    values = []
    keys = []

    def get_index(self, key):
        if key in self.keys:
            return len(self.keys) - self.keys[::-1].index(key) - 1
        return None

    def get(self, key):
        i = self.get_index(key)
        if i is not None:
            return self.values[i]
        else:
            return None

    def init(self, key, value):
        self.keys.append(key)
        self.values.append(value)

    def set(self, key, value):
        i = self.get_index(key)
        if i is not None:
            self.values[i] = value
        else:
            self.init(key, value)

    def remove(self, key):
        i = self.get_index(key)
        if i is not None:
            self.values.pop(i)
            self.keys.pop(i)

    def get_keys(self):
        return self.keys
