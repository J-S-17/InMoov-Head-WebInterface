#/usr/bin/env python
# -*- coding: utf-8 -*-

###################################
# CSC = Combined Server Component #
# Version 2, mit Sprachsteuerung  #
###################################

from flask import *
import imutils, time, sys, os, numpy, head, cv2, requests                                   # import (Python) =  #include (C)

##############################################################
#Kopf softwareseitg modellieren, mithilfe der in "head.py" erstellten Klasse servo()
eye_x_pin       = 13
eye_y_pin       = 12
mouth_pin       = 15
head_y_pin      = 22
head_x_pin      = 11
roll_left_pin   = 16
roll_right_pin  = 18
default_freq    = 50

eye_x=head.servo(eye_x_pin, default_freq, 5, 9)
eye_y=head.servo(eye_y_pin, default_freq, 5, 9)

mouth=head.servo(mouth_pin, default_freq, 5,9, False)

head_y=head.servo(head_y_pin, default_freq, 5,9)
head_x=head.servo(head_x_pin, default_freq, 5,9)
roll_left=head.servo(roll_left_pin, default_freq, 1.75,8.5, False)    # roll (englisch)= Rollen (Drehung um Längsrichtung)
roll_right=head.servo(roll_right_pin, default_freq, 4,9.25, False)

roll_right.pwmObject.start(0) # bei diesen beiden Servos muss hier das PWM-Signal gestartet werden 
roll_left.pwmObject.start(0)  # damit die Funktion roll() aus der Datei head.py funktionieren kann

#head_x.boardConnectNumber=1         #nicht benötigte Attribute. gibt nur an, an welchen Pins die Servos auf der gelöteten Platine angeschlossen sind.
#mouth.boardConnectNumber=2
#eye_x.boardConnectNumber=3
#eye_y.boardConnectNumber=4
#roll_left.boardConnectNumber=5
#roll_right.boardConnectNumber=6
#head_y.boardConnectNumber=7

dictionary= {"HeadX": head_x, "HeadY": head_y, "Roll": (roll_left, roll_right), "EyeX": eye_x, "EyeY": eye_y, "Mouth": mouth}

#################################################################################################################
#Hilfsfunktionen für die Sprachsteuerung 

def STT():                                                                                  #STT = Speech-To-Text: Funktion um Sprache per Google Cloud Speech API umzuwandeln
    API_KEY="AIz--------------------------tOaYmwZX3c"                                       #API-Key, hier einfügen, aus Datenschutzgründen teils gestrichen
    url= "https://www.google.com/speech-api/v2/recognize?output=json&lang=en-us&key="       #url an die man die audio-datei versenden muss
    url+=API_KEY                                                                            #url braucht API-Key hinten angehängt
    header={"Content-Type": "audio/x-flac; rate=44100"}                                     #HTTP-Header Informationen, datentyp "flac" und Tastrate der Audiodatei 44100Hz
    audio_file=open("temp.flac", "rb")                                                      #Audio-datei öffnen
    file_dictionary={"file":audio_file_handle}                                              #kreeire ein Python-Dictionary, welches als Parameter für request.post benötigt wird
    request_answer_object = requests.post(url, files = file_dictionary, headers=header)     #Temporäre Audio Datei an Google versenden, Rückgabe ist JSON-Objekt
    transcript_offset= request_answer_object.text.find("transcript")                        #JSON als Text interpretieren, Offsets zum eigentlichen Transkript ermitteln
    confidence_offset= request_answer_object.text.find("confidence")                        
    offset_to_SOT=len('transcript":"')                                                      #SOT = start of text: Offsets innerhalb der JSON-Zeichenkette
    offset_to_EOT=len('''","''')                                                            #EOT = end of text:
    extracted_text=request_answer_object.text[transcript_offset+offset_to_SOT:confidence_offset-offset_to_EOT] #mithilfe der Offsets, Textbereich aus JSON-Zeichenkette extrahieren, in der das eigentliche Transkript vorhanden ist
    #print('\x1b[6;30;42m' + extracted_text + '\x1b[0m') #Debug Ausgabe
    return extracted_text
    
