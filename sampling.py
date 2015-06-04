import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random

def haversine(lon1, lat1, lon2, lat2):
    from math import radians, cos, sin, asin, sqrt
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    http://boulter.com/gps/distance/
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    m = 6367000.0 * c
    return m

def over_speed(d, max_speed):
    delt_dist = map(lambda x: haversine(x[0], x[1], x[2], x[3]), zip(d.x[1:], d.y[1:], d.x[:-1], d.y[:-1]))
    dt = pd.to_datetime(d.time)
    s = map(lambda x: x.total_seconds(), np.subtract(dt[1:], dt[:-1]))
    df = pd.DataFrame(zip(range(len(s)), s, delt_dist))
    df['speed'] = np.divide(df[2], df[1])
    df = df.fillna(0)
    #df = df.drop(df[df.speed > max_speed].index)
    #return df
    idx = df[df.speed > max_speed].index+1
    i = 0
    drop_idx = []
    while i < len(idx):
        if i+1 >= len(idx) or idx[i+1]-idx[i] > 5:
            drop_idx.append(idx[i])
        else:
            drop_idx += range(idx[i],idx[i+1])
            i += 1
        i += 1
    return drop_idx

def speed(d):
    delt_dist = map(lambda x: haversine(x[0], x[1], x[2], x[3]), zip(d.x[1:], d.y[1:], d.x[:-1], d.y[:-1]))
    dt = pd.to_datetime(d.time)
    s = map(lambda x: x.total_seconds(), np.subtract(dt[1:], dt[:-1]))
    df = pd.DataFrame(zip(range(len(s)), s, delt_dist))
    df['speed'] = np.divide(df[2], df[1])
    df = df.fillna(0)
    return df

sample_data = pd.read_pickle('./data/sample_data.pickle')

i = 0
MAX_SPEED = 60
fined_data = pd.DataFrame()
for id in sample_data.id.unique()[:20]:
    print i, id
    d = sample_data[sample_data.id == id]
    if len(d) <= 1: continue
    drop_idx = over_speed(d, MAX_SPEED)
    while len(drop_idx) != 0:
        d = d.drop(drop_idx)
        d.index = range(len(d))
        drop_idx = over_speed(d, MAX_SPEED)
    assert len(drop_idx) == 0
    fined_data = pd.concat([fined_data, d])
    i += 1

fined_data.to_pickle('./data/fined_data_20.pickle')    