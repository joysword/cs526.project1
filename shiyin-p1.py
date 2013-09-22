from omega import *
from cyclops import *
from omegaToolkit import *
from euclid import *
import csv
from caveutil import *
import sprite

try:
	import xml.etree.cElementTree as ET
except ImportError:
	import xml.etree.ElementTree as ET

import urllib2

def testfunc():
	print "test"

# different radiuses
r_a = 6378137.0
r_b = 6356752.314245

# WGS84 reference ellipsoid constants
wgs84_a = 6378137.0
wgs84_b = 6356752.314245
wgs84_e2 = 0.0066943799901975848
wgs84_a2 = wgs84_a**2 #to speed things up a bit
wgs84_b2 = wgs84_b**2

# coordinate system conversion
def llh2ecef(lat, lon, alt):
	lat *= (math.pi / 180.0)
	lon *= (math.pi / 180.0)

	n = lambda x: wgs84_a / math.sqrt(1 - wgs84_e2*(math.sin(x)**2))

	x = (n(lat) + alt)*math.cos(lat)*math.cos(lon)
	y = (n(lat) + alt)*math.cos(lat)*math.sin(lon)
	z = (n(lat)*(1-wgs84_e2)+alt)*math.sin(lat)

	return Vector3(x,y,z)

crimeType = {'ALL':0, 'HOMICIDE':1, 'KIDNAPPING':2, 'ROBBERY':3, 'BURGLARY':4, 'MOTOR VEHICLE THEFT':5, 'CRIMINAL DAMAGE':6, 'ARSON':7, 'THEFT':8, 'ASSAULT':9, 'CRIM SEXUAL ASSAULT':10}

# INITIALIZE THE SCENE
scene = getSceneManager()
scene.setBackgroundColor(Color(0, 0, 0, 1))
env = getSoundEnvironment()
all = SceneNode.create("everything")

# create a directional light
light1 = Light.create()
light1.setLightType(LightType.Directional)
light1.setLightDirection(Vector3(-1.0, -1.0, -1.0))
light1.setColor(Color(0.7, 0.7, 0.7, 1.0))
light1.setAmbient(Color(0.5, 0.5, 0.5, 1.0))
light1.setEnabled(True)

# load some earth models
torusModel1 = ModelInfo()
torusModel2 = ModelInfo()
torusModel3 = ModelInfo()
torusModel4 = ModelInfo()

torusModel1.name = "earth"
torusModel2.name = "map"
torusModel3.name = 'yahoo_earth'
torusModel4.name = 'yahoo_map'

if caveutil.isCAVE():
	torusModel2.path = "openstreetmap.earth"
	#torusModel2.path = "simple.earth"
	#laptop: crash when start
	#cave: it works!

	torusModel1.path = "mapquestaerial.earth"
	#torusModel.path = "simple.earth"
	#laptop: crash when start
	#cave: it works!

	torusModel3.path = "yahoo_aerial.earth"
	#laptop: it works (without showing anything)
	#cave: works (too low no data)

	torusModel4.path = "yahoo_maps.earth"
	#laptop: crash during running / it works (without showing anything)
	#cave: works (too low no data)

else:
	torusModel1.path = "simple.earth"
	torusModel2.path = "simple.earth"

scene.loadModel(torusModel1)
scene.loadModel(torusModel2)
scene.loadModel(torusModel3)
scene.loadModel(torusModel4)

# create scene objects using the loaded models
torus1 = StaticObject.create("earth")
torus1.getMaterial().setLit(False)
all.addChild(torus1)

torus2 = StaticObject.create("map")
torus2.getMaterial().setLit(False)
all.addChild(torus2)
torus2.setVisible(False)

torus3 = StaticObject.create("yahoo_earth")
torus3.getMaterial().setLit(False)
all.addChild(torus3)
torus3.setVisible(False)

torus4 = StaticObject.create("yahoo_map")
torus4.getMaterial().setLit(False)
all.addChild(torus3)
torus4.setVisible(False)

# paths for crime sprites
spritePath = [None]*11
for i in range(1,11):
	spritePath[i] = "icon/"+str(i)+".png"

# create crime models
spriteSize = sprite.createSizeUniform()
#spriteSize.setFloat(0.1)
spriteWindowSize = sprite.createWindowSizeUniform()
#if caveutil.isCAVE():
#	spriteWindowSize.setVector2f(Vector2(10000, 1000))
#else:
spriteWindowSize.setVector2f(Vector2(854, 480))

# get the camera
cam = getDefaultCamera()
setNearFarZ(1, 20 * r_a)

# set the camera by hand
cam.setPosition(Vector3(193124.87, -4767697.65, 4228566.18))
cam.setOrientation(Quaternion(0.6, 0.8, 0.0, 0.0))

# set a fast speed for travel by default
cam.getController().setSpeed(10000)