def getDirection(input, object):
    #servoToUpdate.writeDegFromServer(int(degmin),int(degmax),int(deg))
    if(object=="head"):
        if (input.find("left")!=-1):
            head_x.adjustDC(head_x.startdc)
            responeDir="Turning Head left"
        elif (input.find("right")!=-1):
            head_x.adjustDC(head_x.enddc)
            responeDir="Turning Head right"
        elif (input.find("up")!=-1):
            head_y.adjustDC(head_y.startdc)
            responeDir="Turning Head up"
        elif (input.find("down")!=-1):
            head_y.adjustDC(head_y.enddc)
            responeDir="Turning Head down"
        else:
            responeDir="Error with dir head"
    
    #head.roll(servoToUpdate[0], servoToUpdate[1], int(deg), int(degmin), int(degmax))
    elif(object=="roll"):
        if (input.find("left")!=-1):
            head.roll(roll_left, roll_right, -45, -45,45)
            responeDir="Roll left"
        elif (input.find("right")!=-1):
            head.roll(roll_left, roll_right, 45, -45,45)
            responeDir="Roll right"
        else:
            print("Error with dir roll")

    elif(object=="eyes"):
        if (input.find("left")!=-1):
            eye_x.adjustDC(eye_x.enddc)
            responeDir="Moving Eyes left"
        elif (input.find("right")!=-1):
            eye_x.adjustDC(eye_x.startdc)
            responeDir="Moving Eyes right"
        elif (input.find("up")!=-1):
            eye_y.adjustDC(eye_y.enddc)
            responeDir="Moving Eyes up"
        elif (input.find("down")!=-1):
            eye_y.adjustDC(eye_y.startdc)
            responeDir="Moving Eyes down"
        else:
            responeDir="Error with dir eyes"
    
    elif(object=="mouth"):
        if (input.find("open")!=-1):
            mouth.adjustDC(mouth.startdc)
            responeDir="Opening Mouth"
        elif (input.find("close")!=-1):
            mouth.adjustDC(mouth.enddc)
            responeDir="Closing Mouth"
        elif (input.find("shut")!=-1):
            responeDir="I will not"  #Bei Kommando "Shut up" nicht reagieren

        else:
            responeDir="Error with dir mouth"

    else:
        responeDir="Supplied False/Unkown Object"

    return responeDir

def createResponse(input):
    if (input.find("head")!=-1):
        response=getDirection(input, "head")

    elif (input.find("eyes")!=-1 or input.find("eye")!=-1):
        response=getDirection(input, "eyes")
    
    elif (input.find("roll")!=-1):
        response=getDirection(input, "roll")

    elif (input.find("mouth")!=-1):
        response=getDirection(input, "mouth")

    '''elif (input.find("camera")!=-1):
        if (input.find("start")!=-1):
            response="redirect camerapage"
        elif(input.find("take")!=-1 and input.find("picture")!=-1):
            response="Take a picture"''' #Work in Progress, Kamera-funktionen sollen irgendwann auch zugänglich werden

    else:
        response="Unkwon Command"

    return response

#################################################################################################################
#Webserver aufsetzen
webServerObject = Flask(__name__) #__name__ = Laufzeitvariabele die sich stets ändert, hier ist sie das aktuelle Arbeitsverzeichnis

@webServerObject.route('/<file>', methods=['GET'])                                   #@ --> Dekorator; .route --> funktion die beim aufruf einer in der klammer spezifierten Seite aufgerufen wird; '/<file>' --> alle möglichen pfade werden von dieser funktion angenommen, variable file enthält den namen der angefragten resource
def requestProcessor(file):                                                         # def X(PARAMETER): --> Funktiondeklaration; weshalb nach @ jetzt def? --> Dekorator
    if file=="VS":                                                        #sonderfall URL "VS" verarbeiten
        createDefaultPicture()                                                      # mit OpenCV ein erstes Bild, für spätere Operationen, aufnehmen. Global in Variable "default" verfügbar
        return Response(stream(),mimetype='multipart/x-mixed-replace; boundary=grenze')
    else:
        for f in os.listdir(os.getcwd()+'/html/'):
            if file==f:
                return send_from_directory("html", file)
        return redirect("http://192.168.0.1/index.html")

