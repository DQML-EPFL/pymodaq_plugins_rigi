# -*- coding: utf-8 -*-
"""
Created on Mon Jul 28 2025

@author: dqml-lab
"""

import numpy as np
import cv2
import pyautogui
import pytesseract

class ScreenshotMaster:

    ############## My methods

    # def __init__(self, region=(50, 55, 1260, 960)) -> None:
    def __init__(self, region=(330, 90, 20, 20)) -> None:
        # Define region: (left, top, width, height)
        pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        self.region = region


    def __del__(self):
        print("Killing ScreenShotMaster")
        
    def set_region(self, region):
        self.region = region

    def start_a_grab_snap(self):
        screenshot = pyautogui.screenshot(region=self.region)
        frame = np.array(screenshot)
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

        pxls = gray.shape[0] * gray.shape[1]
        middle_pixel = gray[int(gray.shape[0]/2)][int(gray.shape[1]/2)]
        intensity = np.sum(gray) / pxls

        text = pytesseract.image_to_string(screenshot,lang='eng', config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789')
        text = int(text)

        return gray, intensity, text


