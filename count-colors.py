import cv2
import numpy as np
import pandas as pd
import os
#import multiprocessing 
#from matplotlib import pyplot as plt

# i1 = '/home/dubravko/gmro/gmro-20161107164501.png'
# i2 = '/home/dubravko/gmro/gmro-20161107050001.png'

# img1 = cv2.imread(i1, 1)
# img2 = cv2.imread(i2, 1)

# rote_balken = ([0, 0, 192], [0,0,255])

# mask = cv2.inRange(img1, np.array(rote_balken[0]), np.array(rote_balken[1]))
# #output = cv2.bitwise_and(img1, img1, mask = mask)

# #cv2.imshow("Rot", np.hstack([img1, output]))
# #cv2.waitkey(0)

# u, c = np.unique(mask, return_counts = True)
# #print(np.asarray((u, c)).T)

# freq = np.asarray((u, c)).T

# freq_df2 = pd.DataFrame(freq, index = ['black', 'red'], columns = ['value', 'Frequency'])

farben = ("rot", "gruen", "weiss")
farbraum = [([0, 0, 192], [0,0,255]), ([32,180,0], [80,202,132]), ([255,255,255], [255,255,255])]
d = dict(zip(farben, farbraum))

h = '/home/dolic/gmro/gmroproc/'
spcnt = len(h.split("/")) - 1

l = []
for f in os.listdir(h):
    if f.endswith('png'):
        l.append(h + f)

df = pd.DataFrame({'value':[], 'Frequency':[], 'Datum':[], 'Zeit':[]})
dfc = pd.DataFrame({'lon':[], 'lat':[], 'Datum':[], 'Zeit':[], 'Farbe':[]})

for i in l:
    img = cv2.imread(i, 1)
    print("Processing ", i)
    dt = i.split("/")[spcnt][5:13]
    zt = i.split("/")[spcnt][13:17]
    for f in farben:
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

df.to_csv('/home/dolic/gmro-count.csv')
dfc.to_csv('/home/dolic/gmro-coord.csv')

