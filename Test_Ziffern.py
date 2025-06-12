import cv2
import imutils
from picamera2 import Picamera2
import threading
from base_ctrl import BaseController
from motor_control import MotorControl
from color_recognition import ColorRecognition
from gesture_control import GestureControl
from digit_recognition import predict_digit
import time
import requests
from tensorflow import keras
from pathlib import Path
import re
from IPython.display import display, clear_output
import matplotlib.pyplot as plt

# Definitionen
rover_ip = "192.168.10.102:8888"
base = BaseController('/dev/serial0', 115200)  
mc = MotorControl()
cr = ColorRecognition()
gc = GestureControl()
challenge_1 = challenge_2 = challenge_2_1 = challenge_3 = challenge_3_1 = challenge_3_2 = False
stop_requested = False

# Modellverzeichnis und Ladecode
KERAS_DIR = Path("~/ugv_pt_rpi/test-marco/src/keras_dateien").expanduser()

files = sorted(KERAS_DIR.glob("rasp_rover_*.keras"),
               key=lambda p: int(re.search(r"_(\d{3})\.keras$", p.name)[1]))

if not files:
    raise FileNotFoundError("❌ Kein Modell gefunden. Bitte trainiere zuerst eins.")

MODEL = keras.models.load_model(files[-1])
print("✅ Modell geladen:", files[-1].name)

def show_frame_in_notebook(img_bgr):
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    plt.figure(figsize=(8, 6))
    plt.imshow(img_rgb)
    plt.axis("off")
    clear_output(wait=True)
    display(plt.gcf())
    plt.close()

# Funktion welche mit threading laufen soll
def challenge():
    global stop_requested

    picam2 = Picamera2()
    picam2.configure(picam2.create_video_configuration(
        main={"format": 'XRGB8888', "size": (480, 480)}))
    picam2.start()

    while not stop_requested:
        img = picam2.capture_array()
        digit, confidence, img_annotated = predict_digit(img, MODEL)

        if digit and confidence >= 0.85:
            print(f"Ziffer erkannt: {digit} mit {confidence:.2f} Sicherheit")
        else:
            print("Keine gültige Ziffer erkannt.")

        show_frame_in_notebook(img_annotated)
        time.sleep(0.1)

    print("Programm wird gestoppt...")
    picam2.close()


# Challenge Thread wird gestartet
thread = threading.Thread(target=challenge)
thread.start()

# Enter Eingabe zum stoppen
input("Drücke Enter zum stoppen...\n")
stop_requested = True

# Thread wird gestoppt
thread.join()
