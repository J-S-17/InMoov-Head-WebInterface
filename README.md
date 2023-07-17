# InMoov-Head-WebInterface

For more info, refer to the main branch

It extends the main branch, by the second school project, which was to implement a very simple Voice control via the old Google Speech API,
which is as of my understanding now deprecated. But maybe it will inspire others, and in the future i may update it to use more modern APIs.

This module also requires to succesfully setup a USB-Microphone. A simple dongle should suffice, although on my raspi zero, it led to very heavy background noise
somehow (probably because of the adapters and usb-hub).

Either refer to the indepth documentation i wrote (Dokumentation.pdf), if you can read german, otherwise
download the files, and install the following packages for python(3)...
flask, opencv
and the programm "sox" for simple audio recording, via a simple "apt-get install sox"


since i used the older working principle of flask, you should be able to simply start the project by executing
"python CSC.py"
if something is not working or you have any questions, let me know :-)

DISCLAIMER
Keep in mind this is my very first GitHub repo and even though the code is very thoroughly commented in german (because it was a school projet)
it may look a bit sluggish, because i simply wrote this via "Trial & Error". Since i am now studying Computer Science and learning about Software-Engineering and 
design-patterns, i notice, a lot of the things could have been done better and prettier. 
Anyway i hope you enjoy!
