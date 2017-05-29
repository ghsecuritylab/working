#!/usr/bin/python
import RPi.GPIO as GPIO
import time

# Zaehler-Variable, global
Counter = 0
Tic = 0

# Pinreferenz waehlen
GPIO.setmode(GPIO.BCM)

# GPIO 18 (Pin 12) als Input definieren und Pullup-Widerstand aktivieren
GPIO.setup(18, GPIO.IN, pull_up_down = GPIO.PUD_UP)

# Callback-Funktion
def Interrupt(channel):
  global Counter
  # Counter um eins erhoehen und ausgeben
  Counter = Counter + 1
  print "Counter " + str(Counter)

# Interrupt-Event hinzufuegen, steigende Flanke
#GPIO.add_event_detect(18, GPIO.RISING, callback = Interrupt, bouncetime = 250)  
GPIO.add_event_detect(18, GPIO.FALLING, callback = Interrupt, bouncetime = 250)  

# Endlosschleife, bis Strg-C gedrueckt wird
try:
  while True:
    # nix Sinnvolles tun
    Tic = Tic + 1
    print "Tic %d" % Tic
    time.sleep(1)
except KeyboardInterrupt:
  GPIO.cleanup()
  print "\nBye"
