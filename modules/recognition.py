from typing import Counter
import pytesseract
import subprocess
import numpy as np
import cv2
import os
import concurrent.futures
import time

MAX_QLINES = 4 # MAX number of lines that a question can have. If are more... F Willy

FIRST_COORDS = 574 # Y-coord of the upper-left corner of the question box
LINE_HEIGHT = 48 # Height of each question line
DISTANCE_QA = 49 # Distance from question to answer
DISTANCE_AA = 115 # Distance from answer to answer
ANSWER_HEIGHT = 58 # Height of each answer
WIDTH = (55,665)

# FILL THIS DICTIONARY WITH DATA OF ALL YOUR PHONES
coords = {"luigi":{"FIRST_COORDS":574, "LINE_HEIGHT":48, "DISTANCE_QA":49, "DISTANCE_AA":115, "ANSWER_HEIGHT":58, "WIDTH":(55,665)},
          "janeth":{"FIRST_COORDS":0, "LINE_HEIGHT":0, "DISTANCE_QA":0, "DISTANCE_AA":0, "ANSWER_HEIGHT":0, "WIDTH":(0,0)},
          "nicole":{"FIRST_COORDS":0, "LINE_HEIGHT":0, "DISTANCE_QA":0, "DISTANCE_AA":0, "ANSWER_HEIGHT":0, "WIDTH":(0,0)},
          "lucero":{"FIRST_COORDS":0, "LINE_HEIGHT":0, "DISTANCE_QA":0, "DISTANCE_AA":0, "ANSWER_HEIGHT":0, "WIDTH":(0,0)},
          "jaime":{"FIRST_COORDS":0, "LINE_HEIGHT":0, "DISTANCE_QA":0, "DISTANCE_AA":0, "ANSWER_HEIGHT":0}, "WIDTH":(0,0)}

path = "C:\\Program Files (x86)\\adb\\platform-tools"
os.chdir(path)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def get_screenshot():
    image_bytes = subprocess.Popen("adb shell screencap -p",
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE, shell=True).stdout.read().replace(b'\r\n', b'\n')
    return cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_GRAYSCALE)[FIRST_COORDS:,:]
    
def simple_recognize(screenshot, answ=True):
    for i in range(len(screenshot)):
        for j in range(len(screenshot[0])):
            if answ: screenshot[i][j] = 255 if screenshot[i][j] <56 else 0
            else: screenshot[i][j] = 255 if screenshot[i][j] <100 else 0
    #cv2.imshow("", screenshot)
    #cv2.waitKey(0)
    return pytesseract.image_to_string(screenshot, lang='spa').strip()

def get_query(counter):
    screenshot = get_screenshot()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_q = [executor.submit(simple_recognize, screenshot[(LINE_HEIGHT + 1) * i: LINE_HEIGHT + (LINE_HEIGHT + 1) * i, 4:-4], False) for i in range(counter)]
        future_a = [executor.submit(simple_recognize, screenshot[(LINE_HEIGHT + 1)*counter + DISTANCE_QA + DISTANCE_AA*i : (LINE_HEIGHT + 1)*counter + DISTANCE_QA + DISTANCE_AA*i + ANSWER_HEIGHT, 55:665]) for i in range(3)]
    
    q_list = [f.result() for f in future_q]
    question = " ".join(q_list)
    answers = [f.result() for f in future_a]
        
    print("\nWilly read:\nQuestion: {}\nAnswers: {}\n".format(question, answers))
    return question, answers


def calc_touch_answers(id, key):
    image_bytes = subprocess.Popen("adb -s "+id + " shell screencap -p",
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE, shell=True).stdout.read().replace(b'\r\n', b'\n')
    ss = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_GRAYSCALE)[coords[key]["FIRST_COORDS"]:,:]

    lines = None
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_q = [executor.submit(simple_recognize, ss[(coords[key]["LINE_HEIGHT"] + 1) * i: coords[key]["LINE_HEIGHT"] + (coords[key]["LINE_HEIGHT"] + 1) * i, 4:-4], False) for i in range(1,MAX_QLINES)]
        for i in range(MAX_QLINES):
            if future_q[i].result() == '':
                lines = i+1
                break
    #print(lines)
    return [(coords[key]["FIRST_COORDS"]+(coords[key]["LINE_HEIGHT"]+1)*lines + coords[key]["DISTANCE_QA"] + coords[key]["DISTANCE_AA"]*i + (coords[key]["ANSWER_HEIGHT"]//2),(coords[key]["WIDTH"][0] + coords[key]["WIDTH"][1]) // 2) for i in range(3)]
    
def touch_screen(id, coords):
    s = time.time()
    subprocess.call("adb -s "+str(id)+" shell input tap "+str(coords[0])+" "+str(coords[1]),shell=True)
    print(round(time.time() - s, 3))
    

def adbshell(command, serial=None, adbpath='adb'):
    args = [adbpath]
    if serial is not None:
        args.append('-s')
        args.append(serial)
    args.append('shell')
    args.append(command)
    return os.linesep.join(subprocess.check_output(args).split('\r\n')[0:-1])

def adbdevices(adbpath='adb'):
    return [dev.split('\t')[0] for dev in subprocess.check_output([adbpath, 'devices']).splitlines() if dev.endswith('\tdevice')]

def touchscreen_devices(serial=None, adbpath='adb'):
    return [dev.splitlines()[0].split()[-1] for dev in adbshell('getevent -il', serial, adbpath).split('add device ') if dev.find('ABS_MT_POSITION_X') > -1]

def tap(devicename, x, y, serial=None, adbpath='adb'):
    adbshell('S="sendevent {}";$S 3 57 0;$S 3 53 {};$S 3 54 {};$S 3 58 50;$S 3 50 5;$S 0 2 0;$S 0 0 0;'.format(devicename, x, y), serial, adbpath)
    adbshell('S="sendevent {}";$S 3 57 -1;$S 0 2 0;$S 0 0 0;'.format(devicename), serial, adbpath)
    serial = adbdevices()[0]
    touchdev = touchscreen_devices(serial)[0]
    #tap(touchdev, 100, 100, serial)


#lines = int(input("How many lines: "))
#start_time = time.time()
#get_query(lines)
#print("FINISH:", time.time()-start_time)
