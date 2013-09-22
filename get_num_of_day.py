import csv

f = open('Crimes2012_final.csv','rb')
res = open('Crimes2012_final_numday.csv','wb')

csvread = csv.reader(f)
csvwrite = csv.writer(res)

for line in csvread:
	myDate = line[0]

	i=5
	month = int(myDate[i])
	i+=1
	while cmp(myDate[i],'-')!=0:
		month=month*10+int(myDate[i])
		i+=1
	i+=1
	day = int(myDate[i])
	i+=1
	while cmp(myDate[i],' ')!=0:
		day=day*10+int(myDate[i])
		i+=1
	n = 0
	if month==1:
		n = day
	elif month==2:
		n = 31+day
	elif month==3:
		n = 31+28+day
	elif month==4:
		n = 31+28+31+day
	elif month==5:
		n = 31+28+31+30+day
	elif month==6:
		n = 31+28+31+30+31+day
	elif month==7:
		n = 31+28+31+30+31+30+day
	elif month==8:
		n = 31+28+31+30+31+30+31+day
	elif month==9:
		n = 31+28+31+30+31+30+31+31+day
	elif month==10:
		n = 31+28+31+30+31+30+31+31+30+day
	elif month==11:
		n = 31+28+31+30+31+30+31+31+30+31+day
	else:
		n = 31+28+31+30+31+30+31+31+30+31+30+day
	hour = 0
	i+=1
	while cmp(myDate[i],':')!=0:
		hour=hour*10+int(myDate[i])
		i+=1
	minute = 0
	i+=1
	while i<len(myDate):
		minute=minute*10+int(myDate[i])
		i+=1
	minute += (n-1)*24*60+hour*60
	csvwrite.writerow((line[0],line[1],line[2],line[3],line[4],line[5],n,minute))

