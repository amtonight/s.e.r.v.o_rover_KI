from color_recognition import ColorRecognition
import time

class MotorControl:
    def __init__(self):

        self.ball_found = False
        
    # Funktion um Frame auf Konturen der Farben Blau, Grün und Rot zu scannen
    def scan_frame(self, img, cr):
        cr.find_contours_blue(img)
        cr.find_contours_green(img)
        cr.find_contours_red(img)

    # Funktion zur Suche des blauen Balles
    def find_blue_ball(self, img, base, cr):
        
        cr.find_contours_blue(img)

        # Wenn eine X-Koordinate des Balles gefunden fahre zum Ball
        if cr.get_x_blue() != None:

            self.drive_to_ball(cr.get_x_blue(), cr.get_radius_blue(), base)

        # Sonst suche nach dem Ball
        else:
            self.look_for_ball(base, img, cr, "blue")


    # Funktion zur Suche des grünen Balles
    def find_green_ball(self, img, base, cr):
        
        cr.find_contours_green(img)

        # Wenn eine X-Koordinate des Balles gefunden fahre zum Ball
        if cr.get_x_green() != None:

            self.drive_to_ball(cr.get_x_green(), cr.get_radius_green(), base)

        # Sonst suche nach dem Ball
        else:
            self.look_for_ball(base, img, cr, "green")

    # Funktion zur Suche des roten Balles
    def find_red_ball(self, img, base, cr):
        
        cr.find_contours_red(img)

        # Wenn eine X-Koordinate des Balles gefunden fahre zum Ball
        if cr.get_x_red() != None:
            
            self.drive_to_ball(cr.get_x_red(), cr.get_radius_red(), base)

        # Sonst suche nach dem Ball
        else:
            self.look_for_ball(base, img, cr, "red")
        
    # Funktion zum Fahren zum Ball
    def drive_to_ball(self, x, radius, base):

        # Abweichung vom Mittelpunkt ermitteln
        self.error = x - 640

        # Erlaubte Abweichung vom Mittelpunkt definieren
        self.dead_zone = 50

        # Wenn die Abweichung klein genug ist:
        if abs(self.error) < self.dead_zone:

            # Wenn Radius des Balles im passendem Bereich bleibe stehen und setze ball_found auf True
            if radius >= 66 and radius <= 70:
                base.send_command({"T": 1, "L": 0, "R": 0})
                self.ball_found = True
                print("Ball gefunden")
                time.sleep(4)
                base.send_command({"T": 1, "L": -0.15, "R": -0.15})
                time.sleep(3)

            # Wenn Radius des Balles zu groß fahre rückwarts
            elif radius > 70:
                base.send_command({"T": 1, "L": -0.01, "R": -0.01})

            # Wenn Radius des Balles zu klein fahre vorwärts mit sich anpassender Geschwindigkeit je nach Abstand
            elif radius < 44:
                base.send_command({"T": 1, "L": 0.15, "R": 0.15})

            elif radius < 54:
                base.send_command({"T": 1, "L": 0.05, "R": 0.05})

            elif radius < 66:
                base.send_command({"T": 1, "L": 0.01, "R": 0.01})

        # Wenn Radius des Balles zu groß fahre rückwarts
        elif radius > 60:
            base.send_command({"T": 1, "L": -0.05, "R": -0.05})
            time.sleep(2)

        # Wenn Rover nicht zentral zum Ball richte den Rover zentral aus
        else:

            # Fahre rechts oder links je nach X-Position des Balles
            if self.error > 0 :
                base.send_command({"T": 1, "L": 0.08, "R": 0.04})

            else:
                base.send_command({"T": 1, "L": 0.04, "R": 0.08})
                

    # Funktion zur Suche nach den Bällen
    def look_for_ball(self, base, img, cr, color):

        self.color = color
        self.base = base
        self.img = img
        self.cr = cr
        
        base.send_command({"T": 1, "L": -0.15, "R": -0.07})
        time.sleep(2) 
        base.send_command({"T": 1, "L": 0, "R": 0})
        time.sleep(0.5)

        if self.color == "red":
            cr.find_contours_red(self.img)
            if self.cr.get_x_red() != None:
                base.send_command({"T": 1, "L": -0.1, "R": -0.1})
                time.sleep(2)
                base.send_command({"T": 1, "L": 0, "R": 0})
                time.sleep(0.5)
                return

        elif self.color == "blue":
            cr.find_contours_blue(self.img)
            if self.cr.get_x_blue() != None:
                base.send_command({"T": 1, "L": -0.1, "R": -0.1})
                time.sleep(2)
                base.send_command({"T": 1, "L": 0, "R": 0})
                time.sleep(0.5)
                return

        elif self.color == "green":
            cr.find_contours_green(self.img)
            if self.cr.get_x_green() != None:
                base.send_command({"T": 1, "L": -0.1, "R": -0.1})
                time.sleep(2)
                base.send_command({"T": 1, "L": 0, "R": 0})
                time.sleep(0.5)
                return
        
        base.send_command({"T": 1, "L": 0.07, "R": 0.15})
        time.sleep(2)
        base.send_command({"T": 1, "L": 0, "R": 0})
        time.sleep(0.5)

        if self.color == "red":
            cr.find_contours_red(self.img)
            if self.cr.get_x_red() != None:
                base.send_command({"T": 1, "L": -0.1, "R": -0.1})
                time.sleep(2)
                base.send_command({"T": 1, "L": 0, "R": 0})
                time.sleep(0.5)
                return

        elif self.color == "blue":
            cr.find_contours_blue(self.img)
            if self.cr.get_x_blue() != None:
                base.send_command({"T": 1, "L": -0.1, "R": -0.1})
                time.sleep(2)
                base.send_command({"T": 1, "L": 0, "R": 0})
                time.sleep(0.5)
                return

        elif self.color == "green":
            cr.find_contours_green(self.img)
            if self.cr.get_x_green() != None:
                base.send_command({"T": 1, "L": -0.1, "R": -0.1})
                time.sleep(2)
                base.send_command({"T": 1, "L": 0, "R": 0})
                time.sleep(0.5)
                return
