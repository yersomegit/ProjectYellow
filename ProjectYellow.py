#!/usr/bin/env python3
# Respond to keyboard/remote and light leds in response
import RPi.GPIO as GPIO
import json
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

PIN_B2in1 = 20
PIN_B2in2 = 25
PIN_B2in3 = 23
PIN_B2in4 = 6

PIN_RELAY_IN1 = 5
PIN_RELAY_IN2 = 12
PIN_RELAY_IN3 = 24
PIN_RELAY_IN4 = 18


REVERSE = 0
FORWARD = 1
global leftMotor
global rightMotor
global downMotor
global relay1off
global relay2off
global relay3off
global relay4off

DIVE_THRESHOLD = -0.2
class CommandSet (object):
    def __init__(self, name):
        self.name = name
        
def dispatchCommand(command):
	#~ jsonData = '{"name": "Frank", "age": 39}'
	#~ jsonToPython = json.loads(jsonData)
	#~ mycmd = CommandSet(name='YellowCmd',ctype='info')
	print ('Command {0}'.format(command))

def on_button_a_pressed(button):
	global relay4off
	dispatchCommand('Button {0} was Pressed'.format(button.name))
	relay4off = not relay4off
	relay4off = False
	GPIO.output(PIN_RELAY_IN4, GPIO.LOW)

def on_button_a_released(button): 
	global relay4off
	dispatchCommand('Button {0} was Released'.format(button.name))
	relay4off = True
	GPIO.output(PIN_RELAY_IN4, GPIO.HIGH)

def on_button_b_pressed(button):
	global relay2off
	dispatchCommand('Button {0} was released'.format(button.name))
	relay2off = not relay2off
	GPIO.output(PIN_RELAY_IN2, relay2off)

def on_button_b_released(button): pass

def on_button_x_pressed(button):
	global relay3off
	dispatchCommand('Button {0} was released'.format(button.name))
	relay3off = not relay3off
	GPIO.output(PIN_RELAY_IN3, relay3off)

def on_button_x_released(button): pass

def on_button_y_pressed(button):
	global relay4off
	dispatchCommand('Button {0} was released'.format(button.name))
	relay4off = not relay4off
	GPIO.output(PIN_RELAY_IN4, relay4off)

def on_button_y_released(button): pass

def on_mode_pressed(button):
	dispatchCommand('Button {0} was released'.format(button.name))
	print ('Button {0}'.format (button))
def on_mode_released(button): pass

def on_start_pressed(button):
	dispatchCommand('Button {0} was released'.format(button.name))

def on_select_pressed(button):
	dispatchCommand('Button {0} was released'.format(button.name))

def on_button_trigger_l_pressed (button):
	global leftMotor
	dispatchCommand('Button {0} was pressed'.format(button.name))
	motorBFwd.stop()
	leftMotor = REVERSE
	controller.set_led(Xbox360Controller.LED_BOTTOM_LEFT_BLINK_ON)

def on_button_trigger_r_pressed (button):
	global rightMotor
	dispatchCommand('Button {0} was pressed'.format(button.name))
	motorAFwd.stop()
	rightMotor = REVERSE
	controller.set_led(Xbox360Controller.LED_BOTTOM_RIGHT_BLINK_ON)


def on_button_trigger_l_released(button):
	global leftMotor
	dispatchCommand('Button {0} was released'.format(button.name))
	motorBBack.stop()
	leftMotor = FORWARD
	controller.set_led(Xbox360Controller.LED_OFF)

def on_button_trigger_r_released(button):
	global rightMotor
	dispatchCommand('Button {0} was released'.format(button.name))
	motorABack.stop()
	rightMotor = FORWARD
	controller.set_led(Xbox360Controller.LED_OFF)

