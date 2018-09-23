import sqlite3
import os


class DatabaseLink:
    """
    A helper class which uses a string to open the corresponding database. Has helper functions to initialise the
    database when empty, and automatically closes the connection when the object goes out of scope.
    """

    def __init__(self, db_name):
        self.name = db_name
        self.path = 'C:\\Users\\Zachary\\Documents\\GitHub\\GW2-Market-Tracker-V2\\Databases\\'
        self.conn = self.connect()
        pass

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def connect(self):
        """
        Connect to the database and return the connection.

        Keyword arguments:
        test -- boolean flag to indicate whether or not to use the testing database (default False)
        """

        conn = sqlite3.connect(os.path.join(self.path, self.name + ".db"), check_same_thread=False)
        conn.row_factory = sqlite3.Row

        return conn

    def close(self):
        """Close the connection to the database."""
        self.conn.close()

    def initialize(self):
        """Initialize a database from the schema file."""
        with open(os.path.join(self.path, self.name + '_schema.sql'), mode='r') as f:
            self.conn.cursor().executescript(f.read())
            self.conn.commit()
        print('Initialized {}.db'.format(self.name))

    def commit(self):
        self.conn.commit()




