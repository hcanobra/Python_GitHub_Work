"""


f_PostgreSQL_open

f_PostgreSQL_close
    conn

f_postgreSQL_inport 
    v_data
    v_table
    v_conn

q_NDL_Fuze_PROJ_Query


c_NDL_Query


"""

# importing sys
import sys
# adding Folder_2 to the system path
sys.path.append('/Users/canobhu/Documents/GitHub/GitHub/Python_API')


import ndl_API as ndl
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import text
import time


def f_PostgreSQL_open ():
  
    engine = create_engine("postgresql+psycopg2://postgres:Tpztlan02VH@localhost/vzw_xlpt")
    conn = engine.connect()

    return(conn)

def f_PostgreSQL_close (conn):
    conn.close()
    return ()

def f_postgreSQL_inport (v_data, v_table, v_conn):
    
    v_data.to_sql(v_table, con = v_conn, if_exists = 'replace', index=False)
    return()

def q_NDL_5GPT_Query ():
    v_sql_commands = ('''
                        SELECT *
                        FROM "5gpt".hourly_ericsson_5gnr_3gpp

                        WHERE  
                            to_date(trans_dt, 'yyyymmdd')  between to_date('20220118', 'yyyymmdd') and current_date
                            AND
                            "region" in ('Mountain','Kansas/Missouri')
                            AND
                            (
                            site like '4G5G%'
                            OR
                            gnb in (
                                '0137238',
                                '0127057',
                                '0137346',
                                '0137147',
                                '0127031',
                                '0137457',
                                '0137137',
                                '0127039',
                                '0127075',
                                '0127049',
                                '0127136',
                                '0127139',
                                '0127300',
                                '0137272',
                                '0127064',
                                '0127081',
                                '0137112',
                                '0127348',
                                '0137452',
                                '0127026',
                                '0137260',
                                '0137244',
                                '0127060',
                                '0127096',
                                '0137257',
                                '0137099',
                                '0127059',
                                '0127277',
                                '0127374',
                                '0137176',
                                '0137177',
                                '0127051',
                                '0137253',
                                '0127383',
                                '0137135',
                                '0137165',
                                '0137129',
                                '0137280',
                                '0127216',
                                '0127227',
                                '0127337',
                                '0137113',
                                '0127321',
                                '0127387',
                                '0127118',
                                '0127037',
                                '0127237',
                                '0127292',
                                '0137086',
                                '0127347',
                                '0127104',
                                '0137236',
                                '0137297',
                                '0127065',
                                '0137161',
                                '0127322',
                                '0127225',
                                '0137298'
                                )
                            )

                ''')
    return (v_sql_commands)
    
def c_NDL_Query (v_query,v_table):
    cn = ndl.Connection()
    
    v_data = cn.commands(v_query)
    print (v_data.head())

    v_conn = f_PostgreSQL_open()
    f_postgreSQL_inport (v_data, v_table, v_conn)
    f_PostgreSQL_close (v_conn)
    

    cn.close
    
    return ()


# // Begining


c_NDL_Query (q_NDL_5GPT_Query(),'hourly_ericsson_5gnr_3gpp')


# // End



