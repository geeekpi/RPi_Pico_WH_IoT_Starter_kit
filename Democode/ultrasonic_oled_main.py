from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import framebuf
import utime


WIDTH = 128
HEIGHT = 64

i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=200000)
oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)
oled.fill(0)

trigger = Pin(3, Pin.OUT)
echo = Pin(2, Pin.IN)

def ultra():
    trigger.low()
    utime.sleep_us(2)
    trigger.high()
    utime.sleep_us(5)
    trigger.low()
    while echo.value() == 0:
        signaloff = utime.ticks_us()
    
    while echo.value() == 1:
        signalon = utime.ticks_us()
    
    timepassed = signalon - signaloff
    distance = (timepassed * 0.034321) / 2
    return distance
  
while True:
    distance = ultra()
    print("The distance from object is: {} cm".format(distance))
    oled.text(str(distance)+" cm", 0, 10)
    oled.show()
    utime.sleep(1)
    oled.fill(0)
    