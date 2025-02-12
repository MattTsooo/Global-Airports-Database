# p2app/engine/main.py
#
# ICS 33 Winter 2025
# Project 2: Learning to Fly
#
# An object that represents the engine of the application.
#
# This is the outermost layer of the part of the program that you'll need to build,
# which means that YOU WILL DEFINITELY NEED TO MAKE CHANGES TO THIS FILE.
import p2app.events
from p2app.events.database import (OpenDatabaseEvent, DatabaseClosedEvent, CloseDatabaseEvent,
DatabaseOpenedEvent, DatabaseOpenFailedEvent)

from p2app.views.menus import FileMenu
from p2app.views import *
from p2app.events import *
from pathlib import Path
import sqlite3

class Engine:
    """An object that represents the application's engine, whose main role is to
    process events sent to it by the user interface, then generate events that are
    sent back to the user interface in response, allowing the user interface to be
    unaware of any details of how the engine is implemented.
    """

    def __init__(self):
        """Initializes the engine"""
        self._connection = None
        self._cursor = None



    def process_event(self, event):
        """A generator function that processes one event sent from the user interface,
        yielding zero or more events in response."""

        # This is a way to write a generator function that always yields zero values.
        # You'll want to remove this and replace it with your own code, once you start
        # writing your engine, but this at least allows the program to run.


        #Database events
        if isinstance(event, OpenDatabaseEvent):
            try:
                self._connection = sqlite3.connect(event.path())
                self._cursor = self._connection.cursor()
                self._cursor.execute('PRAGMA integrity_check')
                self._cursor.execute('PRAGMA foreign_keys = ON;')
                yield DatabaseOpenedEvent(event.path())
            except sqlite3.DatabaseError:
                yield DatabaseOpenFailedEvent('Database does not exist')

        if isinstance(event, CloseDatabaseEvent):
            self._cursor.close()
            self._cursor = None
            self._connection = None
            yield DatabaseClosedEvent()

        if isinstance(event, QuitInitiatedEvent):
            yield EndApplicationEvent



