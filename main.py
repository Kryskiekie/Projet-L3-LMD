#*******************************************************************************
#----------------------------------LANDA YE------------------------------------*
#                                                                              *
#                           par KIEKIE YEDIDIA Chris                           *
#                                                                              *
#                                 2023-2024                                    *
#*******************************************************************************
import cv2
import numpy as np
from ultralytics import YOLO
from pyfirmata import Arduino, SERVO, util
from time import sleep

#Cette fonction permet de mapper une valeur entre deux autres valeurs
def map_range(value, in_min, in_max, out_min, out_max):
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

#Initialisation des variables
port = 'COM9'
angle_init = 90
servo_pinX = 9
servo_pinY = 10

# Initialisation du modele
try:        
    model = YOLO("modelAvion2.pt") #C:/Users/HP/Desktop/ProjetChris/modelAvion.pt
    board=Arduino(port)
except Exception as e:
    print(f'[ERREUR] Échec de chargement du modèle: {e}')
    exit() 


board.digital[servo_pinX].mode=SERVO
board.digital[servo_pinY].mode=SERVO

print('[INFO] Démarrage de la webcam...')

cam = cv2.VideoCapture(0)
if not cam.isOpened():
    print("Camera couldn't Access!!!")
    exit()

ws, hs = 640, 480
cam.set(3, ws)
cam.set(4, hs) 

laser_pin = board.get_pin('d:7:o')

board.digital[servo_pinX].write(angle_init)
board.digital[servo_pinY].write(angle_init)

while cam.isOpened():
    ret, frame = cam.read()
    
    if not ret:
        break

    results = model.track(frame,conf=0.8,max_det = 1, persist=True,stream=True)
    
    for result in results:
        boxes = result.boxes.xyxy.cpu().numpy()
        classes = result.boxes.cls.cpu().numpy().astype(int)

        for i, box in enumerate(boxes):
            x1, y1, x2, y2 = [int(c) for c in box]
            cx = (x1 + x2) // 2
            cy = (y1 + y2) // 2

            angle_x = int(map_range(cx, ws, 0, 0, 180))  # Mapping de la position x à un angle entre 0 et 180 degrés
            angle_y = int(map_range(cy, hs, 0, 180, 0))
            angle_ym = angle_y + 4
            
            print(f"la position de x: {angle_x} et de y: {angle_ym}")
            
            board.digital[servo_pinX].write(angle_x)
            board.digital[servo_pinY].write(angle_ym)
            sleep(0.015)

            class_id = classes[i]
            class_name = model.names[class_id]

            if class_name=="Avion de chasse" or class_name=="Drone":
                laser_pin.write(1)

            else:
                laser_pin.write(1)
            
            cv2.putText(frame, class_name, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (36, 255, 12), 2)
            cv2.circle(frame, (cx, cy), 80, (0, 0, 255), 2)
            cv2.line(frame, (0, cy), (ws, cy), (0, 0, 0), 2)  # x line
            cv2.line(frame, (cx, hs), (cx, 0), (0, 0, 0), 2)  # y line
            cv2.circle(frame, (cx, cy), 15, (0, 0, 255), cv2.FILLED)

    cv2.imshow("Landa Ye", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        laser_pin.write(0)
        break

cam.release()
cv2.destroyAllWindows()
print("Fin du programme")