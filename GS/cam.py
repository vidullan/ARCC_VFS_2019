import numpy as np
import cv2
from multiprocessing import Process

"""
gst-launch-1.0 udpsrc port=5000 \
    ! gdpdepay \
    ! rtph264depay \
    ! avdec_h264 \
    ! videoconvert \
    ! autovideosink sync=false

gst-launch-1.0 rpicamsrc bitrate=1000000 \
    ! 'video/x-h264,width=320,height=240' \
    ! h264parse \
    ! queue \
    ! rtph264pay config-interval=1 pt=96 \
    ! gdppay \
    ! udpsink host=192.168.10.23 port=5000

"""


def receive():
    cap_receive = cv2.VideoCapture('udpsrc port=5000 ! gdpdepay ! rtph264depay ! avdec_h264 ! videoconvert ! appsink', cv2.CAP_GSTREAMER)

    if not cap_receive.isOpened():
        print('VideoCapture not opened')
        exit(0)

    i = 0
    while True:
        ret,frame = cap_receive.read()

        if not ret:
            print('empty frame')
            break
        cv2.imwrite("./dropImgs/"+str(i)+".jpg", frame)
        cv2.imshow('receive', frame)
        if cv2.waitKey(1)&0xFF == ord('q'):
            break
        i+=1

    cap_receive.release()

if __name__ == '__main__':
    r = Process(target=receive)
    r.start()
    r.join()

    cv2.destroyAllWindows()
