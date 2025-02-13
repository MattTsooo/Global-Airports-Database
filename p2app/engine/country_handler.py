from p2app.events import *
import sqlite3

class CountryHandler:
    def __init__(self, connection):
        self._connection = connection

    def start_country_search_event(self, event):
        query_conditions = []
        injection_params = {}

        if event.country_code():
            query_conditions.append('country_code = :cntry_code')
            injection_params['cntry_code'] = event.country_code()

        if event.name():
            query_conditions.append('name = :cntry_name')
            injection_params['cntry_name'] = event.name()

        query = 'SELECT * FROM country'
        if query_conditions:
            query += ' WHERE ' + ' AND '.join(query_conditions)

        cursor = self._connection.execute_queries(query, injection_params)

        while True:
            result = cursor.fetchone()
            if result is None:
                break
            yield CountrySearchResultEvent(Country(result[0], result[1], result[2], result[3],
                                                   result[4], result[5]))


    def load_country_event(self, event):
        try:
            cursor = self._connection.execute_queries('''SELECT *
                                        FROM country
                                        WHERE country_id = :id;''',
                                 {'id': event.country_id()})

            result = cursor.fetchone()
            if result:
                yield CountryLoadedEvent(Country(result[0], result[1], result[2], result[3],
                                             result[4], result[5]))
        except sqlite3.Error:
            yield ErrorEvent('FAILED TO LOAD CONTINENT')


    def save_new_country_event(self, event):
        try:
            cntry_id, cntry_code, cntry_name, con_id, wiki_link, kywrds = event.country()
            kywrds = None if not kywrds or kywrds == '' else kywrds

            self._connection.execute_queries('''INSERT INTO country (country_id, country_code, name, continent_id, wikipedia_link, keywords)
                                        VALUES (:cntry_id, :cntry_code, :cntry_name, :con_id, :wiki_link, :kywrds);''',
                                 {'cntry_id': cntry_id, 'cntry_code': cntry_code, 'cntry_name': cntry_name,
                                  'con_id': con_id, 'wiki_link': wiki_link, 'kywrds': kywrds})
            self._connection.commit()
            country = Country(cntry_id, cntry_code, cntry_name, con_id, wiki_link, kywrds)
            yield CountrySavedEvent(country)

        except sqlite3.Error:
            yield SaveCountryFailedEvent('FAILED TO SAVE NEW COUNTRY')


    def save_country_event(self, event):
        try:
            cntry_id, cntry_code, cntry_name, con_id, wiki_link, kywrds = event.country()
            kywrds = None if not kywrds or kywrds == '' else kywrds

            self._connection.execute_queries('''UPDATE country
                                        SET country_code = :cntry_code, name = :cntry_name, continent_id = :con_id, wikipedia_link = :wiki_link, keywords = :kywrds
                                        WHERE country_id = :cntry_id;''',
                                 {'cntry_id': cntry_id, 'cntry_code': cntry_code, 'cntry_name': cntry_name,
                                  'con_id': con_id, 'wiki_link': wiki_link, 'kywrds': kywrds})
            self._connection.commit()
            country = Country(cntry_id, cntry_code, cntry_name, con_id, wiki_link, kywrds)
            yield SaveCountryEvent(country)

        except sqlite3.Error:
            yield SaveCountryFailedEvent('FAILED TO SAVE COUNTRY')
