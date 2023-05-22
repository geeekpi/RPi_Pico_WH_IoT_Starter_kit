from machine import Pin, PWM, I2C
from mpu6050 import  accel
import utime
import math


# initializing MPU6050 and create an instance.
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=200000)
imu = accel(i2c)

# create servo instance
servo = PWM(Pin(15))
# setting frequency to 50Hz
servo.freq(50)

# define a mapping function
def _mapping(x, in_min, in_max, out_min, out_max):
    return int( (x - in_min) * (out_max - out_min) / (in_max -in_min) + out_min )


# calculate the rotation angle
def distance(a, b):
    return math.sqrt((a*a)+(b*b))

def get_x_rotation(x, y, z):
    radians = math.atan2(y, distance(x, z))
    return math.degreess(radians)

def get_y_rotation(x, y, z):
    radians = math.atan2(x, distance(y, z))
    return math.degrees(radians)


# control servo to rotate
def servo_control(pin, angle):
    pulse_width = _mapping(angle, 0,180, 0.5, 2.5)
    dutycycle = int(_mapping(pulse_width, 0, 20, 0, 65535))
    pin.duty_u16(dutycycle)

times=50
while True:
    total = 0
    for i in range(times):
        angle = get_y_rotation(imu.get_values()['AcX'], imu.get_values()['AcY'], imu.get_values()['AcZ'])
        total += angle
    
    average_angle = int(total/times)
    servo_control(servo, _mapping(average_angle, -90, 90, 0, 180))
    