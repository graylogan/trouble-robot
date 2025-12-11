import time
import serial

PLOTTER_PORT = "/dev/ttyUSB0"
PLOTTER_BAUD = 115200


def open_plotter():
    """
    Open and return a serial connection to the plotter.
    """
    print(f"[PLOTTER] Opening {PLOTTER_PORT} @ {PLOTTER_BAUD} baud")
    return serial.Serial(PLOTTER_PORT, PLOTTER_BAUD, timeout=1)


def close_plotter(ser):
    """
    Safely close the plotter serial port.
    """
    if ser is not None and ser.is_open:
# Return to (0,0) at the end
        send_grbl(ser, "G0 X0")
        time.sleep(1)
        send_grbl(ser, "G0 Y0")
        time.sleep(1)

        print("[PLOTTER] Closing serial port")
        ser.close()


def send_grbl(ser, command: str):
    """
    Send one line of G-code and print GRBL's response.
    """
    line = command.strip()
    print(f"> {line}")

    if ser is None or not ser.is_open:
        raise RuntimeError("send_grbl called with a closed or None serial port")

    ser.write((line + "\n").encode("ascii"))

    # Read lines until we see 'ok' or 'error'
    while True:
        response = ser.readline().decode("ascii", errors="ignore").strip()
        if response:
            print("GRBL:", response)
            if response == "ok" or response.startswith("error"):
                break


def report_position(ser, label: str = "Position"):
    """
    Ask GRBL for its current reported machine status/position.
    """
    print(f"\n--- {label} ---")

    if ser is None or not ser.is_open:
        raise RuntimeError("report_position called with a closed or None serial port")

    ser.write(b"?")
    time.sleep(0.2)   # wait for GRBL to respond
    resp = ser.read_all().decode("ascii", errors="ignore")
    print(resp.strip())


def plotter_initialization(ser):
    """
    Wake up GRBL, unlock, and set coordinate mode.

    IMPORTANT: This function does NOT close the serial port.
    """
    if ser is None or not ser.is_open:
        raise RuntimeError("plotter_initialization called with a closed or None serial port")

    # Wake up GRBL
    ser.write(b"\r\n\r\n")
    time.sleep(2)
    ser.reset_input_buffer()

    # Unlock GRBL and set coordinates
    send_grbl(ser, "$X")        # unlock
    send_grbl(ser, "G92 X0 Y0") # set current pos as (0,0)
    send_grbl(ser, "G90")       # absolute positioning
