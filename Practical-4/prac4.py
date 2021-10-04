import busio
import digitalio
import board
import threading
import time
import math
import os
import RPi.GPIO as GPIO
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

sampling = 5
start = True

def print_values_thread():

     global start_time
     global sampling
     global button
     global start

     # create the spi bus
     spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

     # create the cs (chip select)
     cs = digitalio.DigitalInOut(board.D5)

     # create the mcp object
     mcp = MCP.MCP3008(spi, cs)

     # create analog inputs channel 1&2 on pin 1&2
     chan1 = AnalogIn(mcp, MCP.P1)
     chan2 = AnalogIn(mcp, MCP.P2)

     # calculating the required values
     runtime = 0
     tempAdc = chan1.value
     tempCon = round((chan1.voltage-0.5)*100, 2)
     lghtAdc = chan2.value

     # starting the threading process
     thread = threading.Timer(sampling, print_values_thread)
     thread.daemon = True
     thread.start()

     # calculating the current runtime
     if(start):
         start_time = time.time()
         start = False

     runtime = math.floor(time.time() - start_time)

     # printing out the current values
     print(str(runtime) + " s\t\t" + str(tempAdc) + "\t\t" + str(tempCon) + " C\t\t" + str(lghtAdc))

# Button pressed
def btn_pressed():

    global sampling
    global start

    start = True

    os.system('clear')
    print("Runtime\t\tTemp Reading\tTemp\t\tLight Reading\n")

    if(sampling == 10):
        sampling = 1

    elif(sampling == 1):
        sampling = 5

    elif(sampling == 5):
        sampling = 10

    pass

  if __name__ == "__main__":

    global start_time
    start_time = time.time()

    global button
    button = digitalio.DigitalInOut(board.D6)
    button.direction = digitalio.Direction.INPUT
    button.pull = digitalio.Pull.UP

    os.system('clear')
    print("Runtime\t\tTemp Reading\tTemp\t\tLight Reading\n")

    print_values_thread()

    while True:
        if(button.value == False):
           btn_pressed()
           time.sleep(0.2)
        pass
