"""Module for containing the DBConnection class."""

import sqlite3


class DBConnection:
    """Creates a DBConnection object.

    Instance of this class is a singleton object, i.e., only one instance may
    be taken from this class.

    Note that this class should be only instantiated with context manager.

        :params
            db_url      ->  absolute path of the db file, as a string; if not
                            exists, will be created automatically.
    """

    _db = None
    _instance = None
    _conn = None
    _cursor = None

    def __init__(self, db_url):
        type(self)._db = db_url
        try:
            self._connect()
        except sqlite3.DatabaseError as e:
            print('Error: %s' % e)

    def __enter__(self):
        # Makes sure the connection is obtained.
        return self.instance

    def __exit__(self, exc_type, exc_value, traceback):
        # Makes sure the connection is safely closed.
        if self._conn:
            self._conn.commit()
            self._cursor.close()
            self._conn.close()
            self._instance = None

    @classmethod
    def _connect(cls):
        # Prepares the connection and cursor objects.
        cls._conn = sqlite3.connect(cls._db)
        cls._cursor = cls._conn.cursor()

    @property
    def instance(self):
        # Makes sure the class is instantiated only once.
        if not self._instance:
            self._instance = DBConnection(type(self)._db)
        return self._instance

    @staticmethod
    def group(query, group_by):
        # Manages GROUP BY syntax
        if query.endswith(";"):
            query = query[:-1]
        query += " GROUP BY " + ", ".join(group_by) + ";"
        return query

    @staticmethod
    def order(query, order_by):
        # Manages ORDER BY and DESC syntax
        if query.endswith(";"):
            query = query[:-1]
        query += " ORDER BY "
        fds = []
        for col in order_by:
            fd = "%s" % col['name']
            if col['desc']:
                fd += " DESC"
            fds.append(fd)
        query += ", ".join(fds) + ";"
        return query

    @staticmethod
    def put_limit(query, limit):
        # Manages LIMIT syntax
        if query.endswith(";"):
            query = query[:-1]
        query += " LIMIT %d;" % limit
        return query

    @staticmethod
    def put_offset(query, offset):
        # Manages OFFSET syntax
        if query.endswith(";"):
            query = query[:-1]
        query += " OFFSET %d;" % offset
        return query

    def create_table(self, table):
        """Creates table in database. Returns void.
            :params
                table   ->  Table object
        """
        query = "CREATE TABLE IF NOT EXISTS %s(%s);" % (table.name, table.desc)
        self._cursor.execute(query)

    def drop_table(self, table):
        """Drops table from database. Returns void.
            :params
                table   ->  Table object
        """
        query = "DROP TABLE IF EXISTS %s;" % table.name
        self._cursor.execute(query)

    def delete(self, table, col, val, limit=None, offset=None):
        """Deletes rows from table within given condition, limit and offset.
        Returns void.
            :params
                table   ->  name of the table, as a string
                col     ->  name of the column, as a string
                val     ->  value of the column
                limit   ->  optional; limit of rows to be deleted, as an
                            integer; defaults to None
                offset  ->  optional; offset of rows to be deleted, as an
                            integer; defaults to None
        """
        query = "DELETE FROM %s WHERE %s = :val;" % (table, col)
        if limit:
            query = self.put_limit(query, limit)
        if offset:
            query = self.put_offset(query, offset)
        self._cursor.execute(query, {'val': val})

    def update(self, table, cols, data, conds, vals, limit=None, offset=None):
        """Updates certain cells of certain rows in a table within given
        conditions, limit and offset. Returns void.
            :params
                table   ->  name of the table, as a string
                cols    ->  columns to be updated, as a list of strings
                data    ->  values columns to be set to, as a list of strings
                conds   ->  columns to be bounded, as a list of strings
                vals    ->  values columns bounded with, as a list
                limit   ->  optional; limit of rows to be updated, as an
                            integer; defaults to None
                offset  ->  optional; offset of rows to be updated, as an
                            integer; defaults to None
        """
        col_vals = [col + "col" for col in cols]
        cond_vals = [cond + "val" for cond in conds]
        changes = ", ".join([col + " = :" + col_val for col, col_val
                             in zip(cols, col_vals)])
        clause = " AND ".join([cond + " = :" + cond_val for cond, cond_val
                               in zip(conds, cond_vals)])
        query = "UPDATE %s SET %s WHERE %s;" % (table, changes, clause)
        if limit:
            query = self.put_limit(query, limit)
        if offset:
            query = self.put_offset(query, offset)
        plch = {**dict(zip(col_vals, data)), **dict(zip(cond_vals, vals))}
        self._cursor.execute(query, plch)

    def get_all(self, table, cols, conds=None, vals=None, group_by=None,
                order_by=None, limit=None, offset=None):
        """Fetches certain cells of certain rows in a table within given
        conditions, limit and offset, grouped by and ordered by any sets of
        columns. Returns a list of tuples.
            :params
                table       ->  name of the table, as a string
                cols        ->  columns to be fetched, as a list of strings
                conds       ->  optional; columns to be bounded, as a list of
                                strings; defaults to None
                vals        ->  optional; values columns bounded with, as a
                                list; defaults to None
                group_by    ->  optional; columns to be grouped by, as a list
                                of strings; defaults to None
                order_by    ->  optional; columns to be ordered by, as a list
                                of dictionaries; defaults to None
                limit       ->  optional; limit of rows to be fetched, as an
                                integer; defaults to None
                offset      ->  optional; offset of rows to be fetched, as an
                                integer; defaults to None
        """
        if conds:
            clause = " AND ".join([cond + " = :" + cond for cond in conds])
            clms = ", ".join(cols)
            query = "SELECT %s FROM %s WHERE %s;" % (clms, table, clause)
            plch = dict(zip(conds, vals))
            if group_by:
                query = self.group(query, group_by)
            if order_by:
                query = self.order(query, order_by)
            if limit:
                query = self.put_limit(query, limit)
            if offset:
                query = self.put_offset(query, offset)
            self._cursor.execute(query, plch)
        else:
            clms = ", ".join(cols)
            query = "SELECT %s FROM %s;" % (clms, table)
            if group_by:
                query = self.group(query, group_by)
            if order_by:
                query = self.order(query, order_by)
            if limit:
                query = self.put_limit(query, limit)
            if offset:
                query = self.put_offset(query, offset)
            self._cursor.execute(query)
        return self._cursor.fetchall()

    def get_first(self, table, cols,
                  conds=None, vals=None, group_by=None, first_col="ID"):
        """Fetches certain cells of the first row in a table within given
        conditions, grouped by and ordered by any sets of columns. Returns a
        tuple.
            :params
                table       ->  name of the table, as a string
                cols        ->  columns to be fetched, as a list of strings
                conds       ->  optional; columns to be bounded, as a list of
                                strings; defaults to None
                vals        ->  optional; values columns bounded with, as a
                                list; defaults to None
                group_by    ->  optional; columns to be grouped by, as a list
                                of strings; defaults to None
                first_col   ->  optional; index column, as a string; defaults
                                to "ID"
        """
        ord_dict = [{'name': first_col, 'desc': False}]
        return self.get_all(table, cols, conds, vals, group_by, ord_dict, 1)[0]

    def get_last(self, table, cols,
                 conds=None, vals=None, group_by=None, first_col="ID"):
        """Fetches certain cells of the last row in a table within given
        conditions, grouped by and ordered by any sets of columns. Returns a
        tuple.
            :params
                table       ->  name of the table, as a string
                cols        ->  columns to be fetched, as a list of strings
                conds       ->  optional; columns to be bounded, as a list of
                                strings; defaults to None
                vals        ->  optional; values columns bounded with, as a
                                list; defaults to None
                group_by    ->  optional; columns to be grouped by, as a list
                                of strings; defaults to None
                first_col   ->  optional; index column, as a string; defaults
                                to "ID"
        """
        ord_dict = [{'name': first_col, 'desc': True}]
        return self.get_all(table, cols, conds, vals, group_by, ord_dict, 1)[0]

    def insert(self, table, data, cols=None):
        """Inserts a row of data into the specified columns of a table. If
        no columns specified, insert a row of data into all of the columns.
        Returns void.
            :params
                table   ->  name of the table, as a string
                data    ->  values for columns, as a list
                cols    ->  optional; names of these columns; defaults to None
        """
        clause = ", ".join([":%s" % dat for dat in data])
        plch = dict(zip([str(dat) for dat in data], data))
        if cols:
            clms = ", ".join(cols)
            query = "INSERT INTO %s(%s) VALUES (%s);" % (table, clms, clause)
        else:
            query = "INSERT INTO %s VALUES (%s);" % (table, clause)
        self._cursor.execute(query, plch)