def on_trigger_move(raxis):
	global leftMotor
	global rightMotor
	dispatchCommand('Axis {0} moved to {1}'.format(raxis.name, raxis.value))
	if raxis.name == 'trigger_r' and raxis.value > 0:
		controller.set_led(Xbox360Controller.LED_TOP_RIGHT_ON)
		portled.start(round(raxis.value * 100))
		print ('Right Motor {0} '.format(rightMotor))
		if (rightMotor == FORWARD):
			motorABack.stop()
			motorAFwd.start(round(raxis.value * 100))
		else: 
			motorAFwd.stop()
			motorABack.start(round(raxis.value * 100))

	if raxis.name == 'trigger_r' and raxis.value == 0:
		controller.set_led(Xbox360Controller.LED_OFF)
		portled.start(round(raxis.value * 100))
		motorAFwd.stop()
		motorABack.stop()
	
	if raxis.name == 'trigger_l' and raxis.value > 0:
		controller.set_led(Xbox360Controller.LED_TOP_LEFT_ON)
		starboardled.start(round(raxis.value * 100))
		if (leftMotor == FORWARD):
			motorBBack.stop()
			motorBFwd.start(round(raxis.value * 100))
		else:
			motorBFwd.stop()
			motorBBack.start(round(raxis.value * 100))

	if raxis.name == 'trigger_l' and raxis.value == 0:
		controller.set_led(Xbox360Controller.LED_OFF)
		motorBFwd.stop()
		starboardled.stop()		
on_trigger_l_move = on_trigger_r_move = on_trigger_move

def on_axis_moved(axis):
	dispatchCommand('Axis {0} moved to {1} {2}'.format(axis.name, axis.x , axis.y))
	if axis.name == 'axis_l' and abs(axis.y) < abs(DIVE_THRESHOLD):
		motorA2Back.stop()
		motorA2Fwd.stop()
	if axis.name == 'axis_l' and axis.y < (0 + DIVE_THRESHOLD):
		# dive! (turn on dive led)
		GPIO.output(PIN_verticle, GPIO.HIGH)
		motorA2Back.stop()
		motorA2Fwd.start(abs(round(axis.y * 100)))
	if axis.name == 'axis_l' and axis.y >= (0 - DIVE_THRESHOLD):
		# close to center (turn off dive led)
		GPIO.output(PIN_verticle, GPIO.LOW)
		motorA2Fwd.stop()
		motorA2Back.start(abs(round(axis.y * 100)))

on_axis_r_moved = on_axis_l_moved = on_hat_moved = on_axis_moved
	
try:
	GPIO.setmode(GPIO.BCM) # Pin numbering mode

# Setup LED - mainly for testing purpose
	GPIO.setup(PIN_StarBoard, GPIO.OUT)
	GPIO.setup(PIN_Port, GPIO.OUT)
	GPIO.setup(PIN_verticle, GPIO.OUT)

# Where the pins from the 298 motor controller board are connected 
# Some of these need to be PWM. Is's not clear which ones - but this seems to work  
	GPIO.setup(PIN_in1, GPIO.OUT)
	GPIO.setup(PIN_in2, GPIO.OUT)
	GPIO.setup(PIN_in3, GPIO.OUT)
	GPIO.setup(PIN_in4, GPIO.OUT)

#Second 298 Contoller pins
	GPIO.setup(PIN_B2in1, GPIO.OUT)
	GPIO.setup(PIN_B2in2, GPIO.OUT)
	GPIO.setup(PIN_B2in3, GPIO.OUT)
	GPIO.setup(PIN_B2in4, GPIO.OUT)


# These are the pins where the relay board are connected and 
# because they will remember state betwwen lets initially turn them off 
	GPIO.setup(PIN_RELAY_IN1, GPIO.OUT)
	GPIO.setup(PIN_RELAY_IN2, GPIO.OUT)
	GPIO.setup(PIN_RELAY_IN3, GPIO.OUT)
	GPIO.setup(PIN_RELAY_IN4, GPIO.OUT)
	GPIO.output(PIN_RELAY_IN1, GPIO.HIGH)
	GPIO.output(PIN_RELAY_IN2, GPIO.HIGH)
	GPIO.output(PIN_RELAY_IN3, GPIO.HIGH)
	GPIO.output(PIN_RELAY_IN4, GPIO.HIGH)

# Setup the PWN pins for the LEDs this is frequency apparently 
# not sure why this is called that since all it seems to mean 
# is that they scale from 0 to 100. Like, Percentage power! BAM!      
	portled = GPIO.PWM(PIN_StarBoard, 100)      
	starboardled = GPIO.PWM(PIN_Port, 100) 

