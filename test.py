import SimpleCV
camera = SimpleCV.Camera(camera_index=1)
print camera.getAllProperties()
while True:
	camera.getImage().show()
