#!/usr/bin/env python
# Respond to keyboard/remote and light leds in response
import RPi.GPIO as GPIO
import time

PIN_in1 = 13
PIN_in2 = 19
PIN_in3 = 17
PIN_in4 = 04

try:
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(PIN_in1, GPIO.OUT)
	GPIO.setup(PIN_in2, GPIO.OUT)
	GPIO.setup(PIN_in3, GPIO.OUT)
	GPIO.setup(PIN_in4, GPIO.OUT)

	print ("Motor B Direction one")
	motorAFwd = GPIO.PWM(PIN_in1, 100)
	motorABack = GPIO.PWM(PIN_in2, 100)
	motorBFwd = GPIO.PWM(PIN_in3, 100)
	motorBBack = GPIO.PWM(PIN_in4, 100)

	print ('start it now')
	motorBFwd.start(100) 
	motorAFwd.start(100) 
	
	time.sleep(4)
	print ('Turn it down')
	motorAFwd.start(10) 
	motorBFwd.start(50) 
	time.sleep(4)
	motorAFwd.start(0) 
	motorBFwd.start(0) 
	
	time.sleep(2)
	motorABack.start(10)
	motorBBack.start(100)

	time.sleep(5)

	motorABack.stop()
	motorBBack.stop()
	print('stopped')

	GPIO.cleanup()

except:
	KeyboardInterrupt
	GPIO.cleanup()
