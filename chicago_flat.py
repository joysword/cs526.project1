from omega import *
from cyclops import *

scene = getSceneManager()

# Load a static model
torusModel = ModelInfo()
torusModel.name = "torus"
torusModel.path = "chicago_flat.map.earth"
scene.loadModel(torusModel)

# Create a directional light                                                        
light1 = Light.create()
light1.setLightType(LightType.Directional)
light1.setLightDirection(Vector3(-1.0, -1.0, -1.0))
light1.setColor(Color(0.7, 0.7, 0.7, 1.0))
light1.setAmbient(Color(0.5, 0.5, 0.5, 1.0))
#light1.setEnabled(True)
light1.setEnabled(False)

# Create a scene object using the loaded model
torus = StaticObject.create("torus")
torus.setEffect("colored")
setNearFarZ(1, 2 * torus.getBoundRadius())

cam = getDefaultCamera()

# Setting the camera by hand. Should find a better way
cam.setPosition(torus.getBoundCenter() + Vector3(7768.82, 2281.18, 2034.08))
cam.getController().setSpeed(300)
cam.pitch(3.14159*0.45) #pitch up to start off flying over the city