# set interpolation animation
interp = InterpolActor(cam)
interp.setTransitionType(InterpolActor.SMOOTH)
interp.setDuration(3)
interp.setOperation(InterpolActor.POSITION | InterpolActor.ORIENT)

## HOW TO GO TO A COMMUNITY
def goCommunities(x):
	print "going to %s at (%f,%f)" %(comm[x].name, comm[x].lat, comm[x].lon)
	newLat = comm[x].lat-5/110.94 # 1 lat is 110940 meters, we want 3km south to the particular point
	newLon = comm[x].lon
	newPos = llh2ecef(newLat, newLon, 3000) # 5000 meters high

	interp.setTargetPosition(newPos)
	interp.setTargetOrientation(Quaternion(0.6, 0.8, 0.0, 0.0))
	interp.startInterpolation()
	playMovingSound()
	# TO DO show data of this community

class community:
	name = ''
	lat = 0
	lon = 0
	pos = Vector3()
	numCrime = [[0]*11 for i in range(0,14)]
	numCrimeShown = 0
	numHour = [0]*4
	numDay = [0]*7
	numSeason = [0]*5
	def __init__(self, n, x, y):
		self.name = n
		self.lat = x
		self.lon = y
		self.pos = llh2ecef(x,y,0)
		self.numCrimeShown = 0
		self.numCrime = [[0]*11 for xx in range(0,14)]

comm = [None]*78
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

# SHOW CRIME AS HOUR/DAY/SEASON
nodeHDSParent = SceneNode.create('nodeHDSParent')

all.addChild(nodeHDSParent)

nodeHDS = [[None]*7 for i in range(78)]

for i in range(1,78):
	for j in range(7):
		nodeHDS[i][j] = BoxShape.create(200,1000,200)
		nodeHDSParent.addChild(nodeHDS[i][j])
nodeHDSParent.setChildrenVisible(False)

# HOW TO FILTER CRIME TYPES AND YEARS AND MORE

notCrime = set()
notYear = set()
notCom = set()
needUpdateHDS = True

## CLICK CRIME TYPE FILTER BUTTONS
def clickCrime(crime):
	global needUpdateHDS

	if btn_none.isChecked()==False:
		needUpdateHDS = True

	if crime==0:
		if btnCrime[0].isChecked(): # if we want to show all
			notCrime.clear()
			for j in range(1,11):
				if btnCrime[j].isChecked()==False:
					notCrime.add(j) # collect all crimes currently not checked
					btnCrime[j].setChecked(True)
					clickCrime(j)
		else: # if we want to quit show all
			for j in notCrime:
				btnCrime[j].setChecked(False)
				clickCrime(j)
	else: # individual crime type
		if btnCrime[crime].isChecked(): # if we want to check this crime
			for com in range(1,78):
				for year in range(1,14):
					n = nodeComm[com].getChildByIndex(year)
					n.getChildByIndex(crime).setVisible(True)
					if n.isVisible(): # if this year is visible, toggle crime drawables
						n.getChildByIndex(crime).setChildrenVisible(True)
						comm[com].numCrimeShown+=comm[com].numCrime[year][crime]
						labelComm[com].setText(comm[com].name+' ('+str(comm[com].numCrimeShown)+')')
		else: # if we want to uncheck this crime
			if btnCrime[0].isChecked(): # nothing happens
				btnCrime[crime].setChecked(True)
				return 0
			for com in range(1,78):
				for year in range(1,14):
					n = nodeComm[com].getChildByIndex(year)
					n.getChildByIndex(crime).setVisible(False)
					if n.isVisible(): # if this year is visible, toggle crime drawables
						n.getChildByIndex(crime).setChildrenVisible(False)
						comm[com].numCrimeShown-=comm[com].numCrime[year][crime]
						labelComm[com].setText(comm[com].name+' ('+str(comm[com].numCrimeShown)+')')

## CLICK YEAR FILTER BUTTONS
def clickYear(year):
	global needUpdateHDS

	if btn_none.isChecked()==False:
		needUpdateHDS = True

	if year==0:
		if btnYear[0].isChecked(): # if we want to show all
			notYear.clear()
			for j in range(1,14):
				if btnYear[j].isChecked()==False:
					notYear.add(j) # collect all years currently not checked
					btnYear[j].setChecked(True)
					clickYear(j)
		else: # if we want to quit show all
			for j in notYear:
				btnYear[j].setChecked(False)
				clickYear(j)
	else: # individual year
		if btnYear[year].isChecked(): # if we want to check this year
			for com in range(1,78):
				for crime in range(1,11):
					n = nodeComm[com].getChildByIndex(year)
					n.setVisible(True)
					if n.getChildByIndex(crime).isVisible(): # if this crime is visible, toggle crime drawables
						n.getChildByIndex(crime).setChildrenVisible(True)
						comm[com].numCrimeShown+=comm[com].numCrime[year][crime]
						labelComm[com].setText(comm[com].name+' ('+str(comm[com].numCrimeShown)+')')
		else: # if we want to uncheck this year
			if btnYear[0].isChecked(): # nothing happens
				btnCrime[year].setChecked(True)
				return 0
			for com in range(1,78):
				for crime in range(1,11):
					n = nodeComm[com].getChildByIndex(year)
					n.setVisible(False)
					if n.getChildByIndex(crime).isVisible(): # if this crime is visible, toggle crime drawables
						n.getChildByIndex(crime).setChildrenVisible(False)
						comm[com].numCrimeShown-=comm[com].numCrime[year][crime]
						labelComm[com].setText(comm[com].name+' ('+str(comm[com].numCrimeShown)+')')
					else:
						nodeComm[com].setVisible(False)

