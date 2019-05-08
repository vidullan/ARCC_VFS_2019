import cv2
import glob
import numpy as np

files = glob.glob("./borderImgs/*.jpg")

for f in files:
    img = cv2.imread(f)
    imgP = np.zeros(img.shape)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray,50,150,apertureSize = 3)
    minLineLength = 100
    maxLineGap = 10
    #lines = cv2.HoughLinesP(edges,1,2*np.pi/180,100,minLineLength,maxLineGap)
    #for x1,y1,x2,y2 in lines[0]:
    #    cv2.line(imgs,(x1,y1),(x2,y2),(0,255,0),2)

    imgP[:,:,0] = np.copy(edges)

    imgs = np.concatenate((img, imgP), axis=1)
    cv2.imshow("a",imgs)
    cv2.waitKey(30)
