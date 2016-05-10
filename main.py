import cv2
import numpy as np
from matplotlib import pyplot as plt
from scipy.misc import imresize
import separation
import findLegs
import create
import webcamTakePicture as webcam

ERROR = 3
#ChairLeg: 47-56 cm

def separationBtwLegs(leg1, leg2):
	leg1_x = leg1[0]
	leg1_y = leg1[1]
	leg2_x = leg2[0]
	leg2_y = leg2[1]
	return np.sqrt(np.square(leg1_x-leg2_x) + np.square(leg1_y-leg2_y))
def updateLegMap(chairLegMap, chair_dis, chair_angle, robot_x, robot_y, robot_angle):
	chair_x = chair_dis * np.sin((robot_angle + chair_angle)/180 * np.pi) + robot_x
	chair_y = chair_dis * np.cos((robot_angle + chair_angle)/180 * np.pi) + robot_y
	found = False
	for i in range(0,len(chairLegMap)):
		if chair_x >= chairLegMap[i][0] - ERROR and chair_x <= chairLegMap[i][0] + ERROR and chair_y >= chairLegMap[i][1] - ERROR and chair_y <= chairLegMap[i][1] + ERROR:
			found = True
			break
	if not found:
		chairLegMap.append((chair_x, chair_y))
		plt.plot(chair_x,chair_y,'ro')
	return chairLegMap
def moveTo(aim_x, aim_y, robot_x, robot_y, robot_angle):
	d_aim_x = aim_x - robot_x
	d_aim_y = aim_y - robot_y
	angle = 0
	distanceToGo = np.sqrt(np.square(d_aim_x) + np.square(d_aim_y))
	if aim_x > 0:
		angle = np.arccos(d_aim_y / distanceToGo) / np.pi * 180 - robot_angle
	else:
		angle = -np.arccos(d_aim_y / distanceToGo) / np.pi * 180 - robot_angle
	if angle > 180:
		angle -= 360
	elif angle < -180:
		angle += 360	
	return distanceToGo, angle
	pass
def moveBetweenLegsShort(leg1, leg2, robot_x, robot_y, robot_angle):
	leg1_x = leg1[0]
	leg1_y = leg1[1]
	leg2_x = leg2[0]
	leg2_y = leg2[1]
	mid_x = (leg1_x + leg2_x) / 2
	mid_y = (leg1_y + leg2_y) / 2
	return moveTo(mid_x, mid_y, robot_x, robot_y, robot_angle)

def scatterPlot(array):
	xs = []
	ys = []
	for i in range(0,len(array)):
		xs.append(array[i][0])
		ys.append(array[i][1])
	plt.plot(0,0,'go')
	plt.plot(xs,ys,'ro')
	plt.axis([-200,200,-200,200])
	plt.show()
	pass

def imageProcessing(chairLegMap):
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
			# print ('angle, distance: ', angle, distance) 
			if angle > 20 or distance == 0:
				continue
			chairLegMap = updateLegMap(chairLegMap, distance, angle, currentConfigTranslationX, currentConfigTranslationY, currentConfigDegrees)
	return chairLegMap
def exe():
	robot = create.TetheredDriveApp()
	robot.connect()
	chairLegMap = []
	robotConfigs = []
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

		robot.testDrive()
		currentConfigDegrees += 40
		#We have returned to original rotational config
		if currentConfigDegrees == 360:
			currentConfigDegrees = 0

	# After the robot find all the chair legs possible at this position, we have a map of the legs, it 
	# will try to go to the middle of the two legs. 
	if len(chairLegMap) < 2:
		print("THERE IS ONLY ONE LEG!!")
	else:
		for i in range(0, len(chairLegMap)-1):
			for j in range(i,len(chairLegMap)):
				separationBtwLegs = separationBtwLegs(chairLegMap[i], chairLegMap[j])
				if separationBtwLegs < 56 and separationBtwLegs > 46:
					distanceToGo, angleToTurn = moveBetweenLegsShort(chairLegMap[i], chairLegMap[j], currentConfigTranslationX, currentConfigTranslationY, currentConfigDegrees)
					if angleToTurn < 0:
						robot.rotate(np.abs(angleToTurn),'left')
					else:
						robot.rotate(angleToTurn, 'right')
					safe = True
					while safe and distanceToGo > 0:
						# take a picture before it move forward 
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
								# print ('angle, distance: ', angle, distance) 
								if angle > 20 or distance == 0:
									continue
								if distance < 55:
									robot.rotate(40, 'right')
									currentConfigDegrees += 40
									safe = False
									break
								else:
									if distanceToGo >= 30:
										d = 30
									else:
										d = distanceToGo
									robot.move(d, 'forward')
									distanceToGo -= d
									currentConfigTranslationX = d * np.sin((currentConfigDegrees + angleToTurn)/180 * np.pi) + currentConfigTranslationX
									currentConfigTranslationY = d * np.cos((currentConfigDegrees + angleToTurn)/180 * np.pi) + currentConfigTranslationY
					


		# distanceToGo, angleToTurn = moveBetweenLegsShort(chairLegMap[2], chairLegMap[4], currentConfigTranslationX, currentConfigTranslationY, currentConfigDegrees)
		
		# currentConfigDegrees += angleToTurn
		# robot.move(distanceToGo, 'forward')
		# currentConfigTranslationX = (chairLegMap[2][0] + chairLegMap[4][0]) / 2
		# currentConfigTranslationY = (chairLegMap[2][1] + chairLegMap[4][1]) / 2
		# print('PARK AT: ', currentConfigTranslationX, currentConfigTranslationY, currentConfigDegrees)
		# scatterPlot(chairLegMap);
		plt.plot(0,0,'go')
		# plt.plot(currentConfigTranslationX, currentConfigTranslationY,'bo')
		plt.axis([-200,200,-200,200])
		plt.show()


exe()	




