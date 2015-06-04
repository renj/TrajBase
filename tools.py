import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

FOLDER_ROOT = '/Users/renj/Data/beijing 2008'
__base4 = '0123'

def get_data(f_path, n_rows):
    """
    x: lonitude, y: latitude
    beijing: 116.46, 39.92
    datong: 113.3, 40.12
    tianjing: 117.2, 39.13
    chengde: 117.92, 40.97
    tangshan: 118.02, 39.63
    """
    dat = None
    import os
    if os.path.isfile(f_path):
        if f_path.endswith('txt'):
            if n_rows == None:
                dat = pd.read_csv(f_path, names=['id','time','x','y'])
            else:
                dat = pd.read_csv(f_path, names=['id','time','x','y'], nrows=n_rows)
        else:
            dat = None
    elif os.path.isdir(f_path):
        for f in os.listdir(f_path):
            _f_path = f_path+'/'+f
            _dat = get_data(_f_path, n_rows)
            if dat is None: dat = _dat
            else: dat = pd.concat([dat, _dat])
    return dat

def read_data(read_type = 'file', folder = '02', n_rows = 1000):
    if read_type == 'file':
        f_path = FOLDER_ROOT+'/01/1131.txt'
    elif read_type == '2nd_folder':
        f_path = FOLDER_ROOT+'/'+folder
    elif read_type == '1st_folder':
        f_path = FOLDER_ROOT

    return get_data(f_path, n_rows)

def encode(latitude, longitude, precision=12):
    """
    Encode a position given in float arguments latitude, longitude to
    a geohash which will have the character count precision.
    """
    lat_interval, lon_interval = (-90.0, 90.0), (-180.0, 180.0)
    geohash = []
    bits = [ 2, 1 ]
    bit = 0
    ch = 0
    even = True
    while len(geohash) < precision:
        if even:
            mid = (lon_interval[0] + lon_interval[1]) / 2
            if longitude > mid:
                ch |= bits[bit]
                lon_interval = (mid, lon_interval[1])
            else:
                lon_interval = (lon_interval[0], mid)
        else:
            mid = (lat_interval[0] + lat_interval[1]) / 2
            if latitude > mid:
                ch |= bits[bit]
                lat_interval = (mid, lat_interval[1])
            else:
                lat_interval = (lat_interval[0], mid)
        even = not even
        if bit < 1:
            bit += 1
        else:
            geohash += __base4[ch]
            bit = 0
            ch = 0
    return ''.join(geohash)

def generate_linked_list(_folder, _n_rows, _max_nodes):
    print "Folder: %s, nrows: %d, max_nodes: %d" % (_folder, _n_rows, _max_nodes)

    # Load data
    d = read_data('2nd_folder', _folder, _n_rows)

    print "Load %d lines of data" % (len(d))


    # Set TID
    d.index = range(1, len(d)+1)
    delta_time = np.subtract(d.time[1:], d.time[:-1])
    delta_id = np.subtract(d.id[1:], d.id[:-1])
    split_id = delta_id[delta_id != 0].index
    split_time = delta_time[delta_time > np.timedelta64(10,'m')].index
    split_all = pd.Series([1] + list(split_id) + list(split_time) + [len(d)]).unique()
    split_all.sort()
    window = np.subtract(split_all[1:], split_all[:-1])
    window[-1] += 1

    l_id = []
    idx = 1
    for i in window:
        l_id += [idx] * i
        idx += 1
    print "%d == %d" % (len(d), sum(window))
    d['tid'] = l_id

    print "Set TID %d - %d Total: %d" % (d['tid'].min(), d['tid'].max(), len(d['tid'].unique()))

    # Set hashid
    f = lambda t: encode(t.y, t.x, 64)
    d['hashid'] = d.apply(f, axis=1)

    # Set CID
    import quad
    quad.max_id = len(d.tid.unique())+5
    quad.g_max_nodes = _max_nodes


    Q = quad.QuadTree('', 0)
    print "Max nodes: %d" % (quad.g_max_nodes)
    d.apply(lambda x: Q.insert(x.tid, x.hashid), axis=1)
    _s = Q.generate_linked_list()

    m = {}
    cid = len(d.tid.unique())+5
    for l in _s.split('\n'):
        t = l.split('\t')
        if len(t) == 2 and t[0] not in m.keys():
            m[t[0]] = cid
            cid += 1

    print "Set CID %d - %d. Total %d cells" % (len(d.tid.unique())+5, cid-1, len(m.keys()))
    print "Edge: %d" % (len(_s.split('\n')))

    s = ''
    for l in _s.split('\n'):
        t = l.split('\t')
        if len(t) == 2: s += str(m[t[0]]) + '\t' + t[1] + '\n'
    s = '# TID: %d - %d Total: %d\n# CID: %d - %d Total: %d\n# Edge: %d\n' % (d['tid'].min(), d['tid'].max(), len(d['tid'].unique()), len(d.tid.unique())+5, cid-1, len(m.keys()), len(_s.split('\n'))) + s

    file_name = './data/A_'+_folder+'_'+str(_n_rows)+'_'+str(_max_nodes)+'.txt'
    f = open(file_name,'w')
    f.write(s)
    f.close()

