import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np 
import os
#variables 
width,height=1280,720
folderpath="ARTIFICIAL INTELLENGENCE"
#camera setup 
cap=cv2.VideoCapture(0)
cap.set(3,width)
cap.set(4,height)
 #get the list of presentation images
pathImages=sorted(os.listdir(folderpath),key=len)
print(pathImages)
 #variables
imgNumber=0
hs,ws=int(120*1),int(213*1)
gesTurethreshold=300
buttonpressed=False
buttoncounter=0
buttonDelay=30
hand=0
annotations=[]
 # hand dedector 
detector =HandDetector(detectionCon=0.8,maxHands=1)
while True:
     #import img
    sucess,img=cap.read()
    img=cv2.flip(img,1)
    pathFullImage=os.path.join(folderpath,pathImages[imgNumber])
    imgcurrent=cv2.imread(pathFullImage)
    hands,img=detector.findHands(img)
    cv2.line(img,(0,gesTurethreshold),(width,gesTurethreshold),(0,255,0),10)
    if hands and buttonpressed is False:
      hand=hands[0]
    fingers=detector.fingersUp(hand)
    cx,cy=hand['center']
    lmlist=hand['lmlist']

    #constrain value for  eaiser value
    xval=int(np.interp(lmlist[8][0],[width//2,w],[0,width]))
    yval=int(np.interp(lmlist[8][1],[150,height-150],[0,height]))
    indexfinger=xval,yval

    if cy<=gesTurethreshold:
            if fingers == [1,0,0,0,0]:
             print("Left")
            if imgNumber>0:
                buttonpressed=True
                imgNumber -=1

            if fingers == [0,0,0,0,1]:
                print("Right")
            if imgNumber <len(pathImages)-1:
                buttonpressed=True
                imgNumber +=1

    if fingers == [0,1,1,0,0]:
            cv2.circle(imgcurrent,indexfinger,12,(0,0,255),cv2.FILLED)
     
    if fingers == [0,1,0,0,0]:
            cv2.circle(imgcurrent,indexfinger,12,(0,0,255),cv2.FILLED)
            annotations.append(indexfinger)


            if buttonpressed:
              buttoncounter +=1
              if buttoncounter>buttonDelay:
                buttoncounter=0
                buttonpressed=False
    for i in range(len(annotations)):
        if i !=0:
         cv2.line(imgcurrent,annotations[i-1],annotations[i],(0,0,200),12)

#adding webcam image on the slides
    imgsmall=cv2.resize(img,(ws,hs))
    h,w, _ =imgcurrent.shape
    imgcurrent[0:hs, w-ws:w]=imgsmall

    cv2.imshow("image", img)
    cv2.imshow("slides", imgcurrent)

    key=cv2.waitKey(1)
    if key==ord('q'):
         break
