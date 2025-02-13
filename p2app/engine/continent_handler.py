from p2app.events import *
import sqlite3
import database_handler

class ContinentHandler:
    def __init__(self, connection):
        self._connection = connection



    def start_continent_search(self, event):
        query_conditions = []
        injection_params = {}

        if event.continent_code():
            query_conditions.append('continent_code = :con_code')
            injection_params['con_code'] = event.continent_code()

        if event.name():
            query_conditions.append('name = :con_name')
            injection_params['con_name'] = event.name()

        query = 'SELECT * FROM continent'
        if query_conditions:
            query += ' WHERE ' + ' AND '.join(query_conditions)

        cursor = self._connection.execute_queries(query, injection_params)

        while True:
            result = cursor.fetchone()
            if result is None:
                break
            yield ContinentSearchResultEvent(Continent(result[0], result[1], result[2]))


    def load_continent_event(self, event):
        try:
            cursor = self._connection.execute_queries('''SELECT *
                                            FROM continent
                                            WHERE continent_id = :id;''',
                                {'id': event.continent_id()})
            result = cursor.fetchone()
            if result:
                yield ContinentLoadedEvent(Continent(result[0], result[1], result[2]))

        except sqlite3.Error:
            yield ErrorEvent('FAILED TO LOAD CONTINENT')


    def save_new_continent_event(self, event):
        try:
            con_id, con_code, con_name = event.continent()
            self._connection.execute_queries('''INSERT INTO continent (continent_id, continent_code, name)
                                        VALUES (:c_id, :c_code, :name);''',
                                 {'c_id': con_id, 'c_code': con_code, 'name': con_name})
            self._connection.commit_connection()
            yield ContinentSavedEvent(event.continent())

        except sqlite3.Error:
            yield SaveContinentFailedEvent('FAILED TO SAVE NEW CONTINENT')


    def save_continent_event(self, event):
        try:
            con_id, con_code, con_name = event.continent()
            self._connection.execute_queries('''UPDATE continent
                                    SET continent_code = :c_code, name = :name
                                    WHERE continent_id = :c_id;''',
                                 {'c_id': con_id, 'c_code': con_code, 'name': con_name})
            self._connection.commit_connection()
            yield ContinentSavedEvent(event.continent())

        except sqlite3.Error:
            yield SaveContinentFailedEvent('FAILED TO SAVE CONTINENT')