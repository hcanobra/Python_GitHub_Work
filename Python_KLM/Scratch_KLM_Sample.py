# Python Ver. 3.8.2
# Owner Hugo Cano
# Date 10/27/2021

# IMPORT LIBRARIES
import simplekml
import pandas
#import 

kml = simplekml.Kml()


# Point example.....
doc = kml.newdocument(name='Locations')

pnt = doc.newpoint(name="Home", coords=[(-111.865703,40.493753)])  # lon, lat, optional height
pnt.description = """
                    This is a description for home:
                    
                    This goes on the body of the message for a particular place mark.

                  """
pnt.snippet.content = "This is the content of the snippet"
pnt.snippet.maxlines = 1 #Maximum lines on the Snipped.
pnt.style.iconstyle.icon.href = 'https://maps.google.com/mapfiles/kml/paddle/orange-circle.png' #Icon of the place
pnt.style.labelstyle.color = simplekml.Color.rgb(0, 0, 255) # Color of the icom

pnt.lookat = simplekml.LookAt(gxaltitudemode=simplekml.GxAltitudeMode.relativetoseafloor,
                              latitude=40.493753, longitude=-111.865703,
                              range=9000, heading=0, tilt=0)
                              #Heading : the rotation in degrees from north.
                              #Range : Is the zoom in ratio in meters
                              #Tilt : Is the degrees from vertical view / from ground 



# Line String example.....
doc = kml.newdocument(name='Paths')

doc.newpoint(name="Start", coords=[(-111.8712586406445,40.49391519474754,0)]) 
doc.newpoint(name="End", coords=[(-111.87478508585,40.49186743984068,0)])

ln = doc.newlinestring(name="Path_Close_Home", description="A pathway closed from home",
                        coords=[(-111.8712586406445,40.49391519474754,0), 
                                (-111.8717578138818,40.49425749492877,0),
                                (-111.8720520746815,40.49402277045196,0),
                                (-111.8723367857317,40.493839164215,0),
                                (-111.8728405446884,40.49366123657707,0), 
                                (-111.8732288431019,40.49353322181878,0),
                                (-111.8736438396292,40.49336456250111,0),
                                (-111.8740024136987,40.49322319178218,0),
                                (-111.8742474592608,40.49314358753159,0),
                                (-111.8743828843594,40.49309058367533,0),
                                (-111.8743603499557,40.49298316706573,0),
                                (-111.8742659524198,40.4928337026635,0),
                                (-111.8741271266448,40.49261805818517,0),
                                (-111.8740285074202,40.49247402675388,0),
                                (-111.8740683942639,40.49238938766654,0),
                                (-111.874216102599,40.4922811608763,0),
                                (-111.8743639679293,40.49216740702543,0), 
                                (-111.8744978492501,40.49205492392262,0),
                                (-111.874632303833,40.49194094550989,0),
                                (-111.87478508585,40.49186743984068,0)])
ln.description = """
                    This is a description for hte line:
                    
                    This goes on the body of the message for a particular line.

                  """
ln.style.linestyle.color = simplekml.Color.rgb(0, 0, 255)  # Red
ln.style.linestyle.width = 10  # 10 pixels

#Polygon example.... /// https://simplekml.readthedocs.io/en/latest/styles.html#polystyle

doc = kml.newdocument(name='Polygons')

pol = doc.newpolygon(name="Close_From_Home",
                     outerboundaryis=[(-111.873830597914,40.49092708783552,0),
                                    (-111.8736263513786,40.49073032756931,0),
                                    (-111.8736584879522,40.49060876258474,0),
                                    (-111.8731750587657,40.49031905918942,0),
                                    (-111.8708481340795,40.49104964231203,0),
                                    (-111.871366008402,40.49203131611601,0),
                                    (-111.8724632618517,40.49181637606332,0),
                                    (-111.8728215558804,40.49187871200643,0), 
                                    (-111.8738540039589,40.49105372815903,0), 
                                    (-111.873830597914,40.49092708783552,0)])
pol.description = """
                    This is a description for the polygon:
                    
                    This goes on the body of the message for a particular polygon.

                  """
pol.style.polystyle.color = '700000ff'  # First two digits are the transparency from 00 - 99
pol.style.polystyle.outline = 1
pol.style.polystyle.fill = 1
pol.style.polystyle.outline = 1

print(kml.kml())

kml.save("botanicalgarden.kml")