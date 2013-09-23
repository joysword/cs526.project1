import csv

f = open('CrimesAll_final.csv','rb')

read = csv.reader(f)

crimeType = {'ALL':0, 'HOMICIDE':1, 'KIDNAPPING':2, 'ROBBERY':3, 'BURGLARY':4, 'MOTOR VEHICLE THEFT':5, 'CRIMINAL DAMAGE':6, 'ARSON':7, 'THEFT':8, 'ASSAULT':9, 'CRIM SEXUAL ASSAULT':10}

numCrime = [0]*11
numYear = [0]*14

for line in read:
	numCrime[crimeType[line[2]]]+=1
	numYear[int(line[5])-2000]+=1

for i in range(1,11):
	print i,numCrime[i]
for i in range(1,14):
	print i+2000,numYear[i]
