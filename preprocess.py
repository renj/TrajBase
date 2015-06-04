import bitlist
import numpy as np
import tools
import pandas as pd


def get_step(d):
    delt_dist = map(lambda x: tools.haversine(x[0], x[1], x[2], x[3]), zip(d.x[1:], d.y[1:], d.x[:-1], d.y[:-1]))
    step = np.array(delt_dist+[0])
    a = d.tid[1:].values-d.tid[:-1].values
    idx = a.nonzero()[0]+1
    boo = np.ones(len(d))
    for i in idx:
        boo[idx-1] = 0
    new_step = boo*step
    return new_step


def drop_row(d, md=250):
    tid = 0
    step = 0
    drop = []
    total = len(d)
    d.index = range(len(d))
    for i in d.index:
        if i % int(total/10) == 0:
            print 'Proncessed', i, 'from', total
        r = d.ix[i]
        if r.tid is not tid:
            step = 0
            tid = r.tid
        step += r.step
        if step < md:
            drop.append(i)
        else:
            step = 0
    return drop


def sampling(traj_num, min_dist):
    print 'Start sampling'
    print 'Reading data'
    D = bitlist.read_D(traj_num, 'short', 'old')

    print 'Get step'
    step = get_step(D)
    D['step'] = step
    d = D[:-1].copy()

    d['t1'] = list(D.time[1:])
    d['x1'] = list(D.x[1:])
    d['y1'] = list(D.y[1:])

    print 'Droping rows'
    drop = drop_row(d, min_dist)
    d = d.drop(drop)

    ms = min_dist
    add = []
    idx = 0
    total = len(d[d.step > ms])
    for l in d[d.step > ms].values:
        if idx % int(total/10) == 0:
            print 'Proncessed', idx, 'from', total
        idx += 1
        id, t0, t1, tid, step, x0, y0, x1, y1 = l[0], l[1],l[6], l[4],l[5],l[2],l[3],l[7],l[8]
        #print tid, step, x0, y0, x1, y1
        num = int((step)*1.0/ms)
        delta_x = (x1-x0)/num
        delta_y = (y1-y0)/num
        delta_t = (t1-t0)/num
        for i in range(num):
            x0 += delta_x
            y0 += delta_y
            t0 += delta_t
            add.append((id, tid, t0, x0, y0))

    df = pd.DataFrame(add, columns=['id', 'tid', 'time', 'x', 'y'])
    ndf = pd.concat([D, df])
    del ndf['step']
    ndf.to_pickle('./data/Data_dense'+str(min_dist)+'_'+str(traj_num)+'.pickle')
    return ndf


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
            drop_idx += range(idx[i], idx[i+1])
            i += 1
        i += 1
    return drop_idx


def under_speed(d, min_speed):
    delt_dist = map(lambda x: haversine(x[0], x[1], x[2], x[3]), zip(d.x[1:], d.y[1:], d.x[:-1], d.y[:-1]))
    dt = pd.to_datetime(d.time)
    s = map(lambda x: x.total_seconds(), np.subtract(dt[1:], dt[:-1]))
    df = pd.DataFrame(zip(range(len(s)), s, delt_dist))
    df['speed'] = np.divide(df[2], df[1])
    df = df.fillna(0)
    #df = df.drop(df[df.speed > max_speed].index)
    #return df
    idx = df[df.speed < min_speed].index+1
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


def clean(day):
    folder = '/home/renj/Data/zhenjiang/'
    data = pd.read_csv(folder+'Raw_'+day+'.txt')
    data.columns = ['id', 'x', 'y', 'time', 'speed', 'dir']
    dt = data.time.copy()
    dt.sort()
    data = data.ix[dt.index]
    data.index = range(len(data))
    sample_data = data
    i = 0
    MAX_SPEED = 60
    fined_data = pd.DataFrame()
    for id in sample_data.id.unique():
        print i, id
        d = sample_data[sample_data.id == id]
        d.index = range(len(d))
        if len(d) <= 1:
            continue
        drop_idx = over_speed(d, MAX_SPEED)
        print len(drop_idx)
        while len(drop_idx) != 0:
            d = d.drop(drop_idx)
            d.index = range(len(d))
            drop_idx = over_speed(d, MAX_SPEED)
        assert len(drop_idx) == 0
        fined_data = pd.concat([fined_data, d])
        i += 1
    fined_data.to_pickle(folder+'Fined_'+day+'.pickle')


def trim(day, MAX_SPEED=60, MIN_SPEED=0.1):
    folder = '/home/renj/Data/zhenjiang/'
    data = pd.read_csv(folder+'Raw_'+day+'.txt')
    data.columns = ['id', 'x', 'y', 'time', 'speed', 'dir']
    dt = data.time.copy()
    dt.sort()
    data = data.ix[dt.index]
    data.index = range(len(data))
    sample_data = data
    i = 0
    fined_data = pd.DataFrame()
    for id in sample_data.id.unique():
        print i, id
        d = sample_data[sample_data.id == id]
        d.index = range(len(d))
        if len(d) <= 1:
            continue
        drop_idx = over_speed(d, MAX_SPEED)+under_speed(d, MIN_SPEED)
        print len(drop_idx)
        while len(drop_idx) != 0:
            d = d.drop(drop_idx)
            d.index = range(len(d))
            drop_idx = over_speed(d, MAX_SPEED)
        assert len(drop_idx) == 0
        fined_data = pd.concat([fined_data, d])
        i += 1
    fined_data.to_pickle(folder+'Trimed_'+day+'.pickle')


def split(day, minutes):
    folder = '/home/renj/Data/zhenjiang/'
    d = pd.read_pickle(folder+'Fined_'+day+'.pickle')
    d.index = range(1, len(d)+1)
    d.time = pd.to_datetime(d.time)
    delta_time = np.subtract(d.time[1:], d.time[:-1])
    delta_id = np.subtract(d.id[1:], d.id[:-1])
    split_id = delta_id[delta_id != 0].index
    split_time = delta_time[delta_time > np.timedelta64(minutes, 'm')].index
    split_all = pd.Series([1] + list(split_id) + list(split_time) + [len(d)]).unique()
    split_all.sort()
    window = np.subtract(split_all[1:], split_all[:-1])
    window[-1] += 1
    l_id = []
    idx = 1
    for i in window:
        l_id += [idx] * i
        idx += 1
    assert len(d) == sum(window)
    d['tid'] = l_id
    d.to_pickle(folder+'Splited_'+day+'_'+str(minutes)+'.pickle')


def split_from_trim(day, minutes):
    folder = '/home/renj/Data/zhenjiang/'
    d = pd.read_pickle(folder+'Trimed_'+day+'.pickle')
    d.index = range(1, len(d)+1)
    d.time = pd.to_datetime(d.time)
    delta_time = np.subtract(d.time[1:], d.time[:-1])
    delta_id = np.subtract(d.id[1:], d.id[:-1])
    split_id = delta_id[delta_id != 0].index
    split_time = delta_time[delta_time > np.timedelta64(minutes, 'm')].index
    split_all = pd.Series([1] + list(split_id) + list(split_time) + [len(d)]).unique()
    split_all.sort()
    window = np.subtract(split_all[1:], split_all[:-1])
    window[-1] += 1
    l_id = []
    idx = 1
    for i in window:
        l_id += [idx] * i
        idx += 1
    assert len(d) == sum(window)
    d['tid'] = l_id
    d.to_pickle(folder+'SplitTrim_'+day+'_'+str(minutes)+'.pickle')
