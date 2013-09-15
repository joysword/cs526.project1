scale = 2

box = BoxShape.create(5/scale, 6/scale, 15/scale)
x = LineSet.create()
line = x.addLine()
line.setStart(Vector3(0,0,0))
line.setEnd(Vector3(50,0,0))
line.setThickness(0.5)

y = LineSet.create()
line = y.addLine()
line.setStart(Vector3(0,0,0))
line.setEnd(Vector3(0,50,0))
line.setThickness(0.5)

z = LineSet.create()
line = z.addLine()
line.setStart(Vector3(0,0,0))
line.setEnd(Vector3(0,0,50))
line.setThickness(0.5)

box.setEffect('colored -d white')
x.setEffect('colored -d red')
y.setEffect('colored -d green')
z.setEffect('colored -d blue')

# Create a directional light
light1 = Light.create()
light1.setLightType(LightType.Directional)
light1.setLightDirection(Vector3(-1.0, -1.0, -1.0))
light1.setColor(Color(0.7, 0.7, 0.7, 1.0))
light1.setAmbient(Color(0.5, 0.5, 0.5, 1.0))
light1.setEnabled(True)

box.setPosition(Vector3(0,1.5,0))
box.lookAt(Vector3(1,0,-1), Vector3(0,1,0))

cam = getDefaultCamera()

cam.setPosition(Vector3(0,1,10))