# Setup the PWN pins for the motors. These are connected to the ESC board
	motorAFwd = GPIO.PWM(PIN_in1, 100)
	motorABack = GPIO.PWM(PIN_in2, 100)
	motorBFwd = GPIO.PWM(PIN_in3, 100)
	motorBBack = GPIO.PWM(PIN_in4, 100)

#Setup second 298 board pins only one more motor
	motorA2Fwd = GPIO.PWM(PIN_B2in1, 100)
	motorA2Back = GPIO.PWM(PIN_B2in2, 100)
# Nothing is attached to the second boards second control port 
# But we'll set it up anyways 
	motorB2Fwd = GPIO.PWM(PIN_B2in3, 100)
	motorB2Back = GPIO.PWM(PIN_B2in4, 100)

# Lets power those suckers up a little forwards and backwards 
# so we know everything is good!
	motorAFwd.start(25)
	motorBFwd.start(25)
	motorA2Fwd.start(25)
	time.sleep(.3)
	motorAFwd.stop()
	motorBFwd.stop()
	motorA2Fwd.stop()
	motorABack.stop()
	motorBBack.stop()
	motorA2Back.stop()
	motorABack.start(25)
	motorBBack.start(25)
	motorA2Back.start(25)
	time.sleep(.2)


# Initialise our rather ugly global variables 
	leftMotor = FORWARD
	rightMotor = FORWARD
	downMotor = FORWARD
	relay1off = True
	relay2off = True
	relay3off = True
	relay4off = True
	
# Ensure all motors are stopped - they dont' maintain state so
# This really isn't neccessary but what the hey! 
	motorAFwd.stop()
	motorBFwd.stop()
	motorA2Fwd.stop()

	motorABack.stop()
	motorBBack.stop()
	motorA2Back.stop()


#Flash our LEDs so that we know it's all connected
	GPIO.output(PIN_verticle, True)
	portled.start(10)
	starboardled.start(10)
	time.sleep(0.5)
		
	GPIO.output(PIN_StarBoard, False)
	GPIO.output(PIN_Port, False)
	GPIO.output(PIN_verticle, False)
	portled.start(0)
	starboardled.start(0)

	with Xbox360Controller(0, axis_threshold=0.0) as controller:
		#~ controller.set_rumble(1, 1, 1000) # This no work - it's a mystery
		controller.set_led(Xbox360Controller.LED_ROTATE)

		# Setup all the Button event handlers
		# Initially i had one handler with a bunch of conditional but 
		# I split these because maybe it's optimal (But who knows with python) 
		controller.button_a.when_pressed = on_button_a_pressed
		controller.button_a.when_released = on_button_a_released
		controller.button_b.when_pressed = on_button_b_pressed
		controller.button_b.when_released = on_button_b_released
		controller.button_x.when_pressed = on_button_x_pressed
		controller.button_x.when_released = on_button_x_released
		controller.button_y.when_pressed = on_button_y_pressed
		controller.button_y.when_released = on_button_y_released

		controller.button_select.when_pressed = on_select_pressed
		controller.button_start.when_pressed = on_start_pressed
		controller.button_mode.when_pressed = on_mode_pressed

		controller.button_trigger_l.when_pressed = on_button_trigger_l_pressed
		controller.button_trigger_l.when_released = on_button_trigger_l_released
		controller.button_trigger_r.when_pressed = on_button_trigger_r_pressed
		controller.button_trigger_r.when_released = on_button_trigger_r_released

		# Handling trigger use for left and right motors
		controller.trigger_l.when_moved = on_trigger_l_move
		controller.trigger_r.when_moved = on_trigger_r_move
		
		# useing the hat  
		controller.hat.when_moved = on_hat_moved

		# Left and right axis move event
		controller.axis_l.when_moved = on_axis_l_moved
		controller.axis_r.when_moved = on_axis_r_moved
		time.sleep(1)
		controller.set_led(Xbox360Controller.LED_OFF)
		print ('Control System Ready!')
		signal.pause() # Waits and lets all our event handlers handle events

except SystemExit:
	print ('System Exit')
	pass
except KeyboardInterrupt:
	print('Keyboard Int')
	pass
except FileNotFoundError as err:
	print ('Ensure your controller is turned on! {0}'.format(err))
#~ except Exception as err:
	#~ print ('Stuff went wrong. This may help --> {0}'.format (err))
finally:
    pass
print ('Shutting down.')
GPIO.cleanup()


