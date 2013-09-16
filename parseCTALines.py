import csv

try:
	import xml.etree.cElementTree as ET
except ImportError:
	import xml.etree.ElementTree as ET

csvwrite = csv.writer(open('CHICAGO_DATA/CTARailLines.csv', 'wb'))

tree = ET.parse('CHICAGO_DATA/CTARailLines.kml')

root = tree.getroot()

start = root.find('Folder')

row=[]

count = 0

for segment in start.findall('Placemark'):
	html = segment.find('description').text

	if (html.find('<td>BL</td>')!=-1):
		row.append('BL')
	elif (html.find('<td>BR</td>')!=-1):
		row.append('BR')
	elif (html.find('<td>GR</td>')!=-1):
		row.append('GR')
	elif (html.find('<td>ML</td>')!=-1):
		row.append('ML')
	elif (html.find('<td>OR</td>')!=-1):
		row.append('OR')
	elif (html.find('<td>PK</td>')!=-1):
		row.append('PK')
	elif (html.find('<td>PR</td>')!=-1):
		row.append('PR')
	elif (html.find('<td>RD</td>')!=-1):
		row.append('RD')	
	elif (html.find('<td>YL</td>')!=-1):
		row.append('YL')

	coo = segment.find('MultiGeometry').find('LineString').find('coordinates').text

	points = coo.split(' ')

	for p in points:
		p = p.strip()
		if (cmp(p,'')!=0):
			pp = p.split(',')
			str = pp[0]+","+pp[1]
			row.append(str)

	csvwrite.writerow(row)
	row=[]

