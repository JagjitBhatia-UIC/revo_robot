import cv2
import numpy as np
import sys
import string, random

cap = cv2.VideoCapture(sys.argv[1])
counter = 0

cv2.namedWindow('Frame')
save_dir = None
capturing = False

def getID(size=6, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def writeData(x, y):
    if save_dir is None:
        print "Please specify write mode."
        return
    crop = frame[y - 112 : y + 112, x - 112 : x + 112]
    if random.random() < 0.2:
        path = 'data/classification/validation/' + save_dir + sys.argv[1] + getID() + '.png'
    else:
        path = 'data/classification/training/' + save_dir + sys.argv[1] + getID() + '.png'
    #cv2.imwrite(path, crop)
    cv2.imwrite('data/to_mask/' + save_dir + getID() + '.png', crop)
    print "Written to " + path

def mouseCallback(event, x, y, flags, param):
    global capturing
    global save_dir

    if event == cv2.EVENT_LBUTTONDOWN:
        if x - 112 < 0 or y - 112 < 0 or x + 112 > width or y + 112 > height:
            print "Out of bounds."
            return
        else:
            writeData(x,y)
    elif event == cv2.EVENT_MOUSEMOVE:
        img = frame.copy()
        if save_dir == 'lanes/':
            cv2.rectangle(img, (x - 112, y - 112), (x + 112, y + 112), (255,0,0), 5)
        elif save_dir == 'objects/':
            cv2.rectangle(img, (x - 112, y - 112), (x + 112, y + 112), (0,0,255), 5)
        elif save_dir == 'terrain/':
            cv2.rectangle(img, (x - 112, y - 112), (x + 112, y + 112), (0,255,0), 5)
        else:
            cv2.rectangle(img, (x - 112, y - 112), (x + 112, y + 112), (255,255,255), 5)
        cv2.imshow('Frame', img)
        capturing = False
    '''
    elif event == cv2.EVENT_LBUTTONUP and capturing:
        writeData(x,y)
        capturing = False
        cv2.imshow('Frame', frame)
    '''

def getData():
    global save_dir
    while True:
        press = 0xFF & cv2.waitKey(0)
        if press== ord('l'):
            print "Click on LANE LINES!"
            save_dir = 'lanes/'
        elif press == ord('o'):
            print "Click on OBJECTS!"
            save_dir = 'objects/'
        elif press == ord('t'):
            print "Click on TERRAIN!"
            save_dir = 'terrain/'
        elif press == 32: #Space bar
            return
        elif press == 27: #Esc
            sys.exit()


cv2.setMouseCallback('Frame', mouseCallback)
while cap.get(1) != cap.get(7): # while frame != last frame
    global height, width
    ret, frame = cap.read()
    height, width = frame.shape[:2]
    cv2.imshow('Frame', frame)
    if counter % 25 == 0:
        getData()
    counter += 1

    if 0xFF & cv2.waitKey(5) == 27: #Esc
        break
