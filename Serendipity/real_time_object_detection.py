# From: http://www.kaotop.com/it/18432.html
# import the necessary packages
from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import time
import cv2
import find
import imutils

# initialize the video stream, allow the cammera sensor to warmup,
# and initialize the FPS counter
# print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()
time.sleep(2.0)
fps = FPS().start()

# loop over the frames from the video stream
while True:
	# grab the frame from the threaded video stream and resize it
	# to have a maximum width of 400 pixels
	frame = vs.read()
	frame = imutils.resize(frame, width = 600) #width = 2464
	
	list = find.real_time_find(frame)

	# show the output frame
	cv2.imshow("frame", frame)
	key = cv2.waitKey(1) & 0xFF

	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break
	
	# update the FPS counter
	fps.update()