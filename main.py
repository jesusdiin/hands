import cv2 
import time
import numpy as np
import modules.HandTrackingModule as htm
import math
from subprocess import call

wCam, hCam = 1080, 720

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime =0

detector = htm.handDetector()

minVol = 0
maxVol = 100
vol = 0
volBar = 500
volPer = 0


#call(["amixer", "-D", "pulse", "sset", "Master", "0%"])





while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) != 0:
        print(lmList[4], lmList[9]) #Valores correspondientes a los puntos referencia según medipipe

        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]

        #mitad de la recta
        cx, cy = (x1+x2)//2, (y1+y2)//2

        cv2.circle(img, (x1,y1), 15, (255,0,255), cv2.FILLED)
        cv2.circle(img, (x2,y2), 15, (255,0,255), cv2.FILLED)
        cv2.line(img, (x1,y1), (x2,y2), (0, 128, 0), 3)
        cv2.circle(img, (cx,cy), 15, (255,0,255), cv2.FILLED)

        length = math.hypot(x2-x1, y2-y1)
        print(length)

        # rango de manos 50 - 500
        # Volumen range 0 - 100%
        vol = np.interp(length, [50,400], [minVol, maxVol])
        volBar = np.interp(length, [50,400], [450, 150])
        volPer = np.interp(length, [50,400], [0, 100])
        #print(int(length), vol)
        #call(["amixer", "-D", "pulse", "sset", "Master", str(vol)+'%'])
        print(["amixer", "-D", "pulse", "sset", "Master", str(int(vol))+'%'])
        call(["amixer", "-D", "pulse", "sset", "Master", str(int(vol))+'%'])

        if length<50:
            cv2.circle(img, (cx,cy), 15, (0,0,255), cv2.FILLED)
    
    cv2.rectangle(img, (50,150), (85,500), (0,255,0), 3)
    cv2.rectangle(img, (50, int(volBar)), (85,500), (0,255,0), cv2.FILLED)
    cv2.putText(img, f'{int(volPer)} %', (40, 550), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0),3)


    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (40,70), cv2.FONT_HERSHEY_COMPLEX,
                1, (255,0,255), 3)

    cv2.imshow('TRACKING', img)
    cv2.waitKey(1)
