#!/usr/bin/env python2.7  
import RPi.GPIO as GPIO
import time

channel = 0 #GPIO-Pin

GPIO.add_event_detect(channel, GPIO.RISING)  # add rising edge detection on a channel

if GPIO.event_detected(channel):
    print('Button pressed')