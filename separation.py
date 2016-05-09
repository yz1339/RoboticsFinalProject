import cv2
import numpy as np
import math


img = cv2.imread('matrix/distances-gradient.jpg',cv2.IMREAD_COLOR)
img_height = len(img)
img_width = len(img[0])


ZERO_ANGLE_MARK = 657
LEFT_ANGLE_MARK = 130
RIGHT_ANGLE_MARK = 1184
# x = 130 is -20 degree, x = 657 is 0 degree, x = 1184 is 20 degree
# We need to remeasure again to get rid of error and include more pixels

# This method convert the (x, y) pixel pair of the ending of chair leg to distance and angle
# respective to the robot
def convert(x, y):
	print('NOW CONVERTING')

	x1 = int(math.floor(x))
	y1 = int(math.floor(y))


	#distance = img[x1,img_height-y1][0]

	distance = img[y1-1,x1-1][0]

	
	

	#distance = img[x1,y1][0]
	angle = 25
	if x <= RIGHT_ANGLE_MARK and x >= LEFT_ANGLE_MARK:
		angle = np.floor((x - ZERO_ANGLE_MARK) * 20 / np.abs(ZERO_ANGLE_MARK - LEFT_ANGLE_MARK))
	return (distance, angle)


# calculate distance between two chair legs based on image 
def separation(x1, y1, x2, y2):
	(d1, a1) = convert(x1, y1)
	(d2, a2) = convert(x2, y2)
	return calThirdLine(d1,d2,np.abs(a1)+np.abs(a2));
	pass

# given two lengths of and an angle in between, calculate the thrid line in the triangle
def calThirdLine(l1,l2,angle):
	l3 = (angle*l1 + angle*l2)/180
	return l3


# print(separation(190,500, 500,900))
