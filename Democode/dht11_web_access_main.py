from machine import Pin
from dht import DHT11 
import utime  
import socket
import network
import machine


ssid = 'HUAWEI-B4NKSR'
passwd = 'stm32f429'

DHTPin = Pin(3)

def connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, passwd)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        utime.sleep(1)
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    return ip

def open_socket(ip):
    address = (ip, 80)
    connection = socket.socket()
    connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    connection.bind(address)
    connection.listen(1)
    return connection

def webpage(reading):
    html = f"""
            <!DOCTYPE html>
            <html>
            <head>
            <title>Pico w Temperature and hummidity station</title>
            <meta http-equiv="refresh" content="10">
            </head>
            <body>
            <p>{reading}</p>
            </body>
            </html>
            """
    return str(html)


def serve(connection):
    while connection:
        utime.sleep(1)
        sensor = DHT11(DHTPin)
    
        sensor.measure()
        t = sensor.temperature()
        h = sensor.humidity()
    
        reading = 'Temperature: ' + str(t) + '. Humidity: ' + str(h) + '.'
        client = connection.accept()[0]
        request = client.recv(1024)
        request = str(request)
        html = webpage(reading)
        client.send(html)
        client.close()


ip = connect()
connection = open_socket(ip)

while True:
    serve(connection)
 