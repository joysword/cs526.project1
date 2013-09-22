import csv

# 1 day of week
# 2 type
# 4 comm
# 5 year
# 8 month
# 9 date
# 10 hour

f = open('CrimesAll_final.csv', 'rb')
reshou = open('CrimesAll_hour.csv', 'wb')
reswee = open('CrimesAll_day.csv', 'wb')
ressea = open('CrimesAll_season.csv', 'wb')

csvread = csv.reader(f)
houwrite = csv.writer(reshou)
weewrite = csv.writer(reswee)
seawrite = csv.writer(ressea)

crimeType = {'ALL':0, 'HOMICIDE':1, 'KIDNAPPING':2, 'ROBBERY':3, 'BURGLARY':4, 'MOTOR VEHICLE THEFT':5, 'CRIMINAL DAMAGE':6, 'ARSON':7, 'THEFT':8, 'ASSAULT':9, 'CRIM SEXUAL ASSAULT':10}

hour=[[[[0]*4 for crime in range(11)] for year in range(14)] for comm in range(78)]
weekday=[[[[0]*7 for crime in range(11)] for year in range(14)] for comm in range(78)]
season=[[[[0]*4 for crime in range(11)] for year in range(14)] for comm in range(78)]

#comm year type
for line in csvread:
	comm = int(line[4])
	year = int(line[5])
	crime = crimeType[line[2]]
	h = int(line[10])
	m = int(line[8])
	w = int(line[1])

	if h<6:
		hour[comm][year-2000][crime][0]+=1
		#if comm==32 and year==2013 and crime==8:	
		#	print '0:',hour[32][13][8][0]
	elif h<12:
		hour[comm][year-2000][crime][1]+=1
		#if comm==32 and year==2013 and crime==8:	
		#	print '1:',hour[32][13][8][1]
	elif h<18:
		hour[comm][year-2000][crime][2]+=1
		#if comm==32 and year==2013 and crime==8:
		#	print '2:',hour[32][13][8][2]
	else:
		hour[comm][year-2000][crime][3]+=1
		#if comm==32 and year==2013 and crime==8:
		#	print '3:',hour[32][13][8][3]
	
	if m<4:
		season[comm][year-2000][crime][0]+=1
		#if comm==32 and year==2013 and crime==8:	
		#	print '0:',season[32][13][8][0]
	elif m<7:
		season[comm][year-2000][crime][1]+=1
		#if comm==32 and year==2013 and crime==8:	
		#	print '1:',season[32][13][8][1]
	elif m<10:
		season[comm][year-2000][crime][2]+=1
		#if comm==32 and year==2013 and crime==8:	
		#	print '2:',season[32][13][8][2]
	else:
		season[comm][year-2000][crime][3]+=1
		#if comm==32 and year==2013 and crime==8:	
		#	print '3:',season[32][13][8][3]

	weekday[comm][year-2000][crime][w]+=1
	#if comm==32 and year==2013 and crime==8:
	#	print '%d: %d' %(w,weekday[32][13][8][w-1])

f.close()

for comm in range(1,78):
	for year in range(1,14):
		for crime in range(1,11):
			houwrite.writerow( (comm,year+2000,crime,hour[comm][year][crime][0],hour[comm][year][crime][1],hour[comm][year][crime][2],hour[comm][year][crime][3]) )
			weewrite.writerow( (comm,year+2000,crime,weekday[comm][year][crime][0],weekday[comm][year][crime][1],weekday[comm][year][crime][2],weekday[comm][year][crime][3],weekday[comm][year][crime][4],weekday[comm][year][crime][5],weekday[comm][year][crime][6]) )
			seawrite.writerow( (comm,year+2000,crime,season[comm][year][crime][0],season[comm][year][crime][1],season[comm][year][crime][2],season[comm][year][crime][3]) )

ressea.close()
reswee.close()
reshou.close()