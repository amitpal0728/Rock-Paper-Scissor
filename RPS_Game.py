import random
import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import time
cap= cv2.VideoCapture(0)
cap.set(3,640)#setting image of player
cap.set(4,480)

detector= HandDetector(maxHands=1)

timer=0
stateResult=False
startgame=False
scores = [0,0]# first for ai second for player

while True:
    imgBG = cv2.imread("RPS_Resources/BG.png")
    success,img=cap.read()


    imagescaled = cv2.resize(img,(0,0),None,0.875,0.875)#0,0 are pixel no.,output image is None
    imagescaled=imagescaled[:,80:480]#we are not changing height

    # find hands
    hands, img = detector.findHands(imagescaled)

    if startgame:

        if stateResult is False:
            timer= time.time() - initialTime
            cv2.putText(imgBG, str(int(timer)), (605, 435), cv2.FONT_HERSHEY_PLAIN, 6, (0,0,0), 4)#info to see what are these values
        if timer >3:
            stateResult = True
            timer=0

            if hands:
               playermove = None
               hand=hands[0]
               fingers=detector.fingersUp(hand)
               print(fingers)
               if fingers ==[0,0,0,0,0]:
                   playermove = 1
               if fingers ==[1,1,1,1,1]:
                   playermove = 2
               if fingers ==[0,1,1,0,0] or fingers== [1,1,1,0,0]:
                   playermove = 3

               randomNumber= random.randint(1,3)
               imgAI=cv2.imread(f'RPS_Resources/{randomNumber}.png',cv2.IMREAD_UNCHANGED)

              #player winss
               if (playermove == 1 and randomNumber == 3) or (playermove==2 and randomNumber== 1) or (playermove==3 and randomNumber==2):
                   scores[1]+=1

               # player wins
               if (playermove == 3 and randomNumber == 1) or (playermove == 1 and randomNumber == 2) or (playermove == 2 and randomNumber == 3):
                   scores[0] += 1

               print(playermove)
    imgBG[234:654,795:1195]=imagescaled
    if stateResult:
       imgBG = cvzone.overlayPNG(imgBG, imgAI, (149, 310))

       cv2.putText(imgBG,str(scores[0]), (410,215), cv2.FONT_HERSHEY_PLAIN, 5, (255,255,255), 6)
       cv2.putText(imgBG,str(scores[1]), (1112,215), cv2.FONT_HERSHEY_PLAIN, 5, (255, 255,255),6)

    # cv2.imshow("Image window",img)
    cv2.imshow("BG", imgBG)
    # cv2.imshow("scaled", imagescaled)

    key = cv2.waitKey(1)
    if key==ord('s'):
        startgame=True
        initialTime = time.time()
        stateResult = False
