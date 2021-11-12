Integer = int
Float = float


class String(str):
    def __init__(self, length=None):
        self.length = length
        if self.length is not None and not isinstance(self.length, int):
            raise TypeError("String type should have an integer length.")
