import face_recognition as fr
import cv2 as cv
import pymongo
from pymongo import MongoClient
import base64

client = MongoClient('login stuff')

db = client["medar"]
collection = db.test_collection

# faces_col = db["faces"]
# patient_col = db["patients"]

users_col = db["users"]
profile_col = db["profile"]

known_face_names = []
face_locations = []
face_names = []
known_face_encodings = []

# the actual training and encoding
def addPerson(name):
    # train cv to recognize face after it construct a set of vectors and then encodes it
    id = users_col.find(name)
    patient = profile_col.find(id)
    picture_link = patient.img
    picture = base64.decodestring(picture_link)

    new_person_image = fr.load_image_file(picture)
    new_person_encoding = fr.face_encodings(new_person_image)
    known_face_encodings.append(new_person_encoding)
    face_names.append(name)

    initialize_camera()


def initialize_camera():

    # this enables the video feed
    vid_cap = cv.VideoCapture(0)
    process_this_frame = True
    name = "Unknown"
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
                matches = fr.compare_faces(known_face_encodings,face_encoding)
                name = "Unknown"
                medical_info = "N/A"


                counter = 0
                temp = False
                for i in matches:
                    for j in i:
                         if j == True:
                             temp = True
                             first_match = j
                             break
                         counter+=1


                # If a match was found within encoded_faces, just use the first one.
                if temp:
                    first_match_index = counter
                    name = known_face_names[first_match_index]

        process_this_frame = not process_this_frame
        if(name != 'Unknown'):
            break;
        else:
            print("PERSON IS NOT IN THE SYSTEM")
            break;

    # terminating the final processes
    vid_cap.release()
    cv.destroyAllWindows()
    id = users_col.find(name)
    patient = profile_col.find(id)
    return patient;




def start():
    # REGULAR VERSION WITHOUT THE POPUP#

    print("Welcome to Medi-Vision")
    func = int(input("Type in 1 if you'd like to add someone to the database or Type 2 initialize the camera: "))
    if (func == 1):
        addPerson(input("Provide a name: "))
    else:
        initialize_camera()


start()

#face_landmarks_list = fr.face_landmarks(image)
