#!/usr/local/bin/python3.7
###############################################################
## Get Screenshots from Google Maps traffic view
## Analyze the traffic jams
##
## Dubravko Dolic
###############################################################
import os
import time
import datetime
import cv2
import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Configuration
# Needs to be outsourced in a config file
outfile_path = '/home/ubuntu/images/'
driver_path = '/home/ubuntu/driver/chromedriver'
browser_path = '/usr/bin/google-chrome'
url = 'https://www.google.de/maps/@47.8554527,12.1209407,14.25z/data=!5m1!1e1'
naming_prefix = "gmro"

## Timestamp has to be invoked in each new process
initial_timestamp = datetime.datetime.fromtimestamp(
    time.time()).strftime('%Y%m%d%H%M%S')

## Colours to search for
## should be given fixed, no need to be changed 
col_defs = ("red", "green", "white")
col_space = [([0, 0, 192], [0, 0, 255]), ([32, 180, 0], [80, 202, 132]),
             ([255, 255, 255], [255, 255, 255])]

## Do the screenshot
## Options for selenium: also to be moved to config file?


## Method get screenshot of trafficmap:
def get_trafficmap(url, outfile=outfile_path + naming_prefix + "-" +
                   initial_timestamp + ".png",
                   driver_path=driver_path,
                   browser_path=browser_path):
    if not url.startswith('http'):
        raise Exception('URLs need to start with "http"')

    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")  
    chrome_options.add_argument("--window-size=1280,800")
    chrome_options.binary_location = driver_path
    os.environ["webdriver.chrome.driver"] = browser_path

    driver = webdriver.Chrome(
        executable_path=driver_path,
        chrome_options=chrome_options
    )
    driver.get(url)
    driver.implicitly_wait(3)
    time.sleep(2)
    driver.save_screenshot(outfile)
    driver.close()
    

## Calculate frequency of coloured pixel and numeric matrix with locations
## Write to CSV Files
def create_tensor(imgfile, colors, colorspace, csv_count, csv_coord):
    d = dict(zip(colors, colorspace))
    df = pd.DataFrame({'value': [], 'Frequency': [], 'Datum': [], 'Zeit': []})
    dfc = pd.DataFrame({'lon': [], 'lat': [], 'Date': [],
                        'Time': [], 'Colour': []})
    i = imgfile
    spcnt = len(i.split("/")) - 1
    img = cv2.imread(i, 1)
    print("Processing ", i)
    dt = i.split("/")[spcnt][5:13]   # Extract date
    zt = i.split("/")[spcnt][13:17]  # Extract time
    for f in colors:
        fr = d[f]
        try:
            mask = cv2.inRange(img, np.array(fr[0]), np.array(fr[1]))
            u, c = np.unique(mask, return_counts=True)
            freq = np.asarray((u, c)).T
            freq_df = pd.DataFrame(freq, index=['black', f],
                                   columns=['value', 'Frequency'])
            freq_df['Datum'] = dt
            freq_df['Zeit'] = zt
            df = df.append(freq_df)
            x = mask.nonzero()
            coord_dfc = pd.DataFrame({'lon': x[0], 'lat': x[1], 'Date': dt,
                                      'Time': zt, 'Colour': f})
            dfc = dfc.append(coord_dfc)
        except:
            print("File " + str(i) + " not processed.")
            pass
    df.to_csv(csv_count, header=False, mode='a')
    dfc.to_csv(csv_coord, header=False, mode='a')


### Execution
# Name of file
fn = pfad + prefix + "-" + st + ".png"

mapsc(url = url, outfile = fn)
create_tensor(fn, colors = farben, colorspace = farbraum, csv_count = pfad + prefix + "-count.csv", csv_coord = pfad + prefix + "-coord.csv")
