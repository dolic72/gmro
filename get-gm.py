#!/usr/local/bin/python3.7
###############################################################
## Get Screenshots from Google Maps
## 
## To use library selenium you have to install 
## chromedriver and chrome as headless browser
##
## Point to the installation Path of chromedriver with
## Configurationvariable phjspath
## The mimicked Webbrowser can be configurent with the 
## User Agent settings in dcap.
## pfad und st create the name for the image files
## to save.
## The URL to use for Screenshots can be given to 
## parameter url.
###############################################################
import os
import time
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

## Configuration
pfad = '/home/dolicd/gmro/img/'
hbpath = '/usr/bin/chromedriver'
chrome_path = '/usr/bin/google-chrome'
url = 'https://www.google.de/maps/@47.8554527,12.1209407,14.25z/data=!5m1!1e1'
st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d%H%M%S')
WINDOW_SIZE = "1280, 800"

## Do the screenshot
chrome_options = Options()  
chrome_options.add_argument("--headless")  
chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
chrome_options.binary_location = chrome_path
os.environ["webdriver.chrome.driver"] = hbpath

def make_screenshot(url, output):
    if not url.startswith('http'):
        raise Exception('URLs need to start with "http"')

    driver = webdriver.Chrome(
        executable_path = hbpath,
        chrome_options = chrome_options
    )
    driver.get(url)
    driver.implicitly_wait(3)
    time.sleep(2)
    driver.save_screenshot(pfad + "gmro-" + st + ".png")
    driver.close()

make_screenshot(url, pfad)
    
