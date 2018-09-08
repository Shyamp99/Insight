import face_recognition as fr
import cv2 as cv
import tkinter as tk
from tkinter import *
import pymongo
from pymongo import MongoClient


# the actual training and encoding
def addPerson():
    # train cv to recognize face after it construct a set of vectors and then encodes it
    new_person_image = fr.load_image_file("GET REQUEST FOR MOST RECENT PICTURE")
    new_person_encoding = fr.face_encodings(new_person_image)
    # using get request from DB to get the array which stores all
    known_people =  ##INSERT GET REQUEST HERE##
    # NOW WE UPDATE THE ARRAY BY ADDING THE NEW ENCODED FACE'S VECTOR VALUES
    # UPDATE THE DB WITH THE NEWFOUND ARRAY
    # END OF FUNCTION


def initialize_camera():
    known_face_names =  # insert the fucking get request here
    # this enables the video feed
    vid_cap = cv.VideoCapture(0)

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

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = fr.compare_faces(fr, face_encoding)
                name = "Unknown"
                medical_info = "N/A"

                # If a match was found within known_face_encodings, just use the first one.
                if True in matches:
                    first_match_index = matches.index(True)
                    name = known_face_names[first_match_index]
                    # THEN USE THE NAME TO GET THE DATA FROM THE DICTIONARY OR HASTABLE OR WHATEVER

                face_names.append(name)

        process_this_frame = not process_this_frame  # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv.FONT_HERSHEY_DUPLEX
            cv.putText(frame, name + '\n' + medical_info, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Display the resulting image
        cv.imshow('Video', frame)

        # exut by pressing 'q'
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    # terminating the final processes
    vid_cap.release()
    cv.destroyAllWindows()


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
