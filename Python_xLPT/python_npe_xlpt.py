#!/usr/bin/env python3

import sys
from npe import ws
import pandas as pd
from datetime import date
import datetime

# adding Folder_2 to the system path
sys.path.append('/Users/canobhu/Documents/GitHub/GitHub/Python_API')
import PostgreSQL_API as pg


def c_xlpt ():
    
    print ("########## 1) Extracting data from xLPT ....")
    
    # Month abbreviation, day and year	
    today = date.today()
    d4 = today.strftime("%b_%d_%Y")
    
    df = ws.xlpt('ericsson', 'canobhu', 'DMPL_XLPT_ALL_VER2')
    
    print ('########## %s : Importing xLPT Report'%d4)
    print (df.head())
    
    df = pd.DataFrame(df)
    df.to_csv('/Users/canobhu/Downloads/xLPT_tmp/MTPL_all_%s.csv'%d4, index=False)
    
    c_new_records (df)

    return (df)

def c_new_records (df):

    print ("## 2) Adding new data to PostgreSQL new table ....")

    v_df = df
    
    Previous_Date = datetime.datetime.today() - datetime.timedelta(days=1)
    d1 = Previous_Date.strftime("%m/%d/%Y")   
    v_df['DAY'] = d1
    
    cn = pg.Connection('vzw_xlpt')
    cn.PostgreSQL_load_df ('MTPL_all2',v_df)

    print (v_df)
    return (v_df)

def c_postgresql_query_table (v_databasae):
    cn = pg.Connection(v_databasae)
    cn.PostgreSQL_Create_Table (q_posgresql_query())
    return()    

