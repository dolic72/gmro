#!/usr/local/bin/python3.5
###############################################################
## Get Screenshots from Google Maps
## 
## To use library selenium you have to install 
## PhantomJS (http://phantomjs.org/download.html)
##
## Point to the installation Path of PhantomJS with
## Configurationvariable phjspath
## The mimicked Webbrowser can be configurent with the 
## User Agent settings in dcap.
## pfad und st create the name for the image files
## to save.
## The URL to use for Screenshots can be given to 
## parameter url.
###############################################################
import time
import datetime
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.userAgent"] = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/53 "
    "(KHTML, like Gecko) Chrome/15.0.87"
)

## Configuration
pfad = '/home/dolic/gmro/'
phjspath = '/opt/phantomjs/phantomjs-2.1.1-linux-x86_64/bin/phantomjs'
url = 'https://www.google.de/maps/@47.8554527,12.1209407,14.25z/data=!5m1!1e1'
st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d%H%M%S')

## Do the screenshot
driver = webdriver.PhantomJS(executable_path=phjspath, desired_capabilities=dcap)
driver.set_window_size(1280, 800)
driver.get(url)
driver.implicitly_wait(3)
time.sleep(2)
driver.save_screenshot(pfad + "gmro-" + st + ".png")
