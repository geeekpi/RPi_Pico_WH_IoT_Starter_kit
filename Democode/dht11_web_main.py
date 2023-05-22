from machine import Pin
from dht import DHT11
import network
import socket
import utime
import machine


ssid = 'HUAWEI-B4NKSR'
password = 'stm32f429'


def connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print("waiting for connecting...")
        utime.sleep(1)
    
    ip = wlan.ifconfig()[0]
    print(f'Connect to IP: {ip}')
        
    return ip 

def open_socket(ip):
    addr = (ip, 80)
    connection = socket.socket()
    connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    connection.bind(addr)
    connection.listen(1)
    print(f'binding the port 80 to {ip}')
    return connection


def webpage(reading):
    html = f"""
            <!DOCTYPE html>
            <html>
            <head>
            <title>Pico W Temperature and humidity station</title>
            <meta http-equiv="refresh" content="10">
            </head>
            <body>
            <p>{reading}</p>
            </body>
            </html>
            """
    return str(html)

def serve(connection):
    # start a web server
    
    while True:
        utime.sleep(1)
        sensor = DHT11(Pin(3))
        sensor.measure()
        t = sensor.temperature()
        h = sensor.humidity()
        reading = 'Temperature: ' + str(t) + '. Humidity: ' + str(h) + '%'
        client = connection.accept()[0]
        request = client.recv(1024)
        request = str(request)
        html = webpage(reading)
        client.send(html)
        client.close()



try:
    ip = connect()
    connection = open_socket(ip)
    serve(connection)
except KeyboardInterrupt:
    utime.sleep(5)
    machine.reset()
    
 
    