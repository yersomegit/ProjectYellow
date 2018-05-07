#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  TestRelay.py
#  
#  

import RPi.GPIO as GPIO
import time

PIN_RELAY_IN1 = 5
PIN_RELAY_IN2 = 12
PIN_RELAY_IN3 = 24
PIN_RELAY_IN4 = 18

def main():
	try:
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(PIN_RELAY_IN1, GPIO.OUT)
		GPIO.setup(PIN_RELAY_IN2, GPIO.OUT)
		GPIO.setup(PIN_RELAY_IN3, GPIO.OUT)
		GPIO.setup(PIN_RELAY_IN4, GPIO.OUT)

		GPIO.output(PIN_RELAY_IN1, GPIO.HIGH)
		GPIO.output(PIN_RELAY_IN2, GPIO.HIGH)
		GPIO.output(PIN_RELAY_IN3, GPIO.HIGH)
		GPIO.output(PIN_RELAY_IN4, GPIO.HIGH)
		
		print ('Lightem'' up... ')
		GPIO.output(PIN_RELAY_IN1, GPIO.LOW)
		time.sleep(3)
		GPIO.output(PIN_RELAY_IN2, GPIO.LOW)
		time.sleep(3)
		GPIO.output(PIN_RELAY_IN3, GPIO.LOW)
		time.sleep(3)
		GPIO.output(PIN_RELAY_IN4, GPIO.LOW)
		time.sleep(3)
		print('Cleanup and exit')
		GPIO.cleanup()
	except KeyboardInterrupt:
		pass	
	return 0

if __name__ == '__main__':
	main()

