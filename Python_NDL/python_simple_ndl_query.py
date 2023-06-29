# importing sys
import sys
# adding Folder_2 to the system path
sys.path.append('/Users/canobhu/Documents/GitHub/Python_GitHub_Work/Python_API')


import warnings
warnings.filterwarnings("ignore")

from sqlalchemy import create_engine
from sqlalchemy import text

from operator import concat
import prestodb
from getpass import getpass
import pandas as pd



class Connection:

    # Setup the connection. Username and password optional. If not supplied, will be asked for later on
    def __init__(self, username='', password=''):

        if not username:
            username = "canobhu"
            #username = input("Username: ")
        if not password:
            password = "Tpztlan02VH+"
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

        self.presto_connection._http_session.verify = False
        
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
        
        data_rows1 = self.cursor.fetchall()
        
        df1 = pd.DataFrame(data_rows1)

        frames = df1 

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
    

def q_NDL_Query_Sample ():
    v_sql_commands = ('''              
                    
                    SELECT 

                        environment, 

                        end_location_lat, end_location_lon, 

                        make, model, service_type, start_m_tmsi, start_time,

                        s1_release_cause, 
                         
                        final_disposition, 
                        start_cell, end_cell, 

                        start_enb, end_enb, 
                        enb_cfcq, end_earfcn_dl, 
                        ta_distance_meters, 

                        mean_cqi,  qci_list,  last_cqi, 

                        rsrp_dbm, rsrq_db, pusch_sinr_db, mean_ul_sinr_db, 
                        n1_rsrp_dbm, n2_rsrp_dbm, n3_rsrp_dbm,
                        
                        nr_serving_cell, nr_serving_pci, nr_serving_arfcn, 
                        nr_last_measurement_cell, nr_last_measurement_pci, nr_last_measurement_arfcn, 
                        nr_rsrp_dbm, nr_rsrq_db, nr_dl_sinr_db, 
                        
                        ue_power_headroom_db, 
                        imei, imsi, 

                        confidence, 
                        
                        
                        hr, submkt
                    
                    FROM truecall_hive_views.f_truecall_lsr_raw_v1
                    WHERE 

                        submkt = 'UPNY'
                        AND end_location_lat BETWEEN 40.21 AND 40.22
                        AND end_location_lon BETWEEN -76.79 AND -76.78 
                        
                        AND confidence IN ('High','Medium') 
                        AND rsrp_dbm < -124 
                        AND make IN ('APPLE','SAMSUNG','GOOGLE','MOTOROLA','LG') 
                        AND rsrp_dbm is not null 
                        AND rsrp_dbm is not null
                    
                    LIMIT 1

                    ''')
    return (v_sql_commands)

def c_NDL_Query_Sample ():
    cn = Connection()
    
    v_data = cn.commands(q_NDL_Query_Sample())
    
    print (v_data)
    
    #v_data.to_csv ('/Users/canobhu/Documents/truecall_UPNY.csv')

    cn.close
    
    return ()

# // Begining

c_NDL_Query_Sample ()

# // End
