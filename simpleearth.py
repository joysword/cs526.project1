from omega import *
from cyclops import *
from omegaToolkit import *
from euclid import *
import csv
import caveutil

try:
	import xml.etree.cElementTree as ET
except ImportError:
	import xml.etree.ElementTree as ET

import urllib2

def testfunc():
	print "test"
# radius of the globe
#radius = 6356752.5 + 0000.0
#radius = 6378137

#different radiuses
r_a = 6378137.0
r_b = 6356752.314245

#WGS84 reference ellipsoid constants
wgs84_a = 6378137.0
wgs84_b = 6356752.314245
wgs84_e2 = 0.0066943799901975848
wgs84_a2 = wgs84_a**2 #to speed things up a bit
wgs84_b2 = wgs84_b**2

def llh2ecef(lat, lon, alt):
	lat *= (math.pi / 180.0)
	lon *= (math.pi / 180.0)
	
	n = lambda x: wgs84_a / math.sqrt(1 - wgs84_e2*(math.sin(x)**2))
	
	x = (n(lat) + alt)*math.cos(lat)*math.cos(lon)
	y = (n(lat) + alt)*math.cos(lat)*math.sin(lon)
	z = (n(lat)*(1-wgs84_e2)+alt)*math.sin(lat)
	
	return Vector3(x,y,z)

TYPE = set
(
	["KIDNAPPING",
	"PUBLIC INDECENCY",
	"PUBLIC PEACE VIOLATION",
	"INTERFERENCE WITH PUBLIC OFFICER",
	"PROSTITUTION",
	"LIQUOR LAW VIOLATION",
	"ROBBERY",
	"BURGLARY",
	"WEAPONS VIOLATION",
	"HOMICIDE",
	"OBSCENITY",
	"OTHER OFFENSE",
	"CRIMINAL DAMAGE",
	"THEFT",
	"OFFENSE INVOLVING CHILDREN",
	"GAMBLING",
	"OTHER NARCOTIC VIOLATION",
	"ARSON",
	"OTHER OFFENSE",
	"NARCOTICS",
	"SEX OFFENSE",
	"STALKING",
	"INTIMIDATION",
	"DECEPTIVE PRACTICE",
	"BATTERY",
	"CRIMINAL TRESPASS",
	"MOTOR VEHICLE THEFT",
	"ASSAULT",
	"CRIM SEXUAL ASSAULT",
	"NON-CRIMINAL",
	"INTERFERE WITH PUBLIC OFFICER",
	"RITUALISM",
	"OTHER NARCOTIC VIOLATION",
	"HOMICIDE",
	"OBSCENITY",
	"OFFENSES INVOLVING CHILDREN",
	"NON-CRIMINAL (SUBJECT SPECIFIED)",
	"DOMESTIC VIOLENCE"]
)

btn_allcrime = Button.create(cc)
btn_homicide = Button.create(cc)
btn_kidnap = Button.create(cc)
btn_robbery = Button.create(cc)
btn_burglary = Button.create(cc)
btn_gta = Button.create(cc)
btn_vandalism = Button.create(cc)
btn_arson = Button.create(cc)
btn_theft = Button.create(cc)
btn_assault = Button.create(cc)
btn_sex = Button.create(cc)

crimeType = {'ALL':0, 'HOMICIDE':1, 'KIDNAPPING':2, 'ROBBERY':3, 'BURGLARY':4, 'MOTOR VEHICLE THEFT':5, 'VANDALISM':6, 'ARSON':7, 'THEFT':8, 'ASSAULT':9 'CRIM SEXUAL ASSAULT':10}

class community:
	name = ''
	lat = 0
	lon = 0
	pos = Vector3()
	def __init__(self, n, x, y):
		self.name = n
		self.lat = x
		self.lon = y
		self.pos = llh2ecef(x,y,0)
	def watchme(self):
		print ("watching community %s" %(self.name))

comm = [None]*100

