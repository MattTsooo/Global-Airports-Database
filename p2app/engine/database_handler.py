import sqlite3
from p2app.events import *

class DatabaseHandler:
    def __init__(self):
        self._connection = None
        self._cursor = None


    def open_database(self, path):
        try:
            self._connection = sqlite3.connect(path)
            self._cursor = self._connection.cursor()
            self._cursor.execute('PRAGMA integrity_check')
            self._cursor.execute('PRAGMA foreign_keys = ON;')
            return DatabaseOpenedEvent(path)

        except sqlite3.DatabaseError:
            return DatabaseOpenFailedEvent('DATABASE IS INVALID')


    def close_database(self):
        if self._cursor:
            self._cursor.close()
        self._connection = None
        return DatabaseClosedEvent()


    def execute_queries(self, query, params = None):
        if not self._cursor:
            raise sqlite3.Error('NO CURRENT DATABASE CONNECTION')
        self._cursor.execute(query, params or {})
        return self._cursor


    def commit_connection(self):
        if self._connection:
            self._connection.commit()