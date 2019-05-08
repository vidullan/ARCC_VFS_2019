import cv2
import numpy as np
import glob

files = glob.glob("./targetImgs/*.jpg")

cR = 0.203 #m
qH =  1.5 #m
f = 3.04 * 1e-3 #m
rInPx1 = cR * f * 240 / (qH * 2.76*1e-3)
rInPx2 = cR * f * 320 / (qH * 3.68*1e-3)
print(rInPx1,rInPx2)

for f in files:
    img = cv2.imread(f,0)
    
    circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1, 2*rInPx1,
                                 param1=20,param2=50,minRadius=int(rInPx1 * 0.8),maxRadius=int(rInPx1 * 1.2))
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0,:]:
            # draw the outer circle
            cv2.circle(img,(i[0],i[1]),i[2],(0,255,0),2)
            # draw the center of the circle
            cv2.circle(img,(i[0],i[1]),2,(0,0,255),3)
        
    cv2.imshow('detected circles',img)
    cv2.waitKey(30)
