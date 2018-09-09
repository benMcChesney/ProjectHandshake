import os, uuid, sys, json
import argparse
import tkinter
from tkinter import *

import face_recognition
import cv2

class App:

    def parseCommandArgs(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("-directory")
        args = parser.parse_args()
        return args

    def loadConfig(self, path):
        local_path = os.getcwd() + '\\' + str(path)
        with open(local_path) as json_file:
            jsonConfig = json.loads(json_file.read())
            print("loaded config from data.json!")
            return jsonConfig

    def saveConfigButtonClickHandler(self):
        # set values in config
        # self.config['vision']['maxThreshold'] = self.maxThresholdScale.get()

        local_path = os.getcwd() + '\\config.json'
        with open(local_path, 'w') as outfile:
            json.dump(self.config, outfile)
            print("saved config to data.json!")

    def loadConfigButtonClickHandler(self):
        print("load config!")
        self.config = self.loadConfig(self.args.config)

        # load values in config
        # self.minThresholdScale.set(self.config['vision']['minThreshold'])

    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)

        # parse command line args
        self.args = self.parseCommandArgs()
        # self.config = self.loadConfig(self.args.config)
        print('args parsed!')


        # Create a canvas that can fit the above video source size
        self.canvas = tkinter.Canvas(window, width = 640 , height = 480 )
        self.canvas.pack()

        # self.saveConfigButton = Button(window, text="Save Config", command=lambda: self.saveConfigButtonClickHandler())
        # self.saveConfigButton.pack(padx=15, pady=5, side=LEFT)

        # self.loadConfigButton = Button(window, text="Load Config", command=lambda: self.loadConfigButtonClickHandler())
        # self.loadConfigButton.pack(padx=15, pady=5, side=LEFT)
        # self.loadConfigButton = Button(window, text="Load Config", command=self.loadConfigButtonClickHandler())
        # self.loadConfigButton.pack(padx=15, pady=5, side=LEFT)

        self.video_capture = cv2.VideoCapture(0)
        self.loadFacesFromDirectory(self.args.directory)

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 5
        self.update()

        self.window.mainloop()




    def loadFacesFromDirectory(self, path):
        # load folder of files for face Recognition

        self.known_face_names = []
        self.known_face_encodings = []
        local_path = os.getcwd() + '\\' + str(path)
        files = os.listdir(local_path)


        for file in files:
            dotIndex = file.find('.')
            # print('file is: ', file)
            fileName = file[:dotIndex]
            self.known_face_names.append(fileName)

            local_path = os.getcwd() + '\\' + str(path) + '\\' + file
            file_image = face_recognition.load_image_file(local_path)
            face_encoding = face_recognition.face_encodings(file_image)[0]
            self.known_face_encodings.append(face_encoding)
            print( 'adding face:',fileName)


        print('as')

    def update(self):
        
        # update logic here...
        # Grab a single frame of video
        ret, frame = self.video_capture.read()

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_frame = frame[:, :, ::-1]

        # Find all the faces and face enqcodings in the frame of video
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        # Loop through each face in this frame of video
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)

            name = "Unknown"

            # If a match was found in known_face_encodings, just use the first one.
            if True in matches:
                first_match_index = matches.index(True)
                name = self.known_face_names[first_match_index]

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Display the resulting image
        cv2.imshow('Video', frame)

        # do this at the end of update
        self.window.after(self.delay, self.update)

# Create a window and pass it to the Application object
App(tkinter.Tk(), "Face App Prototype")