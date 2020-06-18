# Face Recognition Test Code
import numpy as np
import cv2

cap = cv2.VideoCapture(0)

while(True):
	ret, frame = cap.read() # Capture frame by frame

	cv2.imshow('frame', frame) # Display resulting frame
	if cv2.waitKey(20) & 0xFF == ord('q'):
		break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
