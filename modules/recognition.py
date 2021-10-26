import pytesseract
import subprocess
import numpy as np
import cv2
import os
import concurrent.futures
import time

FIRST_COORDS = 574 # Y-coord of the upper-left corner of the question box
LINE_HEIGHT = 48 # Height of each question line
DISTANCE_QA = 49 # Distance from question to answer
DISTANCE_AA = 115 # Distance from answer to answer
ANSWER_HEIGHT = 58 # Height of each answer

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
    
#lines = int(input("How many lines: "))
#start_time = time.time()
#get_query(lines)
#print("FINISH:", time.time()-start_time)
