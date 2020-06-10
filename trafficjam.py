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
outfile_path = '/home/dolicd/Downloads/'
driver_path = '/usr/bin/chromedriver'
browser_path = '/usr/bin/google-chrome'
url = 'https://www.google.de/maps/@47.8554527,12.1209407,14.25z/data=!5m1!1e1'
naming_prefix = "gmro"

## Timestamp has to be invoked in each new process
initial_timestamp = datetime.datetime.fromtimestamp(
    time.time()).strftime('%Y%m%d%H%M%S')
## Image file name (to be created)
imgnm = outfile_path + naming_prefix + "-" + initial_timestamp + ".png"


## Colours to search for
## should be given fixed, no need to be changed 
col_defs = ("red", "green", "white")
col_space = [([0, 0, 192], [0, 0, 255]), ([32, 180, 0], [80, 202, 132]),
             ([255, 255, 255], [255, 255, 255])]

## Do the screenshot
## Options for selenium: also to be moved to config file?


## Method get screenshot of trafficmap:
def get_trafficmap(url,
                   outfile=imgnm,
                   driver_path=driver_path,
                   browser_path=browser_path):
    if not url.startswith('http'):
        raise Exception('URLs need to start with "http"')

    chrome_options = Options()
    #chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")  
    chrome_options.add_argument("--window-size=1280,800")
    #chrome_options.binary_location = driver_path
    #os.environ["webdriver.chrome.driver"] = browser_path

    driver = webdriver.Chrome(
        executable_path=driver_path,
        options=chrome_options
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
    dt = initial_timestamp[0:8]   # Extract date
    zt = initial_timestamp[8:]  # Extract time
    for f in colors:
        fr = d[f]
        try:
            # create mask for color range per color 
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
get_trafficmap(url=url)
create_tensor(imgnm,
              colors=col_defs,
              colorspace=col_space,
              csv_count=outfile_path + naming_prefix + "-count.csv",
              csv_coord=outfile_path + naming_prefix + "-coord.csv")
