import csv

try:
	import xml.etree.cElementTree as ET
except ImportError:
	import xml.etree.ElementTree as ET

csvwrite = csv.writer(open('CHICAGO_DATA/commareas.csv', 'wb'))

tree = ET.parse('CHICAGO_DATA/commareas/CommAreas.kml')

root = tree.getroot()
print root
row=[]

at = 0
for segment in root.findall('Placemark'):
	at+=1
	print at
	html = segment.find('description').text

	str = '<strong><span class="atr-name">AREA_NUMBE</span>:</strong> <span class="atr-value">'
	p = html.find(str)
	print "p:",p
	p+=len(str)
	print "p:",p
	print html[p]

	num = 0

	while cmp(html[p],'<')!=0:
		num=num*10+int(html[p])
		print "num:",num
		p+=1

	coo = segment.find('MultiGeometry').find('Point').find('coordinates').text
	points = coo.split(',')
	lon = float(points[0])
	lat = float(points[1])

	row.append(num)
	row.append(lat)
	row.append(lon)

	line = segment.find('MultiGeometry').find('Polygon').find('outerBoundaryIs').find('LinearRing').find('coordinates').text

	points = line.split(' ')

	for p in points:
		p = p.strip()
		if (cmp(p,'')!=0):
			pp = p.split(',')
			str = pp[0]+","+pp[1]
			row.append(str)
	csvwrite.writerow(row)
	row=[]

