import numpy as np
import mediapipe as mp
import cv2 as cv
from rpi_lcd import LCD

signs = ((0, 0, 0, 0, 0), #0
         (0, 1, 0, 0, 0), #1
         (0, 1, 1, 0, 0), #2
         (1, 1, 1, 0, 0), #3
         (0, 1, 1, 1, 1), #4
         (1, 1, 1, 1, 1), #5
         (0, 1, 1, 1, 0), #6
         (0, 1, 1, 0, 1), #7
         (0, 1, 0, 1, 1), #8
         (0, 0, 1, 1, 1)) #9

def detect_gesture(y_lengths, x_lengths):
    open_or_close = []
    y_lengths = np.array(y_lengths)
    y_lengths = -(y_lengths-y_lengths[0])
    x_length = [np.abs(x_lengths[4]-x_lengths[17]), np.abs(x_lengths[5]-x_lengths[17])]
    if x_length[0] > x_length[1]: open_or_close.append(True)
    else: open_or_close.append(False)
    for i in range(1,5):
        if y_lengths[4*i+4] > 1.5*y_lengths[4*i+1]:
            open_or_close.append(True)
        else:
            open_or_close.append(False)
    for index, sign in enumerate(signs):
        if tuple(open_or_close) == sign:
            return index
    return 

def get_signal(cam, hands, show_capture, LCD_connected, lcd):    

    if LCD_connected: lcd.clear()

    print("Looking for a comand...")
    gesture_list = np.empty((1, 0))
    current_command = 0
    freeze_steps, first_command, second_command = None, None, None
    while True:
        success, img = cam.read()
        img = cv.resize(img, (320, 240))
        if show_capture:
            cv.imshow("Image", img)
            cv.waitKey(1)

        imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        results = hands.process(imgRGB)

        if results.multi_hand_landmarks:
            print("User detected")
            for i in range(30):
                success, img = cam.read()
                img = cv.resize(img, (320, 240))
                if show_capture:
                    cv.imshow("Image", img)
                    cv.waitKey(1)

                imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
                results = hands.process(imgRGB)
                
                if results.multi_hand_landmarks:
                    for handLms in results.multi_hand_landmarks:
                        y_lengths, x_lengths = [], []
                        for id, lm in enumerate(handLms.landmark):
                            h, w, c = img.shape
                            y_lengths.append(lm.y*h)
                            x_lengths.append(lm.x*w)

                    val = detect_gesture(y_lengths, x_lengths)
                    if val != None: 
                        #print(val)  # printing the signal val
                        gesture_list = np.append(gesture_list, val)

                        if not current_command and i > 5:
                            if (val - 0.75 < np.mean(gesture_list) < val + 0.75): 
                                print("Line selectd:", val)
                                string = "Line "+str(val)
                                if LCD_connected: lcd.text(string, 1)
                                first_command = val
                                current_command = True
                                freeze_steps = i
                                gesture_list = np.empty((1, 0))
                        elif current_command and i < freeze_steps+12:
                            gesture_list = np.empty((1, 0))
                        elif  current_command and i > freeze_steps+12:
                            if (val - 0.75 < np.mean(gesture_list) < val + 0.75): 
                                print("Control value selectd:", val)
                                string = "Control value "+str(val)
                                if LCD_connected: lcd.text(string, 2)
                                second_command = val
                                break
            #print("Looking cycle completed")
            return (type(first_command) == type(second_command), first_command, second_command)
     