## CLICK INFO FILTER BUTTONS
def clickMoreInfo():
	global needUpdateHDS

	if btn_none.isChecked(): # nothing
		needUpdateHDS = False
		nodeHDSParent.setChildrenVisible(False)

	elif btn_hour.isChecked(): # hour
		needUpdateHDS = False
		nodeHDSParent.setChildrenVisible(False)

		for i in range(1,78):
			comm[i].numHour = [0]*4
		f = open('CrimesAll__hour.csv','rb')
		csvHourRead = csv.reader(f)
		for line in csvHourRead:
			if btnYear[int(line[1])-2000].isChecked() and btnCrime[int(line[2])].isChecked():
				com = int(line[0])
				comm[com].numHour[0]+=int(line[3])
				comm[com].numHour[1]+=int(line[4])
				comm[com].numHour[2]+=int(line[5])
				comm[com].numHour[3]+=int(line[6])
		f.close()

		numHourMax = 0
		for com in range(1,78):
			for i in range(4):
				if comm[com].numHour[i]>numHourMax:
					numHourMax = comm[com].numHour[i]

		if (numHourMax!=0):
			for com in range(1,78):
				for i in range(4):
					ratio = (comm[com].numHour[i]+0.0)/(numHourMax+0.0)
					nodeHDS[com][i].setPosition(comm[com].pos)
					caveutil.orientWithHead(cam,nodeHDS[com][i])
					nodeHDS[com][i].translate(200*(i-1.5),500*ratio+200,0, Space.Local)
					nodeHDS[com][i].setScale(1,ratio,1)

					if (ratio > 0.8):
						nodeHDS[com][i].setEffect('colored -d #A23333')
					elif (ratio > 0.6):
						nodeHDS[com][i].setEffect('colored -d #EA6A40')
					elif (ratio > 0.4):
						nodeHDS[com][i].setEffect('colored -d #DCA53D')
					elif (ratio > 0.2):
						nodeHDS[com][i].setEffect('colored -d #4F9337')
					else:
						nodeHDS[com][i].setEffect('colored -d silver')
					nodeHDS[com][i].setVisible(True)

	elif btn_day.isChecked(): # day
		needUpdateHDS = False

		for i in range(1,78):
			comm[i].numDay = [0]*7
		f = open('CrimesAll__day.csv','rb')
		csvDayRead = csv.reader(f)
		for line in csvDayRead:
			if btnYear[int(line[1])-2000].isChecked() and btnCrime[int(line[2])].isChecked():
				com = int(line[0])
				comm[com].numDay[0]+=int(line[3])
				comm[com].numDay[1]+=int(line[4])
				comm[com].numDay[2]+=int(line[5])
				comm[com].numDay[3]+=int(line[6])
				comm[com].numDay[4]+=int(line[7])
				comm[com].numDay[5]+=int(line[8])
				comm[com].numDay[6]+=int(line[9])
		f.close()

		numDayMax = 0
		for com in range(1,78):
			for i in range(7):
				if comm[com].numDay[i]>numDayMax:
					numDayMax = comm[com].numDay[i]

		if (numDayMax!=0):
			for com in range(1,78):
				for i in range(7):
					ratio = (comm[com].numDay[i]+0.0)/(numDayMax+0.0)
					nodeHDS[com][i].setPosition(comm[com].pos)
					caveutil.orientWithHead(cam,nodeHDS[com][i])
					nodeHDS[com][i].translate(200*(i-1.5),500*ratio+200,0, Space.Local)
					nodeHDS[com][i].setScale(1,ratio,1)

					if (ratio > 0.8):
						nodeHDS[com][i].setEffect('colored -d #A23333')
					elif (ratio > 0.6):
						nodeHDS[com][i].setEffect('colored -d #EA6A40')
					elif (ratio > 0.4):
						nodeHDS[com][i].setEffect('colored -d #DCA53D')
					elif (ratio > 0.2):
						nodeHDS[com][i].setEffect('colored -d #4F9337')
					else:
						nodeHDS[com][i].setEffect('colored -d silver')
			nodeHDSParent.setChildrenVisible(True)
		else:
			nodeHDSParent.setChildrenVisible(False)

	elif btn_season.isChecked(): # season
		needUpdateHDS = False
		nodeHDSParent.setChildrenVisible(False)

		for i in range(1,78):
			comm[i].numSeason = [0]*4
		f = open('CrimesAll__season.csv','rb')
		csvSeasonRead = csv.reader(f)
		for line in csvSeasonRead:
			if btnYear[int(line[1])-2000].isChecked() and btnCrime[int(line[2])].isChecked():
				com = int(line[0])
				comm[com].numSeason[0]+=int(line[3])
				comm[com].numSeason[1]+=int(line[4])
				comm[com].numSeason[2]+=int(line[5])
				comm[com].numSeason[3]+=int(line[6])
		f.close()

		numSeasonMax = 0
		for com in range(1,78):
			for i in range(4):
				if comm[com].numSeason[i]>numSeasonMax:
					numSeasonMax = comm[com].numSeason[i]

		if (numSeasonMax!=0):
			for com in range(1,78):
				for i in range(4):
					ratio = (comm[com].numSeason[i]+0.0)/(numSeasonMax+0.0)
					nodeHDS[com][i].setPosition(comm[com].pos)
					caveutil.orientWithHead(cam,nodeHDS[com][i])
					nodeHDS[com][i].translate(200*(i-1.5),500*ratio+200,0, Space.Local)
					nodeHDS[com][i].setScale(1,ratio,1)

					if (ratio > 0.8):
						nodeHDS[com][i].setEffect('colored -d #A23333')
					elif (ratio > 0.6):
						nodeHDS[com][i].setEffect('colored -d #EA6A40')
					elif (ratio > 0.4):
						nodeHDS[com][i].setEffect('colored -d #DCA53D')
					elif (ratio > 0.2):
						nodeHDS[com][i].setEffect('colored -d #4F9337')
					else:
						nodeHDS[com][i].setEffect('colored -d silver')
					nodeHDS[com][i].setVisible(True)

