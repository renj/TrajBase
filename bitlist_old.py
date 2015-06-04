import numpy as np
import pandas as pd
import sys
import random

def lsh(A, n_tnodes, n_hash):
    seq = range(n_tnodes+2, len(A))
    min_hash = {}
    for i in range(1, n_tnodes+1):
        min_hash[i] = []
    for k in range(n_hash):
        print 'min hashing',k
        for i in range(1, n_tnodes+1):
            min_hash[i].append( A[seq][:,i].nonzero()[0][0] )
        random.shuffle(seq)
    return min_hash

    buk = {}
    for tid in min_hash.keys():
        if str(min_hash[tid]) not in buk.keys():
            buk[str(min_hash[tid])] = []
        buk[str(min_hash[tid])].append(tid)
    ret = {}
    idx = 1
    for key in buk.keys():
        for item in buk[key]:
            ret[item] = idx
            idx += 1
    return ret

def bitlist_origin(A, tnodes, w):
    undo = range(tnodes[0], tnodes[1]+1)
    undo_array = np.zeros(len(A))
    for i in undo: undo_array[i] = 1
    bit_list = []
    now = 0
    ret = {}
    i = 1
    while len(undo) > 0:
        print g_folder,g_n_rows, g_max_nodes, 'bitlist',len(undo)
        best = 0
        if now == w:
            now = 0
        if now == 0:
            best = undo.pop()
            bit_list = A[best]
        else:
            bs = -1
            visited = np.zeros(len(A))
            to_visit = []
            undo_set = set(undo)
            for n in bit_list.nonzero()[0]:
                visited = np.logical_or(visited, A[n])
            to_visit = np.logical_and(visited, undo_array).nonzero()[0]
            for n in to_visit:
                score = sum(A[n]*bit_list)
                if score > bs:
                    best = n
                    bs = score
            if best == 0: best = undo[0]
            bit_list = bit_list + A[best]
            undo.remove(best)

        undo_array[best] = 0
              
        ret[best] = i
        i += 1
        now += 1
        
    return ret

def bitlist_sim_pairwise(A, tnodes, w, sim):
    undo = range(tnodes[0], tnodes[1]+1)
    undo_array = np.zeros(tnodes[1]+1)
    for i in undo: undo_array[i] = 1
    bit_list = []
    now = 0
    ret = {}
    i = 1
    pre = 0
    while len(undo) > 0:
        print len(undo), len(undo_array.nonzero()[0]), pre
        best = 0
        if now == w:
            now = 0
        if now == 0:
            best = undo.pop()
            bit_list = A[best]
            pre = best
        else:
            best = (undo_array * sim[pre]).argmax()
            print sim[pre][best]
            if best == 0:
                best = undo.pop()
            else:
                undo.remove(best)
            pre = best

        undo_array[best] = 0
              
        ret[best] = i
        i += 1
        now += 1
        
    return ret

def bitlist_sim_first(A, tnodes, w, sim):
    undo = range(tnodes[0], tnodes[1]+1)
    undo_array = np.zeros(tnodes[1]+1)
    for i in undo: undo_array[i] = 1
    bit_list = []
    now = 0
    ret = {}
    i = 1
    pre = 0
    while len(undo) > 0:
        print len(undo), len(undo_array.nonzero()[0]), pre
        best = 0
        if now == w:
            now = 0
        if now == 0:
            best = undo.pop()
            bit_list = A[best]
            pre = best
        else:
            best = (undo_array * sim[pre]).argmax()
            print sim[pre][best]
            if best == 0:
                best = undo.pop()
            else:
                undo.remove(best)

            #print pre, best
            #pre = best

        undo_array[best] = 0
              
        ret[best] = i
        i += 1
        now += 1
        
    return ret

def get_data(folder_name, n_rows, max_nodes):
    file_name = "./data/A_%s_%d_%d.txt" % \
        (folder_name, n_rows, max_nodes)
    s = open(file_name, 'r').read()
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

    return A, n_nodes, n_edge, n_tnodes

def filled_bits(_interval, transform, M, n_tnodes, n_nodes, t = None):
    n = 0
    total = 0
    for i in xrange(n_tnodes+1,n_nodes):
        for j in xrange(1,n_tnodes,_interval):
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

def transform(A, t, n_nodes):
    Ak = np.zeros((n_nodes+2,n_nodes+2))
    x,y = A.nonzero()
    for i in xrange(len(x)):
        _x = (x[i] in t) and t[x[i]] or x[i]
        _y = (y[i] in t) and t[y[i]] or y[i]
        Ak[_x][_y] = Ak[_y][_x] = 1
    return Ak

def sim_hamming(A, n_tnodes):
    sim = np.zeros((n_tnodes+1, n_tnodes+1))
    for i in range(1, n_tnodes+1):
        print g_folder,g_n_rows, g_max_nodes, 'sim_hamming',i
        to_visit = np.zeros(len(A))
        for j in A[i].nonzero()[0]:
            to_visit = np.logical_or(to_visit, A[j])
        havent_visit = np.ones(len(A))
        havent_visit[0:i+1] = 0
        to_visit = np.logical_and(to_visit, havent_visit)
        for j in to_visit.nonzero()[0]:
            sim[i][j] = sum(np.logical_not(np.logical_xor(A[i], A[j])))
            sim[j][i] = sim[i][j]
    return sim

