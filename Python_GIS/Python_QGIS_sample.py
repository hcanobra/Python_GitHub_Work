import sys
# adding Folder_2 to the system path
sys.path.append('/Applications/QGIS.app/Contents/Resources/python')
#sys.path.append('/Applications/QGIS.app/Contents/MacOS/lib/python3.9/qgis/core')

import qgis.core  as qgis

import pandas as pd

#layer = iface.addVectorLayer("/Users/canobhu/Downloads/ne_10m_airports/ne_10m_airports.shp","points","ogr")
#help(iface)

layer = qgis.core.iface.activeLayer()

#iface.showLayerProperties(layer)

features = layer.getFeatures()


col_names = []
print (len (layer.attributeTableConfig().columns()))

for i in  (layer.attributeTableConfig().columns()):
    if len (i.name) != 0 :
        col_names.append(i.name)

#help(layer.attributeTableConfig().columns())

print (col_names)

df = pd.DataFrame (features, columns = col_names)

print (df.head())

'''
for feat in features:
    attrs = feat.attributes()
    print(attrs[3])
'''

'''
## Python Interface
iface      
help(iface)

##Add Vector layer:
iface.addVectorLayer("d:/.../points.shp","points", "ogr") 

##Zoom
iface.zoomFull()
iface.zoomToPrevious()
iface.zoomToNext()

##Active Layer
layer = iface.activeLayer()

##Attribute Table
iface.showAttributeTable(layer)

##Layer Properties
iface.showLayerProperties(layer)
##New Project
iface.newProject()   
##Add New Layer
help(iface.addVectorLayer)
iface.addVectorLayer("d:/.../points.shp","points", "ogr") 
layer = iface.activeLayer()
dir(layer)          
##Feature details (Attributes)     
for f in layer.getFeatures():      
  print (f)                              
## run python
..............................
for f in layer.getFeatures():
    print(f['place'], f['amenity'])     
## run python
....................
##Coordinates (Lat, Long)
for f in layer.getFeatures():
  geom = f.geometry() 
  print (geom.asPoint())   
## run python
..............
for f in layer.getFeatures():
  geom = f.geometry()
  print (geom.asPoint().x())      
## runpython
.............................
for f in layer.getFeatures():
  geom = f.geometry()
  print(geom.asPoint().y(), geom.asPoint().x())   (Lat (y)/Long(x))
# run python
................................
##Coordinates along with Other Fields
for f in layer.getFeatures():
  geom = f.geometry()
  print ('%s, %s, %f, %f' % (f['place'], f['amenity'], geom.asPoint().y(), geom.asPoint().x()))
## run python
.............................
'''