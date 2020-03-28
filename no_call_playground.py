# importing the requests library 
import requests 
import sys
import time
import hashlib
import json

from display_helper import LCDScreen

lcd_screen = LCDScreen()

lcd_screen.print("hello\nthere", 20)