import RPi.GPIO as GPIO

MAGNET_PIN = 11

def initialize_magnet():
    """Set up the GPIO pin for the electromagnet (initially OFF)."""
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(MAGNET_PIN, GPIO.OUT)
    GPIO.output(MAGNET_PIN, GPIO.LOW)

def turn_on_magnet():
    """Energize the magnet (HIGH)."""
    GPIO.output(MAGNET_PIN, GPIO.HIGH)
    print("turn on magnet")

def turn_off_magnet():
    """De-energize the magnet (LOW)."""
    GPIO.output(MAGNET_PIN, GPIO.LOW)
    print("turn off magnet")

def cleanup_magnet():
    """Release GPIO resources when the program exits."""
    GPIO.cleanup()
