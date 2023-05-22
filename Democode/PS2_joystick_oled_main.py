from machine import Pin, I2C, ADC
from ssd1306 import SSD1306_I2C
import utime
from random import randint


WIDTH = 128
HEIGHT = 64

i2c_oled = I2C(1, sda=Pin(2), scl=Pin(3), freq=200000)
oled = SSD1306_I2C(WIDTH, HEIGHT, i2c_oled)
oled.fill(0)

vrx = ADC(0)
vry = ADC(1)
sw = Pin(0, Pin.IN, Pin.PULL_UP)

# mapping the reading from 240-65535 to  0-128, screen width
def x_map(reading):
    return int((reading - 240) * (128 - 0) / (65535 - 240) + 0) 

# mapping the reading from 240-65535 to  0-64, screen height
def y_map(reading):
    return int((reading - 240) * (64 - 0) / (65535 - 240) + 0) 


while True:
    
    cx = WIDTH / 2
    cy = HEIGHT /2
    
    read_vrx = vrx.read_u16()
    read_vry = vry.read_u16()
    
    x_rate = x_map(read_vrx) - 88.0
    y_rate = y_map(read_vry) - 44.0
    print(x_rate, y_rate)
    if (cx + x_rate) <= 0:
        rec_x = 0
    else:
        rec_x = int(cx +  x_rate)
        if rec_x >=90:
            rec_x = 128 - 45
    
    if (cy + y_rate) <= 0:
        rec_y = 0
    else:
        rec_y = int(cy +  y_rate)
        if rec_y >=64:
            rec_y = 64 - 15 - 5
# 
    if sw.value() == 0:
        utime.sleep(0.02)
        if sw.value() == 0:
            oled.fill(0)
            oled.text("What you want? ", 0 ,10)
            utime.sleep(0.5)
    
    oled.fill_rect( rec_x, rec_y, 15, 15, 1)
    oled.fill_rect( rec_x+30, rec_y, 15, 15, 1)
    oled.show()
    utime.sleep(randint(1, 3) * 0.1)
    oled.fill(0)
    oled.fill_rect( rec_x, rec_y, 13, 13, 1)
    oled.fill_rect( rec_x+30, rec_y, 13, 13, 1) 
    oled.show()
    utime.sleep(randint(1, 3) * 0.1)
    oled.fill(0)
    