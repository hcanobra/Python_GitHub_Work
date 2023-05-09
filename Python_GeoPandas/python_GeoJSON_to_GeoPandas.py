


import pandas as pd
import geopandas as gpd
from zipfile import ZipFile
import requests, zipfile, io
import matplotlib.pyplot as plt
import fiona

from pykml import parser

def f_Utah_HAST_Maps_5GNRCellsV0():

    #url = '/Users/canobhu/Documents/GitHub/GitHub/Python_GeoPandas/Utah_HAST_Maps_5GNRCellsV0.kmz'

    kmz = ZipFile(url, 'r')

    kml = kmz.open('doc.kml', 'r')
    print (kml)

    gpd.io.file.fiona.drvsupport.supported_drivers['KML'] = 'rw'
    df = gpd.read_file(kml, driver='KML')
    print (df.info)    

    return (df)


url = 'http://txslmdatapa1v/stan_files/HASTmaps/NL/NetworkLayers/Utah_HAST_Maps_5GNRCellsV0.kmz'



r = requests.get(url)
z = zipfile.ZipFile(io.BytesIO(r.content))

kml = z.open('doc.kml', 'r')

gpd.io.file.fiona.drvsupport.supported_drivers['KML'] = 'rw'

c = fiona.open(kml)
print (fiona.listlayers(kml, driver='KML'))

df = gpd.read_file(kml, driver='KML', layer='C-Band')
print (df.info())    
#fiona.listlayers(kml)

'''
print (df)
fig, ax = plt.subplots(1, 1, figsize=(15, 15))
df.plot(ax=ax)
plt.show()
'''