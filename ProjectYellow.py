#!/usr/bin/env python3
# Respond to keyboard/remote and light leds in response
import RPi.GPIO as GPIO
import time
import signal
from xbox360controller import Xbox360Controller 

PIN_Port = 26
PIN_StarBoard = 16
PIN_verticle = 21

PIN_in1 = 13
PIN_in2 = 19
PIN_in3 = 17
PIN_in4 = 4

DIVE_THRESHOLD = -0.2			

def dispatchCommand(command):
	print ('Command {0}'.format(command))
	
def on_button_pressed(button):
	dispatchCommand('Button {0} was pressed'.format(button.name))
	if button.name == 'button_mode': 
		raise SystemExit('Mode Button Pressed')
		
	if button.name == 'button_b': 
		GPIO.output(PIN_Port, GPIO.HIGH)
	if button.name == 'button_x': 
		GPIO.output(PIN_StarBoard, GPIO.HIGH)
	if button.name == 'button_a': 
		GPIO.output(PIN_verticle, GPIO.HIGH)
		
	if button.name == 'button_trigger_l':
		controller.set_led(Xbox360Controller.LED_BOTTOM_LEFT_BLINK_ON)
	if button.name == 'button_trigger_r':
		controller.set_led(Xbox360Controller.LED_BOTTOM_RIGHT_BLINK_ON)
		
def on_button_released(button):
	dispatchCommand('Button {0} was released'.format(button.name))
	if button.name == 'button_mode': 
		raise SystemExit('Mode Button Pressed')

	if button.name == 'button_b': 
		GPIO.output(PIN_Port, GPIO.LOW)
	if button.name == 'button_x': 
		GPIO.output(PIN_StarBoard, GPIO.LOW)
	if button.name == 'button_a': 
		GPIO.output(PIN_verticle, GPIO.LOW)

	if button.name == 'button_trigger_l':
		controller.set_led(Xbox360Controller.LED_OFF)
	if button.name == 'button_trigger_r':
		controller.set_led(Xbox360Controller.LED_OFF)

def on_trigger_move(raxis):
	dispatchCommand('Axis {0} moved to {1}'.format(raxis.name, raxis.value))
	if raxis.name == 'trigger_r' and raxis.value > 0:
		controller.set_led(Xbox360Controller.LED_TOP_RIGHT_ON)
		#~ GPIO.output(PIN_StarBoard, GPIO.HIGH)
		portled.start(round(raxis.value * 100))
		motorAFwd.start(round(raxis.value * 100))

	if raxis.name == 'trigger_r' and raxis.value == 0:
		controller.set_led(Xbox360Controller.LED_OFF)
		#~ GPIO.output(PIN_StarBoard, GPIO.LOW)
		portled.start(round(raxis.value * 100))
		#~ motorAFwd.start(round(raxis.value * 100))
		print ('STOP')
		motorAFwd.stop()
	
	if raxis.name == 'trigger_l' and raxis.value > 0:
		controller.set_led(Xbox360Controller.LED_TOP_LEFT_ON)
		#~ GPIO.output(PIN_Port, GPIO.HIGH)
		starboardled.start(round(raxis.value * 100))
		motorBFwd.start(round(raxis.value * 100))


	if raxis.name == 'trigger_l' and raxis.value == 0:
		controller.set_led(Xbox360Controller.LED_OFF)
		#~ GPIO.output(PIN_Port, GPIO.LOW)
		motorBFwd.start(round(raxis.value * 100))
		starboardled.start(round(raxis.value * 100))		

def on_axis_moved(axis):
	dispatchCommand('Axis {0} moved to {1} {2}'.format(axis.name, axis.x , axis.y))
	if axis.name == 'axis_l' and axis.y < DIVE_THRESHOLD:
		# dive! (turn on dive led)
		GPIO.output(PIN_verticle, GPIO.HIGH)
	if axis.name == 'axis_l' and axis.y >= DIVE_THRESHOLD:
		# close to center (turn off dive led)
		GPIO.output(PIN_verticle, GPIO.LOW)
try:
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(PIN_StarBoard, GPIO.OUT)
	GPIO.setup(PIN_Port, GPIO.OUT)
	GPIO.setup(PIN_verticle, GPIO.OUT)
	GPIO.setup(PIN_in1, GPIO.OUT)
	GPIO.setup(PIN_in2, GPIO.OUT)
	GPIO.setup(PIN_in3, GPIO.OUT)
	GPIO.setup(PIN_in4, GPIO.OUT)

	portled = GPIO.PWM(PIN_StarBoard, 100)      
	starboardled = GPIO.PWM(PIN_Port, 100) 

	motorAFwd = GPIO.PWM(PIN_in1, 100)
	motorABack = GPIO.PWM(PIN_in2, 100)
	motorBFwd = GPIO.PWM(PIN_in3, 100)
	motorBBack = GPIO.PWM(PIN_in4, 100)

	

	#~ GPIO.output(PIN_StarBoard, True)
	#~ GPIO.output(PIN_Port, True)
	GPIO.output(PIN_verticle, True)
	time.sleep(1)

	portled.start(10)
	starboardled.start(10)
	time.sleep(2)
		
	GPIO.output(PIN_StarBoard, False)
	GPIO.output(PIN_Port, False)
	GPIO.output(PIN_verticle, False)
	portled.start(0)
	starboardled.start(0)

	#~ Xbox360Controller(0, axis_threshold=0.2)
	with Xbox360Controller(0, axis_threshold=0.0) as controller:
		#~ controller.set_rumble(1, 1, 1000)
		controller.set_led(Xbox360Controller.LED_ROTATE)
		time.sleep(1)
		controller.set_led(Xbox360Controller.LED_OFF)
		# Button events
		controller.button_a.when_pressed = on_button_pressed
		controller.button_a.when_released = on_button_released
		controller.button_b.when_pressed = on_button_pressed
		controller.button_b.when_released = on_button_released
		controller.button_x.when_pressed = on_button_pressed
		controller.button_x.when_released = on_button_released
		controller.button_y.when_pressed = on_button_pressed
		controller.button_y.when_released = on_button_released

		controller.button_trigger_l.when_pressed = on_button_pressed
		controller.button_trigger_l.when_released = on_button_released
		controller.button_trigger_r.when_pressed = on_button_pressed
		controller.button_trigger_r.when_released = on_button_released
		
		controller.button_select.when_pressed = on_button_pressed
		controller.button_start.when_pressed = on_button_pressed
		controller.button_mode.when_pressed = on_button_pressed
		
		# Handling trigger use for left and right motors
		controller.trigger_l.when_moved = on_trigger_move
		controller.trigger_r.when_moved = on_trigger_move
		
		# useing the hat  
		controller.hat.when_moved = on_axis_moved
				
		# Left and right axis move event
		controller.axis_l.when_moved = on_axis_moved
		controller.axis_r.when_moved = on_axis_moved
		print ('Start signal pause')
		signal.pause()

except SystemExit:
	pass
	
except KeyboardInterrupt:
	pass
print ('Start GPIO Cleanup')
GPIO.cleanup()