@webServerObject.route('/')                                         #sonderfall bei URL http://IP/
def leer():
    return send_from_directory("html", "index.html")                #

@webServerObject.route('/formloader', methods=['POST'])
def majorProcessor():
    formData = request.form['data']
    servo, deg, degmin, degmax = formData.split(":")
    servoToUpdate=dictionary[servo]
    if servo=="Roll":
        head.roll(servoToUpdate[0], servoToUpdate[1], int(deg), int(degmin), int(degmax))
    else:
        servoToUpdate.writeDegFromServer(int(degmin),int(degmax),int(deg))
    return '', 204

@webServerObject.route('/startrecording')                       #bei Aufruf, Audio vom Mikrofon aufnehmen
def sox_recorder():
    print("start recording")
    os.popen("sox\sox -v 1.5 -q -t waveaudio -c1 -d temp.flac") #os.popen --> dont wait for exit
    return '', 204

@webServerObject.route('/stoprecording')                        #bei Aufruf, Aufnahme stoppen, Sprache in Text umwandeln, aus diesem Text Aufgabenstellung interpretieren
def speechprocesser():
    print("stop recording")
    os.system("pkill sox")                     #os.system --> wait for exit #windows? os.system("taskkill /IM sox.exe /F /T")
    INtext=STT()                                                #Spracherkennungsfunktion durchführen, Rückgabewert ist der gesprochene Text
    OUTtext=createResponse(INtext)                              #Mithilfe des gesprochenen Textes eine Antwort kreeiren und gleichzeitig Servos ansteuern
    return jsonify(intext=INtext, outtext=OUTtext)              #Sowohl gesprochener Text (Frage), als auch die Rückmeldung (Antwort) als JSON-Objekt zurückgeben.

################################################################################################################

#Bilderkennungsfunktionen
def createDefaultPicture():                         #Ziel: einmalig ein erstes Referenzbild erstellen, um später die globale Variable "default" in getFrame verwenden können zu.
    global default                                  #Variable "default" als globale variable im lokalen Namensraum der Funktion createDefaultPicture() "importieren"
    ret, frame = cameraObject.read()                #ret--> True falls Bildaufnehmen geglückt ist, Standardfall; frame--> aufgenommenes Bild, TYP ist numpy.ndarray, ein eigener arrayartiger Datentyp, der das Bild in form von bytes enthält. Bytes entsprechen Pixel des Bildes
    frame = imutils.resize(frame, width=200)        #die größe des bildes auf breite 200 pixel reduzieren, Effizienssteigerung in der Programmverarbeitung, durch kleinere Datenmengen
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  #verkleinertes bild in graustufen konvertieren
    blur = cv2.GaussianBlur(gray, (21, 21), 0)      #Graufstufen Bild unscharf machen, um Bildrauschen der Webcam zu "vertuschen" bzw. unterdrücken
    default=blur.astype("float")                    #Unscharfes,graues,verkleinertes-gesamt bild konvertieren. Datentyp bleibt numpy.ndArray, aber Pixel-byte-Werte innerhalb des Arrays intern zu Gleitkommazahlen verändert. für spätere Verarbeitung wichtig!


