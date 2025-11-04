import serial
import sys
import time
import glob

def find_esp_port():
    ports = glob.glob('/dev/ttyUSB*') + glob.glob('/dev/ttyACM*')
    if ports:
        return sorted(ports)[-1]
    raise Exception("No ESP32 port found—check dmesg.")

def drain_responses(ser, timeout=0.4):
    end = time.time() + timeout
    while time.time() < end:
        while ser.in_waiting:
            line = ser.readline().decode('utf-8', errors='ignore').strip()
            if line:
                print(f"ESP32: {line}")
        time.sleep(0.01)

def main():
    try:
        PORT = find_esp_port()
        print(f"Using port: {PORT}")
        ser = serial.Serial(PORT, 115200, timeout=0.1)
        ser.dtr = False
        ser.rts = False
        time.sleep(0.1)
        ser.reset_input_buffer()
        drain_responses(ser, timeout=0.2)
        print("Ready. Enter angles or 'q' to quit. Prefix with 's' for smooth move.")
        while True:
            try:
                user_input = input("Angle: ").strip()
            except EOFError:
                break
            if not user_input:
                continue
            if user_input.lower() == 'q':
                break
            ser.write((user_input + '\n').encode())
            ser.flush()
            time.sleep(0.05)
            drain_responses(ser, timeout=0.2)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'ser' in locals():
            ser.close()

if __name__ == "__main__":
    main()

