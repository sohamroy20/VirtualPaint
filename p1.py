import cv2
import numpy as np
framewidth = 640
frameheight = 480
cap = cv2.VideoCapture(0)
cap.set(3, framewidth)
cap.set(4, frameheight)
cap.set(10,130)
mycolors = [[5,107,0,19,255,255],[109,113,186,120,255,255],[0,113,83,9,235,255],[111,77,128,179,255,192]]
#orange,blue,red,violet
mycolvalues = [[51,153,255],[255,45,45],[51,51,255],[204,0,204]]  #BGR
mypoints=[]#x,y,colorid

def findcolor(img,mycolors,mycolvalues):
    count = 0
    newpoints=[]
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    for color in mycolors:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imgHSV, lower, upper)
        x,y=getcontours(mask)
        cv2.circle(imgresult,(x,y),10,mycolvalues[count],cv2.FILLED)
        if x!=0 and y!= 0:
            newpoints.append([x,y,count])
        count+=1
        #cv2.imshow(str(color[0]), mask)
    return newpoints

def getcontours(img):
    contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    x,y,w,h=0,0,0,0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area>400:
            cv2.drawContours(imgresult, cnt, -1, (255, 0, 0), 2)
            peri = cv2.arcLength(cnt,True)

            approx = cv2.approxPolyDP(cnt,0.03*peri,True)
            x, y, w, h = cv2.boundingRect(approx)
    return (x+w//2,y)


def draw(mypoints,mycolvalues):
    for point in mypoints:
        cv2.circle(imgresult,(point[0],point[1]),10,mycolvalues[point[2]],cv2.FILLED)



while True:
    success, img = cap.read()
    imgresult = img.copy()
    newpoints= findcolor(img,mycolors,mycolvalues)
    if len(newpoints)!=0:
        for newp in newpoints:
            mypoints.append(newp)
    if len(mypoints)!=0:
        draw(mypoints,mycolvalues)

    cv2.imshow("Result", imgresult)
    if cv2.waitKey(1) & 0xFF == ord('x'):
        break



