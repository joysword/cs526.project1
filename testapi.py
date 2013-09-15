try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

import urllib2

train_xml = urllib2.urlopen('http://lapi.transitchicago.com/api/1.0/ttpositions.aspx?key=484807ed614d4ffb8f31bab10357ba4f&rt=red,blue,brn,g,org,p,pink,y').read()
root = ET.fromstring(train_xml)
for route in root:
	for train in route:
		lat = float(train.find('lat').text)
		lon = float(train.find('lon').text)
		print "route: %s, train: %s, at: (%f,%f)" %(route.get('name'), train.find('rn').text, lat, lon)