def sim_jaccard(A, n_tnodes):
    sim = np.zeros((n_tnodes+1, n_tnodes+1))
    for i in range(1, n_tnodes+1):
        print g_folder,g_n_rows, g_max_nodes, 'sim_jaccard',i
        to_visit = np.zeros(len(A))
        for j in A[i].nonzero()[0]:
            to_visit = np.logical_or(to_visit, A[j])
        havent_visit = np.ones(len(A))
        havent_visit[0:i+1] = 0
        to_visit = np.logical_and(to_visit, havent_visit)
        for j in to_visit.nonzero()[0]:
            sim[i][j] = sum(np.logical_and(A[i], A[j])) \
                * 1.0 / sum(np.logical_or(A[i],A[j]))
            sim[j][i] = sim[i][j]
    return sim


def to_pickle(obj, file_name):
    import pickle
    f = open('./data/'+file_name,'w')
    pickle.dump(obj, f)
    f.close()

def to_file(obj, file_name):
    import json
    f = open('./result/'+file_name,'w')
    f.write(json.dumps(obj, indent=4))
    f.close()

global g_folder
global g_n_rows
global g_max_nodes

g_folder = '01'
g_n_rows = 1000
g_max_nodes = 100

if __name__ == '__main__':

    if len(sys.argv) == 4:
        g_folder = sys.argv[1]
        g_n_rows = int(sys.argv[2])
        g_max_nodes = int(sys.argv[3])

    A, n_nodes, n_edge, n_tnodes = \
        get_data(g_folder, g_n_rows, g_max_nodes)
    """
    sim_h = sim_hamming(A, n_tnodes)
    to_pickle(sim_h, ('SH_%s_%d_%d.pickle'\
         % (g_folder, g_n_rows, g_max_nodes)))

    sim_j = sim_jaccard(A, n_tnodes)
    to_pickle(sim_j, ('SJ_%s_%d_%d.pickle'\
         % (g_folder, g_n_rows, g_max_nodes)))
    """

    import time

    t1 = time.time()
    lsh_t = lsh(A, n_tnodes, 100)
    t2 = time.time()
    lsh_t['time'] = t2-t1

    to_pickle(lsh_t, ('MINH_%s_%d_%d.pickle'\
        % (g_folder, g_n_rows, g_max_nodes)))

    """
    results = []
    for w  in [4,16,64]:
        rst = {}
        rst['width'] = w
        rst['n_cell'] = n_nodes - n_tnodes
        rst['n_trajectory'] = n_tnodes
        r = filled_bits(w, False, A, n_tnodes, n_nodes)
        rst['bitlist#_seq'] = r[0]
        rst['bitlist#_total'] = r[1]
   

        t1 = time.time()
        t = bitlist_origin(A, (1, n_tnodes), w)
        t2 = time.time()

        to_pickle(t, ('BLT_%s_%d_%d.pickle'\
             % (g_folder, g_n_rows, g_max_nodes)))
        Ak = transform(A, t, n_nodes)
        r = filled_bits(w, False, Ak, n_tnodes, n_nodes)
        rst['bitlist#_origin'] = r[0]
        rst['time_origin'] = t2-t1

        t1 = time.time()
        t = bitlist_sim_pairwise(A, (1, n_tnodes), w, sim_h)
        t2 = time.time()
        Ak = transform(A, t, n_nodes)
        r = filled_bits(w, False, Ak, n_tnodes, n_nodes)
        rst['bitlist#_2wise_sim_hamming'] = r[0]
        rst['time_2wise_sim_hamming'] = t2-t1

        t1 = time.time()
        t = bitlist_sim_pairwise(A, (1, n_tnodes), w, sim_j)
        t2 = time.time()
        Ak = transform(A, t, n_nodes)
        r = filled_bits(w, False, Ak, n_tnodes, n_nodes)
        rst['bitlist#_2wise_sim_jaccard'] = r[0]
        rst['time_2wise_sim_jaccard'] = t2-t1

        t1 = time.time()
        t = bitlist_sim_first(A, (1, n_tnodes), w, sim_h)
        t2 = time.time()
        Ak = transform(A, t, n_nodes)
        r = filled_bits(w, False, Ak, n_tnodes, n_nodes)
        rst['bitlist#_first_sim_hamming'] = r[0]
        rst['time_first_sim_hamming'] = t2-t1

        t1 = time.time()
        t = bitlist_sim_first(A, (1, n_tnodes), w, sim_j)
        t2 = time.time()
        Ak = transform(A, t, n_nodes)
        r = filled_bits(w, False, Ak, n_tnodes, n_nodes)
        rst['bitlist#_first_sim_jaccard'] = r[0]
        rst['time_first_sim_jaccard'] = t2-t1

        results.append(rst)

    to_file( results, ('BL_%s_%d_%d.txt'% \
                (g_folder, g_n_rows, g_max_nodes)))
    """

