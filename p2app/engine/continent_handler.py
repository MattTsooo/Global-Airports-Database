from p2app import *
import sqlite3

class ContinentHandler:
    def __init__(self, connection, event):
        self._connection = connection
        self._event = event
        self._cursor.execute('PRAGMA integrity_check')
        self._cursor.execute('PRAGMA foreign_keys = ON;')


    def