def getFrame():                                     #Ziel: ein AKTUELLES Bild mit Referenzbild in der globalen Variable "default" vergleichen, bewegung erkennen, bewegung umrahmen und als JPEG für Funktion gen() verfügbar machen
    global default                                  #Variable "default" als globale variable im lokalen Namensraum der Funktion createDefaultPicture() "importieren"
    _, frame = cameraObject.read()                  #aktuelles Bild in Variable frame einlesen
    frame = imutils.resize(frame, width=200)        # wieder verkleinern
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # wieder farben entfernen
    blur = cv2.GaussianBlur(gray, (21, 21), 0)      # und Unschärfe anwenden

    cv2.accumulateWeighted(blur, default, 0.25)     # WICHTIG!!!: das Referenzbild Bild wird immer wieder aktualisiert (eben mit dieser Funktion), so ist es möglich auch Lichtveränderungen als Falschalarme für Bewegung zu vermeiden! Parameter 0.25 --> das aktuelle bild wird nur mit 25% Gewichtung zum Referenzbild vereint zusammengefügt. WICHTIG ist ebenfalls dass hier der Datentyp von dem Referenzbild eine Rolle spielt, siehe Dokumentation
    imgDiff = cv2.absdiff(blur, cv2.convertScaleAbs(default))       #absolute Differenz zwischen AKTUELL AUFGENOMMENES unscharfes Bild und dem Referenzbild bilden. Das Referenzbild muss von seinem vorher (in createDefaultPicture) geänderten Datentyp kurzzeitig in eine anderes konvertiert werden (wird mit convertScaleAbs erledigt)
    thresh = cv2.threshold(imgDiff, 3, 255, cv2.THRESH_BINARY)[1]   #hier werden alle Pixel mit der vorher gebildeten Differenz verglichen, nämlich ob diese Differenz jeweils größer als 3 (Zweiter Parameter) ist, und falls ja: dann auf den wert 255 (Dritter Parameter) gesetzt, was die "Graustufe" Weiß darstell. [1]--> OpenCV Funktion threshold liefert zwei Sachen als Array zurück: nur das zweite Element (also [0],[1]) ist relevant.
    thresh2 = cv2.dilate(thresh, None, iterations=15)               #pixel in umgebung werden ebenfalls weiß, sorgt für kontrastanhebung, Iterations-parameter gibt Intensität vor.

    conts =cv2.findContours(thresh2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[1] # Prozedur zur Konturenerkennung nach dem "border following algorithm"; cv2.RETR_EXTERNAL besagt, die Funktion findContours soll eine Liste mit allen äußeren Konturen zurückgeben; cv2.CHAIN_APPROX_SIMPLE --> Optimierung der Liste durch Auslassen bestimmter Konturpunkte.
    for c in conts:                                                 #über die Liste aller gefundenen Bewegungsbereiche (Konturansammlungen) iterieren
        if (cv2.contourArea(c)>5000):                               #falls Bereich größer als 5000 Quadratpixel groß ist...
            (x,y,w,h)=cv2.boundingRect(c)                           #...bestimme die x,y-Koordinate und Breite, Höhe eines diesen Bereich umgebenden Rechtecks
            cv2.rectangle(frame, (x,y), (x+w, y+h), (0, 255, 0), 2) #zeichne dieses Rechteck über das aktuelle Farbbild "frame", Farbe des Rechtecks wird mit dem RGB Tuppel (0, 255, 0) auf Grün gesetzt
    _, jpeg = cv2.imencode('.jpg', frame)                           #codiere das Bild als .jpg
    return jpeg.tobytes()                                           #gibt das jpg binär zurück

#################################################################
#Livestream generierende Funktion
def stream():
    while True:
        frame = getFrame()
        yield (b'--grenze\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n') #damit gen funktion nicht beendet, sondern stets ein neues Bild zurück gibt, response oben verarbeitet es eigentlich als next(returned iterator object via yield in gen func)
#################################################################
#start des Webservers
cameraObject=cv2.VideoCapture(0)                #erstelle Webcam Objekt
webServerObject.run(host="0.0.0.0", port=80)    #host=0.0.0.0 bedeutet für alle Teilnehmer des Netzwerkes zugänglich
cameraObject.release()                          #nachdem Webserver beendet wurde, gebe die Kamera resource wieder frei