import threading
from pyimagesearch.centroidtracker import CentroidTracker
from pyimagesearch.trackableobject import TrackableObject
from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import imutils
import dlib
import cv2
import logging
import queue
import time


class QueueTrackerDaemon(threading.Thread):

    def __init__(self, proto_file='mobilenet_ssd/MobileNetSSD_deploy.prototxt',
                 model_file='mobilenet_ssd/MobileNetSSD_deploy.caffemodel',
                 input_file='videos/queue_1080.mp4', log_level='DEBUG',
                 output_file = None):
        threading.Thread.__init__(self, target=None, name='peopleCountThread', daemon=True)
        self.protoFile = proto_file
        self.modelFile = model_file
        self.inputFile = input_file
        self.outputFile = output_file
        # initialize logger

        # assuming loglevel is bound to the string value obtained from the
        # input argument. Convert to upper case to allow the user to
        # specify --log=DEBUG or --log=debug
        numeric_level = getattr(logging, log_level.upper(), None)
        if not isinstance(numeric_level, int):
            raise ValueError('Invalid log level: %s' % log_level)
        logging.basicConfig(filename='queueTrackerDaemon.log', level=numeric_level)

        # initialize the video writer (we'll instantiate later if need be)
        self.writer = None

        # initialize the list of class labels MobileNet SSD was trained to
        # detect
        self.CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
                   "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
                   "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
                   "sofa", "train", "tvmonitor"]

        # load our serialized model from disk
        logging.info("loading model...")
        self.net = cv2.dnn.readNetFromCaffe(proto_file, model_file)

        logging.info("opening video file...")
        self.vs = cv2.VideoCapture(input_file)

        # initialize the frame dimensions (we'll set them as soon as we read
        # the first frame from the video)
        self.W = None
        self.H = None

        # instantiate our centroid tracker, then initialize a list to store
        # each of our dlib correlation trackers, followed by a dictionary to
        # map each unique object ID to a TrackableObject
        self.ct = CentroidTracker(maxDisappeared=40, maxDistance=50)
        self.trackers = []
        self.trackableObjects = {}

        # initialize the total number of frames processed thus far
        self.totalFrames = 0

        # initialize the start frame queue. We'll make a few assumptions here:
        #   1) no line cutting -- the actual queue is FIFO, so we don't have to track objects
        #   2) no one leaves the queue without getting inside because your bar is awesome and worth the wait
        self.startFramesQueue = queue.Queue()

        # initialize current wait time in seconds.
        self.currentWaitTime = 0

        # people that have left
        self.exitedIDs = []


        # start the frames per second throughput estimator
        #self.fps = FPS().start() #not using fps for now, can enable later

    def get_current_wait_seconds(self):
        return self.currentWaitTime

    def get_current_wait_minutes(self):
        return self.currentWaitTime / 60

    def get_queue_length(self):
        return self.startFramesQueue.qsize()

    def run(self, confidence_thresh=0.4, skip_frames=30):
        firstframe = self.vs.read()
        if not firstframe[0]:
            logging.error(f"Did not get a single frame from input file {self.inputFile}")
            raise ValueError('Input file did not produce a single frame.')
        while True:
            # grab the next frame and handle if we are reading from
            # VideoStream
            frame = self.vs.read()
            frame = frame[1]

            # if we are viewing a video and we did not grab a frame then we
            # have reached the end of the video, restart
            if frame is None:
                self.vs = cv2.VideoCapture(self.inputFile)
                # also save out the video and delete the writer
                if self.writer is not None:
                    self.writer.release()
                    self.writer = None
                continue
            # resize the frame to have a maximum width of 500 pixels (the
            # less data we have, the faster we can process it), then convert
            # the frame from BGR to RGB for dlib
            frame = imutils.resize(frame, width=500)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # if the frame dimensions are empty, set them and init our queue magic numbers (obviously make this better)
            if self.W is None or self.H is None:
                (self.H, self.W) = frame.shape[:2]
                queueXmin = 0
                queueXmax = 5 * self.W // 8
                queueYmin = self.H // 4
                queueYmax = 3 * self.H // 4
                exitXmin = 0
                exitXmax = self.W // 5
                exitYmin = self.H // 4
                exitYmax = 3 * self.H // 4

            # if we're outputting video (for the demo) check that the writer is initialized.
            if self.outputFile is not None and self.writer is None:
                fourcc = cv2.VideoWriter_fourcc(*"MJPG")
                self.writer = cv2.VideoWriter(self.outputFile, fourcc, 30,
                                         (self.W, self.H), True)

            # initialize the current status along with our list of bounding
            # box rectangles returned by either (1) our object detector or
            # (2) the correlation trackers
            status = "Waiting"
            rects = []

            # check to see if we should run a more computationally expensive
            # object detection method to aid our tracker
            if self.totalFrames % skip_frames == 0:
                # set the status and initialize our new set of object trackers
                status = "Detecting"
                trackers = []

                # convert the frame to a blob and pass the blob through the
                # network and obtain the detections
                blob = cv2.dnn.blobFromImage(frame, 0.007843, (self.W, self.H), 127.5)
                self.net.setInput(blob)
                detections = self.net.forward()

                # loop over the detections
                for i in np.arange(0, detections.shape[2]):
                    # extract the confidence (i.e., probability) associated
                    # with the prediction
                    confidence = detections[0, 0, i, 2]

                    # filter out weak detections by requiring a minimum
                    # confidence
                    if confidence > confidence_thresh:
                        # extract the index of the class label from the
                        # detections list
                        idx = int(detections[0, 0, i, 1])

                        # if the class label is not a person, ignore it
                        if self.CLASSES[idx] != "person":
                            continue

                        # compute the (x, y)-coordinates of the bounding box
                        # for the object
                        box = detections[0, 0, i, 3:7] * np.array([self.W, self.H, self.W, self.H])
                        (startX, startY, endX, endY) = box.astype("int")

                        # construct a dlib rectangle object from the bounding
                        # box coordinates and then start the dlib correlation
                        # tracker
                        tracker = dlib.correlation_tracker()
                        rect = dlib.rectangle(startX, startY, endX, endY)
                        tracker.start_track(rgb, rect)

                        # add the tracker to our list of trackers so we can
                        # utilize it during skip frames
                        trackers.append(tracker)

            # otherwise, we should utilize our object *trackers* rather than
            # object *detectors* to obtain a higher frame processing throughput
            else:
                # loop over the trackers
                for tracker in trackers:
                    # set the status of our system to be 'tracking' rather
                    # than 'waiting' or 'detecting'
                    status = "Tracking"

                    # update the tracker and grab the updated position
                    tracker.update(rgb)
                    pos = tracker.get_position()

                    # unpack the position object
                    startX = int(pos.left())
                    startY = int(pos.top())
                    endX = int(pos.right())
                    endY = int(pos.bottom())

                    # add the bounding box coordinates to the rectangles list
                    rects.append((startX, startY, endX, endY))

            # draw box where the queue exists -- once an object enters this
            # area they are "in" the queue, and once they either exit or disappear we will
            # pop the queue and calculate the wait time.
            cv2.rectangle(frame, (queueXmin, queueYmin), (queueXmax, queueYmax), (0, 0, 255), 2)

            # now draw the exit box
            cv2.rectangle(frame, (exitXmin, exitYmin), (exitXmax, exitYmax), (0, 255, 0), 2)

            # use the centroid tracker to associate the (1) old object
            # centroids with (2) the newly computed object centroids
            objects = self.ct.update(rects)


            # loop over the tracked objects
            for (objectID, centroid) in objects.items():
                # check to see if a trackable object exists for the current
                # object ID
                to = self.trackableObjects.get(objectID, None)



                # if there is no existing trackable object, create one
                if to is None:
                    # check to see if the person magically appeared in the queue. If so, it's not real. Skip.
                    if queueXmin < centroid[0] < queueXmax and queueYmin < centroid[1] < queueYmax:
                        continue
                    to = TrackableObject(objectID, centroid)

                # otherwise, there is a trackable object so we can utilize it
                # to determine direction
                else:

                    # check to see if the object has been counted or not
                    if not to.counted:
                        # if the direction is negative (indicating the object
                        # is moving up) AND the centroid is above the center
                        # line, count the object
                        if queueXmin < centroid[0] < queueXmax and queueYmin < centroid[1] < queueYmax:
                            self.startFramesQueue.put(self.totalFrames)
                            to.counted = True

                # if the object is in the exit, execute the exit procedure
                if exitXmin < centroid[0] < exitXmax and exitYmin < centroid[1] < exitYmax and \
                        objectID not in self.exitedIDs:
                    start_frame = self.startFramesQueue.get()
                    self.currentWaitTime = round((self.totalFrames - start_frame) / 30.0) #assume 30 fps like a stream
                    self.exitedIDs.append(objectID)

                # store the trackable object in our dictionary
                self.trackableObjects[objectID] = to

                objColor = (0, 255, 0) if queueXmin < centroid[0] < queueXmax and \
                                          queueYmin < centroid[1] < queueYmax else (255, 0, 0)
                # draw both the ID of the object and the centroid of the
                # object on the output frame
                text = "ID {}".format(objectID)
                cv2.putText(frame, text, (centroid[0] - 10, centroid[1] - 10),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, objColor, 2)
                cv2.circle(frame, (centroid[0], centroid[1]), 4, objColor, -1)

            # construct a tuple of information we will be displaying on the
            # frame
            info = [
                ("Queue Length", self.startFramesQueue.qsize()),
                ("Last Wait Time (sec)", self.currentWaitTime),
                ("Status", status),
            ]

            # loop over the info tuples and draw them on our frame
            for (i, (k, v)) in enumerate(info):
                text = "{}: {}".format(k, v)
                cv2.putText(frame, text, (10, self.H - ((i * 20) + 20)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

            # check to see if we should write the frame to disk
            if self.writer is not None:
                self.writer.write(frame)
            # show the output frame
            cv2.imshow("Frame", frame)
            key = cv2.waitKey(1) & 0xFF

            # if the `q` key was pressed, break from the loop
            if key == ord("q"):
                break

            # try and simulate a real 30fps stream since we're using an input file and getting like 110+ fps
            #time.sleep(1.0/40)

            # increment the total number of frames processed thus far and
            # then update the FPS counter
            self.totalFrames += 1
            #fps.update()
