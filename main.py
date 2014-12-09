import cv2
import numpy as np

def filter(hsv):
    blue = cv2.inRange(hsv,np.array((100,100,100)),np.array((140,255,255)))
    return blue

c = cv2.VideoCapture(0)
center = [0,0]
_,f = c.read()
dim = f.shape
drawing = np.zeros((dim[0],dim[1],3), np.uint8)
while(1):
    _,f = c.read()
    f = cv2.flip(f,1)
    blur = cv2.medianBlur(f,5)
    hsv = cv2.cvtColor(f,cv2.COLOR_BGR2HSV)
    both = filter(hsv)
    erode = cv2.erode(both,None,iterations = 3)
    dilate = cv2.dilate(erode,None,iterations = 10)

    contours,hierarchy = cv2.findContours(dilate,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    i=0

    for cnt in contours:
    	if(i==1):
    		break
    	i = i+1
        x,y,w,h = cv2.boundingRect(cnt)
        cx,cy = x+w/2, y+h/2
        if 100 < hsv.item(cy,cx,0) < 140:
            color = [0,255,0]
            cv2.line(f, (x,y), (x+w/4,y), color,2) 
            cv2.line(f, (x,y), (x,y+h/4), color,2) 
            
            cv2.line(f, (x+w,y), ((x+w)-w/4,y), color,2) 
            cv2.line(f, (x+w,y), ((x+w),y+h/4), color,2) 
            
            cv2.line(f, (x,y+h), (x,y+h-h/4), color,2) 
            cv2.line(f, (x,y+h), (x+w/4,y+h), color,2) 
            
            cv2.line(f, (x+w,y+h), (x+w-w/4,y+h), color,2) 
            cv2.line(f, (x+w,y+h), (x+w,y+h-h/4), color,2) 
        center[0] = x+w/2
        center[1] = y+h/2
    print "center"+str(center)
    f[center[0]][center[1]] = [0,0,0]
    drawing[center[0]][center[1]] = [255,255,255]
    # f = f + drawing
    cv2.imshow('img',f)
    cv2.imshow('draw',drawing)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
c.release()