import os
import pandas as pd
import matplotlib.pyplot as plt

FOLDER_ROOT = '/home/zhengrenjie/Data/'
FOLDER_ROOT = '/Users/renj/Data/beijing 2008/'

def trim_data(data, scope):
    _d = data
    _d = _d[_d.x > scope[0]]
    _d = _d[_d.x < scope[1]]
    _d = _d[_d.y > scope[2]]
    _d = _d[_d.y < scope[3]]
    return _d

def get_array1(_d, scope, scale = 100):
    a = {}
    x_min = scope[0]
    x_max = scope[1]
    y_min = scope[2]
    y_max = scope[3]
    for x in range(int(x_min*scale-1), int(x_max*scale)):
        a[x] = {}
        for y in range(int(y_min*scale-1), int(y_max*scale)):
            a[x][y] = set()
    for id,time,x,y in _d.values:
        _x = int(x*scale)
        _y = int(y*scale)
        #a[_x][_y] = 1
        a[_x][_y].add(id)

    _a = {}
    for x in a:
        _a[x] = {}
        for y in a[x]:
            _a[x][y] = len(a[x][y])

    frame = pd.DataFrame(_a)
    z = frame.fillna(0).values
    return z

def get_array(_d, scale = 100):
    a = {}
 
    for id,time,x,y in _d.values:
        _x = int(x*scale)
        _y = int(y*scale)
        #a[_x][_y] = 1
        if _x not in a.keys():
            a[_x] = {}
        if _y not in a[_x].keys():
            a[_x][_y] = set()
        a[_x][_y].add(id)

    _a = {}
    for x in a:
        _a[x] = {}
        for y in a[x]:
            _a[x][y] = len(a[x][y])

    frame = pd.DataFrame(_a)
    z = frame.fillna(0).values
    return z

def get_data(f_path):
    dat = None
    import os
    if os.path.isfile(f_path):
        if f_path.endswith('txt'):
            dat = pd.read_csv(f_path, names=['id','time','x','y'])
        else:
            dat = None
    elif os.path.isdir(f_path):
        for f in os.listdir(f_path):
            _f_path = f_path+'/'+f
            _dat = get_data(_f_path)
            if dat is None: dat = _dat
            else: dat = pd.concat([dat, _dat])
    return dat

def read_data(read_type = 'file' ):
    if read_type == 'file':
        f_path = FOLDER_ROOT+'01/1131.txt'
    elif read_type == '2nd_folder':
        f_path = FOLDER_ROOT+'/01'
    elif read_type == '1st_folder':
        f_path = FOLDER_ROOT

    return get_data(f_path)

def draw_pics():
    d = read_data()

    scope = (116.1, 116.7, 39.6, 40.2)
    _d = trim_data(d, scope)
    Z, extent = get_array(_d, scope, 50)

    fig1 = plt.figure(1,(12,6))
    fig1.clf()

    ax1 = fig1.add_subplot(1,2,1)
    im = ax1.imshow(Z, extent = extent, interpolation="nearest")

    ax2 = fig1.add_subplot(1,2,2)
    ax2.plot(_d.x,_d.y,'.')

    plt.draw()
    plt.show()

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

def get_result(_d, scale = 100):
    import time
    t1 = time.time()
    Z = get_array(_d, scale)
    t2 = time.time()
    num_nonzero = len(Z.nonzero()[0])
    cell_bolder = haversine((scope[0]*scale-1)*1.0/scale, (scope[1]*scale)*1.0/scale, scope[0]*scale*1.0/scale, scope[1]*scale*1.0/scale)
    ans = {}
    ans["Cell bolder length"] = cell_bolder
    ans['Scale'] = scale
    x_min = scope[0]
    x_max = scope[1]
    y_min = scope[2]
    y_max = scope[3]
    ans['Shape'] = ( (int(x_max*scale) - (int(x_min*scale-1)))\
        , (int(y_max*scale) - int(y_min*scale-1)))
    ans['Cell Number'] = ans['Shape'][0] * ans['Shape'][1]
    ans['Sum'] = Z.sum()
    ans['Max'] = Z.max()
    ans['_id'] = scale
    ans['Non zero elements'] = num_nonzero
    ans['Nonzero rate'] = num_nonzero*1.0/ans['Cell Number']
    ans['Average cell volume'] = Z.sum()*1.0/(num_nonzero)
    ans["Time"] = t2-t1
    return ans


"""
import pymongo
conn = pymongo.Connection(host = '10.60.43.110')
db = conn.TrajDB
d = read_data()
scope = (115.9, 116.9, 39.4, 40.4)
_d = trim_data(d, scope)

ans = get_result(_d, scale = 100)
db.experiment.insert(ans)
"""
