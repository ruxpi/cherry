import cv2
import datetime
import imutils
import sys
import time
import pdb

def image_process(frame):
	frame = imutils.resize(frame, width=500)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (21, 21), 0)
	return frame, gray

def get_bg():
	camera = cv2.VideoCapture(0)
	(grabbed, frame) = camera.read()

	if not grabbed:
		print("no camera")
		camera.release()
		return 0 
	(_, gray) = image_process(frame)

	return gray

def record_video():
	start_time = datetime.datetime.now()

	cap = cv2.VideoCapture(0)

	# Define the codec and create VideoWriter object
	fourcc = cv2.VideoWriter_fourcc(*'MJPG')
	out = cv2.VideoWriter('{}.avi'.format(time.time()),fourcc, 20.0, (640,480))

	while(cap.isOpened() and (datetime.datetime.now() - start_time) < datetime.timedelta(seconds=10)):
	    ret, frame = cap.read()
	    if ret==True:
	        #frame = cv2.flip(frame,0)

	        # write the flipped frame
	        out.write(frame)

	        cv2.imshow('frame',frame)
	        if cv2.waitKey(1) & 0xFF == ord('q'):
	            break
	    else:
	        break

	# Release everything if job is finished
	cap.release()
	out.release()


def detect_movement(bg_image, rec_bool):
	last_detect_time = None

	#open connection to webcam
	camera = cv2.VideoCapture(0)
	if rec_bool == 1:
		print("recording start")
		# pdb.set_trace()
		#frame_size = bg_image.shape[:2]
		#fourcc = cv2.VideoWriter_fourcc('8', 'B', 'P', 'S')
		#pdb.set_trace()
		#out = cv2.VideoWriter('output.avi', -1, 30.0, frame_size, True)

	while True:
		# grab first frame, if frame can't be grabbed, exit
		(grabbed, frame) = camera.read()

		if not grabbed:
			print('unable to grab camera')
			break

		#process frame
		(frame, gray) = image_process(frame) #Potentially problematic tupple issue

		#compute absolute diff between background and current frame
		frameDelta = cv2.absdiff(bg_image, gray)
		thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

		# dilate the thresholded image to fill in holes, then find contours
		thresh = cv2.dilate(thresh, None, iterations=2)
		(_, cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
			cv2.CHAIN_APPROX_SIMPLE)

		# loop over the contours
		movement = 0
		for c in cnts:
			# if the contour is too small, ignore it
			if cv2.contourArea(c) > 500:
				movement = 1

		if rec_bool == 1:

			if movement == 0 and (datetime.datetime.now() - last_detect_time > datetime.timedelta(seconds = 1)):
				#out.release()
				camera.release()
				return 0

			if movement == 1:
				last_detect_time = datetime.datetime.now()

			print("recording video")
			#pdb.set_trace()
			camera.release()
			record_video()
			camera = cv2.VideoCapture(0)
			#print(frame)

		else:
			if movement == 1:
				camera.release()
				detect_movement(bg_image, 1)
				camera = cv2.VideoCapture(0)
			else:
				print("no movement detected")


bg_image = get_bg()
detect_movement(bg_image, 0)







