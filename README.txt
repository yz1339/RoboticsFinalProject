This program contains the following files:

main.py: contains the exe() to execute the program, the updateLegMap() function, and the function to move the robot to a position in the map.
separation.py: contains a method to convert the pixel position in a image to it's pysical distance and angle to the robot.
findLegs.py: contains all the image processing methods. The findLegs method will return an array of all the chair legs' pixel positions in the image.
webcamTakePicture.py: program that allow the webcam to take a picture. This piece of code is credited to the following source:
	http://stackoverflow.com/questions/11094481/capturing-a-single-image-from-my-webcam-in-java-or-python 
create.py: the program to control the robot. We added the rotate and move function. This code is credited to the following source: 
	http://www.irobotweb.com/~/media/MainSite/PDFs/About/STEM/Create/Python_Tethered_Driving.pdf
The matrix folder contains the depth matrix. You need this image to run the program properly!



To run the program, you need to have openCV and all the other import files installed. Also, you need to connect your laptop to a webcam on port 1, and connect the robot as well. 
After successfully connect to the robot and webcam, you can run the program by the following command line: python main.py