##############################################################################################################
# CREATE MENUS
mm = MenuManager.createAndInitialize()
menu0_chicago = mm.getMainMenu().addSubMenu("Chicago Panel")

menu1_0_comm = menu0_chicago.addSubMenu("WATCH A COMMUNITY")

menu1_0_1 = menu1_0_comm.addSubMenu("Far North Side")
menu1_0_2 = menu1_0_comm.addSubMenu("Northwest Side")
menu1_0_3 = menu1_0_comm.addSubMenu("North Side")
menu1_0_4 = menu1_0_comm.addSubMenu("West Side")
menu1_0_5 = menu1_0_comm.addSubMenu("Central")
menu1_0_6 = menu1_0_comm.addSubMenu("South Side")
menu1_0_7 = menu1_0_comm.addSubMenu("Southwest Side")
menu1_0_8 = menu1_0_comm.addSubMenu("Far Southwest Side")
menu1_0_9 = menu1_0_comm.addSubMenu("Far Southeast Side")

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

btn_15 = menu1_0_2.addButton("Portage Park", "goCommunities(15)")
btn_16 = menu1_0_2.addButton("Irving Park", "goCommunities(16)")
btn_17 = menu1_0_2.addButton("Dunning", "goCommunities(17)")
btn_18 = menu1_0_2.addButton("Montclare", "goCommunities(18)")
btn_19 = menu1_0_2.addButton("Belmont Cragin", "goCommunities(19)")
btn_20 = menu1_0_2.addButton("Hermosa", "goCommunities(20)")

btn_05 = menu1_0_3.addButton("North Center", "goCommunities(5)")
btn_06 = menu1_0_3.addButton("Lake View", "goCommunities(6)")
btn_07 = menu1_0_3.addButton("Lincoln Park", "goCommunities(7)")
btn_21 = menu1_0_3.addButton("Avondale", "goCommunities(21)")
btn_22 = menu1_0_3.addButton("Logan Square", "goCommunities(22)")

btn_23 = menu1_0_4.addButton("Humboldt Park", "goCommunities(23)")
btn_24 = menu1_0_4.addButton("West Town", "goCommunities(24)")
btn_25 = menu1_0_4.addButton("Austin", "goCommunities(25)")
btn_26 = menu1_0_4.addButton("West Garfield Park", "goCommunities(26)")
btn_27 = menu1_0_4.addButton("East Garfield Park", "goCommunities(27)")
btn_28 = menu1_0_4.addButton("Near West Side", "goCommunities(28)")
btn_29 = menu1_0_4.addButton("North Lawndale", "goCommunities(29)")
btn_30 = menu1_0_4.addButton("South Lawndale", "goCommunities(30)")
btn_31 = menu1_0_4.addButton("Lower West Side", "goCommunities(31)")

btn_08 = menu1_0_5.addButton("Near North Side", "goCommunities(8)")
btn_32 = menu1_0_5.addButton("Loop", "goCommunities(32)")
btn_33 = menu1_0_5.addButton("Near South Side", "goCommunities(33)")

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

