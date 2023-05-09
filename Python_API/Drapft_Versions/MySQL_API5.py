# Python 3.8.2
# Date: 10.27.2021
# Author: Hugo Cano

# IMPORT LIBRARIES 
from sqlalchemy import create_engine
#from sqlalchemy import text
from getpass import getpass
import pandas as pd



# static helper methods
class Connection:

    # Setup the connection. Username and password optional. If not supplied, will be asked for later on
    def __init__(self):

        v_databasae = 'vzw_sandbox'
        self.engine = create_engine("mysql+pymysql://{user}:{pw}@10.141.219.198/{db}"
                            .format(user="dba",
                                    pw="Tpztlan02VH",
                                    db=v_databasae))

    # Execute query
    def mysql_query_df(self, query):
        print('Processing MySQL Query... ', query)

        v_result = self.engine.execute(query)   # Execute the query, calls itself to open the Engine
        df = pd.DataFrame(v_result)             # Convert the result into DataFrame

        df.columns = v_result.keys()            # Add column names to the DataFrame

        return (df)

    def mysql_close(self):
        self.engine.close()                     # Close the connection to the Engine


    def mysql_load_df(self,v_table,v_data):
        #v_data = pd.DataFrame(v_data)
        v_data.self.to_sql(v_table, con = self.engine, if_exists = 'replace', index=False)

    # Closses the connection to NDL
    def close(self):
        self.engine.close()