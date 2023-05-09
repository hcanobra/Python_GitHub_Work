

# importing sys
import sys
# adding Folder_2 to the system path
sys.path.append('/Users/canobhu/Documents/GitHub/GitHub/Python_API')

from numpy import isnan
import numpy as np
import ndl_API as ndl
import PostgreSQL_API as pg
import pandas as pd
import geopandas as gp


from sqlalchemy import create_engine, engine




def q_NDL_Fuze_PROJ_Query ():
    v_sql_commands = ('''
                        SELECT
                        *
                        FROM  fuze_presto_views.dmp_rfds_sp_fuze_projects_view

                    ''')
    return (v_sql_commands)

def q_NDL_Fuze_Dash_Query ():
    v_sql_commands = ('''
    
                        SELECT *
                        FROM  fuze_presto_views.dmp_rfds_sp_fuze_dash_view 

                    ''')
    return (v_sql_commands)

def q_posgresql_Fuze_query ():
    v_sql_commands = ('''
                    SELECT 
                        * 
                    FROM public.vzw_fuze_proj
                    WHERE 
                        (
                            "Projects_atoll_site_latitude" is NOT Null
                            OR
                            "Projects_sarf_latitude" is NOT Null
                        )
                        AND
                        (
                            "Projects_atoll_site_longitude" is NOT Null
                            OR
                            "Projects_sarf_longitude" is NOT Null
                        )
                        
                    ''')
    return (v_sql_commands)

def q_posgresql_qgis_table ():
    v_sql_commands = ('''
    
                            BEGIN;
                            DROP TABLE IF EXISTS public.vzw_fuze_qgis;

                            CREATE TABLE public.vzw_fuze_qgis as
                            SELECT 
                                FLOC."Projects_Fuze_project_id",
                                FLOC."Projects_parent_solution_id",
                                FLOC."Projects_site_info_id",
                                FLOC."lat",
                                FLOC."lon",
                                FLOC."geometry",

                                FPRO."Projects_local_market",
                                FPRO."Projects_name",
                                FPRO."Projects_Site_name",
                                FPRO."Projects_Status",
                                FPRO."Projects_project_scope",
                                FPRO."Projects_trans_contr_bandwidth",
                                FPRO."Projects_plan_year",
                                FPRO."Projects_por",
                                FPRO."Projects_pl_initiative",
                                FPRO."Projects_pl_rationale",
                                FPRO."Projects_proj_category",
                                FPRO."Projects_pslc",
                                FPRO."Projects_Subtype",
                                FPRO."Projects_rf_rank",
                                FPRO."Projects_modification_type",
                                FPRO."Projects_type",
                                FPRO."Projects_site_type",
                                FPRO."Projects_activation_forecast_date",
                                EXTRACT (MONTH FROM to_date (FPRO."Projects_activation_forecast_date", 'mm/dd/yyyy')) as "Projects_Activation_Month",



                                FDSH."Dashboar_Status",
                                FDSH."Dashboar_RF_Rank",
                                FDSH."Dashboar_Flagged_Project",
                                FDSH."Dashboar_Project_subtype",
                                FDSH."Dashboar_Ready_to_Construct_F",
                                FDSH."Dashboar_Ready_to_Construct_A",
                                FDSH."Dashboar_PM_Project_Manager_Group",
                                FDSH."Dashboar_C_Band_bucket"

                            FROM public.vzw_fuze_loc FLOC
                            LEFT JOIN public.vzw_fuze_proj FPRO ON FLOC."Projects_Fuze_project_id" = FPRO."Projects_Fuze_project_id"
                            LEFT JOIN public.vzw_fuze_dash FDSH ON FLOC."Projects_Fuze_project_id" = FDSH."Dashboar_Fuze_project_id"
                            WHERE "Projects_local_market" IN ('Salt Lake City','Helena','Boise')
                            ;
                            COMMIT;
                    ''')
    return (v_sql_commands)

