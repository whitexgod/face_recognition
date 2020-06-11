import face_recognition
import numpy as np
from datetime import datetime
import os
import cv2


video_capture = cv2.VideoCapture(0)

known_face_encodings = []
known_face_names = []

iamTuhin = face_recognition.load_image_file('/Users/tuhin/PycharmProjects/face_rec/images/tuhin.jpg')
iamTuhinEncoding = face_recognition.face_encodings(iamTuhin)[0]

iamMark = face_recognition.load_image_file('/Users/tuhin/PycharmProjects/face_rec/images/Mark_Zuckerberg.jpg')
iamMarkEncoding = face_recognition.face_encodings(iamMark)[0]

iamTrump = face_recognition.load_image_file('/Users/tuhin/PycharmProjects/face_rec/images/donald+trump.png')
iamTrumpEncoding = face_recognition.face_encodings(iamTrump)[0]

known_face_encodings = [iamTuhinEncoding, iamMarkEncoding, iamTrumpEncoding]
known_face_names = ['Tuhin','Mark', 'Trump']

face_locations =[]
face_encodings = []
face_names = []
process_this_frame = True

i=0

while True:

    ret, frame = video_capture.read()
    small_frame = cv2.resize(frame, (0,0), fx=0.5, fy=0.5)
    rgb_small_frame = small_frame[:,:,::-1]

    if process_this_frame:
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        name_list = []
        face_names =[]

        for face_encoding in face_encodings:

            matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.6)

            face_distances = face_recognition.face_distance(known_face_encodings,face_encoding)
            best_match_index = np.argmin(face_distances)

            if matches[best_match_index]:
                name = known_face_names[best_match_index]
                face_names.append(name)
                #now = datetime.now()

    i += 1

    if i ==5:
        curr_name = name
        print(curr_name)

    if len(face_names) == 0:
        i = 0

    process_this_frame = not process_this_frame

    for (top, right, bottom, left), name in zip(face_locations,face_names):
        top *= 2
        right *= 2
        bottom *=2
        left *= 2

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        cv2.rectangle(frame, (left, bottom-35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left+6,bottom-6), font, 1.0, (255,255,255), 1)

    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()