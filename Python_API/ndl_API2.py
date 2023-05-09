from operator import concat
import prestodb
from getpass import getpass
import pandas as pd

# static helper methods

class Connection:

    # Setup the connection. Username and password optional. If not supplied, will be asked for later on
    def __init__(self, username='', password=''):

        if not username:
            username = "canobhu"
            #username = input("Username: ")
        if not password:
            password = "Tpztlan02VH("
            #password = getpass("Password: ")

        # Parameters used to setup the presto connection with the NDL databases
        # use port 443 when 8385 is blocked by firewall
        self.presto_connection = prestodb.dbapi.connect(
            host='ndl-presto.nss.vzwnet.com',
            port=8385,
            user=username,
            catalog='hive',
            http_scheme='https',
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
        
        data_rows1 = self.cursor.fetchmany(10000)
        data_rows2 = self.cursor.fetchmany(10000)
        
        df1 = pd.DataFrame(data_rows1)
        df2 = pd.DataFrame(data_rows2)
        
        y = 1
        
        #df1 = data_rows1
        frames = df1 

        if len(data_rows2) != 0:
            while len(data_rows2) != 0:            
                df3 = [frames,df2]
                frames = pd.concat(df3)
                                                
                print (y)
                data_rows2 = self.cursor.fetchmany(10000)
                df2 = pd.DataFrame(data_rows2)
                y = y+1

        frames = frames.sample(frac=0.50, replace=True, random_state=1)        
        
        headers = self.cursor.description

        for header in headers:
            # each header has other meta data associated to
            # it like type, etc. Just get the name at index 0
            header_names.append(header[0])

        frames.columns = header_names

        return (frames)

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
        return self.hiveql_query_df(query)


    # Those are EXAMPLE functions JUST FOR TESTING

    def printing (self,query):
        print(query())
        self.hiveql_query_df(query)
        return (self)
    
