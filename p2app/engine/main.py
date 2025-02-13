# p2app/engine/main.py
#
# ICS 33 Winter 2025
# Project 2: Learning to Fly
#
# An object that represents the engine of the application.
#
# This is the outermost layer of the part of the program that you'll need to build,
# which means that YOU WILL DEFINITELY NEED TO MAKE CHANGES TO THIS FILE.


from p2app.events import *
from p2app.engine import database_handler as dh
from p2app.engine import continent_handler as conh
from p2app.engine import country_handler as ch
from p2app.engine import region_handler as rh

class Engine:
    """An object that represents the application's engine, whose main role is to
    process events sent to it by the user interface, then generate events that are
    sent back to the user interface in response, allowing the user interface to be
    unaware of any details of how the engine is implemented.
    """

    def __init__(self):
        """Initializes the engine"""
        self._connection = dh.DatabaseHandler()
        self._continent_handler = conh.ContinentHandler(self._connection)
        self._country_handler = ch.CountryHandler(self._connection)
        self._region_handler = rh.RegionHandler(self._connection)



    def process_event(self, event):
        """A generator function that processes one event sent from the user interface,
        yielding zero or more events in response."""

        # This is a way to write a generator function that always yields zero values.
        # You'll want to remove this and replace it with your own code, once you start
        # writing your engine, but this at least allows the program to run.


        """
        database events
        """
        if isinstance(event, OpenDatabaseEvent):
            yield from self._connection.open_database(event.path())

        if isinstance(event, CloseDatabaseEvent):
            yield from self._connection.close_database()

        if isinstance(event, QuitInitiatedEvent):
            yield from EndApplicationEvent()

        """
        continent events
        """
        if isinstance(event, StartContinentSearchEvent):
            yield from self._continent_handler.start_continent_search(event)


        if isinstance(event, LoadContinentEvent):
            yield from self._continent_handler.load_continent_event(event)


        if isinstance(event, SaveNewContinentEvent):
            yield from self._continent_handler.save_new_continent_event(event)


        if isinstance(event, SaveContinentEvent):
            yield from self._continent_handler.save_continent_event(event)


        """
        country events
        """
        if isinstance(event, StartCountrySearchEvent):
            yield from self._country_handler.start_country_search_event(event)


        if isinstance(event, LoadCountryEvent):
            yield from self._country_handler.load_country_event(event)


        if isinstance(event, SaveNewCountryEvent):
            yield from self._country_handler.save_new_country_event(event)


        if isinstance(event, SaveCountryEvent):
            yield from self._country_handler.save_country_event(event)


        """
        region events
        """
        if isinstance(event, StartRegionSearchEvent):
            yield from self._region_handler.start_region_search_event(event)


        if isinstance(event, LoadRegionEvent):
            yield from self._region_handler.load_region_event(event)


        if isinstance(event, SaveNewRegionEvent):
            yield from self._region_handler.save_new_region_event(event)


        if isinstance(event, SaveRegionEvent):
            yield from self._region_handler.save_region_event(event)