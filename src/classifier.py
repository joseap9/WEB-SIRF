import cv2
import face_recognition
import numpy as np

import urllib.request

import dbPsql


camera = cv2.VideoCapture(0)
#lista de imagenes leidas desde la base de datos (la imagenes se guardan via https)
picture_list = []
#lista de nombres de cada rostro(imagen)
known_face_names = []

#recorrido de logitud de datos de la tabla
for x in range(dbPsql.lenn()):
    #extraccion de cada imagen
    url = dbPsql.get_nombres()[x]['imagen']
    #respuesta del url
    response = urllib.request.urlopen(url)
    #agrega cada imagen en la lista
    picture_list.append(response)
    #agrga cada nombre en la lista
    known_face_names.append(dbPsql.get_nombres()[x]['nombre_completo'])



# lista de rostros procesados
picture_processing_list = []

#proceso de reconocimiento por cada imagen existen dentro de la lista anteriormente llenada
for pic in picture_list:
    load_pic = face_recognition.load_image_file(pic)
    pro_pic = face_recognition.face_encodings(load_pic)[0]
    #agrega data dentro de la lista
    picture_processing_list.append(pro_pic)

# se inician listas necesarios para proceso de reconocimiento
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
# se guardan los nombres de los asistentes
asistentes = []


def gen_frame():  
    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]

            # Only process every other frame of video to save time
           
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(picture_processing_list, face_encoding)
                name = "No Registrado"
                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(picture_processing_list, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]

                face_names.append(name)
                if name not in asistentes and name != "No Registrado":
                        asistentes.append(name)
                
            

            # Display the results
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                # Draw a box around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                # Draw a label with a name below the face
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    