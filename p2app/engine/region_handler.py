from p2app.events import *
import sqlite3

class RegionHandler:
    def __init__(self, connection):
        self._connection = connection


    def start_region_search_event(self, event):
        query_conditions = []
        injection_params = {}

        if event.region_code():
            query_conditions.append('region_code = :rgn_code')
            injection_params['rgn_code'] = event.region_code()

        if event.local_code():
            query_conditions.append('local_code = :lcl_code')
            injection_params['lcl_code'] = event.local_code()

        if event.name():
            query_conditions.append('name = :rgn_name')
            injection_params['rgn_name'] = event.name()

        query = 'SELECT * FROM region'
        if query_conditions:
            query += ' WHERE ' + ' AND '.join(query_conditions)

        cursor = self._connection.execute_queries(query, injection_params)

        while True:
            result = cursor.fetchone()
            if result is None:
                break
            yield RegionSearchResultEvent(Region(result[0], result[1], result[2], result[3],
                                                 result[4], result[5], result[6], result[7]))


    def load_region_event(self, event):
        try:
            cursor = self._connection.execute_queries('''SELECT *
                                        FROM region
                                        WHERE region_id = :id;''',
                                 {'id': event.region_id()})

            result = cursor.fetchone()
            if result:
                yield RegionLoadedEvent(Region(result[0], result[1], result[2], result[3],
                                           result[4], result[5], result[6], result[7]))
        except sqlite3.Error:
            yield ErrorEvent('FAILED TO LOAD REGION')


    def save_new_region_event(self, event):
        try:
            rgn_id, rgn_code, lcl_code, rgn_name, con_id, cntry_id, wiki_link, kywrds = event.region()
            kywrds = None if not kywrds or kywrds == '' else kywrds
            wiki_link = None if not wiki_link or wiki_link == '' else wiki_link

            self._connection.execute_queries('''INSERT INTO region (region_id, region_code, local_code, name, continent_id, country_id, wikipedia_link, keywords)
                                        VALUES (:region_id, :region_code, :local_code, :region_name, :continent_id, :country_id, :wikipedia_link, :keywords);''',
                                 {'region_id': rgn_id, 'region_code': rgn_code, 'local_code': lcl_code,
                                  'region_name': rgn_name, 'continent_id': con_id, 'country_id': cntry_id,
                                  'wikipedia_link': wiki_link, 'keywords': kywrds})
            self._connection.commit_connection()
            region = Region(rgn_id, rgn_code, lcl_code, rgn_name, con_id, cntry_id, wiki_link, kywrds)
            yield RegionSavedEvent(region)

        except sqlite3.Error:
            yield SaveRegionFailedEvent('FAILED TO SAVE NEW REGION')


    def save_region_event(self, event):
        try:
            rgn_id, rgn_code, lcl_code, rgn_name, con_id, cntry_id, wiki_link, kywrds = event.region()
            kywrds = None if not kywrds or kywrds == '' else kywrds
            wiki_link = None if not wiki_link or wiki_link == '' else wiki_link

            self._connection.execute_queries('''UPDATE region
                                        SET region_code = :rgn_code, local_code = :lcl_code, name = :rgn_name, 
                                            continent_id = :con_id, country_id = :cntry_id, wikipedia_link = :wiki_link, keywords = :kywrds
                                        WHERE region_id = :rgn_id;''',
                                 {'rgn_id': rgn_id, 'rgn_code': rgn_code, 'lcl_code': lcl_code,
                                  'rgn_name': rgn_name, 'con_id': con_id, 'cntry_id': cntry_id, 'wiki_link': wiki_link,
                                  'kywrds': kywrds})
            self._connection.commit_connection()
            region = Region(rgn_id, rgn_code, lcl_code, rgn_name, con_id, cntry_id, wiki_link, kywrds)
            yield RegionSavedEvent(region)

        except sqlite3.Error:
            yield SaveRegionFailedEvent('FAILED TO SAVE REGION')