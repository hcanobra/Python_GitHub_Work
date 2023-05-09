import prestodb
from getpass import getpass
import pandas as pd

# static helper methods

class Connection:

    # Setup the connection. Username and password optional. If not supplied, will be asked for later on
    def __init__(self, username='', password=''):

        # Parameters used to setup the presto connection with the NDL databases
        host = 'ndl-presto.nss.vzwnet.com'
        port = 8385
        catalog = 'hive'
        http_scheme = 'https'

        if not username:
            #username = input("Username: ")
            username = 'canobhu'
        if not password:
            #password = getpass("Password: ")
            password = 'Tpztlan02VH$'

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

    # Closses the connection to NDL
    def close(self):
        self.presto_connection.close()

    # Takes an HQL (Hive Query language) query and returns a pandas dataframe filled with the data
    def hiveql_query_df(self, query):
        header_names = []

        print('Processing Hive Query... '+query)

        # process the query and get the data
        self.cursor.execute(query)
        data = self.cursor.fetchall()

        headers = self.cursor.description

        for header in headers:
            # each header has other meta data associated to
            # it like type, etc. Just get the name at index 0
            header_names.append(header[0])

        df = pd.DataFrame(data, columns=header_names)

        return (df)

    # Returns a dataframe containing the available databases in NDL
    def databases_df(self):
        query = 'show schemas'
        print('Print Schema')
        return self.hiveql_query_df(query)

    # Returns a dataframe containing the available tables for a given database in NDL
    def tables_df(self, schema):
        query = 'show tables from "' + schema + '"'
        return self.hiveql_query_df(query)

    # Returns a dataframe containing the available columns for a given table within a database in NDL
    def columns_df(self, schema, table):
        query = 'describe ' + schema + '.' + table
        return self.hiveql_query_df(query)

    # This is a dummy funciton that calls internally the Query function and retrives the result fo the query in NDL
    def commands(self,query):
        return self.hiveql_query_df(query())


    # Those are EXAMPLE functions JUST FOR TESTING

    def printing (self,query):
        print(query())
        self.hiveql_query_df(query())
        return (self)
    
