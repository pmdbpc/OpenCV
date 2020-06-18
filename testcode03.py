# -*- coding: utf-8 -*-
# Created on Sun May 17 11:25:33 2020 - @author: pmdbpc
# Face & Eye Recognition Test Code
import numpy as np
import cv2
from scipy.spatial import distance
from operator import itemgetter

faceFrontCascade = cv2.CascadeClassifier(r'C:\Users\pmdbpc\Desktop\TestCode\cascades\data\haarcascade_frontalface_alt2.xml')
faceProfileCascade = cv2.CascadeClassifier(r'C:\Users\pmdbpc\Desktop\TestCode\cascades\data\haarcascade_profileface.xml')
eyeCascade = cv2.CascadeClassifier(r'C:\Users\pmdbpc\Desktop\TestCode\cascades\data\haarcascade_lefteye_2splits.xml')

cap = cv2.VideoCapture(0)

(prevX,prevY,prevW,prevH) = (0,0,0,0)

count = True

def euclideanDist(num1, num2, num3, num4):
    val1=(num1, num2)
    val2=(num3, num4)
    dist = distance.euclidean(val1, val2)
    print("Euclidean Distance: ", dist)
    return int(dist)

# Can only call this function if video capture is currently inactive
def captureSingleFrame():
    iterationVal = 0
    while(cap.isOpened()):
        ret, frame = cap.read()
        if iterationVal > 0:
            break
        cv2.imwrite('image04.jpg', frame)
        iterationVal+=1

iterVal = 0
#captureSingleFrame()
while(True):
    #if iterVal > 0:
    #    break
    ret, frame = cap.read() # Capture frame by frame
    #frame = cv2.imread(r'C:\Users\pmdbpc\Desktop\TestCode\image01.jpg', 0)
    #frame = cv2.imread(r'C:\Users\pmdbpc\Desktop\TestCode\image02.jpg', 0)
    #frame = cv2.imread(r'C:\Users\pmdbpc\Desktop\TestCode\image03.jpg', 0)
    #frame = cv2.imread(r'C:\Users\pmdbpc\Desktop\TestCode\image04.jpg', 0)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frontFace = faceFrontCascade.detectMultiScale(frame, scaleFactor=1.5, minNeighbors=5)
    eyes = eyeCascade.detectMultiScale(frame, scaleFactor=1.5, minNeighbors=5)
    #iterVal += 1
    sortedEyes = sorted(eyes, key=itemgetter(0))
    if frontFace is ():
        print('None')
        for iteration in range(len(sortedEyes)-1):
            if (sortedEyes[iteration+1][0] - sortedEyes[iteration][0]) < 100:
                eyeX, eyeY, eyeH, eyeW = sortedEyes[iteration]
                cv2.rectangle(frame, ((eyeX-30), (eyeY-30)), ((eyeX+120), (eyeY+120)), (0,255,0), 2)
    elif frontFace is not None:
        for (x,y,w,h) in frontFace:
            cv2.rectangle(frame, (x,y), (x+w,y+h), (0,0,255), 2)
    cv2.imshow('frame', frame) # Display resulting frame
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break
    
#while(True):    
#    if cv2.waitKey(20) & 0xFF == ord('q'):
#        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()


# Reference Links:
# https://www.youtube.com/watch?time_continue=20&v=ydSXgBZ1ybk&feature=emb_logo
# https://www.youtube.com/watch?v=PmZ29Vta7Vc






