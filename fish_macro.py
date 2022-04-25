import os
import win32com.client
import cv2
import time
import random
import numpy as np
import pyautogui
# from PIL import ImageGrab

#!-----------global variable--------------!#
max_fish_cast = 999                                 # max number of fishing rod
keystroke = "e"                                     # keystroke of fishing
center = (1080//2, 1920//2)                         # half of rendering resolution of the game
# render_res = (1080, 1920)                         # rendering resolution of the game
halfwindowsize = (200//2, 200//2)                   # caputre window size for each frame
low_H, high_H =   3,  33                            # min & max threshold of Hue 
low_S, high_S =  50, 170                            # min & max threshold of Saturation
low_V, high_V = 215, 255                            # min & max threshold of lightness
precision = 0.65                                    # the higher the precision is, the harder for the detection
path = "{}/..".format(os.path.realpath(__file__))   # directory of contianing folder 
#!-----------global variable--------------!#

def capture():
    return np.array(pyautogui.screenshot())
    # img_rgb = ImageGrab.grab()
    # return np.array(img_rgb.getdata(),dtype='uint8')\
    #             .reshape((img_rgb.size[1],img_rgb.size[0],3))

def match(feature, center, alpha:float=0.65) -> bool:
    # screen shoot and crop frame only at the center 
    img_rgb = capture()
    crop_img = img_rgb[center[0]-halfwindowsize[1]: center[0]+halfwindowsize[1], 
                       center[1]-halfwindowsize[0]: center[1]+halfwindowsize[0]]

    # thresholding
    frame_HSV = cv2.cvtColor(crop_img, cv2.COLOR_RGB2HSV)
    frame_threshold = cv2.inRange(frame_HSV, (low_H, low_S, low_V), (high_H, high_S, high_V))

    pattern = feature.copy()
    pattern.shape[::-1]

    # matching
    res = cv2.matchTemplate(frame_threshold, pattern, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    # cv2.imwrite("{}/debug/iamge{} {}.png".format(path, time.time(), max_val), frame_threshold) # debug

    return max_val > alpha

def main():
    shell = win32com.client.Dispatch("WScript.Shell")   # shell to send keystroke

    # load pattern, thresholding
    pattern = cv2.cvtColor(cv2.imread("{}/fishcaught.png".format(path),1), cv2.COLOR_BGR2HSV)
    pattern = cv2.inRange(pattern, (low_H, low_S, low_V), (high_H, high_S, high_V))
    # cv2.imwrite("{}/debug/image{}.png".format(path, time.time()), pattern) # debug

    # im = cv2.cvtColor(capture(), cv2.COLOR_BGR2GRAY)
    # center = tuple(c//4*3//2 for c in im.shape) 
    print("center  {}".format(center))
    print("Running...")

    caught_fish = 0
    timeout_sec = 34
    time_start = time.time()
    timeout = lambda curr: curr > timeout_start + timeout_sec

    for cast in range(max_fish_cast):
        timeout_start = time.time()
        found = False

        while not found and not timeout(time.time()):
            found = match(pattern, center)

        # pull if success, or recast if timeout
        shell.SendKeys(keystroke)

        # on success, wait for wait for pulling animation, and recast
        if found and cast < max_fish_cast - 1:
            caught_fish += 1
            # print("caught {}".format(caught_fish))     # debug
            time.sleep(6 + random.randint(15, 20) / 10)
            shell.SendKeys(keystroke)


    print("It took {} minutes to cast {} fishing."
          .format(round((time.time() - time_start) / 60), cast+1))

if __name__ == "__main__":
    main()