btn_70 = menu1_0_8.addButton("Ashburn", "goCommunities(70)")
btn_71 = menu1_0_8.addButton("Auburn Gresham", "goCommunities(71)")
btn_72 = menu1_0_8.addButton("Beverly", "goCommunities(72)")
btn_73 = menu1_0_8.addButton("Washington Heights", "goCommunities(73)")
btn_74 = menu1_0_8.addButton("Mount Greenwood", "goCommunities(74)")
btn_75 = menu1_0_8.addButton("Morgan Park", "goCommunities(75)")

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
btnCrime = [None]*11
for i in range(0,11):
	btnCrime[i] = Button.create(cc)
	btnCrime[i].setCheckable(True)
	btnCrime[i].setChecked(True)
	btnCrime[i].setUIEventCommand('clickCrime('+str(i)+')')
btnCrime[0].setChecked(False)

btnCrime[0].setText("ALL MAJOR CRIMES")
btnCrime[1].setText("Homicide")
btnCrime[2].setText("Kidnapping")
btnCrime[3].setText("Robbdery")
btnCrime[4].setText("Burglary (Forcible Entry)")
btnCrime[5].setText("Motor Vehicle Theft")
btnCrime[6].setText ("Vandalism (and damage to the City of Chicago)")
btnCrime[7].setText("Arson")
btnCrime[8].setText("Theft (over $500)")
btnCrime[9].setText("Aggravated Assault")
btnCrime[10].setText("Aggravated Sexual Assault")

menu1_2filter = menu0_chicago.addSubMenu("FILTER YEARS")
cc = menu1_2filter.getContainer()
btnYear = [None]*14
for ii in range(0,14): # from 2013 to 2001
	if (ii==0):
		btnYear[0] = Button.create(cc)
		btnYear[0].setCheckable(True)
		btnYear[0].setChecked(False)
		btnYear[0].setUIEventCommand('clickYear(0)')
		btnYear[0].setText("ALL YEARS")
	else:
		i = 14-ii
		btnYear[i] = Button.create(cc)
		btnYear[i].setCheckable(True)
		btnYear[i].setChecked(False)
		btnYear[i].setUIEventCommand('clickYear('+str(i)+')')
		btnYear[i].setText(str(2000+i))
btnYear[13].setChecked(True)

menu1_3more = menu0_chicago.addSubMenu("MORE INFO")
cc = menu1_3more.getContainer()
btn_none = Button.create(cc)
btn_none.setUIEventCommand('clickMoreInfo()')
btn_none.setCheckable(True)
btn_none.setRadio(True)
btn_none.setChecked(True)
btn_none.setText('no more info')

btn_hour = Button.create(cc)
btn_hour.setUIEventCommand('clickMoreInfo()')
#btn_hour.setChecked(True)
btn_hour.setCheckable(True)
btn_hour.setRadio(True)
btn_hour.setText('hour of day')

btn_day = Button.create(cc)
btn_day.setUIEventCommand('clickMoreInfo()')
btn_day.setCheckable(True)
btn_day.setRadio(True)
btn_day.setText('day of week')

btn_season = Button.create(cc)
btn_season.setUIEventCommand('clickMoreInfo()')
btn_season.setCheckable(True)
btn_season.setRadio(True)
btn_season.setText('season of year')

menu1_4simu = menu0_chicago.addSubMenu("REAL TIME WATCH")
cc = menu1_4simu.getContainer()
label_simu = Label.create(cc)
label_simu.setText("TEST SIMULATION")
# TO DO simulation

# CTA stops
f = open('CHICAGO_DATA/cta_L_stops/cta_L_stops_final.csv', 'rb')
ctastops = csv.reader(f)
for stop in ctastops:
	model = SphereShape.create(50, 3)

	pos = llh2ecef(float(stop[1]), float(stop[0]), 0.0)
	model.setPosition(pos)
	model.setEffect('colored -d white')

	text = Text3D.create('font/helvetica.ttf', 100, stop[2])
	if caveutil.isCAVE()==False:
		text = Text3D.create('font/helvetica.ttf', 15, stop[2])
	caveutil.orientWithHead(cam, text)
	text.roll(math.pi/4*0.75)

	posText = llh2ecef(float(stop[1]), float(stop[0]), 100.0)
	text.setPosition(posText)
	text.setFixedSize(True)
	if caveutil.isCAVE():
		text.setColor(Color('black'))
	else:
		text.setColor(Color('white'))

	all.addChild(model)
	all.addChild(text)
f.close()

