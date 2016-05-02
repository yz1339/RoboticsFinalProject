from cv2 import *

def takePicture():

	# initialize the camera
	cam = VideoCapture(1)   # 0 -> index of camera
	s, img = cam.read()
	if s:    # frame captured without any errors
	    namedWindow("cam-test",CV_WINDOW_AUTOSIZE)
	    imshow("cam-test",img)
	    waitKey(0)
	    destroyWindow("cam-test")
	    # imwrite("test1.jpg",img) #save image
	    return img