def q_posgresql_query ():

    print ("## 3) Creating new temporary teable, completing the join and removing temporary tables ....")

    v_query = ('''
               CREATE TABLE public."MTPL_all_temp" AS
                    select * from public."DMPL_XLPT_ALL_VER2"
                    union 
                    select * from public."MTPL_all2";
                    
                DROP TABLE IF EXISTS public."DMPL_XLPT_ALL_VER2";
                
                CREATE TABLE public."DMPL_XLPT_ALL_VER2" AS
                    SELECT * from public."MTPL_all_temp"
                    ORDER BY "DAY","HR","MARKET","ENODEB","EUTRANCELL";
                
                DROP TABLE IF EXISTS public."MTPL_all_temp";
                
                DROP TABLE IF EXISTS public."MTPL_all2";
                
                DELETE FROM public."DMPL_XLPT_ALL_VER2"
	                WHERE "HR" = '*';
                 
                UPDATE public."DMPL_XLPT_ALL_VER2" SET "MARKET" = 'MKT10'
                WHERE "MARKET" IN ('10','010');
                
                UPDATE public."DMPL_XLPT_ALL_VER2" SET "MARKET" = 'MKT11'
                WHERE "MARKET" IN ('11','011');
                
                UPDATE public."DMPL_XLPT_ALL_VER2" SET "MARKET" = 'MKT12'
                WHERE "MARKET" IN ('12','012');
                
                UPDATE public."DMPL_XLPT_ALL_VER2" SET "MARKET" = 'MKT13'
                WHERE "MARKET" IN ('13','013');
                
                DROP TABLE IF EXISTS Public."DMPL_XLPT_DAY";
                
                CREATE TABLE public."DMPL_XLPT_DAY" AS 
                SELECT 
                    "DAY",
                    "MARKET",
                    "ENODEB",
                    "SITE",
                    SUM ("Peak_#_UE_In_Connected_Mode") AS "Peak_#_UE_In_Connected_Mode",
                    AVG ("UE_DL_Throughput_Mbps") AS "UE_DL_Throughput_Mbps",
                    AVG ("Cell_Throughput_Mbps") AS "Cell_Throughput_Mbps",
                    AVG ("Cell_Availability") AS "Cell_Availability",
                    SUM ("SIP_SC_Call_Attempts") AS "SIP_SC_Call_Attempts",
                    SUM ("SIP_SC_Call_Completions") AS "SIP_SC_Call_Completions",
                    SUM ("SIP_SC_Short_Calls") AS "SIP_SC_Short_Calls",
                    /* Setup_Fail% */
                    (
                        (
                            (NULLIF((SUM(NULLIF("Setup_Fail%_Num",0) :: FLOAT)),0))
                        /
                            (NULLIF((SUM(NULLIF("Setup_Fail%_Den",0) :: FLOAT)),0))
                        )*100
                    )AS "Setup_Fail%",
                    /* Context_Drop% */
                    (
                        (
                            (NULLIF((SUM(NULLIF("Context_Drop%_Num",0) :: FLOAT)),0))
                        /
                            (NULLIF((SUM(NULLIF("Context_Drop%_Den",0) :: FLOAT)),0))
                        )*100
                    )AS "Context_Drop%",
                    /*RRC_Setup_Failure%*/
                    (		
                        (	
                            (NULLIF((SUM(NULLIF("RRC_Setup_Failure%_Num",0) :: FLOAT)),0))
                        /	
                            (NULLIF((SUM(NULLIF("RRC_Setup_Failure%_Den",0) :: FLOAT)),0))
                        )*100	
                    )AS "RRC_Setup_Failure%",
                    /*Bearer_Setup_Failure%*/		
                    (		
                        (	
                            (NULLIF((SUM(NULLIF("Bearer_Setup_Failure%_Num",0) :: FLOAT)),0))
                        /	
                            (NULLIF((SUM(NULLIF("Bearer_Setup_Failure%_Den",0) :: FLOAT)),0))
                        )*100	
                    )AS "Bearer_Setup_Failure%",
                    /*Bearer_Drop%*/		
                    (		
                        (	
                            (NULLIF((SUM(NULLIF("Bearer_Drop%_Num",0) :: FLOAT)),0))
                        /	
                            (NULLIF((SUM(NULLIF("Bearer_Drop%_Den",0) :: FLOAT)),0))
                        )*100	
                    )AS "Bearer_Drop%",
                    /*Context_Setup_Failure%*/		
                    (		
                        (	
                            (NULLIF((SUM(NULLIF("Context_Setup_Failure%_Num",0) :: FLOAT)),0))
                        /	
                            (NULLIF((SUM(NULLIF("Context_Setup_Failure%_Den",0) :: FLOAT)),0))
                        )*100	
                    )AS "Context_Setup_Failure%",
                    /*S1U_SIP_SC_CallSetupFailure%*/		
                    (		
                        (	
                            (NULLIF((SUM(NULLIF("SIP_SC_Call_Setup_Failures",0) :: FLOAT)),0))
                        /	
                            (NULLIF((SUM(NULLIF("SIP_SC_Call_Attempts",0) :: FLOAT)),0))
                        )*100	
                    )AS "S1U_SIP_SC_CallSetupFailure%",
                    /*S1U_SIP_SC_CallDrop%*/		
                    (		
                        (	
                            (NULLIF((SUM(NULLIF("SIP_SC_Call_Drops",0) :: FLOAT)),0))
                        /	
                            (NULLIF((SUM(NULLIF("SIP_SC_Call_Completions",0) :: FLOAT)),0))
                        )*100	
                    )AS "S1U_SIP_SC_CallDrop%",

                    SUM ("Downlink_Data_Volume_MB_Test") AS "Downlink_Data_Volume_MB_Test",
                    AVG ("Downlink_Throughput_in_Mbps") AS "Downlink_Throughput_in_Mbps",
                    SUM ("DL_Data_Vol_MAC_in_MB") AS "DL_Data_Vol_MAC_in_MB",
                    SUM ("UL_Data_Vol_MAC_in_Mb") AS "UL_Data_Vol_MAC_in_Mb"


                FROM public."DMPL_XLPT_ALL_VER2"


                WHERE 
                    "FREQ" IS NOT NULL


                GROUP BY 
                        "ENODEB",
                        "DAY",
                        "MARKET",
                        "SITE"
                ORDER BY
                    "DAY",
                    "ENODEB";
                ''')
    
    return(v_query)

#/Begin

c_xlpt ()
#v_df = c_csv ()
c_postgresql_query_table ('vzw_xlpt')

#/End





