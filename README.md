# Temperature Reader

1. Find latest image and process it (imageprocess.py)
	- Find and load latest image from webcam
	- Use screen module to find the screen
	- Use the found screen object to fix the perspective and crop the image

2. Read the temperature from the processed image
	- Load image
	- Use segment definitions to detect temperature