comm[1] = community("Rogers Park", 42.01, -87.67)
comm[2] = community("West Ridge", 42, -87.69)
comm[3] = community("Uptown", 41.97, -87.66)
comm[4] = community("Lincoln Square", 41.97, -87.69)
comm[9] = community("Edison Park", 42.01, -87.81)
comm[10] = community("Norwood Park", 41.98, -87.8)
comm[11] = community("Jefferson Park", 41.98, -87.77)
comm[12] = community("Forest Glen", 41.983333, -87.75)
comm[13] = community("North Park", 41.95, -87.68)
comm[14] = community("Albany Park", 41.97, -87.72)
comm[76] = community("O'Hare", 42, -87.92)
comm[77] = community("Edgewater", 41.99, -87.66)
comm[15] = community("Portage Park", 41.95, -87.76)
comm[16] = community("Irving Park", 41.95, -87.73)
comm[17] = community("Dunning", 41.95, -87.81)
comm[18] = community("Montclare", 41.93, -87.8)
comm[19] = community("Belmont Cragin", 41.93, -87.76)
comm[20] = community("Hermosa", 41.92, -87.73)
comm[5] = community("North Center", 41.95, -87.68)
comm[6] = community("Lake View", 41.94352, -87.654102)
comm[7] = community("Lincoln Park", 41.92, -87.65)
comm[21] = community("Avondale", 41.94, -87.71)
comm[22] = community("Logan Square", 41.928333, -87.706667)
comm[23] = community("Humboldt Park", 41.902809, -87.720886)
comm[24] = community("West Town", 41.9, -87.68)
comm[25] = community("Austin", 41.9, -87.76)
comm[26] = community("West Garfield Park", 41.88, -87.73)
comm[27] = community("East Garfield Park", 41.88, -87.7)
comm[28] = community("Near West Side", 41.87, -87.67)
comm[29] = community("North Lawndale", 41.86, -87.71)
comm[30] = community("South Lawndale", 41.85, -87.71)
comm[31] = community("Lower West Side", 41.85, -87.66)
comm[8] =  community("Near North Side", 41.9, -87.63)
comm[32] = community("Loop", 41.883333, -87.633333)
comm[33] = community("Near South Side", 41.85, -87.62)
comm[34] = community("Armour Square", 41.833333, -87.633333)
comm[35] = community("Douglas", 41.83, -87.62)
comm[36] = community("Oakland", 41.82, -87.6)
comm[37] = community("Fuller Park", 41.81, -87.626667)
comm[38] = community("Grand Boulevard", 41.81, -87.62)
comm[39] = community("Kenwood", 41.81, -87.6)
comm[40] = community("Washington Park", 41.79, -87.62)
comm[41] = community("Hyde Park", 41.79, -87.62)
comm[42] = community("Woodlawn", 41.78, -87.6)
comm[43] = community("South Shore", 41.76, -87.58)
comm[60] = community("Bridgeport", 41.84, -87.65)
comm[69] = community("Greater Grand Crossing", 41.76, -87.61)
comm[56] = community("Garfield Ridge", 41.816667, -87.76)
comm[57] = community("Archer Heights", 41.81, -87.73)
comm[58] = community("Brighton Park", 41.82, -87.7)
comm[59] = community("McKinley Park", 41.83, -87.67)
comm[61] = community("New City", 41.81, -87.66)
comm[62] = community("West Elsdon", 41.79, -87.72)
comm[63] = community("Gage Park", 41.79, -87.69)
comm[64] = community("Clearing", 41.78, -87.76)
comm[65] = community("West Lawn", 41.77, -87.72)
comm[66] = community("Chicago Lawn", 41.77, -87.69)
comm[67] = community("West Englewood", 41.78, -87.67)
comm[68] = community("Englewood", 41.779786, -87.644778)
comm[70] = community("Ashburn", 41.75, -87.71)
comm[71] = community("Auburn Gresham", 41.74, -87.66)
comm[72] = community("Beverly", 41.71, -87.68)
comm[73] = community("Washington Heights", 41.72, -87.65)
comm[74] = community("Mount Greenwood", 41.7, -87.71)
comm[75] = community("Morgan Park", 41.69, -87.67)
comm[44] = community("Chatham", 41.74, -87.611667)
comm[45] = community("Avalon Park", 41.75, -87.59)
comm[46] = community("South Chicago", 41.74, -87.55)
comm[47] = community("Burnside", 41.73, -87.6)
comm[48] = community("Calumet Heights", 41.728333, -87.579722)
comm[49] = community("Roseland", 41.71, -87.62)
comm[50] = community("Pullman", 41.71, -87.62)
comm[51] = community("South Deering", 41.71, -87.56)
comm[52] = community("East Side", 41.7, -87.56)
comm[53] = community("West Pullman", 41.68, -87.63)
comm[54] = community("Riverdale", 41.66, -87.61)
comm[55] = community("Hegewisch", 41.66, -87.55)

##############################################################################################################
# CREATE MENUS
mm = MenuManager.createAndInitialize()
menu0_chicago = mm.getMainMenu().addSubMenu("Chicago Panel")

menu1_0_comm = menu0_chicago.addSubMenu("GO TO A COMMUNITY")
 
menu1_0_1 = menu1_0_comm.addSubMenu("Far North Side")
menu1_0_2 = menu1_0_comm.addSubMenu("Northwest Side")
menu1_0_3 = menu1_0_comm.addSubMenu("North Side")
menu1_0_4 = menu1_0_comm.addSubMenu("West Side")
menu1_0_5 = menu1_0_comm.addSubMenu("Central")
menu1_0_6 = menu1_0_comm.addSubMenu("South Side")
menu1_0_7 = menu1_0_comm.addSubMenu("Southwest Side")
menu1_0_8 = menu1_0_comm.addSubMenu("Far Southwest Side")
menu1_0_9 = menu1_0_comm.addSubMenu("Far Southeast Side")

#cc = menu1_0_1.getContainer()
#btn_01 = Button.create(cc)
#btn_02 = Button.create(cc)
#btn_03 = Button.create(cc)
#btn_04 = Button.create(cc)
#btn_09 = Button.create(cc)
#btn_10 = Button.create(cc)
#btn_11 = Button.create(cc)
#btn_12 = Button.create(cc)
#btn_13 = Button.create(cc)
#btn_14 = Button.create(cc)
#btn_76 = Button.create(cc)
#btn_77 = Button.create(cc)
btn_01 = menu1_0_1.addButton("Rogers Park", "goCommunities(1)")
btn_02 = menu1_0_1.addButton("West Ridge", "goCommunities(2)")
btn_03 = menu1_0_1.addButton("Uptown", "goCommunities(3)")
btn_04 = menu1_0_1.addButton("Lincoln Square", "goCommunities(4)")
btn_09 = menu1_0_1.addButton("Edison Park", "goCommunities(9)")
btn_10 = menu1_0_1.addButton("Norwood Park", "goCommunities(10)")
btn_11 = menu1_0_1.addButton("Jefferson Park", "goCommunities(11)")
btn_12 = menu1_0_1.addButton("Forest Glen", "goCommunities(12)")
btn_13 = menu1_0_1.addButton("North Park", "goCommunities(13)")
btn_14 = menu1_0_1.addButton("Albany Park", "goCommunities(14)")
btn_76 = menu1_0_1.addButton("O'Hare", "goCommunities(76)")
btn_77 = menu1_0_1.addButton("Edgewater", "goCommunities(77)")

