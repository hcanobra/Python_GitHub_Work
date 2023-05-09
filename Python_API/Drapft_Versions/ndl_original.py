import prestodb
from getpass import getpass
import pandas as pd
from ndl.utils import perf

# static helper methods


# Used for extracting the column names (headers) for a particular query
def get_header_names(headers):
    header_names = []
    for header in headers:
        # each header has other meta data associated to
        # it like type, etc. Just get the name at index 0
        header_names.append(header[0])
    return header_names


class Connection:

    # Setup the connection. Username and password optional. If not supplied, will be asked for later on
    def __init__(self, username='', password=''):

        # Parameters used to setup the presto connection with the NDL databases
        host = 'ndl-presto.nss.vzwnet.com'
        port = 8385
        catalog = 'hive'
        http_scheme = 'https'

        if not username:
            username = input("Username: ")
        if not password:
            password = getpass("Password: ")

        self.presto_connection = prestodb.dbapi.connect(
            host=host,
            port=port,
            user=username,
            catalog=catalog,
            http_scheme=http_scheme,
            auth=prestodb.auth.BasicAuthentication(username, password)
        )

        # This is used later to execute queries and such
        self.cursor = self.presto_connection.cursor()

    def close(self):
        self.presto_connection.close()

    # Takes an HQL (Hive Query language) query and returns a pandas dataframe filled with the data
    def hiveql_query_df(self, query):
        print('Processing Hive Query: ' + query)

        # start measuring the performance of the query
        measure = perf.Measure()

        # process the query and get the data
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        columns = get_header_names(self.cursor.description)
        df = pd.DataFrame(data, columns=columns)

        # measure the query performance time
        measure.stop_and_print_measure()

        return df

    # Returns a dataframe containing the available databases in NDL
    def databases_df(self):
        query = 'show schemas'
        return self.hiveql_query_df(query)

    # Returns a dataframe containing the available tables for a given database in NDL
    def tables_df(self, schema):
        query = 'show tables from "' + schema + '"'
        return self.hiveql_query_df(query)

    # Returns a dataframe containing the available columns for a given table within a database in NDL
    def columns_df(self, schema, table):
        query = 'describe ' + schema + '.' + table
        return self.hiveql_query_df(query)
