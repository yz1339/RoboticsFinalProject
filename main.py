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
	chair_x = chair_dis * np.sin((robot_angle + chair_angle)/180 * np.pi) + robot_x
	chair_y = chair_dis * np.cos((robot_angle + chair_angle)/180 * np.pi) + robot_y
	print('chair x, chair y: ', chair_x, chair_y)
	found = False
	for i in range(0,len(chairLegMap)):
		if chair_x >= chairLegMap[i][0] - ERROR and chair_x <= chairLegMap[i][0] + ERROR and chair_y >= chairLegMap[i][1] - ERROR and chair_y <= chairLegMap[i][1] + ERROR:
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

	print ("d_mid_x: ",d_mid_x," d_mid_y: ", d_mid_y)
	angle = 0
	distanceToGo = np.sqrt(np.square(d_mid_x) + np.square(d_mid_y))
	if d_mid_x > 0:
		angle = np.arccos(d_mid_y / distanceToGo) / np.pi * 180 - robot_angle
	elif d_mid_x < 0:
		angle = np.arccos(d_mid_y / distanceToGo) / np.pi * 180 + robot_angle
		if d_mid_y > 0:
			angle = -angle
		else:
			angle = 360 - angle
	else:
		if d_mid_y > 0:
			angle = -robot_angle
		elif d_mid_y < 0:
			angle = 180 - robot_angle
		else:
			print("WE ARE IN THE MIDDLE OF TWO LEGS!!")

	return distanceToGo, angle

def exe():
	#found = False
	robot = create.TetheredDriveApp()
	robot.connect()
	chairLegMap = []
	currentConfigDegrees = 0
	currentConfigTranslationX = 0
	currentConfigTranslationY = 0
	for i in range(0,9):
		img = webcam.takePicture()
		legs = findLegs.findLegs(img)
		if legs is not "none":
			for j in range (0,len(legs)):
				x = legs[j][0]
				y = legs[j][1]
		
				cv2.circle(img, (int(x), int(y)), 5, (0,225,225), -1)
				cv2.imshow('circle',img)
				cv2.waitKey(0)

				distance, angle = separation.convert(x,y)
				print ('angle, distance: ', angle, distance) 
				if angle > 20 or distance == 0:
					continue
				chairLegMap = updateLegMap(chairLegMap, distance, angle, currentConfigTranslationX, currentConfigTranslationY, currentConfigDegrees)

		#Figureout how to rotate 60 degrees
		robot.testDrive()
		currentConfigDegrees += 40
		# print currentConfigDegrees
		#We have returned to original rotational config
		if currentConfigDegrees == 360:
			currentConfigDegrees = 0
	print "Chair Map:"
	print chairLegMap
	# After the robot find all the chair legs possible at this position, we have a map of the legs, it 
	# will try to go to the middle of the two legs. 
	if len(chairLegMap) < 2:
		print("THERE IS ONLY ONE LEG!!")

	# for i in range(0, len(chairLegMap)-1):
	# 	for j in range(i,len(chairLegMap)):
			# separationBtwLegs = np.sqrt(np.square(chairLegMap[i][0]-chairLegMap[j][0]) + np.square(chairLegMap[i][1]-chairLegMap[j][1]))
			# #These two will be some sort of threshold values we will calculate later
			# if separationBtwLegs > 0 and separationBtwLegs < 0:
			# 	#Rotate to the angle of the area between the two chair leg, considering currentConfigDegrees
			# 	midAngle = (chairLegMap[a][1] + chairLegMap[b][1])/2
			# 	robot.rotateRight()
			# 	#move forward the distance of the chair legs from robot + an arbitrary amount
			# 	robot.moveForward()
	else:
		distanceToGo, angleToTurn = moveBetweenLegsShort(chairLegMap[2], chairLegMap[4], currentConfigTranslationX, currentConfigTranslationY, currentConfigDegrees)
		print('angle: ', angleToTurn)
		if angleToTurn < 0:
			robot.rotate(np.abs(angleToTurn),'left')
			currentConfigDegrees -= angleToTurn
		else:
			robot.rotate(angleToTurn, 'right')
			currentConfigDegrees += angleToTurn
		robot.move(distanceToGo, 'forward')
		currentConfigTranslationX = (chairLegMap[2][0] + chairLegMap[1][0]) / 2
		currentConfigTranslationY = (chairLegMap[2][1] + chairLegMap[1][1]) / 2
		print('PARK AT: ', currentConfigTranslationX, currentConfigTranslationY, currentConfigDegrees)


exe()	