#cc = menu1_0_2.getContainer()
#btn_15 = Button.create(cc)
#btn_16 = Button.create(cc)
#btn_17 = Button.create(cc)
#btn_18 = Button.create(cc)
#btn_19 = Button.create(cc)
#btn_20 = Button.create(cc)
btn_15 = menu1_0_2.addButton("Portage Park", "goCommunities(15)")
btn_16 = menu1_0_2.addButton("Irving Park", "goCommunities(16)")
btn_17 = menu1_0_2.addButton("Dunning", "goCommunities(17)")
btn_18 = menu1_0_2.addButton("Montclare", "goCommunities(18)")
btn_19 = menu1_0_2.addButton("Belmont Cragin", "goCommunities(19)")
btn_20 = menu1_0_2.addButton("Hermosa", "goCommunities(20)")

#cc = menu1_0_3.getContainer()
#btn_05 = Button.create(cc)
#btn_06 = Button.create(cc)
#btn_07 = Button.create(cc)
#btn_21 = Button.create(cc)
#btn_22 = Button.create(cc)
btn_05 = menu1_0_3.addButton("North Center", "goCommunities(5)")
btn_06 = menu1_0_3.addButton("Lake View", "goCommunities(6)")
btn_07 = menu1_0_3.addButton("Lincoln Park", "goCommunities(7)")
btn_21 = menu1_0_3.addButton("Avondale", "goCommunities(21)")
btn_22 = menu1_0_3.addButton("Logan Square", "goCommunities(22)")

#cc = menu1_0_4.getContainer()
#btn_23 = Button.create(cc)
#btn_24 = Button.create(cc)
#btn_25 = Button.create(cc)
#btn_26 = Button.create(cc)
#btn_27 = Button.create(cc)
#btn_28 = Button.create(cc)
#btn_29 = Button.create(cc)
#btn_30 = Button.create(cc)
#btn_31 = Button.create(cc)
btn_23 = menu1_0_4.addButton("Humboldt Park", "goCommunities(23)")
btn_24 = menu1_0_4.addButton("West Town", "goCommunities(24)")
btn_25 = menu1_0_4.addButton("Austin", "goCommunities(25)")
btn_26 = menu1_0_4.addButton("West Garfield Park", "goCommunities(26)")
btn_27 = menu1_0_4.addButton("East Garfield Park", "goCommunities(27)")
btn_28 = menu1_0_4.addButton("Near West Side", "goCommunities(28)")
btn_29 = menu1_0_4.addButton("North Lawndale", "goCommunities(29)")
btn_30 = menu1_0_4.addButton("South Lawndale", "goCommunities(30)")
btn_31 = menu1_0_4.addButton("Lower West Side", "goCommunities(31)")

#cc = menu1_0_5.getContainer()
#btn_08 = Button.create(cc)
#btn_32 = Button.create(cc)
#btn_33 = Button.create(cc)
btn_08 = menu1_0_5.addButton("Near North Side", "goCommunities(8)")
btn_32 = menu1_0_5.addButton("Loop", "goCommunities(32)")
btn_33 = menu1_0_5.addButton("Near South Side", "goCommunities(33)")

#cc = menu1_0_6.getContainer()
#btn_34 = Button.create(cc)
#btn_35 = Button.create(cc)
#btn_36 = Button.create(cc)
#btn_37 = Button.create(cc)
#btn_38 = Button.create(cc)
#btn_39 = Button.create(cc)
#btn_40 = Button.create(cc)
#btn_41 = Button.create(cc)
#btn_42 = Button.create(cc)
#btn_43 = Button.create(cc)
#btn_60 = Button.create(cc)
#btn_69 = Button.create(cc)
btn_34 = menu1_0_6.addButton("Armour Square", "goCommunities(34)")
btn_35 = menu1_0_6.addButton("Douglas", "goCommunities(35)")
btn_36 = menu1_0_6.addButton("Oakland", "goCommunities(36)")
btn_37 = menu1_0_6.addButton("Fuller Park", "goCommunities(37)")
btn_38 = menu1_0_6.addButton("Grand Boulevard", "goCommunities(38)")
btn_39 = menu1_0_6.addButton("Kenwood", "goCommunities(39)")
btn_40 = menu1_0_6.addButton("Washington Park", "goCommunities(40)")
btn_41 = menu1_0_6.addButton("Hyde Park", "goCommunities(41)")
btn_42 = menu1_0_6.addButton("Woodlawn", "goCommunities(42)")
btn_43 = menu1_0_6.addButton("South Shore", "goCommunities(43)")
btn_60 = menu1_0_6.addButton("Bridgeport", "goCommunities(60)")
btn_69 = menu1_0_6.addButton("Greater Grand Crossing", "goCommunities(69)")

