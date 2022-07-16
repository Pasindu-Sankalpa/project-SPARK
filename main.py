import gesture
import pwm
import mediapipe as mp
import cv2 as cv
import threading
import time
import RPi.GPIO as IO
from rpi_lcd import LCD

# Define the action parameters
lcd_connected = False
show_capture = False

if lcd_connected: lcd = LCD()
else: lcd = None

# setting up the model
mpHands = mp.solutions.hands
model = mpHands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)

# setting up the GPIO
lines = pwm.set_GPIO()
stopThread = [False for _ in range(len(lines))]
line0 = threading.Thread(target=pwm.controller, args=(lines[0], 0, lambda : stopThread[0]))
line1 = threading.Thread(target=pwm.controller, args=(lines[1], 0, lambda : stopThread[1]))
line2 = threading.Thread(target=pwm.controller, args=(lines[2], 0, lambda : stopThread[2]))
line3 = threading.Thread(target=pwm.controller, args=(lines[3], 0, lambda : stopThread[3]))

if __name__ == "__main__":
    while True:
        try:    
            cam = cv.VideoCapture(0)
            ret, line, Control_val = gesture.get_signal(cam, model, show_capture, lcd_connected, lcd)
            cam.release()
            if ret:
                if line == 1:
                    stopThread[0] = True
                    time.sleep(2)
                    stopThread[0] = False
                    line0 = threading.Thread(target=pwm.controller, args=(lines[0], Control_val, lambda : stopThread[0]))
                    line0.start()
                elif line == 2:
                    stopThread[1] = True
                    time.sleep(2)
                    stopThread[1] = False
                    line1 = threading.Thread(target=pwm.controller, args=(lines[1], Control_val, lambda : stopThread[1]))
                    line1.start()
                elif line == 3:
                    stopThread[2] = True
                    time.sleep(2)
                    stopThread[2] = False
                    line2 = threading.Thread(target=pwm.controller, args=(lines[2], Control_val, lambda : stopThread[2]))
                    line2.start()
                elif line == 4:
                    stopThread[3] = True
                    time.sleep(2)
                    stopThread[3] = False
                    line3 = threading.Thread(target=pwm.controller, args=(lines[3], Control_val, lambda : stopThread[3]))
                    line3.start()
                
                time.sleep(1.5)
        except:
            for i in range(len(lines)):
                lines[i].ChangeDutyCycle(0)
            print("Process terminated by admin")
            break
    
        
