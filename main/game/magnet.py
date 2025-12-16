import RPi.GPIO as GPIO


class Magnet:
    def __init__(self, pin: int):
        """Magnet controller for a single GPIO pin.

        Parameters:
            pin: The GPIO pin number (BOARD or BCM numbering based on global mode).

        Notes:
            Best practice is to set the global GPIO mode (BOARD or BCM)
            once in your main program before creating this class.
        """
        self.pin = pin
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, GPIO.LOW)

    def on(self) -> None:
        """Energize the magnet (HIGH)."""
        GPIO.output(self.pin, GPIO.HIGH)
        print("turn on magnet")

    def off(self) -> None:
        """De-energize the magnet (LOW)."""
        GPIO.output(self.pin, GPIO.LOW)
        print("turn off magnet")


__all__ = ["Magnet"]
