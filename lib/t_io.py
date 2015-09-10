import RPi.GPIO as GPIO
import time

# remove warning
GPIO.setwarnings(False)

# Set GPIO pins
SW = 7
LED_L = 11
LED_R = 13
# State Variable
bt_state = 0


def setup():
    #Setup GPIOS
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(SW, GPIO.IN)

    GPIO.setup(LED_L, GPIO.OUT, initial = GPIO.HIGH)
    GPIO.setup(LED_R, GPIO.OUT, initial = GPIO.HIGH)

def update():
    global bt_state
    bt_state = GPIO.input(SW)
    if bt_state == True:
        time.sleep(0.1) #avoid chuttering

def get_bt_state():
    return bt_state

def led_on():
    GPIO.output(LED_L, True)
    GPIO.output(LED_R, True)

def led_off():
    GPIO.output(LED_L, False)
    GPIO.output(LED_R, False)