# CTA lines
f = open('CHICAGO_DATA/CTARailLines.csv','rb')
ctaLines = csv.reader(f)
for seg in ctaLines:
	xLine = LineSet.create()
	oldPos = Vector3()
	for i in range(0,len(seg)):
		if i==0:
			if (seg[i]=='BL'):
				xLine.setEffect("colored -d #00a1de")
			elif (seg[i]=='BR'):
				xLine.setEffect("colored -d #62361b")
			elif (seg[i]=='GR'):
				xLine.setEffect("colored -d #009b3a")
			elif (seg[i]=='ML'):
				xLine.setEffect("colored -d #565a5c")
			elif (seg[i]=='OR'):
				xLine.setEffect("colored -d #f9461c")
			elif (seg[i]=='PK'):
				xLine.setEffect("colored -d #e27ea6")
			elif (seg[i]=='PR'):
				xLine.setEffect("colored -d #522398")
			elif (seg[i]=='RD'):
				xLine.setEffect("colored -d #c60c30")
			elif (seg[i]=='YL'):
				xLine.setEffect("colored -d #f9e300")
		elif i==1:
			coo = seg[i].split(',')
			oldPos = llh2ecef(float(coo[1]),float(coo[0]), 0.0)
		else:
			coo = seg[i].split(',')
			pos = llh2ecef(float(coo[1]),float(coo[0]), 0.0)
			l = xLine.addLine()
			l.setStart(oldPos)
			l.setEnd(pos)
			l.setThickness(60.0)
			oldPos = pos
	all.addChild(xLine)
f.close()

# GET TRAIN LOCATION FROM CTA
nodeTrainParent = SceneNode.create("allTrain")
all.addChild(nodeTrainParent)

def getTrainInfo():
	print ("updating...")
	train_xml = urllib2.urlopen('http://lapi.transitchicago.com/api/1.0/ttpositions.aspx?key=484807ed614d4ffb8f31bab10357ba4f&rt=red,blue,brn,g,org,p,pink,y').read()
	root = ET.fromstring(train_xml)

	num = nodeTrainParent.numChildren()
	for i in range(0,num):
		nodeTrainParent.removeChildByIndex(0)

	for route in root:
		for train in route:
			lat = float(train.find('lat').text)
			lon = float(train.find('lon').text)
			heading = float(train.find('heading').text)

			pos = llh2ecef(lat, lon, 70)
			model = BoxShape.create(50,40,300)
			#model.setBoundingBoxVisible(True)
			model.setPosition(pos[0],pos[1],pos[2])
			lookHeading = heading-90 # let east is 0, south is 90, west is 180, north is 270
			if lookHeading<0:
				lookHeading+=360
			lookLat = lat - math.sin(lookHeading*math.pi/180.0)/1109.4
			lookLon = lon + math.cos(lookHeading*math.pi/180.0)/852.7
			model.lookAt(llh2ecef(lookLat, lookLon, 110), model.convertWorldToLocalPosition(1.1*Vector3(pos[0],pos[1],pos[2])))
			#model.yaw()
			model.setEffect('colored -d white')
			nodeTrainParent.addChild(model)
	print ("updated!")

# VICE CITY
#viceCity="""

nodeComm = [None]*78
nodeYear = [None]*14
nodeCrime = [None]*11

nodeViceCityParent = SceneNode.create('VICE CITY')
all.addChild(nodeViceCityParent)

for i in range(0,78):
	name = "comm"+str(i)
	nodeComm[i] = SceneNode.create(name)
	nodeViceCityParent.addChild(nodeComm[i])
	for j in range(0,14):
		name1 = name+"year"+str(2000+j)
		nodeYear[j] = SceneNode.create(name1)
		if (j==13):
			nodeYear[j].setVisible(True)
		else:
			nodeYear[j].setVisible(False)
		nodeComm[i].addChild(nodeYear[j])
		for k in range(0,11):
			name2 = name1+"crimetype"+str(k)
			nodeCrime[k] = SceneNode.create(name2)
			nodeYear[j].addChild(nodeCrime[k])

count = 0
f = open('CrimesAll_final.csv', 'rb')
lines = csv.reader(f)
atLine = 0
for items in lines:
	atLine+=1
	if (atLine>1000):
		break
	crime_type = items[2]
	crime_comm = int(items[4])
	crime_year = int(items[5])
	crime_lat = float(items[6])
	crime_lon = float(items[7])
	#crime_year = 2013
	#crime_lat = float(items[5])
	#crime_lon = float(items[6])

	pos = llh2ecef(crime_lat, crime_lon, 100.0)

	crimeIcon = sprite.createSprite(spritePath[crimeType[crime_type]], spriteSize, spriteWindowSize, True)
	crimeIcon.setPosition(pos)
	crimeIcon.getMaterial().setLit(False)
	nodeComm[crime_comm].getChildByIndex(crime_year-2000).getChildByIndex(crimeType[crime_type]).addChild(crimeIcon)
	comm[crime_comm].numCrime[crime_year-2000][crimeType[crime_type]]+=1
 	if crime_year==2013:
 		comm[crime_comm].numCrimeShown+=1
f.close()

