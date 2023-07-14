import RPi.GPIO as GPIO #Bibliothek heißt eigentlich RPi.GPIO, soll in der Klasse aber einfach mit GPIO abgekürzt werden, Bibliothek ermöglicht Nutzung der GPIO pins am Raspberry Pi
import time
GPIO.setmode(GPIO.BOARD) # Welche Pin Nummerierung? --> BOARD. Es gibt nämlich auch noch andere Nummerierungsarten wie GPIO.BCM

class servo():
    def __init__(self, pin, freq, dc_start_percentage_for50hz, dc_end_percentage_for50hz, direction=True): #Konstruktor, Stichwort self ist das gleiche wie "this" in Java oder C++
        self.started=False
        if freq==50:
                self.startdc=dc_start_percentage_for50hz        #falls Frequenz=50Hz werte einfach für Klassenattribute übernehmen
                self.enddc=dc_end_percentage_for50hz
                self.freq=50 #in Hz
        else:
            self.adjustFreq(freq, self.started)                 #andernfalls mit Methode adjustFreq Tastgradwertebereich updaten
        self.direction=direction
        self.delta=0.75
        self.range_pwm=self.enddc-self.startdc                  #weitere für die funktionsweise notwendige Attribute setzen
        self.pin=pin
        GPIO.setup(self.pin, GPIO.OUT)
        self.pwmObject=GPIO.PWM(self.pin, self.freq)
        self.boardConnectNumber=0

    def __del__(self):              #Destruktor, beim löschen einer Instanz soll das PWM-Signal beendet werden
        self.pwmObject.stop()

    def writeDegFromServer(self, deg_min,deg_max,deg):  #konvertiert Gradzahl in Tastgrad und setzt den Servo
        self.range_deg=deg_max-deg_min                  #möglicher Bereich in Grad
        self.range_pwm=self.enddc-self.startdc          #möglicher Tastgradbereich
        percent=(deg-deg_min)/self.range_deg            #Berechne Prozentzahl, indem die Gradzahl durch den möglichen Bereich in Grad dividiert wird
        dc=self.startdc+(percent*self.range_pwm)        #berechne mithilfe von Prozentzahl, den zu setzenden Tastgrad
        self.adjustDC(dc)                               #setze berechneten Tastgrad, mit Klassenmethode adjustDC(...)

    def adjustFreq(self, freq, started=True):
        fbase=50
        factor=int(freq/fbase)                          #Tastgrad neu berechnen, für höhere Frequenzen
        self.startdc=self.startdc*factor
        self.enddc=self.enddc*factor
        self.freq=freq
        if started==True:
            self.pwmObject.stop()                           #PWM mit anderer Frequenz neustarten, erfordert neue Instanziierung des PWM-Objektes
            del self.pwmObject
            self.pwmObject=GPIO.PWM(self.pin, self.freq)

    def adjustDC(self, dc):
        if dc<self.startdc:                     #prüfe, ob versehentlich die berechneten Tastgrade
            dc=self.startdc                     #größer als die zulässigen sind
        if dc>self.enddc:                       #falls dem so ist, entsprechend auf minimum oder maxiumum setzen
            dc=self.enddc

        if self.direction==True:                #invertiere Tastgrad bezogen auf dem möglichen Bereich,
            dc = self.enddc + self.startdc - dc #sorgt für die richtige Richtung des Servos

        if self.started==True:
                self.pwmObject.ChangeDutyCycle(dc)      #normalerweise brauchen Servo, die keiner kontinuierlichen Last ausgesetzt sind,
                time.sleep(self.delta)                  #kein andauerndes PWM-Signal, sondern werden gesetzt und eine kurze Zeit später ausgeschaltet,
                self.pwmObject.ChangeDutyCycle(0)       #indem der Tastgrad auf null gesetzt wird
        else:
            self.pwmObject.start(dc)            #falls servo das erste mal gestartet wird, muss es noch
            time.sleep(self.delta)              #mit .start() initialisiert werden
            self.pwmObject.ChangeDutyCycle(0)
            self.started=True


def roll(servo_left, servo_right, deg, deg_min, deg_max):                   #ist NICHT teil der Klasse servo(), benutzt aber Methoden von ihr
    range_deg=deg_max-deg_min                                               
    percent=(deg-deg_min)/range_deg
    set1=servo_left.enddc-(percent*(servo_left.enddc-servo_left.startdc))       #Tastgradwert für linken Servo in Abhängigkeit des eingestellten Grades berechnen
    set2=servo_right.startdc+(percent*(servo_right.enddc-servo_right.startdc))  #Tastgradwert für rechten Servo in Abhängigkeit des eingestellten Grades berechnen
    servo_left.pwmObject.ChangeDutyCycle(set1)                                  #Tastgrad für linken Servo setzen
    servo_right.pwmObject.ChangeDutyCycle(set2)                                 #Tastgrad für rechten Servo setzen
    time.sleep(0.75)                                                            #kurz warten, bis Servos sich selbst eingestellt haben
    servo_left.pwmObject.ChangeDutyCycle(0)                                     #nun Servos wieder ausschalten
    servo_right.pwmObject.ChangeDutyCycle(0)

