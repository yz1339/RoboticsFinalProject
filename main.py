import cv2
import numpy as np
from matplotlib import pyplot as plt
from scipy.misc import imresize
import separation
import findLegs
import create
import webcamTakePicture as webcam

ERROR = 3

def updateLegMap(chairLegMap, chair_dis, chair_angle, robot_x, robot_y, robot_angle):
	chair_x = chair_dis * np.sin(robot_angle + chair_angle)
	chair_y = chair_dis * np.cos(robot_angle + chair_angle)
	found = False
	for i in range(0,len(chairLegMap)):
		if chair_x in (chairLegMap[i][0] - ERROR, chairLegMap[i][0] + ERROR) and chair_y in (chairLegMap[i][1] - ERROR, chairLegMap[i][1] + ERROR):
			found = True
			break
	if not found:
		chairLegMap.append((chair_x, chair_y))
	return chairLegMap

def moveBetweenLegsShort(leg1, leg2, robot_x, robot_y, robot_angle):
	leg1_x = leg1[0]
	leg1_y = leg1[1]
	leg2_x = leg2[0]
	leg2_y = leg2[1]
	mid_x = (leg1_x + leg2_x) / 2
	mid_y = (leg1_y + leg2_y) / 2
	d_mid_x = mid_x - robot_x
	d_mid_y = mid_y - robot_y

	distanceToGo = np.sqrt(np.square(d_mid_x) + np.square(d_mid_y))
	if mid_x > 0:
		angle = np.arccos(mid_y / distanceToGo) / np.pi * 180 - robot_angle
	elif mid_x < 0:
		angle = np.arccos(mid_y / distanceToGo) / np.pi * 180 + robot_angle
		 
	return distanceToGo, angleToTurn

def exe():
	#found = False
	robot = create.TetheredDriveApp()
	robot.connect()
	chairLegMap = []
	currentConfigDegrees = 0
	currentConfigTranslationX = 0
	currentConfigTranslationY = 0
	for i in range(0,6):
		img = webcam.takePicture()
		legs = findLegs.findLegs(img)
		for j in range (len(legs)):
			x = [j][0]
			y = legs[j][1]
			distance, angle = separation.convert(x,y)

			currentAngle = angle + currentConfigDegrees
			chairLegMap = updateLegMap(chairLegMap, distance, angle, currentConfigTranslationX, currentConfigTranslationY, currentConfigDegrees)

		#Figureout how to rotate 60 degrees
		robot.testDrive()
		currentConfigDegrees += 60
		print currentConfigDegrees
		#We have returned to original rotational config
		if currentConfigDegrees == 360:
			currentConfigDegrees = 0
	# for a in range(len(chairLegMap)):
	# 	for b in range(len(chairLegMap)):
	# 		calculatedSep = separation.separation(chairLegMap[a][0], chairLegMap[a][1], chairLegMap[b][0], chairLegMap[b][1])
	# 		#These two will be some sort of threshold values we will calculate later
	# 		if calculatedSep > 0	and calculatedSep < 0:
	# 			#Rotate to the angle of the area between the two chair leg, considering currentConfigDegrees
	# 			midAngle = (chairLegMap[a][1] + chairLegMap[b][1])/2
	# 			robot.rotateRight()
	# 			#move forward the distance of the chair legs from robot + an arbitrary amount
	# 			robot.moveForward()


exe()	




