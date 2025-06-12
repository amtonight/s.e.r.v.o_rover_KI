import cv2  # Library for image processing
import imutils  # Library for image processing
import numpy as np  # Library for mathematical calculations

class ColorRecognition:
    def __init__(self):
        
        # Blaue Color Range definieren
        self.color_lower_blue = np.array([105, 240, 130])
        self.color_upper_blue = np.array([112, 255, 230])
        
        # Grüner Color Range definieren
        self.color_lower_green = np.array([63, 100, 80])
        self.color_upper_green = np.array([70, 255, 220])
        
        # Rote Color Range definieren
        self.color_lower_red1 = np.array([0, 120, 100])
        self.color_upper_red1 = np.array([5, 255, 205])
        
        self.color_lower_red2 = np.array([175, 120, 100])
        self.color_upper_red2 = np.array([180, 255, 205])

        # Mindestradius des Balles definieren
        self.min_radius = 6

        # X-Koordinate und Radius des blauen Balles definieren
        self.x_blue = None
        self.radius_blue = None

        # X-Koordinate und Radius des grünen Balles definieren
        self.x_green = None
        self.radius_green = None

        # X-Koordinate und Radius des roten Balles definieren
        self.x_red = None
        self.radius_red = None

    # Funktion zum Finden von blauen Konturen im Frame
    def find_contours_blue(self, img):

        self.img = img

        # Frame weichzeichnen und in HSV konvertieren
        self.blurred = cv2.GaussianBlur(self.img, (11, 11), 0)
        self.hsv = cv2.cvtColor(self.blurred, cv2.COLOR_BGR2HSV)

        # Blaue Maske anhand der Color Range erstellen
        self.mask_blue = cv2.inRange(self.hsv, self.color_lower_blue, self.color_upper_blue)  
        self.mask_blue = cv2.erode(self.mask_blue, None, iterations=1)
        self.mask_blue = cv2.dilate(self.mask_blue, None, iterations=5)
            
        # Konturen innerhalb der blauen Maske finden
        self.cnts_blue = cv2.findContours(self.mask_blue.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        self.cnts_blue = imutils.grab_contours(self.cnts_blue)

        # Wenn eine blaue Kontur gefunden wurden:
        if len(self.cnts_blue) > 0:

            # Größte blaue Kontur finden
            self.c_blue = max(self.cnts_blue, key=cv2.contourArea)
            ((self.x_blue, self.y_blue), self.radius_blue) = cv2.minEnclosingCircle(self.c_blue)

            # Wenn die gefunden Kontur groß genug ist setze X-Koordinate sowie Radius
            if self.radius_blue < self.min_radius:
                self.x_blue = None
                self.radius_blue = None

    # Getter X Blau
    def get_x_blue(self):
        return self.x_blue

    # Getter Radius Blau
    def get_radius_blue(self):
        return self.radius_blue


    # Funktion zum Finden von grünen Konturen im Frame
    def find_contours_green(self, img):
        
        self.img = img

        # Frame weichzeichnen und in HSV konvertieren
        self.blurred = cv2.GaussianBlur(self.img, (11, 11), 0)
        self.hsv = cv2.cvtColor(self.blurred, cv2.COLOR_BGR2HSV)

        # Grüne Maske anhand der Color Range erstellen
        self.mask_green = cv2.inRange(self.hsv, self.color_lower_green, self.color_upper_green)
        self.mask_green = cv2.erode(self.mask_green, None, iterations=1)
        self.mask_green = cv2.dilate(self.mask_green, None, iterations=5)
            
        # Konturen innerhalb der grünen Maske finden
        self.cnts_green = cv2.findContours(self.mask_green.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        self.cnts_green = imutils.grab_contours(self.cnts_green)

        # Wenn eine grüne Kontur gefunden wurden:
        if len(self.cnts_green) > 0:

            # Größte grüne Kontur finden
            self.c_green = max(self.cnts_green, key=cv2.contourArea)
            ((self.x_green, self.y_green), self.radius_green) = cv2.minEnclosingCircle(self.c_green)

            # Wenn die gefunden Kontur groß genug ist setze X-Koordinate sowie Radius
            if self.radius_green < self.min_radius:
                self.x_green = None
                self.radius_green = None
                

    # Getter X Grün
    def get_x_green(self):
        return self.x_green

    # Getter Radius Grün
    def get_radius_green(self):
        return self.radius_green
        
    # Funktion zum Finden von roten Konturen im Frame
    def find_contours_red(self, img):
            
        self.img = img

        # Frame weichzeichnen und in HSV konvertieren
        self.blurred = cv2.GaussianBlur(self.img, (11, 11), 0)
        self.hsv = cv2.cvtColor(self.blurred, cv2.COLOR_BGR2HSV)

        # Rote Maske anhand der 2 Color Ranges erstellen
        self.mask_red1 = cv2.inRange(self.hsv, self.color_lower_red1, self.color_upper_red1)
        self.mask_red2 = cv2.inRange(self.hsv, self.color_lower_red2, self.color_upper_red2)
        self.mask_red = cv2.bitwise_or(self.mask_red1, self.mask_red2)

        self.mask_red = cv2.erode(self.mask_red, None, iterations=1)
        self.mask_red = cv2.dilate(self.mask_red, None, iterations=5)

        # Konturen innerhalb der roten Maske finden
        self.cnts_red = cv2.findContours(self.mask_red.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        self.cnts_red = imutils.grab_contours(self.cnts_red)  # Extract contours

        # Wenn eine grüne Kontur gefunden wurden:
        if len(self.cnts_red) > 0:

            # Größte rote Kontur finden
            self.c_red = max(self.cnts_red, key=cv2.contourArea)  # Find the largest red contour
            ((self.x_red, self.y_red), self.radius_red) = cv2.minEnclosingCircle(self.c_red)  # Compute the minimum enclosing circle of the red contour

            # Wenn die gefunden Kontur groß genug ist setze X-Koordinate sowie Radius
            if self.radius_red < self.min_radius:
                self.x_red = None
                self.radius_red = None

    # Getter X Rot
    def get_x_red(self):
        return self.x_red

    # Getter Radius Rot
    def get_radius_red(self):
        return self.radius_red
        