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
	found = False
	while(!found)
		create.rotateRight()
		img = webcam.takePicture()
		findLegs.findLegs(img)
		