def exCmd(cmd): 
    r = os.popen(cmd) 
    text = r.read() 
    r.close() 
    return text

def runmat( folder_name, n_rows, max_nodes ):
    file_name = "'../data/A_%s_%d_%d.txt'" % (folder_name, n_rows, max_nodes)
    ls = open(file_name[2:-1], 'r').read().split('\n')
    print len(ls)-3
    print ls[-2].split('\t')[0]
    n_nodes = int(ls[-2].split('\t')[0])+1
    n_edge = len(ls)-4
    
    cmd = '/Applications/MATLAB_R2014a.app/bin/matlab -nodesktop -nodisplay -r "\ncd ./Slashburn;'
    cmd += "[A] = LoadAdjacentMat(%s,%d,%d,%d,4);" % (file_name, n_nodes, n_edge, n_nodes)
    cmd += "[niter, gccsize, Ak, I, J] = SlashBurn(A,100,1);"
    cmd += "save('../data/T_%s_%d_%d.mat','J');" % (folder_name, n_rows, max_nodes)
    cmd += ' exit;"'
    print cmd
    print exCmd(cmd)

def filled_bits(_interval, transform, M, n_tnodes, n_nodes, t = None):
    n = 0
    total = 0
    for i in xrange(1,n_tnodes+1):
        for j in xrange(1,n_nodes,_interval):
            total += 1
            for k in xrange(_interval):
                if j+k > n_nodes: break
                if transform:
                    if M[t[i]][j+k] == 1:
                        #print j+k,
                        n += 1
                        break                    
                else:
                    if M[i][j+k] == 1:
                        #print j+k,
                        n += 1
                        break
    return (n, total)


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

def analysis(folder_name, n_rows, max_nodes ):
    file_name = "'../data/A_%s_%d_%d.txt'" % (folder_name, n_rows, max_nodes)
    s = open(file_name[2:-1], 'r').read()
    ls = s.split('\n')
    n_nodes = int(ls[-2].split('\t')[0])+2
    n_edge = len(ls)-4
    n_tnodes = int(ls[0].split(' ')[-1])
    
    
    A = np.zeros( (n_nodes+2,n_nodes+2) )
    for l in s.split('\n'):
        t = l.split('\t')
        if len(t) == 2:
            t1 = int(t[0])
            t2 = int(t[1])
            A[t1][t2] = A[t2][t1] = 1

    #plt.figure(figsize=(10,10))
    #plt.spy(A)
    
    import scipy.io as sio
    mat_file = './data/T_%s_%d_%d.mat' % (folder_name, n_rows, max_nodes)
    _t = sio.loadmat(mat_file)['J'][0]
    t = np.array([0]*(n_nodes+2))
    for i in range(len(_t)):
        t[_t[i]] = i+1
    Ak = np.zeros((n_nodes+2,n_nodes+2))
    x,y = A.nonzero()
    for i in xrange(len(x)):
        _x = t[x[i]]
        _y = t[y[i]]
        Ak[_x][_y] = Ak[_y][_x] = 1
    #plt.figure(figsize=(10,10))
    #plt.spy(Ak)
    
    result = {'folder_name': folder_name,
              'n_rows': n_rows,
              'max_nodes': max_nodes,
              'n_nodes': n_nodes,
              'n_edge': n_edge,
              'n_traj_nodes': n_tnodes,
              'bit_width':{}
              }
    for i in [4, 8, 32, 128]:
        a1 = filled_bits(i, False, A, n_tnodes, n_nodes)
        a2 = filled_bits(i, True, Ak, n_tnodes, n_nodes, t)
        result['bit_width'][i] = {'A': a1[0],
                                  'Ak': a2[0],
                                  'Total': a1[1],
                                }
        print "A: %d, Ak: %d, total: %d == %d" % (a1[0],a2[0],a1[1],a2[1])
    import json
    js_result = json.dumps(result, indent = 4)
    print js_result
    file_name = "./data/R_%s_%d_%d.txt" % (folder_name, n_rows, max_nodes)
    f = open(file_name, 'w')
    f.write(js_result)
    f.close()
    return result

if __name__ == '__main__':

    import sys
    _folder = '03'
    _n_rows = 3000
    _max_nodes = 100
    if len(sys.argv) == 4:
        _folder = sys.argv[1]
        _n_rows = int(sys.argv[2])
        _max_nodes = int(sys.argv[3])

    generate_linked_list(_folder, _n_rows, _max_nodes)
    runmat(_folder, _n_rows, _max_nodes)
    analysis(_folder,_n_rows,_max_nodes)

