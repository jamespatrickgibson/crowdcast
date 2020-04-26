'''
Author: Thomas Gautier
Email: tgautieriv@gmail.com
Date: 4/25/2020
Written for hack:now hackathon
Copyright, all rights reserved.

This is copied and based on
https://www.tensorscience.com/object-recognition/person-detection-in-video-streams-using-python-opencv-and-deep-learning

model pulled from: https://github.com/chuanqi305/MobileNet-SSD
'''

# imports
from imutils.video import VideoStream
from imutils.video import FPS
import argparse
import imutils
import time
import cv2
from datetime import datetime, time
import numpy as np
import time as time2

# set up args
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")
ap.add_argument("-t", "--tracker", type=str, default="csrt", help="OpenCV object tracker type")
args = vars(ap.parse_args())

# extract the OpenCV version info
(major, minor) = cv2.__version__.split(".")[:2]
# if we are using OpenCV 3.2 or an earlier version, we can use a special factory
# function to create the entity that tracks objects
if int(major) == 3 and int(minor) < 3:
    tracker = cv2.Tracker_create(args["tracker"].upper())
    #tracker = cv2.TrackerGOTURN_create()
# otherwise, for OpenCV 3.3 or newer,
# we need to explicity call the respective constructor that contains the tracker object:
else:
    # initialize a dictionary that maps strings to their corresponding
    # OpenCV object tracker implementations
    OPENCV_OBJECT_TRACKERS = {
            "csrt": cv2.TrackerCSRT_create,
            "kcf": cv2.TrackerKCF_create,
            "boosting": cv2.TrackerBoosting_create,
            "mil": cv2.TrackerMIL_create,
            "tld": cv2.TrackerTLD_create,
            "medianflow": cv2.TrackerMedianFlow_create,
            "mosse": cv2.TrackerMOSSE_create
    }
# grab the appropriate object tracker using our dictionary of
# OpenCV object tracker objects
    tracker = OPENCV_OBJECT_TRACKERS[args["tracker"]]()
    #tracker = cv2.TrackerGOTURN_create()
# if the video argument is None, then the code will read from webcam (work in progress)
if args.get("video", None) is None:
    vs = VideoStream(src=0).start()
    time2.sleep(2.0)
# otherwise, we are reading from a video file
else:
    vs = cv2.VideoCapture(args["video"])

# loop over the frames of the video, and store corresponding information from each frame
firstFrame = None
initBB2 = None
fps = None
differ = None
now = ''
framecounter = 0
trackeron = 0

while True:
    frame = vs.read()
    frame = frame if args.get("video", None) is None else frame[1]
    # if the frame can not be grabbed, then we have reached the end of the video
    if frame is None:
            break

    # resize the frame to 500
    frame = imutils.resize(frame, width=500)

    framecounter = framecounter+1
    if framecounter > 1:

        (H, W) = frame.shape[:2]
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        # if the first frame is None, initialize it
        if firstFrame is None:
            firstFrame = gray
            continue

        # compute the absolute difference between the current frame and first frame
        frameDelta = cv2.absdiff(firstFrame, gray)
        thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

        # dilate the thresholded image to fill in holes, then find contours on thresholded image
        thresh = cv2.dilate(thresh, None, iterations=2)
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if imutils.is_cv2() else cnts[1]

        # loop over the contours identified
        contourcount = 0
        for c in cnts:
            contourcount =  contourcount + 1

           # if the contour is too small, ignore it
            if cv2.contourArea(c) < args["min_area"]:
                continue

            # compute the bounding box for the contour, draw it on the frame,
            (x, y, w, h) = cv2.boundingRect(c)
            initBB2 =(x,y,w,h)

            #let's use MobileNet to check to see if those things are people
            prott1 = r'C:\Downloads\MobileNetSSD_deploy.prototxt'
            prott2 = r'C:\Downloads\MobileNetSSD_deploy.caffemodel'
            net = cv2.dnn.readNetFromCaffe(prott1, prott2)

            CLASSES = ["person"]
            COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

            trackbox = frame[y:y + h, x:x + w]
            trackbox = cv2.resize(trackbox, (224, 224))
            cv2.imshow('image', trackbox)
            blob = cv2.dnn.blobFromImage(cv2.resize(trackbox, (300, 300)), 0.007843, (300, 300), 127.5)
            net.setInput(blob)
            detections = net.forward()

            #loop through detections
            for i in np.arange(0, detections.shape[2]):
                confidence = detections[0, 0, i, 2]

                confidence_level = 0.7

                if confidence > confidence_level:
                    # extract the index of the class label from the `detections`, then compute the (x, y)-coordinates of
                    # the bounding box for the object
                    idx = int(detections[0, 0, i, 1])
                    box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                    (startX, startY, endX, endY) = box.astype("int")
                    # draw the prediction on the frame
                    label = "{}: {:.2f}%".format(CLASSES[idx],
                                                 confidence * 100)
                    cv2.rectangle(frame, (startX, startY), (endX, endY),
                                  COLORS[idx], 2)
                    y = startY - 15 if startY - 15 > 15 else startY + 15
                    cv2.putText(frame, label, (startX, y),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)

            # draw some shit
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 2)
            # Start tracker
            now = datetime.now()
            if differ == None or differ > 9:
                tracker.init(frame, initBB2)
                fps = FPS().start()


    # check to see if we are currently tracking an object, if so, ignore other boxes
    # this code is relevant if we want to identify particular persons (section 2 of this tutorial)
    if initBB2 is not None:

        # grab the new bounding box coordinates of the object
        (success, box) = tracker.update(frame)

        # check to see if the tracking was a success
        differ = 10
        if success:
            (x, y, w, h) = [int(v) for v in box]
            cv2.rectangle(frame, (x, y), (x + w, y + h),(0, 255, 0), 2)
            differ = abs(initBB2[0]-box[0]) + abs(initBB2[1]-box[1])
            i = tracker.update(lastframe)
            if i[0] != True:
                time2.sleep(4000)
        else:
            trackeron = 1

        # update the FPS counter
        fps.update()
        fps.stop()

        # initialize the set of information we'll be displaying on
        # the frame
        info = [
            ("Success", "Yes" if success else "No"),
            ("FPS", "{:.2f}".format(fps.fps())),
        ]

        # loop over the info tuples and draw them on our frame
        for (i, (k, v)) in enumerate(info):
            text = "{}: {}".format(k, v)
            cv2.putText(frame, text, (10, H - ((i * 20) + 20)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

        # draw the text and timestamp on the frame
        now2 = datetime.now()
        time_passed_seconds = str((now2-now).seconds)
        cv2.putText(frame, 'Detecting persons',(10, 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    # show the frame and record if the user presses a key
    cv2.imshow("Video stream", frame)
    key = cv2.waitKey(1) & 0xFF

    # if the `q` key is pressed, break from the lop
    if key == ord("q"):
        break
    if key == ord("d"):
        firstFrame = None
    lastframe = frame

# finally, stop the camera/stream and close any open windows
vs.stop() if args.get("video", None) is None else vs.release()
cv2.destroyAllWindows()
# todo-finish copy pasting the example
# TODO- do all the shit now