import machine
import time

pwm = machine.PWM(machine.Pin(13), freq=50)
current_angle = [90]

def set_servo_angle(angle):
    pulse_width = int((angle / 180.0) * 1000 + 1000)
    duty = int((pulse_width * 65535) / 20000)
    pwm.duty_u16(duty)

def move_to_angle(target):
    step_size = 1
    step_delay = 0.030
    if current_angle[0] < target:
        for pos in range(current_angle[0], target + 1, step_size):
            set_servo_angle(pos)
            time.sleep(step_delay)
    elif current_angle[0] > target:
        for pos in range(current_angle[0], target - 1, -step_size):
            set_servo_angle(pos)
            time.sleep(step_delay)
    current_angle[0] = target

set_servo_angle(90)
current_angle[0] = 90

while True:
    print("Moving to 125...")
    move_to_angle(125)
    time.sleep(1)
    print("Moving to 90...")
    move_to_angle(90)
    time.sleep(1)
    print("Moving to 40...")
    move_to_angle(40)
    time.sleep(3)
