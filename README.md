# InMoov-Head-WebInterface
This project creates a WebInterface running on a Raspberry Pi (any version with wifi connectivity will work) to control head movements for the head part of the inmoov.fr Android-robot project. It extends the main branch, by the second schoo project, which was to implement a very simple Voice control via the old Google Speech API,
which is as of my understanding now deprecated. But maybe it will inspire others, and in the future i may update it to use more modern APIs.

This project was a school project, i included the documentation (in german) and presentation for it.
For understanding the software part, the presentation slides are (i think) very helpful.

First of all you need to build the head of course, for that refer to inmoov.fr.
This project consists of the actual head and the shoulder/neck part, so the head can stand by itself.
It controls six servos in total, 2 (MG996r or aquivalent) for rolling the head, 1 (HS-805BB or ...) for the pitch, 1 (HS-805BB) for the yaw, 
and two (sg90) for the eyes vertical and horizontal movement.
In one of the eyes i incooperated one USB-WebCam, i used a Hercules Twist HD, you could use any other usb webcam, but then youll need to
change the 3d-model for the eyes from the inmoov.fr website. If you want to use an original Raspberry Pi Camera, thats also cool,
there are 3d Models for that, but then you need to adjust the CSC.py code to use it, which shouldn't be that hard :-)

After connecting all the servos to the Raspbery Pi (just connect all Power and GND lanes from the servos, connect them to a powerfull power supply,
GND from the powersupply also with the Pi, and the PWM-pins of each servo to a GPIO-pin you like, don't forget to set them in the CSC.py code)
You need to setup the Raspberry.
For that either refer to the indepth documentation i wrote (Dokumentation.pdf), if you can read german, otherwise just set your Pi as a Hotspot,
download the files, and install following packages for python(3)...
flask, opencv

since i used the older working principle of flask, you should be able to simply start the project by executing
"python CSC.py"
if something is not working or you have any questions, let me know :-)

DISCLAIMER
Keep in mind this is my very first GitHub repo and even though the code is very thoroughly commented in german (because it was a school projet)
it may look a bit sluggish, because i simply wrote this via "Trial & Error". Since i am now studying Computer Science and learning about Software-Engineering and 
design-patterns, i notice, a lot of the things could have been done better and prettier. 
Anyway i hope you enjoy!
