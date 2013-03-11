import SimpleCV
camera = SimpleCV.Camera(camera_index=0)
print camera.getAllProperties()
while True:
	camera.getImage().show()
