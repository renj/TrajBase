import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random
import pickle

def lsh(A, n_tnodes, w, n_hash):
    seq = range(n_tnodes+2, len(A))
    min_hash = {}
    for i in range(1, n_tnodes+1):
        min_hash[i] = []
    for k in range(n_hash):
        print 'min hashing',k
        for i in range(1, n_tnodes+1):
            min_hash[i].append( A[seq][:,i].nonzero()[0][0] )
        random.shuffle(seq)

    f = open('min_hash.pickle', 'w')
    pickle.dump(min_hash, f)
    f.close()

    return 

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

if __name__ == '__main__':
    folder_name = '02'
    n_rows = 2000
    max_nodes = 50
    file_name = '/home/zhengrenjie/TrajBase/data/A_%s_%d_%d.txt' % (folder_name, n_rows, max_nodes)
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

    sim = np.zeros((n_tnodes+1, n_tnodes+1))
    for i in range(1, n_tnodes+1):
        print i
        to_visit = np.zeros(len(A))
        for j in A[i].nonzero()[0]:
            to_visit = np.logical_or(to_visit, A[j])
        havent_visit = np.ones(len(A))
        havent_visit[0:i+1] = 0
        to_visit = np.logical_and(to_visit, havent_visit)
        for j in to_visit.nonzero()[0]:
            sim[i][j] = sum(np.logical_not(np.logical_xor(A[i], A[j])))
            sim[j][i] = sim[i][j]

    f = open('sim.pickle', 'w')
    pickle.dump(sim, f)
    f.close()
        
    """
    lsh_t = lsh(A, n_tnodes, 8, 100)
    """
