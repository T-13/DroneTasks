import network
import socket
from machine import UART


# CONFIGURATION
AP_NAME = "PixRacer"
AP_PASS = "pixracer"
HOST = "0.0.0.0"
PORT = 14450
UART = 0
BAUDRATE = 115200


# Connect and transparently send raw data from UDP to UART
sta_if = network.WLAN(network.STA_IF)
ap_if = network.WLAN(network.AP_IF)

sta_if.active(True)
ap_if.active(False)

sta_if.connect(AP_NAME, AP_PASS)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((HOST, PORT))

uart = UART(UART, BAUDRATE)
uart.init(BAUDRATE)

while True:
    data = s.recv(1024)
    uart.write(data)
