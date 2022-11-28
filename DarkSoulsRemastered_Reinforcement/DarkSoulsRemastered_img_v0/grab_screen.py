# Done by Frannecklp

import cv2
import numpy as np
import win32gui, win32ui, win32com, win32api
import mss, mss.tools
from win32api import GetSystemMetrics
import time


class GrabScreen():
    def __init__(self):
        self.hwnd = 0
        self.scale_percent = 50
        self.x, self.y, self.og_w, self.og_h = self.process_location()
        self.res_w = 224
        self.res_h = 224
        self.dims = (224, 224)

    def process_location(self):
        def winEnumHandler(hwnd, ctx):
            if win32gui.IsWindowVisible(hwnd) and 'dark souls' in win32gui.GetWindowText(hwnd).lower():
                print(hex(hwnd), hwnd, win32gui.GetWindowText(hwnd))
                self.hwnd = hwnd

        win32gui.EnumWindows(winEnumHandler, None)

        rect = win32gui.GetWindowRect(self.hwnd)  #get location and dimensions
        name = win32gui.GetWindowText(self.hwnd)  #get name of process

        if "dark souls" in name.lower():
            x = rect[0]
            y = rect[1]
            w = rect[2] - x
            h = rect[3] - y

            print("Window %s:" % win32gui.GetWindowText(self.hwnd))
            print("\tLocation: (%d, %d)" % (x, y))
            print("\t    Size: (%d, %d)" % (w, h))

            return x, y, w, h

        else:
            print("DARK SOULS: REMASTERED not currently running")
            return 0, 0, 0, 0

    def capture(self):

        with mss.mss() as sct:
            # Part of the screen to capture
            window = {"left": self.x, "top": self.y, "width": self.og_w, "height": self.og_h}

            img = np.array(sct.grab(window))
            #print(img.shape)

            #img = cv2.cvtColor(np.array(img), cv2.COLOR_BGRA2GRAY) #CHECK
            cropped = img[20:self.og_h-10, 87:self.og_w-88]
            #print(cropped.shape)

            self.dims = (self.res_w, self.res_h)

            # resize image
            resized = cv2.resize(cropped, self.dims, interpolation=cv2.INTER_AREA)
            #print(resized.shape)
            #print()

        return resized


