import cv2
import numpy as np
from matplotlib import pyplot as plt
from scipy.misc import imresize
import separation

# For our matrix we are using 5 * 10 intervals


h = 960
w = 1280
voteM = np.zeros((192,128))
def vote(x1, y1):
	# voting function
	i = np.floor(float(x1)/w *128)
	j = np.floor(float(y1)/h * 192)
	print(x1, i, y1, j)
	voteM[i][j] = voteM[i][j] + 1;
	pass

	
def drawLegs(img, topTen):
	# draw points out
	for i in range(0,len(topTen)):
		x = int(topTen[i][0]) * 10
		y = int(topTen[i][1]) * 5
		cv2.circle(img, (x, y), 5, (225,0,0), -1)
		# print(separation.convert(x,y), x, y)
		cv2.imshow('circle',img)
		cv2.waitKey(0)
	cv2.destroyAllWindows()

def unionFind(topTen):
	chairs = []
	for i in range(0,len(topTen)):
		
		y = int(topTen[i][1])
	pass

def findLegs():
	img = cv2.imread('chairLeg1.jpg')
	# img = imresize(img,(480,640))
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	lower_hue = np.array([0,0,0])
	upper_hue = np.array([50,50,100])
	mask = cv2.inRange(img, lower_hue, upper_hue)
	lines = cv2.HoughLinesP(mask, 1, np.pi, 75, None, 13, 1);

	for x1,y1,x2,y2 in lines[0]:
	    angle = np.arctan2(y2 - y1, x2 - x1) * 180. / np.pi
	    if angle != 0:
	    		cv2.line(img,(x1,y1),(x2,y2),(0,255,0),1)
	    		vote(x1, y1);

	# get top 10 votes
	topTen = []
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
		# topTen[i] = maxVote
		# topCX[i] = maxX
		# topCY[i] = maxY
		topTen.append((maxX,maxY))
		voteM[maxX][maxY] = 0

	print(topTen)
	drawLegs(img,topTen)
	# print(topCX)
	# print(topCY)

findLegs()










