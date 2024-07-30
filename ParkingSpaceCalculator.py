import cv2 
import numpy as np
import cvzone
import pickle

width, height = 107, 48

with open('CarParkPos', 'rb') as f:
    posList = pickle.load(f)


capture = cv2.VideoCapture('carPark.mp4')

def checkParkingSpace(imgPro):
    
    spaceCounter = 0

    for pos in posList:
       x, y = pos

       imgCrop = imgPro[y:y+height, x:x+width]
    #    cv2.imshow(str(x*y), imgCrop)
       count = cv2.countNonZero(imgCrop)
       if count < 950:
           color = (0,255,255)
           thickness = 4
           spaceCounter += 1
       else:
           color = (0,0,255)
           thickness = 2

       cv2.rectangle(frame, pos, (pos[0]+width, pos[1]+height), color, thickness)   
       cvzone.putTextRect(frame, str(count), (x, y+height-3), scale=1, thickness=2, offset=0, colorR=color) 
       cvzone.putTextRect(frame, f'Free: {spaceCounter}/{len(posList)}', (100, 50), scale=3, thickness=5, offset=20, colorR=(255,0,255))
while True:
    if capture.get(cv2.CAP_PROP_POS_FRAMES) == capture.get(cv2.CAP_PROP_FRAME_COUNT):
         capture.set(cv2.CAP_PROP_POS_FRAMES, 0)

    isTrue, frame = capture.read()
    
    imgGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3,3), 1)
    imgThresh = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
    
    
    imgMedian = cv2.medianBlur(imgThresh, 5)
    kernel = np.ones((3,3), np.uint8)
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)
    checkParkingSpace(imgDilate) 
    
    # for pos in posList:
    #    cv2.rectangle(frame, pos, (pos[0]+width, pos[1]+height), (255,0,255), 2) 
    cv2.imshow('Video', frame)
    # cv2.imshow('blur', imgBlur)
    # cv2.imshow('threshold', imgMedian)
    cv2.waitKey(1)