for k in range(1,11):
	print "loop's # of crime in 2013 [%d] = %d" %(k,comm[32].numCrime[13][k])

print "comm[32].numCrimeShown:",comm[32].numCrimeShown

labelComm = [None]*78

# COMMUNITY LABELS
for i in range(1,78):
	if caveutil.isCAVE():
		labelComm[i] = Text3D.create('font/Franchise-Bold-hinted.ttf', 200, comm[i].name+' ('+str(comm[i].numCrimeShown)+')')
	else:
		labelComm[i] = Text3D.create('font/Franchise-Bold-hinted.ttf', 20, comm[i].name+' ('+str(comm[i].numCrimeShown)+')') # TO DO : change the value

	posComm = llh2ecef(comm[i].lat, comm[i].lon, 300.0)
	labelComm[i].setPosition(posComm)
	labelComm[i].setFixedSize(True)
	labelComm[i].setColor(Color('black'))
	caveutil.orientWithHead(cam, labelComm[i])
	all.addChild(labelComm[i])

toggleStereo()

# TEST FACE CAMERA
#testObject = PlaneShape.create(20, 20)
#testObject.setEffect("colored -d red")
#all.addChild(testObject)
#caveutil.positionAtHead(cam, testObject, 2)
#caveutil.orientWithHead(cam, testObject)

r = 0
r2 = 0

#handle events from the wand
# left button toggle between two maps

isButton7down = False
wandOldPos = Vector3()
wandOldOri = Quaternion()

def playBtnDownSound(e):
	print ('button down')
	sd = SoundInstance(env.loadSoundFromFile('btnDown',"sound/menu/down.wav"))
	sd.setPosition( e.getPosition() )
	sd.setVolume(1.0)
	sd.setWidth(20)
	sd.play()
def playBtnUpSound(e):
	print ('button up')
	sd = SoundInstance(env.loadSoundFromFile('btnUp',"sound/menu/up.wav"))
	sd.setPosition( e.getPosition() )
	sd.setVolume(1.0)
	sd.setWidth(20)
	sd.play()

def playMovingSound():
	print ('on the move')
	sd = SoundInstance(env.loadSoundFromFile('moving',"sound/move.wav"))
	sd.setPosition( cam.getPosition() )
	sd.setVolume(1.0)
	sd.setWidth(20)
	sd.play()

def playBGM():
	sd = SoundInstance(env.loadSoundFromFile('bgm',"sound/bgm.wav"))
	sd.setPosition( cam.getPosition() )
	sd.setVolume(0.3)
	sd.setWidth(20)
	#sd.play()

# TO DO: LEGEND
uim = UiModule.createAndInitialize()
wf = uim.getWidgetFactory()
ui = uim.getUi()

legend = wf.createImage("legend", ui)
legend.setData(loadImage('icon/1.png'))
legend.setLayer(WidgetLayer.Front)
#legend.setSize(Vector2(200,200))
legend.setPosition(Vector2(854,480)-legend.getSize())

def onEvent():
	global userScaleFactor
	global isButton7down
	global wandOldPos

	e = getEvent()

	if (e.isButtonDown(EventFlags.ButtonLeft)):
		playBtnDownSound(e)
		print("changing map")
		if torus1.isVisible():
			torus1.setVisible(False)
			torus2.setVisible(True)
		elif torus2.isVisible():
			torus2.setVisible(False)
			torus3.setVisible(True)
		elif torus3.isVisible():
			torus3.setVisible(False)
			torus4.setVisible(True)
		else:
			torus4.setVisible(False)
			torus1.setVisible(True)

	elif (e.isButtonDown(EventFlags.Button7)):
		playBtnDownSound(e)
		#if isButton7down==False:
		isButton7down = True
		wandOldPos = e.getPosition()
		wandOldOri = e.getOrientation()
		print "wandOldPos:",wandOldPos
		print "wandOldOri:",wandOldOri

	elif (e.isButtonUp(EventFlags.Button7)):
		isButton7down = False

	elif (e.isButtonDown(EventFlags.Button2)):
		playBtnDownSound(e)

	elif (e.isButtonUp(EventFlags.Button2)):
		playBtnUpSound(e)

	elif (e.isButtonDown(EventFlags.Button3)):
		playBtnDownSound(e)

	elif (e.isButtonUp(EventFlags.Button3)):
		playBtnUpSound(e)

	elif (e.getType()==EventType.Update) and (isButton7down):
		e.getAxis(0)

	elif e.isKeyDown(ord('j')): # left
		#cam.setPosition( cam.convertLocalToWorldPosition( Vector3(-1,0,0)*100 ) )
		cam.translate( -100, 0, 0, Space.Local )
	elif e.isKeyDown(ord('l')): # right
		#cam.setPosition( cam.convertLocalToWorldPosition( Vector3(1,0,0)*100 ) )
		cam.translate( 100, 0, 0, Space.Local )
	elif e.isKeyDown(ord('i')): # forward
		#cam.setPosition( cam.convertLocalToWorldPosition( Vector3(0,0,-1)*100 ) )
		cam.translate( 0, 0, -100, Space.Local )
	elif e.isKeyDown(ord('k')): # backward
		#cam.setPosition( cam.convertLocalToWorldPosition( Vector3(0,0,1)*100 ) )
		cam.translate( 0, 0, 100, Space.Local )
	elif e.isKeyDown(ord('y')): # up
		#cam.setPosition( cam.convertLocalToWorldPosition( Vector3(0,1,0)*100 ) )
		cam.translate( 0, 100, 0, Space.Local )
	elif e.isKeyDown(ord('h')): # down
		#cam.setPosition( cam.convertLocalToWorldPosition( Vector3(0,-1,0)*100 ) )
		cam.translate( 0, -100, 0, Space.Local )
	elif e.isKeyDown(ord('b')):
		cam.rotate( Vector3(1,0,0), 10*math.pi/180, Space.Local )
	elif e.isKeyDown(ord('n')):
		cam.rotate( Vector3(-1,0,0), 10*math.pi/180, Space.Local )

	elif e.getServiceType() == ServiceType.Wand:
		if isButton7down:
			trans = e.getPosition()-wandOldPos
			#cam.setPosition( cam.convertLocalToWorldPosition( trans*cam.getController.getSpeed() ) )
			cam.translate( trnas*cam.getController.getSpeed(), Space.Local)
			oriVecOld = quaternionToEuler(wandOldOri)
			oriVec = quaternionToEuler(wandOri)
			cam.rotate( oriVec-oriVecOld, 5*math.pi/180, Space.Local )

