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


from p2app.events import *
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
                yield DatabaseOpenFailedEvent('DATABASE DOES NOT EXIST')

        if isinstance(event, CloseDatabaseEvent):
            self._cursor.close()
            self._cursor = None
            self._connection = None
            yield DatabaseClosedEvent()

        if isinstance(event, QuitInitiatedEvent):
            yield EndApplicationEvent



        #Continent events
        if isinstance(event, StartContinentSearchEvent):
            if event.continent_code() and event.name():
                self._cursor.execute('''SELECT continent_id, continent_code, name
                                     FROM continent
                                     WHERE continent_code = :code and name = :name;''',
                        {'code': event.continent_code(), 'name': event.name()})
            elif event.continent_code():
                self._cursor.execute('''SELECT continent_id, continent_code, name
                                            FROM continent
                                            WHERE continent_code = :code''',
                                {'code': event.continent_code()})
            elif event.name():
                self._cursor.execute('''SELECT continent_id, continent_code, name
                                            FROM continent
                                            WHERE name = :name;''',
                                {'name': event.name()})

            while True:
                result = self._cursor.fetchone()
                if result is None:
                    break
                yield ContinentSearchResultEvent(Continent(result[0], result[1], result[2]))


        if isinstance(event, LoadContinentEvent):
            try:
                self._cursor.execute('''SELECT continent_id, continent_code, name
                                            FROM continent
                                            WHERE continent_id = :id;''',
                                {'id': event.continent_id()})

                result = self._cursor.fetchone()
                yield ContinentLoadedEvent(Continent(result[0], result[1], result[2]))
            except sqlite3.Error:
                yield ErrorEvent('FAILED TO LOAD CONTINENT')




        if isinstance(event, SaveNewContinentEvent):
            con_id, con_code, con_name = event.continent()
            try:
                self._cursor.execute('''INSERT INTO continent (continent_id, continent_code, name)
                                            VALUES (:c_id, :c_code, :name);''',
                                {'c_id': con_id, 'c_code': con_code, 'name': con_name})
                self._connection.commit()
                yield ContinentSavedEvent(event.continent())

            except sqlite3.Error:
                yield SaveContinentFailedEvent('FAILED TO SAVE NEW CONTINENT')


        if isinstance(event, SaveContinentEvent):
            con_id, con_code, con_name = event.continent()
            try:
                self._cursor.execute('''UPDATE continent
                                        SET continent_id = :c_id, continent_code = :c_code, name = :name
                                        WHERE continent = :c_id;''',
                                        {'c_id': con_id, 'c_code': con_name, 'name': con_name})
            except sqlite3.Error:
                yield SaveContinentFailedEvent('FAILED TO SAVE CONTINENT')



        #Country events
        if isinstance(event, StartCountrySearchEvent):
            if event.country_code() and event.name():
                self._cursor.execute('''SELECT country_id, country_code, name, continent_id, wikipedia_link, keywords
                                            FROM country
                                            WHERE country_code = :cntry_code and name = :name;''',
                                {'cntry_code': event.country_code(), 'name': event.name()})

            elif event.country_code():
                self._cursor.execute('''SELECT country_id, country_code, name, continent_id, wikipedia_link, keywords
                                            FROM country
                                            WHERE country_code = :code''',
                                     {'code': event.country_code()})

            elif event.name():
                self._cursor.execute('''SELECT country_id, country_code, name, continent_id, wikipedia_link, keywords
                                            FROM country
                                            WHERE name = :name''',
                                     {'name': event.name()})

            while True:
                result = self._cursor.fetchone()
                if result is None:
                    break
                yield CountrySearchResultEvent(Country(result[0], result[1], result[2], result[3],
                                                       result[4], result[5]))



        if isinstance(event, LoadCountryEvent):
            try:
                self._cursor.execute('''SELECT country_id, country_code, name, continent_id, wikipedia_link, keywords
                                            FROM country
                                            WHERE country_id = :id;''',
                                {'id': event.country_id()})

                result = self._cursor.fetchone()
                yield CountryLoadedEvent(Country(result[0], result[1], result[2], result[3],
                                                       result[4], result[5]))
            except sqlite3.Error:
                yield ErrorEvent('FAILED TO LOAD CONTINENT')


        if isinstance(event, SaveNewCountryEvent):
            try:
                cntry_id, cntry_code, cntry_name, con_id, wiki_link, kywrds = event.country()
                if kywrds == '':
                    kywrds = None
                self._cursor.execute('''INSERT INTO country (country_id, country_code, name, continent_id, wikipedia_link, keywords)
                                            VALUES (:cntry_id, :cntry_code, :cntry_name, :con_id, :wiki_link, :kywrds);''',
                                {'cntry_id': cntry_id, 'cntry_code': cntry_code, 'cntry_name': cntry_name, 'con_id': con_id, 'wiki_link': wiki_link, 'kywrds': kywrds})
                self._connection.commit()
                yield CountrySavedEvent(event.country())

            except sqlite3.Error:
                yield SaveCountryFailedEvent('FAILED TO SAVE NEW COUNTRY')


        if isinstance(event, SaveCountryEvent):
            pass


        #Region events
        if isinstance(event, StartRegionSearchEvent):
            pass

        if isinstance(event, LoadRegionEvent):
            pass

        if isinstance(event, SaveNewRegionEvent):
            pass

        if isinstance(event, SaveRegionEvent):
            pass