from machine import I2C, Pin
from machine_i2c_lcd import I2cLcd
from mpu6050 import accel
import utime
import math


# Initializing MPU6050
imu_bus = I2C(0, sda=Pin(0), scl=Pin(1), freq=200000)
imu = accel(imu_bus)


# Initializing LCD1602
i2c = I2C(1, sda=Pin(2), scl=Pin(3), freq=200000)
I2C_ADDR = i2c.scan()[0]
lcd = I2cLcd(i2c, I2C_ADDR, 2, 16)

# mapping function
def _mapping(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * ( out_max - out_min) / (in_max - in_min) + out_min

def dist(a,b):
    return math.sqrt((a*a)+(b*b))

def get_y_rotation(x,y,z):
    radians = math.atan2(x,dist(y,z))
    return -math.degrees(radians)

def get_x_roation(x,y,z):
    radians = math.atan2(y, dist(x, z))
    return math.degrees(radians)

while True:
    x ="{:.2f}".format(imu.get_values()['AcX'] / 16384.0)
    y ="{:.2f}".format(imu.get_values()['AcY'] / 16384.0)
    z ="{:.2f}".format(imu.get_values()['AcZ'] / 16384.0)
    
    gyx = "{:.2f}".format(imu.get_values()['GyX'] / 131.0)
    gyy = "{:.2f}".format(imu.get_values()['GyY'] / 131.0)
    gyz = "{:.2f}".format(imu.get_values()['GyZ'] / 131.0)
    
    temp = "{:.2f}".format(imu.get_values()['Tmp'])
    
    angle = get_y_rotation(x, y, z)
    
    
    
    
    
    lcd.move_to(0,0)
    lcd.putstr("angle:"+ angle)
    utime.sleep(0.01)