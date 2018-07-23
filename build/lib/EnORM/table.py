"""Module for containing the Table class."""

class Table:
    """Creates a Table object.

        :params
            name        ->  name of the Table object, as a string
            *args[]     ->  columns, as a list of Column objects
    """

    def __init__(self, name, *args):
        self.name = name
        self.args = args

    @property
    def desc(self):
        """Prepares the table description. Returns a string."""
        lines = []
        for arg in self.args:
            line = "%s %s" % (arg.col_name, arg.vartype.upper())
            if arg.vartype.upper() == "VARCHAR" and not arg.max_l:
                raise AttributeError('VARCHAR needs a max length')
            if arg.max_l:
                line += "(%s)" % str(arg.max_l)
            if arg.default:
                line += " DEFAULT %s" % str(arg.default)
            if not arg.null:
                line += " NOT NULL"
            if arg.unique:
                line += " UNIQUE"
            if arg.p_key:
                line += " PRIMARY KEY"
            if arg.autoinc:
                line += " AUTOINCREMENT"
            lines.append(line)
        return ', '.join(lines)
