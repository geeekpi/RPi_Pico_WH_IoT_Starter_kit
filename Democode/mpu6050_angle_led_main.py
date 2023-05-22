from machine import I2C, Pin
from mpu6050 import accel
from ssd1306 import SSD1306_I2C
import utime
import math


WIDTH = 128
HEIGHT = 64

# Initializing OLED display
i2c_bus = I2C(0, sda=Pin(0), scl=Pin(1), freq=200000)
oled = SSD1306_I2C(WIDTH, HEIGHT, i2c_bus)
oled.fill(0)

# Initializing MPU6050
imu_bus = I2C(1, sda=Pin(2), scl=Pin(3), freq=200000)
imu = accel(imu_bus)

# mapping function
def _mapping(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * ( out_max - out_min) / (in_max - in_min) + out_min

def dist(a,b):
    return math.sqrt((a*a)+(b*b))

def get_y_rotation(x,y,z):
    radians = math.atan2(x,dist(y,z))
    return -math.degrees(radians)

def get_x_rotation(x,y,z):
    radians = math.atan2(y, dist(x, z))
    return math.degrees(radians)

while True:
    x = imu.get_values()['AcX'] / 16384.0
    y = imu.get_values()['AcY'] / 16384.0
    z = imu.get_values()['AcZ'] / 16384.0
    
    roll = get_y_rotation(x, y, z)
    pitch = get_x_rotation(x, y, z)
    
    print(roll, pitch)
    oled.text("roll: {:.3f}".format(roll), 0, 10)
    oled.text("pitch: {:.3f}".format(pitch), 0, 20)
    oled.show()
    utime.sleep(0.01)
    oled.fill(0)
    