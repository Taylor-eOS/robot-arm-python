import machine
import time
import sys

SAFE_MIN = 40
SAFE_MAX = 120
pwm = machine.PWM(machine.Pin(13), freq=50)
current_angle = [90]

def set_servo_angle(angle):
    angle = int(max(0, min(180, int(round(angle)))))
    pulse_width = int((angle / 180.0) * 1000 + 1000)
    duty = int((pulse_width * 65535) / 20000)
    pwm.duty_u16(duty)
    current_angle[0] = angle

def move_to_angle(target):
    start = int(current_angle[0])
    target = int(target)
    if start == target:
        return
    step_size = 5
    step_delay = 0.05
    direction = 1 if start < target else -1
    current_pos = start
    while True:
        next_pos = current_pos + direction * step_size
        if (direction > 0 and next_pos > target) or (direction < 0 and next_pos < target):
            next_pos = target
        set_servo_angle(next_pos)
        time.sleep(step_delay)
        current_pos = next_pos
        if current_pos == target:
            break

def within_safe(angle):
    try:
        a = int(angle)
    except:
        return False
    return SAFE_MIN <= a <= SAFE_MAX

set_servo_angle(90)
print(f"Simple servo ready. Safe range {SAFE_MIN}-{SAFE_MAX} degrees.")

while True:
    try:
        line = sys.stdin.readline()
        if not line:
            time.sleep(0.02)
            continue
        line = line.strip()
        if not line:
            continue
        try:
            smooth = line.lower().startswith('s')
            angle_text = line[1:] if smooth else line
            angle = int(angle_text)
            if not within_safe(angle):
                print(f"But sir, I must politely refuse: {angle} is outside of the safe the range of {SAFE_MIN}-{SAFE_MAX}. Complain to whomever set that range, or set a better one in the ESP32 code if your servo can handle different angles.")
                continue
            if smooth:
                move_to_angle(angle)
            else:
                set_servo_angle(angle)
            print(f"At: {current_angle[0]}")
        except ValueError:
            print(f"Invalid angle: {line}")
    except Exception as e:
        print("Loop err:", e)
        time.sleep(0.1)

