# Webcam test

import numpy as np
import cv2

cap = cv2.VideoCapture(0)

while(True):
	ret, frame = cap.read()	# Capture frame by frame
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)	# Our operations on the frame come here
	cv2.imshow('frame', frame)
	cv2.imshow('gray', gray)
	if cv2.waitKey(20) & 0xFF == ord('q'):
		break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
