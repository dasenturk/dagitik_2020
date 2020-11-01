#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 12:35:18 2020

@author: damla
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


df = pd.read_csv("lab8_0.30-4.18-1.57.csv", names=["timeStamp", "sensor_mac", "transmitter_mac", "rssi"], header=None)


stcouple = df.groupby(["sensor_mac", "transmitter_mac"], as_index=False)["rssi"]

n=len(stcouple)


print("Minimum rssi values per <sensor_mac, transmitter_mac> couple:\n" , stcouple.min(), "\n")
print("Maximum rssi values per <sensor_mac, transmitter_mac> couple:\n", stcouple.max())

stdict = dict(stcouple.apply(list))


values = stdict.values()
values_list = list(values)
keys = stdict.keys()
keys_list = list(keys)

#cift1 = values_list[0]

for i in range (0,n):
    minrssi=min(values_list[i])
    maxrssi=max(values_list[i])
    step_array = np.arange(start=minrssi-1, stop=maxrssi+1, step=1)
    sa=values_list[i]
    for value in step_array:
        if value not in sa:
            step_array=np.delete(step_array, np.where(step_array == value))
    x=len(step_array)
    zero_array=np.zeros(x)
    za=list(zero_array)
    for k in range(x):
        z=step_array[k]
        y=sa.count(z)
        za[k]=(y)
    print("\n")
    print(step_array)
    print(za)
    bir=plt.figure(1)
    plt.subplot(2,4,i+1)
    plt.bar(step_array,za,color='seagreen',width=0.75)
    plt.title(keys_list[i])
    bir.show()

    

stcouple2=df.groupby(["sensor_mac", "transmitter_mac"], as_index=False)["timeStamp"]
stdict2=dict(stcouple2.apply(list))

values2 = stdict2.values()
values_list2 = list(values2)

w=100

def frekans(lst):
    t_ilk=lst[0]
    t_son=lst[w-1]
    f=w/(t_son-t_ilk)
    return f

def aralik(frekans, deger):
    counter=0
    for item in frekans:
        if deger <= item <= deger+0.05:
            counter += 1
    return counter

for i in range (0,n):
    tw=values_list2[i]
    time_window_i=list(tw[0:w])
    mef_i=list()
    p=len(tw)
    f=frekans(time_window_i)
    mef_i.append(f)
    for k in range (w,p):
        x=tw[k]
        time_window_i.append(x)
        if len(time_window_i)>w:
            time_window_i.pop(0)
        f2=frekans(time_window_i)
        mef_i.append(f2)
    dglm_array=np.arange(start=1.5, stop=2.5, step=0.05)
    c=len(dglm_array)
    zero_array2=np.zeros(c)
    za2=list(zero_array2)
    for j in range (0,c):
       a=dglm_array[j]
       b=aralik(mef_i, a)
       za2[j]=(b)
    print("\n")
    print(dglm_array)
    print(za2)
    iki = plt.figure(2)
    plt.subplot(2,4,i+1)
    plt.plot(mef_i, color='indianred')
    plt.title(keys_list[i])
    iki.show()
    uc = plt.figure(3)
    plt.subplot(2,4,i+1)
    plt.bar(dglm_array, za2, color='dodgerblue', width=0.15)
    plt.title(keys_list[i])
    uc.show()
    
    







