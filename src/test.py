import face_recognition
import cv2
import numpy as np
import urllib.request

import dbPsql

def gen_frames():
    #abre camara y captura video
    video_capture = cv2.VideoCapture(0)


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


    while True:
            # captura frames del video
            ret, frame = video_capture.read()

            # redimensiona frames del video a 1/4 para hacer mas rapido el proceso de reconocimiento
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

            #convierte la imagen en el modo de imagen que utiliza la libreria face_recognition
            rgb_small_frame = small_frame[:, :, ::-1]


            #procesa cada frame de video
            if process_this_frame:
                # encuentra todas los rostros que se encuentren dentro del frame del video
                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

                face_names = []
                for face_encoding in face_encodings:

                    # mira si la face hace match dentro de la lista de caras registradas
                    matches = face_recognition.compare_faces(picture_processing_list, face_encoding)
                    name = "No Registrado"

                    # # si una cara que hace match es encotrada:
                    # si es True:
                    #     first_match_index = matches.index(True)
                    #     name = known_face_names[first_match_index]
                    # mismo numero de lista con known_face_names y picture_processing_list

                    #ajustes de distancias con la cara detectada
                    face_distances = face_recognition.face_distance(picture_processing_list, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = known_face_names[best_match_index]

                    face_names.append(name)

            process_this_frame = not process_this_frame


            # arroja los resultados
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                # dibuja un cuadro alrededor del rostro
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                # dibuja una etiqueta con el nombre del rostro
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

            # Display the resulting image
            cv2.imshow('Video', frame)

            # presiona q para salir
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    video_capture.release()
    cv2.destroyAllWindows()

gen_frames()