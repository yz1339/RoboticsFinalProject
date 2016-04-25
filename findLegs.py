import cv2
import numpy as np
from matplotlib import pyplot as plt




img = cv2.imread('chairLeg1.jpg')
imgcopy = cv2.imread('chairLeg1.jpg')
#gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
#edges = cv2.Canny(img,50,150,apertureSize = 3)
#minLineLength = 100
#maxLineGap = 10
#lines = cv2.HoughLinesP(edges,1,np.pi/180,100,minLineLength,maxLineGap)
#for x1,y1,x2,y2 in lines[0]:
#    cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)

#cv2.imwrite('houghlines5.jpg',img)


gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, 10, 120)
lines = cv2.HoughLinesP(edges, 1, np.pi, 5, None, 13, 1);


for x1,y1,x2,y2 in lines[0]:
    angle = np.arctan2(y2 - y1, x2 - x1) * 180. / np.pi
    print angle
    if angle != 0:
    	cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)
#for line in lines[0]:
#    pt1 = (line[0],line[1])
#    pt2 = (line[2],line[3])
#    Angle = np.arctan(line[3] - line[1], line[2] - line[0]) * 180.0 / np.pi/2;

    
    #if(Angle == 0):
    #cv2.line(img, pt1, pt2, (0,0,255), 3)
cv2.imwrite("temp2.jpg", img)







