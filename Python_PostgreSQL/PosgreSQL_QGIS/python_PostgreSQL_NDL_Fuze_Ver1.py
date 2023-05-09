
from datetime import date

# importing sys
import sys
# adding Folder_2 to the system path
sys.path.append('/Users/canobhu/Documents/GitHub/GitHub/Python_PostgreSQL/PosgreSQL_QGIS')

import python_PostgreSQL_NDL_Fuze as psg_fuze
import python_PostgreSQL_NDL_Fuze_geo as psg_fuze_geo


# Month abbreviation, day and year	
today = date.today()
d4 = today.strftime("%b_%d_%Y")

print ('########## %s : Extracting Fuze informaiton fron NDL'%d4)
psg_fuze.c_main()

print ('########## %s : Generating Geo location for QGIS from Fuze information'%d4)
psg_fuze_geo.c_main()


