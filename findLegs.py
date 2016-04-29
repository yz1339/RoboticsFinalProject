import cv2
import numpy as np
from matplotlib import pyplot as plt

# For our matrix we are using 5 * 10 intervals
img = cv2.imread('chairLeg1.jpg')
imgcopy = cv2.imread('chairLeg1.jpg')

h = len(img)
w = len(img[0])
voteM = np.zeros((192,128))
def vote(x1, y1):
	# voting function
	i = np.floor(float(x1)/w *128)
	j = np.floor(float(y1)/h * 192)
	print(x1, i, y1, j)
	voteM[i][j] = voteM[i][j] + 1;
	pass


#gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
#edges = cv2.Canny(img,50,150,apertureSize = 3)
#minLineLength = 100
#maxLineGap = 10
#lines = cv2.HoughLinesP(edges,1,np.pi/180,100,minLineLength,maxLineGap)
#for x1,y1,x2,y2 in lines[0]:
#    cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)

#cv2.imwrite('houghlines5.jpg',img)


gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#gray = cv2.GaussianBlur(gray, (3, 3), 0)
edges = cv2.Canny(gray, 10, 250)

#plt.imshow(edges)
#plt.show()


lower_hue = np.array([0,0,0])
upper_hue = np.array([50,50,100])
#upper_hue = np.array([28,28,28])

mask = cv2.inRange(img, lower_hue, upper_hue)

cv2.imwrite('mask.jpg',mask)
cv2.imshow('mask',mask) 
cv2.waitKey(0)

lines = cv2.HoughLinesP(mask, 1, np.pi, 75, None, 13, 1);


for x1,y1,x2,y2 in lines[0]:
    angle = np.arctan2(y2 - y1, x2 - x1) * 180. / np.pi
   	
    if angle != 0:
    		cv2.line(img,(x1,y1),(x2,y2),(0,255,0),1)

    		vote(x1, y1);

    		# cv2.imshow('lol',img)
    		# cv2.waitKey(0)

	
cv2.imshow('vote',voteM)
cv2.waitKey(0)
# get top 10 votes
topTen = np.zeros(10)
topCX = np.zeros(10)
topCY = np.zeros(10)
for i in range(0,10):
	maxVote = 0
	maxX = 0
	maxY = 0
	for x in range(0,len(voteM)):
		for y in xrange(0,len(voteM[0])):
			if (voteM[x][y] > maxVote):
				maxVote = voteM[x][y]
				maxX = x
				maxY = y
	topTen[i] = maxVote
	topCX[i] = maxX
	topCY[i] = maxY
	voteM[maxX][maxY] = 0

print(topTen)
print(topCX)
print(topCY)


# draw points out
for i in range(0,10):
	cv2.circle(img, (int(topCX[i]) * 10, int(topCY[i]) * 5), 5, (225,0,0), -1)
	pass
cv2.imshow('circle',img)
cv2.waitKey(0)






#for line in lines[0]:
#    pt1 = (line[0],line[1])
#    pt2 = (line[2],line[3])
#    Angle = np.arctan(line[3] - line[1], line[2] - line[0]) * 180.0 / np.pi/2;

    
    #if(Angle == 0):
    #cv2.line(img, pt1, pt2, (0,0,255), 3)
cv2.imwrite("temp.jpg", img)







