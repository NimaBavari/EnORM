class Label:
    """Docstring here."""

    def __init__(self, denotee, text):
        self.denotee = denotee
        self.text = text


class Key:
    """Docstring here."""

    def label(self, alias):
        return Label(self, alias)


class Record:
    """Docstring here."""

    pass