#cc = menu1_0_7.getContainer()
#btn_56 = Button.create(cc)
#btn_57 = Button.create(cc)
#btn_58 = Button.create(cc)
#btn_59 = Button.create(cc)
#btn_61 = Button.create(cc)
#btn_62 = Button.create(cc)
#btn_63 = Button.create(cc)
#btn_64 = Button.create(cc)
#btn_65 = Button.create(cc)
#btn_66 = Button.create(cc)
#btn_67 = Button.create(cc)
#btn_68 = Button.create(cc)
btn_56 = menu1_0_7.addButton("Garfield Ridge", "goCommunities(56)")
btn_57 = menu1_0_7.addButton("Archer Heights", "goCommunities(57)")
btn_58 = menu1_0_7.addButton("Brighton Park", "goCommunities(58)")
btn_59 = menu1_0_7.addButton("McKinley Park", "goCommunities(59)")
btn_61 = menu1_0_7.addButton("New City", "goCommunities(61)")
btn_62 = menu1_0_7.addButton("West Elsdon", "goCommunities(62)")
btn_63 = menu1_0_7.addButton("Gage Park", "goCommunities(63)")
btn_64 = menu1_0_7.addButton("Clearing", "goCommunities(64)")
btn_65 = menu1_0_7.addButton("West Lawn", "goCommunities(65)")
btn_66 = menu1_0_7.addButton("Chicago Lawn", "goCommunities(66)")
btn_67 = menu1_0_7.addButton("West Englewood", "goCommunities(67)")
btn_68 = menu1_0_7.addButton("Englewood", "goCommunities(68)")

#cc = menu1_0_8.getContainer()
#btn_70 = Button.create(cc)
#btn_71 = Button.create(cc)
#btn_72 = Button.create(cc)
#btn_73 = Button.create(cc)
#btn_74 = Button.create(cc)
#btn_75 = Button.create(cc)
btn_70 = menu1_0_8.addButton("Ashburn", "goCommunities(70)")
btn_71 = menu1_0_8.addButton("Auburn Gresham", "goCommunities(71)")
btn_72 = menu1_0_8.addButton("Beverly", "goCommunities(72)")
btn_73 = menu1_0_8.addButton("Washington Heights", "goCommunities(73)")
btn_74 = menu1_0_8.addButton("Mount Greenwood", "goCommunities(74)")
btn_75 = menu1_0_8.addButton("Morgan Park", "goCommunities(75)")

#cc = menu1_0_9.getContainer()
#btn_44 = Button.create(cc)
#btn_45 = Button.create(cc)
#btn_46 = Button.create(cc)
#btn_47 = Button.create(cc)
#btn_48 = Button.create(cc)
#btn_49 = Button.create(cc)
#btn_50 = Button.create(cc)
#btn_51 = Button.create(cc)
#btn_52 = Button.create(cc)
#btn_53 = Button.create(cc)
#btn_54 = Button.create(cc)
#btn_55 = Button.create(cc)
btn_44 = menu1_0_9.addButton("Chatham", "goCommunities(44)")
btn_45 = menu1_0_9.addButton("Avalon Park", "goCommunities(45)")
btn_46 = menu1_0_9.addButton("South Chicago", "goCommunities(46)")
btn_47 = menu1_0_9.addButton("Burnside", "goCommunities(47)")
btn_48 = menu1_0_9.addButton("Calumet Heights", "goCommunities(48)")
btn_49 = menu1_0_9.addButton("Roseland", "goCommunities(49)")
btn_50 = menu1_0_9.addButton("Pullman", "goCommunities(50)")
btn_51 = menu1_0_9.addButton("South Deering", "goCommunities(51)")
btn_52 = menu1_0_9.addButton("East Side", "goCommunities(52)")
btn_53 = menu1_0_9.addButton("West Pullman", "goCommunities(53)")
btn_54 = menu1_0_9.addButton("Riverdale", "goCommunities(54)")
btn_55 = menu1_0_9.addButton("Hegewisch", "goCommunities(55)")

menu1_1filter = menu0_chicago.addSubMenu("FILTER CRIME TYPES")

cc = menu1_1filter.getContainer()

btnCrime[None]*11

for crime in crimeType:
	btnCrime[crime.value] = Button.create(cc)
	btncrime[crime.value] = setCheckable(True)