def c_postgresql_locations ():
    v_databasae = 'vzw_fuze'
    
    cn = pg.Connection('vzw_fuze')
    
    v_data =cn.PostgreSQL_query_df (q_posgresql_Fuze_query())

    v_loc_df = v_data


    v_loc_df_atol = v_loc_df[np.logical_and (v_loc_df['Projects_atoll_site_latitude'].isnull() != True, v_loc_df['Projects_sarf_latitude'].isnull() != False)]
    v_loc_df_sarf = v_loc_df[np.logical_and (v_loc_df['Projects_sarf_latitude'].isnull() != True, v_loc_df['Projects_atoll_site_latitude'].isnull() != False)]
    v_loc_df_both = v_loc_df[np.logical_and (v_loc_df['Projects_sarf_latitude'].isnull() != True, v_loc_df['Projects_atoll_site_latitude'].isnull() != True)]


    v_loc_df_atol =  v_loc_df_atol[['Projects_Fuze_project_id','Projects_parent_solution_id','Projects_site_info_id','Projects_atoll_site_latitude','Projects_atoll_site_longitude']]
    v_loc_df_atol.rename(columns={'Projects_atoll_site_latitude':'lat','Projects_atoll_site_longitude':'lon'}, inplace=True)

    v_loc_df_sarf =  v_loc_df_sarf[['Projects_Fuze_project_id','Projects_parent_solution_id','Projects_site_info_id','Projects_sarf_latitude','Projects_sarf_longitude']]
    v_loc_df_sarf.rename(columns={'Projects_sarf_latitude':'lat','Projects_sarf_longitude':'lon'}, inplace=True)

    v_loc_df_both =  v_loc_df_both[['Projects_Fuze_project_id','Projects_parent_solution_id','Projects_site_info_id','Projects_atoll_site_latitude','Projects_atoll_site_longitude']]
    v_loc_df_both.rename(columns={'Projects_atoll_site_latitude':'lat','Projects_atoll_site_longitude':'lon'}, inplace=True)

    v_loc_df_final = pd.concat([v_loc_df_atol,v_loc_df_sarf,v_loc_df_both])


    cn.PostgreSQL_load_geo('vzw_fuze_loc', v_loc_df_final,'lon','lat')
    
    cn.PostgreSQL_Create_Table (q_posgresql_qgis_table())

    return()    

def q_posgresql_Fuze_cband_ready_query ():
    v_sql_commands = ('''
                    SELECT 
                    fp.Projects_Fuze_project_id,
                    fp.Projects_Site_name,
                    fp.Projects_site_info_id,
                    STR_TO_DATE(Projects_activation_forecast_date,'%m/%d/%Y') as Project_Activation_Withdraw_Milestone_F,
                    fp.Projects_trans_contr_bandwidth,
                    fp.Projects_plan_year,
                    fp.Projects_Subtype,
                    fp.Projects_atoll_site_latitude,
                    fp.Projects_atoll_site_longitude,
                    ds.Dashboar_C_Band_bucket,
                    fp.Projects_local_market,
                    fp.Projects_Status,
                    ds.Dashboar_Status,
                    "CBand_Ready" as CBand_Status,
                    fp.Projects_trans_dt

                    FROM public.vzw_fuze_proj fp
                    JOIN public.vzw_fuze_dash ds on fp.Projects_Fuze_project_id = ds.Dashboar_Fuze_project_id

                    WHERE 
                    ds.Dashboar_C_Band_bucket = 'Built/Capable'
                    AND
                    fp.Projects_Subtype = '5G L-Sub6 - Carrier Add'
                        
                    ''')
    return (v_sql_commands)

def c_NDL_Query (v_query,v_table):
    
    
    ## ///// CREATE THE CONNECTION TON NDL AND PULL THE DATE FROM THE QUERY
    cn = ndl.Connection()
    v_data = cn.commands(v_query)
    print (v_data.head())
    cn.close

    ## //// CREATE A CONNECITON TO POSTGRESQL AND PUSH THE DATA FRAME FROM NDL
    cn = pg.Connection('vzw_fuze')
    cn.PostgreSQL_load_df (v_table,v_data)
    # I NEED TO FIGURE IT OUT HOW TO CLOSE THE CONNECTION..........
     
     
    
    return(v_data)
    
def c_main ():

    c_postgresql_locations ()                                       # AFTER INFORMAITON IS EXTRACTED FROM FUZE VIA NDL THIS FUNCITON JOINS BOTH TABLES, AND GENERATES TWO TABLES, 
                                                                    # 1ST TABLE) CONTAINING FUZE PROJECTS SOME BASIC INFORMAIOTN ABOUT THE PROJECT AND THE LAT LONG INFORMATION --- NAMED: vzw_fuze_loc
                                                                    # 2ND TABLE) CONTAINING PROJECT INFORMATION AND DASHBOARD INFORMATION - NAMED: vzw_fuze_qgis

# ///////// BEGIN 

'''
v_data = c_NDL_Query (q_NDL_Fuze_PROJ_Query(),'vzw_fuze_proj')   # THIS FUNTION EXTRACTS FROM NDL ALL FUZE PROJECT INFORMAITON FORM A NDL VIEW AND CRATE A TABLE IN POSTGRESQL
v_data = c_NDL_Query (q_NDL_Fuze_Dash_Query(),'vzw_fuze_dash')   # THIS FUNTION EXTRACTS FROM NDL ALL FUZE DASHBOARD INFORMAITON FORM A NDL VIEW AND CRATE A TABLE IN POSTGRESQL
'''


# ///////// END 
