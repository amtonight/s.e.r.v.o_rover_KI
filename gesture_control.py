import cv2
import mediapipe as mp
import time

class GestureControl:
    def __init__(self):

        # MediaPipe Hands vorbereiten
        self.hands = mp.solutions.hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
        self.last_pommesgabel_state = False
        self.sequence_state = 0

    def release(self):
        cv2.destroyAllWindows()

    def is_finger_extended(self, lm, tip_id, pip_id):
        return lm[tip_id].y < lm[pip_id].y

    def detect_pommesgabel(self, lm):
        zeige = self.is_finger_extended(lm, 8, 6)
        klein = self.is_finger_extended(lm, 20, 18)
        daumen_oben = self.is_finger_extended(lm, 4, 3)
        mittel = self.is_finger_extended(lm, 12, 10)
        ring = self.is_finger_extended(lm, 16, 14)
        return zeige and klein and not mittel and not ring

    def wait_for_pommesgabel(self, img):

        self.img = img
        rgb = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                if self.detect_pommesgabel(hand_landmarks.landmark):
                    if not self.last_pommesgabel_state:
                        print("Pommesgabel erkannt")
                        self.last_pommesgabel_state = True


    def count_fingers(self, lm):
        fingers = [
            lm[8].y > lm[6].y,
            lm[12].y > lm[10].y,
            lm[16].y > lm[14].y,
            lm[20].y > lm[18].y,
        ]
        return sum(fingers)

    def update_count_sequence(self, count):
        if self.sequence_state == 0 and count == 1:
            print("Zählfolge-Schritt 1 erkannt")
            self.sequence_state = 1
        elif self.sequence_state == 1 and count == 2:
            print("Zählfolge-Schritt 2 erkannt")
            self.sequence_state = 2
        elif self.sequence_state == 2 and count == 3:
            print("Zählfolge 1→2→3 erkannt!")
            self.sequence_state = 3

    def finger_count_detector(self, img):

        self.img = img
        rgb = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb)
        
        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                count = self.count_fingers(handLms.landmark)
                self.update_count_sequence(count)

