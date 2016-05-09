import cv2
import numpy as np
from matplotlib import pyplot as plt
from scipy.misc import imresize
import separation

# For our matrix we are using 5 * 10 intervals



def vote(x1, y1, voteM):
	
	# voting function
	i = np.floor(x1/10)
	j = np.floor(y1/5)
	voteM[i-1][j-1] = voteM[i-1][j-1] + 1;
	return voteM
	pass

	
def drawLegs(img, topTen):
	# draw points out
	for i in range(0,len(topTen)):
		x = (int(topTen[i][0]) + 1) * 10
		y = (int(topTen[i][1]) + 1) * 5
		cv2.circle(img, (x, y), 5, (225,0,0), -1)
		# print(separation.convert(x,y), x, y)
		# cv2.imshow('circle',img)
		# cv2.waitKey(0)
	# cv2.destroyAllWindows()

def unionFind(topTen):
	legs = []	
	for i in range(0,len(topTen)):
		x = (int(topTen[i][0]) + 1)
		y = (int(topTen[i][1]) + 1)
		found = False
		for j in range(0,len(legs)):
			for k in range(0,len(legs[j])):
				if y >= legs[j][k][1] - 2 and y <= legs[j][k][1] + 2 and x >= legs[j][k][0] - 2 and x <= legs[j][k][0] + 2:
					legs[j].append((x,y))
					found = True
					break
		if not found:
			legs.append([(x,y)])	
	u_legs = []
	for i in range(0,len(legs)):
		xs = []
		ys = []
		for j in range(0,len(legs[i])):	
			xs.append(legs[i][j][0])
			ys.append(legs[i][j][1])
		u_legs.append((np.mean(xs),np.mean(ys)))
	return u_legs

def findLegs():
	img = cv2.imread('chairLeg1.jpg')
	# img = imresize(img,(480,640))
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	lower_hue = np.array([0,0,0])
	upper_hue = np.array([50,50,100])
	# upper_hue = np.array([30,30,30])

	mask = cv2.inRange(img, lower_hue, upper_hue)
	# cv2.imshow('mask', mask)
	# cv2.waitKey(0)
	lines = cv2.HoughLinesP(mask, 1, np.pi, 75, None, 13, 1);
	voteM = np.zeros((128,196))
	for x1,y1,x2,y2 in lines[0]:
	    angle = np.arctan2(y2 - y1, x2 - x1) * 180. / np.pi
	    if angle != 0:
	    		cv2.line(img,(x1,y1),(x2,y2),(0,255,0),1)
	    		print(x1,y1)




	    		voteM = vote(x1, y1, voteM)
	cv2.imshow('hough', img)
	cv2.waitKey(0)
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
	topTen.sort()
	drawLegs(img,topTen)
	return unionFind(topTen)
	# print(topCX)
	# print(topCY)


legs = findLegs()
print(legs)
for i in range(0,len(legs)):
	print(separation.convert(legs[i][0]*10, legs[i][1]*5))





