import face_recognition as fr
import cv2 as cv


function start():

#the actual training and encoding
function addPerson():
    #insert get request as a var and store it here
    new_person_image = fr.load_image_file("the get request")
    new_person_encoding = fr.face_encodings(new_person_image)

function initialize_camera():
    known_face_names =
    #this enables the video feed
    vid_cap = cv.VideoCapture(0)

    while True:
        #take a single frame from the feed and then resize it to 1/4 off the size for faster processing
        ret, frame = vid_cap.read()
        small_frame = cv.resize(frame, (0, 0), fx=0.25, fy=0.25)
        #a small frame to easily show that the computer recognizes someone
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

                # If a match was found gitin known_face_encodings, just use the first one.
                if True in matches:
                    first_match_index = matches.index(True)
                    name = known_face_names[first_match_index]

                face_names.append(name)

        process_this_frame = not process_this_frame


face_landmarks_list = fr.face_landmarks(image)
