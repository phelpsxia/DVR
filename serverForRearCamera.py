from flask import Flask,jsonify
import time
import serial
import string
import pynmea2
import os
import subprocess

global latval, longval 
app = Flask(__name__)

@app.route("/")
def sendMessage():
    getLocation()
    os.system("sudo service motion restart")
    return jsonify(lat=latval,long=longval)
    
    #return message
def getLocation():
    port = "/dev/ttyAMA0" # the serial port to which the pi is connected.
 
#create a serial object
    ser = serial.Serial(port, baudrate = 9600, timeout = 0.5)
 
    while 1:
        try:
            data = ser.readline()
        except:
            print("loading") 
#wait for the serial port to churn out data
 
        if data[0:6] == '$GPGGA': # the long and lat data are always contained in the GPGGA string of the NMEA data
            msg = pynmea2.parse(data)
            print msg

#parse the latitude and print
            latval = msg.lat
            concatlat = "lat:" + str(latval)
            print concatlat

 
#parse the longitude and print
            longval = msg.lon
            concatlong = "long:"+ str(longval)
            print concatlong
    return latval, longval
           
    time.sleep(1)#wait a little before picking the next data.
    
