import machine
import time
import sys

SAFE_MIN = 40
SAFE_MAX = 120
pwm = machine.PWM(machine.Pin(13), freq=50)
current_angle = [90]

def set_servo_angle(angle):
    print("PWM set:", angle)
    pulse_width = int((angle / 180.0) * 1000 + 1000)
    duty = int((pulse_width * 65535) / 20000)
    pwm.duty_u16(duty)

def move_to_angle(target):
    start = current_angle[0]
    if start == target:
        print("Move start:", start, "->", target, "(no change)")
        return
    print("Move start:", start, "->", target)
    step_size = 5
    step_delay = 0.05
    direction = 1 if start < target else -1
    current_pos = start
    while True:
        next_pos = current_pos + direction * step_size
        if (direction > 0 and next_pos > target) or (direction < 0 and next_pos < target):
            next_pos = target
        set_servo_angle(next_pos)
        print("Step:", next_pos)
        time.sleep(step_delay)
        current_pos = next_pos
        if current_pos == target:
            break
    current_angle[0] = target
    print("Move done")

def within_safe(angle):
    return SAFE_MIN <= angle <= SAFE_MAX

set_servo_angle(90)
current_angle[0] = 90
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
            smooth = line.startswith('s')
            angle = int(line[1:] if smooth else line)
            if not within_safe(angle):
                print(f"Refused: {angle} outside safe range {SAFE_MIN}-{SAFE_MAX}")
                continue
            print(f"Got input: {line}")
            if smooth:
                move_to_angle(angle)
            else:
                set_servo_angle(angle)
                current_angle[0] = angle
        except ValueError:
            print(f"Invalid angle: {line}")
    except Exception as e:
        print("Loop err:", e)
        time.sleep(0.1)