""" Some Query Samples:

select * from public.hourly_ericsson_5gnr_3gpp
ORDER BY 
	TO_DATE ("day", 'MM/DD/YYYY'), "hr"

select
	TO_DATE ("day", 'MM/DD/YYYY') AS "Date",
	"site",
	"region",
	SUM(NULLIF("5gnr_peak_numof_ue",'') :: FLOAT) AS "5gnr_peak_numof_ue",
	(NULLIF((SUM(NULLIF("5gnr_endc_setup_failure_num",'') :: FLOAT)),0) / NULLIF((SUM(NULLIF("5gnr_endc_setup_failure_den",'') :: FLOAT)),0))*100 AS "5gnr_endc_setup_failure_pct",
	
	(NULLIF((SUM(NULLIF("5gnr_addition_failure_num",'') :: FLOAT)),0) / NULLIF((SUM(NULLIF("5gnr_addition_failure_den",'') :: FLOAT)),0))*100 AS "5gnr_addition_failure_pct",
	
	(NULLIF((SUM(NULLIF("5gnr_endc_drop_num",'') :: FLOAT)),0) / NULLIF((SUM(NULLIF("5gnr_endc_drop_den",'') :: FLOAT)),0))*100 AS "5gnr_endc_drop_pct",

	(((64.0*(NULLIF((AVG(NULLIF("pmmacvoldldrb",'') :: FLOAT)),0)))/(NULLIF((AVG(NULLIF("pmmactimedldrb",'') :: FLOAT)),0)))/1000.0 )AS "5GNR_DL_UE_MAC_Throughput_Mbps_19Q3",
	(((64.0*(NULLIF((AVG(NULLIF("pmmacvolulresue",'') :: FLOAT)),0)))/(NULLIF((AVG(NULLIF("pmmactimeulresue",'') :: FLOAT)),0)))/1000.0 )AS "5GNR_UL_MAC_UE_Throughput_Mbps_19Q3"

from public.hourly_ericsson_5gnr_3gpp
WHERE TO_DATE ("day", 'MM/DD/YYYY') = '2022-01-19'
      AND "region" in ('Mountain','Kansas/Missouri')
group by 
	"day",
	"site",
	"region"

ORDER BY 
	(((64.0*(NULLIF((AVG(NULLIF("pmmacvoldldrb",'') :: FLOAT)),0)))/(NULLIF((AVG(NULLIF("pmmactimedldrb",'') :: FLOAT)),0)))/1000.0 )  DESC ,
	TO_DATE ("day", 'MM/DD/YYYY')
	
	
############################################################

select
	TO_DATE ("day", 'MM/DD/YYYY') AS "Date",
	"hr",
	"region",

	SUM(NULLIF("5gnr_peak_numof_ue",'') :: FLOAT) AS "5gnr_peak_numof_ue",
	(NULLIF((SUM(NULLIF("5gnr_endc_setup_failure_num",'') :: FLOAT)),0) / NULLIF((SUM(NULLIF("5gnr_endc_setup_failure_den",'') :: FLOAT)),0))*100 AS "5gnr_endc_setup_failure_pct",
	
	(NULLIF((SUM(NULLIF("5gnr_addition_failure_num",'') :: FLOAT)),0) / NULLIF((SUM(NULLIF("5gnr_addition_failure_den",'') :: FLOAT)),0))*100 AS "5gnr_addition_failure_pct",
	
	(NULLIF((SUM(NULLIF("5gnr_endc_drop_num",'') :: FLOAT)),0) / NULLIF((SUM(NULLIF("5gnr_endc_drop_den",'') :: FLOAT)),0))*100 AS "5gnr_endc_drop_pct",

	(((64.0*(NULLIF((AVG(NULLIF("pmmacvoldldrb",'') :: FLOAT)),0)))/(NULLIF((AVG(NULLIF("pmmactimedldrb",'') :: FLOAT)),0)))/1000.0 )AS "5GNR_DL_UE_MAC_Throughput_Mbps_19Q3",
	(((64.0*(NULLIF((AVG(NULLIF("pmmacvolulresue",'') :: FLOAT)),0)))/(NULLIF((AVG(NULLIF("pmmactimeulresue",'') :: FLOAT)),0)))/1000.0 )AS "5GNR_UL_MAC_UE_Throughput_Mbps_19Q3"
	
from public.hourly_ericsson_5gnr_3gpp
WHERE "region" in ('Mountain','Kansas/Missouri')
group by 
	"day",
	"hr",
	"region"
ORDER BY 
	TO_DATE ("day", 'MM/DD/YYYY'), "hr"



	(NULLIF((SUM("5gnr_endc_setup_failure_num" :: FLOAT)),0) / NULLIF((SUM("5gnr_endc_setup_failure_den" :: FLOAT)),0))*100 AS "5gnr_endc_setup_failure_pct",

	(NULLIF((SUM("5gnr_addition_failure_num" :: FLOAT)),0) / NULLIF((SUM("5gnr_addition_failure_den" :: FLOAT)),0))*100 AS "5gnr_addition_failure_pct",

	(NULLIF((SUM("5gnr_endc_drop_num" :: FLOAT)),0) / NULLIF((SUM("5gnr_endc_drop_den" :: FLOAT)),0))*100 AS "5gnr_endc_drop_pct",

	sum ("5gnr_peak_numof_ue" :: FLOAT) AS "5gnr_peak_numof_ue"

	(((64.0*(NULLIF(avg ("pmmacvoldldrb" :: FLOAT),0)))/(NULLIF(avg ("pmmactimedldrb" :: FLOAT),0)))/1000.0 )AS "5GNR_DL_UE_MAC_Throughput_Mbps_19Q3",
	(((64.0*(NULLIF(avg ("pmmacvolulresue" :: FLOAT),0)))/(NULLIF(avg ("pmmactimeulresue" :: FLOAT),0)))/1000.0 )AS "5GNR_UL_MAC_UE_Throughput_Mbps_19Q3"


###########################################################################

select * from public.hourly_ericsson_5gnr_3gpp
WHERE "region" in ('Mountain')
AND TO_DATE ("day", 'MM/DD/YYYY') = '2022-01-19'
 
 
##########################################################################################################################################################################
SELECT 
distinct("day"),
"hr"

FROM "5gpt".hourly_ericsson_5gnr_3gpp 

WHERE 
    to_date(trans_dt, 'yyyymmdd')  between to_date('20220118', 'yyyymmdd') and current_date
    AND
    gnb in (
            '0137238',
            '0127057',
            '0137346',
            '0137147',
            '0127031',
            '0137457',
            '0137137',
            '0127039',
            '0127075',
            '0127049',
            '0127136',
            '0127139',
            '0127300',
            '0137272',
            '0127064',
            '0127081',
            '0137112',
            '0127348',
            '0137452',
            '0127026',
            '0137260',
            '0137244',
            '0127060',
            '0127096',
            '0137257',
            '0137099',
            '0127059',
            '0127277',
            '0127374',
            '0137176',
            '0137177',
            '0127051',
            '0137253',
            '0127383',
            '0137135',
            '0137165',
            '0137129',
            '0137280',
            '0127216',
            '0127227',
            '0127337',
            '0137113',
            '0127321',
            '0127387',
            '0127118',
            '0127037',
            '0127237',
            '0127292',
            '0137086',
            '0127347',
            '0127104',
            '0137236',
            '0137297',
            '0127065',
            '0137161',
            '0127322',
            '0127225',
            '0137298'
            )
    
GROUP BY 
    "day",
    "hr"
ORDER BY
    "day",
    "hr"

"""