'ALL':0, 'HOMICIDE':1, 'KIDNAPPING':2, 'ROBBERY':3, 'BURGLARY':4, 'MOTOR VEHICLE THEFT':5, 'VANDALISM':6, 'ARSON':7, 'THEFT':8, 'ASSAULT':9 'CRIM SEXUAL ASSAULT':10}
btnCrime[0].setText("ALL MAJOR CRIMES")
btnCrime[1].setText("Homicide")
btnCrime[2].setText("Kidnapping")
btnCrime[3].setText("Robbdery")
btnCrime[4].setText("Burglary (Forcible Entry)")
btnCrime[setText("Motor Vehicle Theft")
btnCrime[alism.setText ("Vandalism (and damage to the City of Chicago)")
btnCrime[n.setText("Arson")
btnCrime[t.setText("Theft (over $500)")
btnCrime[ult.setText("Aggravated Assault")
btnCrime[setText("Aggravated Sexual Assault")

btn_allcrime.setCheckable(True)
btn_homicide.setCheckable(True)
btn_kidnap.setCheckable(True)
btn_robbery.setCheckable(True)
btn_burglary.setCheckable(True)
btn_gta.setCheckable(True)
btn_vandalism.setCheckable(True)
btn_arson.setCheckable(True)
btn_theft.setCheckable(True)
btn_assault.setCheckable(True)
btn_sex.setCheckable(True)

btn_allcrime.setChecked(True)
btn_homicide.setChecked(False)
btn_kidnap.setChecked(False)
btn_robbery.setChecked(False)
btn_burglary.setChecked(False)
btn_gta.setChecked(False)
btn_vandalism.setChecked(False)
btn_arson.setChecked(False)
btn_theft.setChecked(False)
btn_assault.setChecked(False)
btn_sex.setChecked(False)

btn_allcrime.setUIEventCommand('clickAllCrime()')
btn_homicide.setUIEventCommand('clickHom()')
btn_kidnap.setUIEventCommand('clickKid()')
btn_robbery.setUIEventCommand('clickRob()')
btn_burglary.setUIEventCommand('clickBur()')
btn_gta.setUIEventCommand('clickGta()')
btn_vandalism.setUIEventCommand('clickVan()')
btn_arson.setUIEventCommand('clickArs()')
btn_theft.setUIEventCommand('clickThe()')
btn_assault.setUIEventCommand('clickAss()')
btn_sex.setUIEventCommand('clickSex()')

menu1_2simu = menu0_chicago.addSubMenu("REAL TIME WATCH")

cc = menu1_2simu.getContainer()
label_simu = Label.create(cc)
label_simu.setText("TEST SIMULATION")

scene = getSceneManager()

# deal with audio                                                                         
env = getSoundEnvironment()

# set the background to black
scene.setBackgroundColor(Color(0, 0, 0, 1))

all = SceneNode.create("everything")

# Create a directional light
light1 = Light.create()
light1.setLightType(LightType.Directional)
light1.setLightDirection(Vector3(-1.0, -1.0, -1.0))
light1.setColor(Color(0.7, 0.7, 0.7, 1.0))
light1.setAmbient(Color(0.5, 0.5, 0.5, 1.0))
light1.setEnabled(True)

# Load a static model
torusModel = ModelInfo()
torusModel.name = "earth"

torusModel2 = ModelInfo()
torusModel2.name = "map"

if caveutil.caveutil.isCAVE() == False:
	torusModel2.path = "annotation.earth"
	#laptop: it works!
	#cave:

	torusModel.path = "annotation.earth"
	#laptop:it works!
	#cave: failed to load jpeg and tiff

#torusModel.path = "vertical_datum.earth"
#laptop:
#cave: failed

#torusModel.path = "feature_geom.earth"
#laptop:
#cave: failed

else:
	#torusModel2.path = "openstreetmap.earth"
	torusModel2.path = "annotation.earth"
	#laptop: crash when start
	#cave: it works!

	#torusModel.path = "mapquestaerial.earth"
	torusModel.path = "annotation.earth"
	#laptop: crash when start
	#cave: it works!

#torusModel2.path = "yahoo_maps.earth"
#laptop: crash during running / it works (without showing anything)
#cave: works (too low no data)

#torusModel.path = "yahoo_aerial.earth"
#laptop: it works (without showing anything)
#cave: works (too low no data)

#scene.loadModel(torusModel)
#scene.loadModel(torusModel2)

# Create a scene object using the loaded model
#torus1 = StaticObject.create("earth")
#torus1.getMaterial().setLit(False)
#all.addChild(torus1)

#torus2 = StaticObject.create("map")
#torus2.getMaterial().setLit(False)
#all.addChild(torus2)
#torus2.setVisible(False)

setNearFarZ(1, 20 * r_a)

cam = getDefaultCamera()

# Setting the camera by hand
cam.setPosition(Vector3(193124.87, -4767697.65, 4228566.18))
cam.setOrientation(Quaternion(0.6, 0.8, 0.0, 0.0))

# set a fast speed for travel by default
cam.getController().setSpeed(10000)

# CTA stops
f = open('CTA_L_Stops')
ctastops = [line.rstrip('\n') for line in f]

for name in ctastops:
	#print name
	foo = name.strip(' ()"')
	bar = foo.partition(', ')

	model = SphereShape.create(100, 4)
	lat = float(bar[0]) * math.pi/180
	lon = float(bar[2]) * math.pi/180

	#radius = getRadius(lat, r_a, r_b)

	pos = llh2ecef(float(bar[0]), float(bar[2]), 0.0)
	model.setPosition(pos)
	model.setEffect('colored -d red')
	all.addChild(model)
f.close()

# a line
xLine = LineSet.create()
xLine.setEffect("colored -d blue")
f = open('LINE')
ctastops = [line.rstrip('\n') for line in f]
firsttime = 1
oldPos = Vector3()
for row in ctastops:
	second = row.partition(',')
	#print "first:",first
	first = second[2].partition(',')
	if (firsttime == 1):
		oldPos = llh2ecef(float(first[0]), float(second[0]), 0.0)
		firsttime = 0
	else:
		pos = llh2ecef(float(first[0]), float(second[0]), 0.0)
		l = xLine.addLine()
		l.setStart(oldPos)
		l.setEnd(pos)
		l.setThickness(100.0)
		oldPos = pos
f.close()
all.addChild(xLine)

# SIN CITY
def createCrimeDrawable():
	return BoxShape.create(15,15,15)

#sincity="""
nodeYear = [None]*14

for i in range(1,14):
	name = "year"+str(2000+i)
	nodeYear[i] = SceneNode.create(name)
	all.addChild(nodeYear[i])
	for j in range(0,78):
		name = "year"+str(2000+i)+"comm"+str(j)
		nodeYear[i].addChild(SceneNode.create(name))

count = 0
f = open('CrimesAll_final.csv', 'rb')
lines = csv.reader(f)
count = 0
for items in lines:
	if (cmp(items[2],'HOMICIDE')==0):
		crime_comm = int(items[4])
		crime_year = int(items[5])
		crime_lat = float(items[6])
		crime_lon = float(items[7])
		
		pos = llh2ecef(crime_lat, crime_lon, 8.0)

		model = createCrimeDrawable()
		model.setPosition(pos)
		#model.lookAt(Vector3(0,0,0), Vector3(pos[0],pos[1],pos[2]))
		model.setEffect('colored -d blue')
		nodeYear[crime_year-2000].getChildByIndex(crime_comm).getChildByIndex().addChild(model)
		count+=1
		# TO DO ELSE
f.close()

print "total number of homicide is %d" %(count)

for i in range(1,14):
	nodeYear[i].setChildrenVisible(False)

#nodeYear[13].setChildrenVisible(True)
#print "2013 visible"
#"""

# since the scale here is pretty large stereo doesnt help much
# so lets start with it turned off
#toggleStereo()

#put the camera to Chicago

# it would be better to set the speed based on the height over the surface
# to move slower as you get closer

# TEST FACE CAMERA
testObject = PlaneShape.create(20, 20)
all.addChild(testObject)
caveutil.caveutil.positionAtHead (cam, testObject, 2)

d0 = 0
d1 = 0
d2 = 0
r = 0
r2 = 0

def clickAllCrime():
	if btn_allcrime.isChecked():
		btn_homicide.setChecked(False)
		btn_assault.setChecked(False)
		btn_vandalism.setChecked(False)
		btn_gta.setChecked(False)
		btn_burglary.setChecked(False)
		btn_sex.setChecked(False)
		btn_arson.setChecked(False)
		btn_kidnap.setChecked(False)
		btn_theft.setChecked(False)
		btn_robbery.setChecked(False)
		print "checked"
	else:
		print "unchecked"

#handle events from the wand
# left button toggle between two maps

isButton7down = False
wandOldPos = Vector3()
wandOldOri = Quaternion()

def playBtnDownSound(e):
	sd = SoundInstance(env.loadSoundFromFile("/sound/menu/down.wav"))
	sd.setPosition( e.getPosition() )
	sd.setVolume(1.0)
	sd.setWidth(20)
	sd.play()
def playBtnUpSound(e):
	sd = SoundInstance(env.loadSoundFromFile("/sound/menu/up.wav"))
	sd.setPosition( e.getPosition() )
	sd.setVolume(1.0)
	sd.setWidth(20)
	sd.play()

#uim = UiModule.createAndInitialize()
#wf = uim.getWidgetFactory()
#ui = uim.getUi()

#newBtn = wf.createButton('testButton', ui)
#newBtn.setUIEventCommand('testfunc()')

#newBtn.setPosition(Vector3(20,20))

def onEvent():
	global userScaleFactor

	e = getEvent()

	if (e.isButtonDown(EventFlags.ButtonLeft)):
		playBtnDownSound(e)
		print("Left button pressed")
		if torus1.isVisible():
			torus1.setVisible(False)
			torus2.setVisible(True)
		else:
			torus1.setVisible(True)
			torus2.setVisible(False)

	elif (e.isButtonDown(EventFlags.Button7)):
		playBtnDownSound(e)
		isButton7down = True
		wandOldPos = e.getPosition()
		wandOldOri = e.getOrientation()

	elif (e.isButtonUp(EventFlags.Button7)):
		isButton7down = False
	
	elif (e.getType()==EventType.Update) and (isButton7down):
		wandPos = e.getPosition()
		cam.setPosition( cam.getPosition() + (wandPos-wandOldPos)*cam.getController().getSpeed()*0.01 )
		wandOri = e.getOrientation()
		cam.setOrientation( cam.getOrientation() + (wandOri-wandOldOrientation)*0.01 )

def onUpdate(frame, t, dt):
	d = cam.getPosition()
	d0 = float(d.x)
	d1 = float(d.y)
	d2 = float(d.z)
	r = math.sqrt(d0*d0 + d1*d1 + d2*d2) - r_a # altitude in cm
	if r<500:
		r=500
	cam.getController().setSpeed(r)

setEventFunction(onEvent)
setUpdateFunction(onUpdate)


## HOW TO GO TO A COMMUNITY
def goCommunities(x):
	print "going to %s at (%f,%f)" %(comm[x].name, comm[x].lat, comm[x].lon)

conditionstat="""
	if x<39: # 1 - 38
		if x<20: # 1 - 19
			if x<10: # 1 - 9
				if x<5: # 1 - 4
					if x<3:
						if x==1: # 1
							print btn_01.getText();
						else: # 2
							print btn_02.getText();
					else:
						if x==3: # 3
							print btn_03.getText();
						else: # 4
							print btn_04.getText();
				else: # 5 - 9
					if x<8:
						if x==5: # 5
							print btn_05.getText();
						elif x==6: # 6
							print btn_06.getText();
						else: # 7
							print btn_07.getText();
					else:
						if x==8: # 8
							print btn_08.getText();
						else: # 9
							print btn_09.getText();
			else: # 10 - 19
				if x<15: # 10 - 14
					if x<13:
						if x==10: # 10
							print btn_10.getText();
						elif x==11: # 11
							print btn_11.getText();
						else: # 12
							print btn_12.getText();
					else:
						if x==13: # 13
							print btn_13.getText();
						else: # 14
							print btn_14.getText();
				else: # 15 - 19
					if x<18:
						if x==15: # 15
							print btn_15.getText();
						elif x==16: # 16
							print btn_16.getText();
						else: # 17
							print btn_17.getText();
					else:
						if x==18: # 18
							print btn_18.getText();
						else: # 19
							print btn_19.getText();
		else: # 20 - 38
			if x<30: # 20 - 29
				if x<25: # 20 - 24
					if x<23:
						if x==20: # 20
							print btn_20.getText();
						elif x==21: # 21
							print btn_21.getText();
						else: # 22
							print btn_22.getText();
					else:
						if x==23: # 23
							print btn_23.getText();
						else: # 24
							print btn_24.getText();
				else: # 25 - 29
					if x<28:
						if x==25: # 25
							print btn_25.getText();
						elif x==26: # 26
							print btn_26.getText();
						else: # 27
							print btn_27.getText();
					else:
						if x==28: # 28
							print btn_28.getText();
						else: # 29
							print btn_29.getText();
			else: # 30 - 38
				if x<35: # 30 - 34
					if x<33:
						if x==30: # 30
							print btn_30.getText();
						elif x==31: # 31
							print btn_31.getText();
						else: # 32
							print btn_32.getText();
					else:
						if x==33: # 33
							print btn_33.getText();
						else: # 34
							print btn_34.getText();
				else: # 35 - 38
					if x<37:
						if x==35: # 35
							print btn_35.getText();
						else: # 36
							print btn_36.getText();
					else:
						if x==37: # 37
							print btn_37.getText();
						else: # 38
							print btn_38.getText();
	else: # 39 - 77
		if x<59: # 39 - 58
			if x<49: # 39 - 48
				if x<44: # 39 - 43
					if x<42:
						if x==39: # 39
							print btn_39.getText();
						elif x==40: # 40
							print btn_40.getText();
						else: # 41
							print btn_41.getText();
					else:
						if x==42: # 42
							print btn_42.getText();
						else: # 43
							print btn_43.getText();
				else: # 44 - 48
					if x<47:
						if x==44: # 44
							print btn_44.getText();
						elif x==45: # 45
							print btn_45.getText();
						else: # 46
							print btn_46.getText();
					else:
						if x==47: # 47
							print btn_47.getText();
						else: # 48
							print btn_48.getText();
			else: # 49 - 58
				if x<54: # 49 - 53
					if x<52:
						if x==49: # 49
							print btn_49.getText();
						elif x==50: # 50
							print btn_50.getText();
						else: # 51
							print btn_51.getText();
					else:
						if x==52: # 52
							print btn_52.getText();
						else: # 53
							print btn_53.getText();
				else: # 54 - 58
					if x<57:
						if x==54: # 54
							print btn_54.getText();
						elif x==55: # 55
							print btn_55.getText();
						else: # 56
							print btn_56.getText();
					else:
						if x==57: # 57
							print btn_57.getText();
						else: # 58
							print btn_58.getText();
		else: # 59 - 77
			if x<69: # 59-68
				if x<64: # 59 - 63
					if x<62:
						if x==59:
							print btn_59.getText();
						elif x==60:
							print btn_60.getText();
						else:
							print btn_61.getText();
					else:
						if x==62:
							print btn_62.getText();
						else:
							print btn_63.getText();
				else: # 64 - 68
					if x<67:
						if x==64:
							print btn_64.getText();
						elif x==65:
							print btn_65.getText();
						else:
							print btn_66.getText();
					else:
						if x==67:
							print btn_67.getText();
						else:
							print btn_68.getText();
			else: # 69 - 77
				if x<74: # 69 - 73
					if x<72:
						if x==69:
							print btn_69.getText();
						elif x==70:
							print btn_70.getText();
						else:
							print btn_71.getText();
					else:
						if x==72:
							print btn_72.getText();
						else:
							print btn_73.getText();
				else:
					if x<76:
						if x==74:
							print btn_74.getText();
						else:
							print btn_75.getText();
					else:
						if x==76:
							print btn_76.getText();
						else:
							print btn_77.getText();
"""

## HOW TO FILTER CRIME TYPES

def clickCrime(i):
	if (btnCrime[i].isChecked()):
		btnCrime[i].setChecked(False)
		for i in range(2001,2014):
			if nodeYear[i-2000].isVisible():
				for j in range(1,78):
					if nodeYear[i-2000].getChildeByIndex(j).isVisible():
						nodeYear[i-2000].getChildeByIndex(j).setChildrenVisible(False);


def clickHom():
	if btn_homicide.isChecked():
		btn_allcrime.setChecked(False)
		for i in range(2001,2013):
			if nodeYear[i-2000].isVisible():
				nodeYear[i-2000].getChildByIndex()
				setChildrenVisible

	else:
		print "unchecked"
def clickAss():
	if btn_assault.isChecked():
		btn_allcrime.setChecked(False)
		print "checked"
	else:
		print "unchecked"
def clickVan():
	if btn_vandalism.isChecked():
		btn_allcrime.setChecked(False)
		print "checked"
	else:
		print "unchecked"
def clickGta():
	if btn_gta.isChecked():
		btn_allcrime.setChecked(False)
		print "checked"
	else:
		print "unchecked"
def clickBur():
	if btn_burglary.isChecked():
		btn_allcrime.setChecked(False)
		print "checked"
	else:
		print "unchecked"
def clickThe():
	if btn_theft.isChecked():
		btn_allcrime.setChecked(False)
		print "checked"
	else:
		print "unchecked"
def clickRob():
	if btn_robbery.isChecked():
		btn_allcrime.setChecked(False)
		print "checked"
	else:
		print "unchecked"
def clickSex():
	if btn_sex.isChecked():
		btn_allcrime.setChecked(False)
		print "checked"
	else:
		print "unchecked"
def clickArs():
	if btn_arson.isChecked():
		btn_allcrime.setChecked(False)
		print "checked"
	else:
		print "unchecked"
def clickkid():
	if btn_kid.isChecked():
		btn_allcrime.setChecked(False)
		print "checked"
	else:
		print "unchecked"

#GET TRAIN LOCATION FROM CTA
def getTrainInfo():

	train_xml = urllib2.urlopen('http://lapi.transitchicago.com/api/1.0/ttpositions.aspx?key=484807ed614d4ffb8f31bab10357ba4f&rt=red,blue,brn,g,org,p,pink,y').read()
	root = ET.fromstring(train_xml)
	for route in root:
		for train in route:
			lat = float(train.find('lat').text)
			lon = float(train.find('lon').text)
			heading = float(train.find('heading').text)
			pos = llh2ecef(lat, lon, 100.0)
			model = BoxShape.create(100,20,200)
			model.setBoundingBoxVisible(True)
			model.setPosition(pos[0],pos[1],pos[2])
			model.lookAt(Vector3(0,0,0), Vector3(pos[0],pos[1],pos[2]))
			model.setEffect('colored -d blue')
			all.addChild(model)

getTrainInfo()

never ="""
												!!!KIDNAPPING : 165
		INTERFERE WITH PUBLIC OFFICER : 0
		PUBLIC PEACE VIOLATION : 2077
		INTERFERENCE WITH PUBLIC OFFICER : 845
	???PROSTITUTION : 1115 (ICON)
		LIQUOR LAW VIOLATION : 314
		RITUALISM : 0
															!!!ROBBERY : 7314 (7379) (ICON)
															BURGLARY (FORCIBLE ENTRY): 10915 (7272) (ICON)
!!!WEAPONS VIOLATION : 2125 (ICON)
		OTHER NARCOTIC VIOLATION : 2
												!!!HOMICIDE : 269 (273) (ICON)
		OBSCENITY : 16
		OFFENSES INVOLVING CHILDREN : 0
		OTHER OFFENSE : 11619
																???CRIMINAL DAMAGE (TO CITY OF CHICAGO PROPERTY, *VANDALISM): 19193 (434) (ICON)
															!!!MOTOR VEHICLE THEFT : 8276 (ICON)
															???THEFT (over $500): 42018 (8944) (ICON)
		OFFENSE INVOLVING CHILDREN : 1453
		GAMBLING : 430
		PUBLIC INDECENCY : 6
		NON-CRIMINAL (SUBJECT SPECIFIED) : 0
												!!!ARSON : 261 (ICON)
		INTIMIDATION : 93
		SEX OFFENSE : 616
		NARCOTICS : 22027
		DECEPTIVE PRACTICE : 7351
		BATTERY : 35456
		CRIMINAL TRESPASS : 5208
		STALKING : 81
																ASSAULT (AGGRAVATED*): 11297 (2479) (ICON)
												CRIM SEXUAL ASSAULT (AGGRAVATED*): 761 (190) (ICON)
		NON-CRIMINAL : 3
		DOMESTIC VIOLENCE : 0
"""

areas="""
Far North Side
	01 	Rogers Park
	02 	West Ridge
	03 	Uptown
	04 	Lincoln Square
	09	Edison Park
	10	Norwood Park
	11	Jefferson Park
	12	Forest Glen
	13	North Park
	14	Albany Park
	76	"O'Hare"
	77	Edgewater
Northwest Side
	15	Portage Park
	16	Irving Park
	17	Dunning
	18	Montclare
	19	Belmont Cragin
	20	Hermosa
North Side
	5 	North Center
	6 	Lake View
	7	Lincoln Park
	21	Avondale
	22	Logan Square
West Side
	23	Humboldt Park
	24	West Town
	25	Austin
	26	West Garfield Park
	27	East Garfield Park
	28	Near West Side
	29	North Lawndale
	30	South Lawndale
	31	Lower West Side
Central
	8 	Near North Side
	32	Loop
	33	Near South Side
South Side
	34	Armour Square
	35	Douglas
	36	Oakland
	37	Fuller Park
	38	Grand Boulevard
	39	Kenwood
	40	Washington Park
	41	Hyde Park
	42	Woodlawn
	43	South Shore
	60	Bridgeport
	69	Greater Grand Crossing
Southwest Side
	56	Garfield Ridge	
	57	Archer Heights	
	58	Brighton Park
	59	McKinley Park
	61	New City
	62	West Elsdon
	63	Gage Park
	64	Clearing
	65	West Lawn
	66	Chicago Lawn
	67	West Englewood
	68	Englewood
Far Southwest Side
	70	Ashburn
	71	Auburn Gresham
	72	Beverly
	73	Washington Heights
	74	Mount Greenwood
	75	Morgan Park
Far Southeast Side
	44	Chatham
	45	Avalon Park
	46	South Chicago
	47	Burnside
	48	Calumet Heights
	49	Roseland
	50	Pullman
	51	South Deering
	52	East Side
	53	West Pullman
	54	Riverdale
	55	Hegewisch
"""


	

