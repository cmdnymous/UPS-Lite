#!/usr/bin/env python
import struct
import smbus
import sys
import time
import RPi.GPIO as GPIO

def readVoltage(bus):
        "This function returns as float the voltage from the Raspi UPS Hat via the provided SMBus object"
        address = 0x36
        read = bus.read_word_data(address, 0X02)
        swapped = struct.unpack("<H", struct.pack(">H", read))[0]
        voltage = swapped * 1.25 /1000/16
        return voltage

def readCapacity(bus):
        "This function returns as a float the remaining capacity of the battery connected to the Raspi UPS Hat via the provided SMBus object"
        address = 0x36
        read = bus.read_word_data(address, 0X04)
        swapped = struct.unpack("<H", struct.pack(">H", read))[0]
        capacity = swapped/256
        return capacity
 
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(4,GPIO.IN)
bus = smbus.SMBus(1)  # 0 = /dev/i2c-0 (port I2C0), 1 = /dev/i2c-1 (port I2C1)
address = 0x36 #PowerOnReset
bus.write_word_data(address, 0xfe,0x0054)
address = 0x36 #QuickStart
bus.write_word_data(address, 0x06,0x4000)

for i in range(6):
        print ("  ")
while True:
        for i in range(5):
                sys.stdout.write("\033[F") #back to previous line 
                sys.stdout.write("\033[K") #clear line 
        print ("####################")
        print ("Voltage:%5.2fV" % readVoltage(bus))
        print ("Battery:%5i%%" % readCapacity(bus))
        #if readCapacity(bus) == 100:
                #print ("Battery FULL")
        #if readCapacity(bus) < 5:
                #print ("Battery LOW")
        if (GPIO.input(4) == GPIO.HIGH):
                print ("External Power Supply Conected")
        if (GPIO.input(4) == GPIO.LOW):
                print ("No External Power Supply Conected")
        print ("####################")

        if readCapacity(bus) < 10 and (GPIO.input(4) == GPIO.LOW):
                os.system("sudo shutdown -h now")
                time.sleep(10)

        time.sleep(2)
