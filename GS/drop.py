import cv2
import numpy as np
import glob

files = glob.glob("./dropImgs/*.jpg")

dW = 0.54 #m
qH =  1.2 #m
f = 3.04 * 1e-3 #m
wInPx1 = int(dW * f * 240 / (qH * 2.76*1e-3))
wInPx2 = int(dW * f * 320 / (qH * 3.68*1e-3))
print(wInPx1,wInPx2)

dCircum = wInPx1 * 4
dArea = wInPx1 * wInPx1

def angle_cos(p0, p1, p2):
    d1, d2 = (p0-p1).astype('float'), (p2-p1).astype('float')
    return abs( np.dot(d1, d2) / np.sqrt( np.dot(d1, d1)*np.dot(d2, d2) ) )

for f in files:

    squares = []

    img = cv2.imread(f,0)
    img = cv2.GaussianBlur(img, (5, 5), 0)
    
    for thrs in xrange(0, 255, 26):
        if thrs == 0:
            bin = cv2.Canny(img, 0, 50, apertureSize=5)
            bin = cv2.dilate(bin, None)
        else:
            _retval, bin = cv2.threshold(img, thrs, 255, cv2.THRESH_BINARY)
        bin, contours, _hierarchy = cv2.findContours(bin, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            cnt_len = cv2.arcLength(cnt, True)
            cnt = cv2.approxPolyDP(cnt, 0.02*cnt_len, True)
            
            if len(cnt) == 4 and cv2.contourArea(cnt) > dArea * 0.6 and cv2.contourArea(cnt) < dArea * 1.4 and cv2.isContourConvex(cnt):
                #print(cv2.contourArea(cnt), dArea)
                
                cnt = cnt.reshape(-1, 2)
                max_cos = np.max([angle_cos( cnt[i], cnt[(i+1) % 4], cnt[(i+2) % 4] ) for i in xrange(4)])
                if max_cos < 0.1:
                    squares.append(cnt)
                #img2 = np.copy(img)
                #cv2.drawContours( img2, [cnt], -1, (255, 255, 255), 3 )
                #cv2.imshow("d",img2)
                #cv2.waitKey(0)
    cv2.drawContours( img, squares, -1, (0, 255, 0), 3 )
    #cv2.rectangle(img, (0,0),(wInPx1,wInPx1),(255,255,255))
    cv2.imshow('detected dropoff',img)
    cv2.waitKey(30)
