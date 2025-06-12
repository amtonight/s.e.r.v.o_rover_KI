#ipynb file (jupyter notebook)


import cv2
import imutils
from picamera2 import Picamera2
import threading
from base_ctrl import BaseController
from motor_control import MotorControl
from color_recognition import ColorRecognition
from gesture_control import GestureControl
import time
import requests

# Definitionen
rover_ip = "192.168.10.102:8888"
base = BaseController('/dev/serial0', 115200)  
mc = MotorControl()
cr = ColorRecognition()
gc = GestureControl()
challenge_1 = challenge_2 = challenge_2_1 = challenge_3 = challenge_3_1 = challenge_3_2 = False
stop_requested = False

# Funktion welche mit threading laufen soll
def challenge():
    global challenge_1, challenge_2, challenge_2_1, challenge_3, challenge_3_1, challenge_3_2, stop_requested

    picam2 = Picamera2()
    picam2.configure(picam2.create_video_configuration(main={"format": 'XRGB8888', "size": (1280, 720)})) 
    picam2.start()

    while True:
        img = picam2.capture_array()
        cr.x_red = None
        cr.x_blue = None
        cr.x_green = None

        if challenge_1 == False:
            gc.wait_for_pommesgabel(img)
            if gc.last_pommesgabel_state == True:
                mc.find_red_ball(img, base, cr)
                if mc.ball_found == True:
                    challenge_1 = True
                    mc.ball_found = False
                    cr.x_red = None
                    cr.x_blue = None
                    cr.x_green = None

        elif challenge_2 == False:

            if challenge_2_1 == False:
                gc.finger_count_detector(img)
                if gc.sequence_state == 3:
                    mc.find_green_ball(img, base, cr)
                    if mc.ball_found == True:
                        challenge_2_1 = True
                        mc.ball_found = False
            
            else:
                mc.find_blue_ball(img, base, cr)
                if mc.ball_found == True:
                    challenge_2 = True
                    mc.ball_found = False
                    cr.x_red = None
                    cr.x_blue = None
                    cr.x_green = None
                    
        elif challenge_3 == False:

            if challenge_3_1 == False:
               if gc.sequence_state == 3:
                    mc.find_blue_ball(img, base, cr)
                    if mc.ball_found == True:
                        challenge_3_1 = True
                        mc.ball_found = False
            
            elif challenge_3_2 == False:
                mc.find_green_ball(img, base, cr)
                if mc.ball_found == True:
                    challenge_3_2 = True
                    mc.ball_found = False
                    
            else:
                mc.find_red_ball(img, base, cr)
                if mc.ball_found == True:
                    challenge_3 = True
                    mc.ball_found = False   

        if stop_requested:
            print("Programm wird gestoppt...")
            picam2.close()
            break


# Challenge Thread wird gestartet
thread = threading.Thread(target=challenge)
thread.start()

# Enter Eingabe zum stoppen
input("Drücke Enter zum stoppen...\n")
stop_requested = True

# Thread wird gestoppt
thread.join()