trainDeltaT = 0
bgmDeltaT = 0
labelCommDeltaT = 0
#getTrainInfo()
#playBGM()

def onUpdate(frame, t, dt):
	global trainDeltaT
	global bgmDeltaT
	global labelCommDeltaT

	d = cam.getPosition()
	d0 = float(d.x)
	d1 = float(d.y)
	d2 = float(d.z)
	r = math.sqrt(d0*d0 + d1*d1 + d2*d2) - r_a # altitude in cm
	if r<400:
		r=400
	cam.getController().setSpeed(r*1.2)

	#if (t-trainDeltaT>=10):
		#print "start updating CTA trains"
		#trainDeltaT = t
		#getTrainInfo()

	if (t-bgmDeltaT>=86):
		print "replaying bgm"
		bgmDeltaT = t
		#playBGM()

	if (t-labelCommDeltaT>1):
		labelCommDeltaT = t
		for i in range(1,78):
			caveutil.orientWithHead(cam, labelComm[i])
		#if needUpdateHour or needUpdateSeason or needUpdateDay:
		if needUpdateHDS:
			print ('needUpdateHDS is True, start do it again')
			clickMoreInfo()

setEventFunction(onEvent)
setUpdateFunction(onUpdate)


never ="""
												!!!KIDNAPPING : 165 (ICON USING OTHERS)
		INTERFERE WITH PUBLIC OFFICER : 0
		PUBLIC PEACE VIOLATION : 2077
		INTERFERENCE WITH PUBLIC OFFICER : 845
	???PROSTITUTION : 1115 (ICON)
		LIQUOR LAW VIOLATION : 314
		RITUALISM : 0
															!!!ROBBERY : 7314 (7379) (ICON GET)
															BURGLARY (FORCIBLE ENTRY): 10915 (7272) (ICON GET)
!!!WEAPONS VIOLATION : 2125 (ICON)
		OTHER NARCOTIC VIOLATION : 2
												!!!HOMICIDE : 269 (273) (ICON GET)
		OBSCENITY : 16
		OFFENSES INVOLVING CHILDREN : 0
		OTHER OFFENSE : 11619
																???CRIMINAL DAMAGE (TO CITY OF CHICAGO PROPERTY, *VANDALISM): 19193 (434) (ICON GET)
															!!!MOTOR VEHICLE THEFT : 8276 (ICON GET)
															???THEFT (over $500): 42018 (8944) (ICON GET)
		OFFENSE INVOLVING CHILDREN : 1453
		GAMBLING : 430
		PUBLIC INDECENCY : 6
		NON-CRIMINAL (SUBJECT SPECIFIED) : 0
												!!!ARSON : 261 (ICON GET)
		INTIMIDATION : 93
		SEX OFFENSE : 616
		NARCOTICS : 22027
		DECEPTIVE PRACTICE : 7351
		BATTERY : 35456
		CRIMINAL TRESPASS : 5208
		STALKING : 81
																ASSAULT (AGGRAVATED*): 11297 (2479) (ICON GET)
												CRIM SEXUAL ASSAULT (AGGRAVATED*): 761 (190) (ICON GET)
		NON-CRIMINAL : 3
		DOMESTIC VIOLENCE : 0
"""

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
