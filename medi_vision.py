import face_recognition as fr
import cv2 as cv
import tkinter as tk
from tkinter import *
import pymongo
from pymongo import MongoClient

client = MongoClient('mongodb://kuber:password123@ds249942.mlab.com:49942/medar')

db = client["medar"]
collection = db.test_collection

# faces_col = db["faces"]
# patient_col = db["patients"]

users_col = db["users"]
profile_col = db["profile"]

names = []
encoded_faces = []

# the actual training and encoding
def addPerson():
    # train cv to recognize face after it construct a set of vectors and then encodes it
    new_person_image = fr.load_image_file("GET REQUEST FOR MOST RECENT PICTURE")
    new_person_encoding = fr.face_encodings(new_person_image)
    encoded_faces.append(new_person_encoding)
    names.append()


def initialize_camera():

    # this enables the video feed
    vid_cap = cv.VideoCapture(0)
    process_this_frame = True

    while True:
        # take a single frame from the feed and then resize it to 1/4 off the size for faster processing
        ret, frame = vid_cap.read()
        small_frame = cv.resize(frame, (0, 0), fx=0.25, fy=0.25)
        # a small frame to easily show that the computer recognizes someone
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = fr.face_locations(rgb_small_frame)
            face_encodings = fr.face_encodings(rgb_small_frame, face_locations)

            #face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = fr.compare_faces(fr, encoded_faces)
                name = "Unknown"
                medical_info = "N/A"

                # If a match was found within encoded_faces, just use the first one.
                if True in matches:
                    first_match_index = matches.index(True)
                    name = names[first_match_index]
                    # THEN USE THE NAME TO GET THE DATA FROM THE DICTIONARY OR HASTABLE OR WHATEVER

                #face_names.append(name)

        process_this_frame = not process_this_frame
        if(name != 'Unknown'):
            break;
        else:
            print("PERSON IS NOT IN THE SYSTEM")
            break;

    # terminating the final processes
    vid_cap.release()
    cv.destroyAllWindows()
    id = users_col.find("name")
    patient = profile_col.find("patient")
    return patient;




def start():
    # REGULAR VERSION WITHOUT THE POPUP#

    print("Welcome to Medi-Vision")
    func = input("Type in 1 if you'd like to start the ")
    if (func == 1):
        addPerson()
    else:
        initialize_camera()

        # NOW WITH POPUP THAT INCLUDES THE BUTTONS
        # tk = Tk()
        # var = StringVar()
        # label = Label(tk, textvariable=var, relief=RAISED)
        #
        # var.set("Welcome to Medi-Vision \n"+"Would you like to add someone or"
        #                                     "launch Medi-Vision", )  # What you want the text to be
        # label.pack()
        #
        # tk.geometry("100x150")  # The size of the box
        # tk.wm_title("Insight")  # The name of it
        # b1 = Button(master, text="Starup Camera", command=initialize_camera())
        # b2 = Button(master, text="Add New Person", command=addPerson())
        # b1.pack(side = LEFT)
        # b2.pack(side = RIGHT)
        # tk.mainloop()

start()

#face_landmarks_list = fr.face_landmarks(image)
