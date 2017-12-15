from __future__ import print_function
import httplib2
import os
from multiprocessing import Process, Pipe 
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import numpy as np
import cv2
import datetime
import os
import time
#from mpuProcess import read_word_2c 
import smbus
import math

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/drive.file'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Drive API Python Quickstart'



def videoRecording(parent_conn):
    cap = cv2.VideoCapture(1)
    fps = 60.0
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    count = 0
    nametag = ["",""]
    while True:
        if cap.isOpened():
            print('camera is opened')
        else:
            cap.release()
            time.sleep(5)
            cap = cv2.VideoCapture(1)
        start_time = time.time()
        print(start_time)
        dt = str(datetime.datetime.now())
        global newname
        newname = 'DVR_'+dt+'.avi'    
        out = cv2.VideoWriter(newname, fourcc, fps, (640,480))
        while(cap.isOpened()):
            
            ret, frame = cap.read()
            if ret==True:
                frame = cv2.flip(frame,0)
        # write the flipped frame
                out.write(frame)
                elapsed_time = time.time() - start_time
		flag = parent_conn.recv()
                print("flag:%s" % (flag))
                #cv2.imshow('frame',frame)
                if int(elapsed_time) > 15:
	            #print(count)
		    count +=1
		    break
                    
                if count == 1:
		    if nametag[1][0:3] == "DVR":
		    	os.remove(nametag[1])     
                   
                if count == 0:
                    if nametag[0][0:3] == "DVR":
                        os.remove(nametag[0])

                nametag[count] = newname		    

                if flag == 1:
                    if nametag[0][0:3] == "DVR":
                        upload(nametag[0])
                    if nametag[1][0:3] == "DVR":
                        upload(nametag[1])
       		   
		if count == 2:
		    count = 0
 
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                
            else:
                break
		
		
# Release everything if job is finished
    cap.release()
    out.release()
    cv2.destroyAllWindows()

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'drive-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def upload(newname):
    """Shows basic usage of the Google Drive API.

    Creates a Google Drive API service object and outputs the names and IDs
    for up to 10 files.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)
    FILES = (
        (newname,None),
        #('hello.txt','application/vnd.google-apps.document'),
    )

    for filename, mimeType in FILES:
        metadata = {'name': filename}
        if mimeType:
            metadata['mimeType'] = mimeType
        res = service.files().create(body=metadata, media_body=filename).execute()
        if res:
            print('uploaded "%s" (%s)' % (filename, res['mimeType']))

def read_word(adr):
    high = bus.read_byte_data(address, adr)
    low = bus.read_byte_data(address, adr+1)
    val = (high << 8) + low
    return val

def read_word_2c(adr):
    val = read_word(adr)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val

def mpu(child_conn):
    global bus 
    bus = smbus.SMBus(1) # or bus = smbus.SMBus(1) for Revision 2 boards
    global address
    address = 0x68       # This is the address value read via the i2cdetect command
    power_mgmt_1 = 0x6b

# Now wake the 6050 up as it starts in sleep mode
    bus.write_byte_data(address, power_mgmt_1, 0)

    while True:
        time.sleep(0.1)
        gyro_xout = read_word_2c(0x43)
        accel_xout = read_word_2c(0x3b)
        accel_xout_scaled = accel_xout / 16384.0
        #gyro_yout = mpuProcess.read_word_2c(0x45)
        #gyro_zout = mpuProcess.read_word_2c(0x47)

        if abs(gyro_xout/131) >= 20:
            fg = 1
            
        if accel_xout <= -10:
            fg = 1
            
        else:
            fg = 0
  
        child_conn.send(fg)
        print("fg:%s" % (fg))
        time.sleep(0.5)

    
            
if __name__ == "__main__":
    parent_conn, child_conn = Pipe()
    p1 = Process(target=videoRecording, args=(parent_conn,))
    p2 = Process(target=mpu, args=(child_conn,))
    p1.start()
    p2.start()
    
