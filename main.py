import cv2
import numpy as np
from matplotlib import pyplot as plt
from scipy.misc import imresize
import separation
import findLegs
import create
import webcamTakePicture as webcam

robotSpaces = []
chairs = []

def exe():
	#found = False
	robot = create.TetheredDriveApp()
	robot.connect()
	chairLegMap = []
	currentConfigDegrees = 0
	currentConfigTranslationX = 0
	currentConfigTranslationY = 0
	for i in range(1,8):
		img = webcam.takePicture()
		legs = findLegs.findLegs(img)
		for j in range (len(legs)):
			x = [j][0]
			y = legs[j][1]
			temp = separation.convert(x,y)
			currentAngle = temp[1]
			currentAngle = temp[1]+currentConfigDegrees
			chairLegMap.append(temp)
		#Figureout how to rotate 60 degrees
		robot.testDrive()
		currentConfigDegrees += 60
		#We have returned to original rotational config
		if currentConfigDegrees == 360:
			currentConfigDegrees = 0
	for a in range(len(chairLegMap)):
		for b in range(len(chairLegMap)):
			calculatedSep = separation.separation(chairLegMap[a][0], chairLegMap[a][1], chairLegMap[b][0], chairLegMap[b][1])
			#These two will be some sort of threshold values we will calculate later
			if calculatedSep > 0	and calculatedSep < 0:
				#Rotate to the angle of the area between the two chair leg, considering CurrentConfigDegrees
				midAngle = (chairLegMap[a][1] + chairLegMap[b][1])/2
				robot.rotateRight()
				#move forward the distance of the chair legs from robot + an arbitrary amount
				robot.moveForward()


exe()	




