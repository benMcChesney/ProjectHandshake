import tkinter
import cv2
import PIL.Image, PIL.ImageTk
import time
import os, uuid, sys, json
import argparse
from tkinter import *
import argparse

class App:

    def parseCommandArgs(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("-config")
        args = parser.parse_args()
        print(args.config)
        return args

    def loadConfig(self, path):
        local_path = os.getcwd() + '\\' + path
        with open(local_path) as json_file:
            jsonConfig = json.loads(json_file.read())
            print("loaded config from data.json!")
            return jsonConfig

    def saveConfigButtonClickHandler(self):
        self.config['vision']['minThreshold'] = self.minThresholdScale.get()
        self.config['vision']['maxThreshold'] = self.maxThresholdScale.get()
        local_path = os.getcwd() + '\\config.json'
        with open(local_path, 'w') as outfile:
            json.dump(self.config, outfile)
            print("saved config to data.json!")

    def loadConfigButtonClickHandler(self):
        print("load config!")
        self.config = self.loadConfig(self.args.config)
        self.minThresholdScale.set(self.config['vision']['minThreshold'])
        self.maxThresholdScale.set(self.config['vision']['maxThreshold'])

    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)

        # parse command line args
        self.args = self.parseCommandArgs()
        self.config = self.loadConfig(self.args.config)
        print('args parsed!')

        # end loading
        self.video_source = self.config['camera']['device_id']

        # open video source (by default this will try to open the computer webcam)
        self.vid = VideoCapturre(self.video_source)

        # Create a canvas that can fit the above video source size
        self.canvas = tkinter.Canvas(window, width = self.vid.width * 2 + 10 , height = self.vid.height + 50 )
        self.canvas.pack()

        #setup UI
        self.minThreshold = 17
        self.maxThreshold = 255

        self.minThresholdScale = Scale(window, variable=self.minThreshold, from_=0, to=255, label="min threshold", orient=HORIZONTAL)
        self.minThresholdScale.set(self.config['vision']['minThreshold'])
        self.minThresholdScale.pack(padx=15, pady=5, side=LEFT)

        self.maxThresholdScale = Scale(window, variable=self.maxThreshold, from_=0, to=255, label="max threshold", orient=HORIZONTAL)
        self.maxThresholdScale.set(self.config['vision']['maxThreshold'])
        self.maxThresholdScale.pack(padx=15,pady=5,side=LEFT)

        self.saveConfigButton = Button(window, text="Save Config", command=lambda: self.saveConfigButtonClickHandler())
        self.saveConfigButton.pack(padx=15, pady=5, side=LEFT)

        self.loadConfigButton = Button(window, text="Load Config", command=lambda: self.loadConfigButtonClickHandler())
        self.loadConfigButton.pack(padx=15, pady=5, side=LEFT)
        # self.loadConfigButton = Button(window, text="Load Config", command=self.loadConfigButtonClickHandler())
        # self.loadConfigButton.pack(padx=15, pady=5, side=LEFT)

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 5
        self.update()

        self.window.mainloop()

    def snapshot(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_color_frame()

        if ret:
            cv2.imwrite("frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

    def update(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_color_frame()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        ret, threshold = cv2.threshold(gray, self.minThresholdScale.get(), self.maxThresholdScale.get(), cv2.THRESH_BINARY)

        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(5, 0, image = self.photo, anchor = tkinter.NW)
            self.threshold = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(threshold))
            self.canvas.create_image(10 + self.vid.width, 0, image=self.threshold, anchor=tkinter.NW)

        self.window.after(self.delay, self.update)

class VideoCapturre:
    def __init__(self, video_source=0):
        # Open the video source
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

        # Get video source width and height
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def get_color_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                # Return a boolean success flag and the current frame converted to BGR
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return (ret, None)

    # Release the video source when the object is destroyed
    def __del__(self):
         if self.vid.isOpened():
            self.vid.release()

# Create a window and pass it to the Application object
App(tkinter.Tk(), "Tkinter and OpenCV")