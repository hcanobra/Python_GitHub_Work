# Python 3.8.2
# Date: 10.27.2021
# Author: Hugo Cano

# IMPORT LIBRARIES 
        #from sqlalchemy import create_engine
        #import mysql.connector
import simplekml
import pandas as pd
from sqlalchemy import text
import MySQLAPI

def c_query ():                         # Query Definition
    query = text("""
                SELECT DISTINCT(Site),
                Lat as lat,
                Lon as lon
                FROM vzw_escalations.escalation_locations
            """)
    return (query)

def c_query_cband_ready ():                         # Query Definition
    query = text("""
            SELECT 
            Projects_Site_name,
            Projects_atoll_site_latitude,
            Projects_atoll_site_longitude,
            concat(Projects_Fuze_project_id," / ",Project_Activation_Withdraw_Milestone_F," / ",Dashboar_C_Band_bucket)

            FROM vzw_sandbox.cband_ready
            """)
    return (query)

def c_query_cband_forecast ():                         # Query Definition
    query = text("""
            SELECT 
            Projects_Site_name,
            Projects_atoll_site_latitude,
            Projects_atoll_site_longitude,
            concat(Projects_Fuze_project_id," / ",Project_Activation_Withdraw_Milestone_F," / ",Dashboar_C_Band_bucket)

            FROM vzw_sandbox.cband_forecast
            """)
    return (query)

def c_DataFrame (query):                # Connection to MySQL and Execute Query
    cn = MySQLAPI.Connection()          # Open the Engine
    result = cn.mysql_query_df(query)   # Execute the query
    cn.mysql_close                      # Close the Engine
    return (result)

def c_klm_point (df):
    kml = simplekml.Kml()
    doc = kml.newdocument(name='Locations')
    print (df)
    print (len(df.index))

    i=0
    while i < len(df.index):
        pnt = doc.newpoint(name=df.iloc[i,0], coords=[(df.iloc[i,2],df.iloc[i,1])])  # lon, lat, optional height 
        pnt.description = df.iloc[i,3]       
        pnt.style.iconstyle.icon.href = 'https://maps.google.com/mapfiles/kml/paddle/orange-circle.png' #Icon of the place
        i=i+1
 
    kml.save("/Users/canobhu/Documents/GitHub/QGIS/KLM_Resources/Python_KLM.kml") 

# Begin

#query = c_query()

query = c_query_cband_forecast() # BUILDS KLM FILE FOR CBAND READY SITES

df = c_DataFrame (query)
c_klm_point (df)

#print (df)

# End



