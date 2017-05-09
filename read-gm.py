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
import cv2
import numpy as np
import pandas as pd
import os

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
prefix = "gmro"

## Colours to search for
farben = ("rot", "gruen", "weiss")
farbraum = [([0, 0, 192], [0,0,255]), ([32,180,0], [80,202,132]), ([255,255,255], [255,255,255])]

## Do the screenshot
def mapsc(url, outfile, exec_path = phjspath, des_cap = dcap):
    driver = webdriver.PhantomJS(executable_path=exec_path, desired_capabilities=des_cap)
    driver.set_window_size(1280, 800)
    driver.get(url)
    driver.implicitly_wait(3)
    time.sleep(2)
    driver.save_screenshot(outfile)


## Calculate frequency of coloured pixel and numeric matrix with locations
## Write to CSV Files
def create_tensor(imgfile, colors, colorspace, csv_count, csv_coord):
    d = dict(zip(colors, colorspace))
    df = pd.DataFrame({'value':[], 'Frequency':[], 'Datum':[], 'Zeit':[]})
    dfc = pd.DataFrame({'lon':[], 'lat':[], 'Datum':[], 'Zeit':[], 'Farbe':[]})
    i = imgfile
    spcnt = len(i.split("/")) - 1
    img = cv2.imread(i, 1)
    print("Processing ", i)
    dt = i.split("/")[spcnt][5:13]
    zt = i.split("/")[spcnt][13:17]
    for f in colors:
        fr = d[f]
        try:
            mask = cv2.inRange(img, np.array(fr[0]), np.array(fr[1]))
            u, c = np.unique(mask, return_counts = True)
            freq = np.asarray((u, c)).T
            freq_df = pd.DataFrame(freq, index = ['black', f], columns = ['value', 'Frequency'])
            freq_df['Datum'] = dt
            freq_df['Zeit'] = zt
            df = df.append(freq_df)
            x = mask.nonzero()
            coord_dfc = pd.DataFrame({'lon':x[0], 'lat':x[1], 'Datum':dt, 'Zeit':zt, 'Farbe':f})
            dfc = dfc.append(coord_dfc)
        except:
            print("File " + str(i) + " not processed.")
            pass
    df.to_csv(csv_count, mode = 'a')
    dfc.to_csv(csv_coord, mode = 'a')


### Execution
# Name of file
fn = pfad + prefix + "-" + st + ".png"

mapsc(url = url, outfile = fn)
create_tensor(fn, colors = farben, colorspace = farbraum, csv_count = pfad + prefix + "-count.csv", csv_coord = pfad + prefix + "-coord.csv")
