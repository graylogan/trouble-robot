#!/usr/bin/env python3

from serial import serial_for_url
import time

def run():
    arduino = serial_for_url("rfc2217://localhost:4000")
    try:
        while True:
            ts = time.strftime("%Y-%m-%d %H:%M:%S")
            arduino.write((ts + "\n").encode())
            resp = arduino.readline()
            print(resp.decode(errors="replace").rstrip())
            time.sleep(3)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    run()
