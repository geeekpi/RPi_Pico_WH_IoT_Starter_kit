from machine import Pin
import network
import socket
import utime
import machine


PIR = Pin(15, Pin.IN, Pin.PULL_UP)

SSID = 'HUAWEI-B4NKSR'
PASS = 'stm32f429'

def connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASS)
    while wlan.isconnected() == False:
        print("waiting for connection...")
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
    print(f'Binding to 80 port on {ip}')
    return connection

def webpage(reading):
    html = f"""
            <!DOCTYPE html>
            <html>
            <head>
            <title> Pico W web motion detect system</title>
            <meta http-equiv="refresh" content="2">
            </head>
            <body>
            <p>{reading}</p>
            </body>
            </html>
            """
    return str(html)

def serve(connection):
    while True:
        if PIR.value() == 0:
            reading = "There is no motion detected...."
        else:
            reading = 'Alarm! Motion detected, please check the fence and call 911...'
        
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
    utime.sleep(3)
    machine.reset()
        
    

 
    
    