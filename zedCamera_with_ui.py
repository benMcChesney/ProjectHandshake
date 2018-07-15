import tkinter
import cv2
import PIL.Image, PIL.ImageTk
import time
import os, uuid, sys, json
import argparse
from tkinter import *
import argparse
import pyzed.camera as zcam
import pyzed.types as tp
import pyzed.core as core
import pyzed.defines as sl

camera_settings = sl.PyCAMERA_SETTINGS.PyCAMERA_SETTINGS_BRIGHTNESS
str_camera_settings = "BRIGHTNESS"
step_camera_settings = 1

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

    def print_camera_information(self, cam):
        print("Resolution: {0}, {1}.".format(round(cam.get_resolution().width, 2), cam.get_resolution().height))
        print("Camera FPS: {0}.".format(cam.get_camera_fps()))
        print("Firmware: {0}.".format(cam.get_camera_information().firmware_version))
        print("Serial number: {0}.\n".format(cam.get_camera_information().serial_number))

    def __init__(self, window, window_title, zedCamera):
        self.window = window
        self.window.title(window_title)

        # parse command line args
        self.args = self.parseCommandArgs()
        self.config = self.loadConfig(self.args.config)
        print('args parsed!')

        # end loading
        self.video_source = self.config['camera']['device_id']

        # init zedCamera
        self.zedCamera = zedCamera
        self.runtime = zcam.PyRuntimeParameters()
        self.mat = core.PyMat()
        self.print_camera_information(self.zedCamera)

        # open video source (by default this will try to open the computer webcam)
        self.vid = VideoCapturre(self.video_source)

        # Create a canvas that can fit the above video source size
        self.canvas = tkinter.Canvas(window, width = 680 * 2 + 25 , height = 380 + 50 )
        self.canvas.pack()

        # setup UI
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
        err = self.zedCamera.grab(runtime)
        if err == tp.PyERROR_CODE.PySUCCESS:
            self.zedCamera.retrieve_image(mat, sl.PyVIEW.PyVIEW_DEPTH)
            gray = mat.get_data()
            self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(gray))
            self.canvas.create_image(5, 10, image=self.photo, anchor=tkinter.NW)

            ret, threshold = cv2.threshold(gray, self.minThresholdScale.get(), self.maxThresholdScale.get(),
                                           cv2.THRESH_TOZERO)
            if ret:
                self.threshold = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(threshold))
                self.canvas.create_image( 700 , 10, image=self.threshold, anchor=tkinter.NW)

            #cv2.imshow("ZED", mat.get_data())
            #key = cv2.waitKey(5)

        # ret, frame = self.vid.get_color_frame()
         # cv2.cvtColor(mat.get_data(), cv2.COLOR_BGR2GRAY)



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

# Setup Zed Camera
print("Running...")
init = zcam.PyInitParameters()
init.camera_resolution = sl.PyRESOLUTION.PyRESOLUTION_VGA
init.camera_fps = 30  # Set fps at 30
init.depth_mode = sl.PyDEPTH_MODE.PyDEPTH_MODE_ULTRA
init.coordinate_units = sl.PyUNIT.PyUNIT_CENTIMETER

zedCamera = zcam.PyZEDCamera()
if not zedCamera.is_opened():
    print("Opening ZED Camera...")
status = zedCamera.open(init)
if status != tp.PyERROR_CODE.PySUCCESS:
    print(repr(status))
    print('error opening camera!! abort abort')
    exit()

runtime = zcam.PyRuntimeParameters()
mat = core.PyMat()

# Create a window and pass it to the Application object
App(tkinter.Tk(), "Tkinter and OpenCV", zedCamera)
