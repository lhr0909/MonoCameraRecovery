import SimpleCV
camera = SimpleCV.Camera(camera_index=0)
camera.loadCalibration("default")
print camera.getAllProperties()
while True:
	camera.getImageUndistort().show()
