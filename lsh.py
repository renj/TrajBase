import pickle
import pandas as pd
import numpy as np
import sys
import time
import random
import tools
import quad
import bitlist

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

from itertools import combinations
def lsh(min_hash, b, r, A, n_tnodes):
    sim = np.zeros((n_tnodes+1, n_tnodes+1))
    for i in range(b):
        buk = {}
        for tid in min_hash.keys():
            k = str(min_hash[tid][i*r:(i+1)*r])
            if str(k) not in buk.keys():
                buk[k] = []
            buk[k].append(tid)
        print 'buk builded'
        sys.stdout.flush()
        for key in buk.keys():
            for i,j in combinations(buk[key], 2):
                #print i,j
                if sim[i][j] != 0: continue
                sim[i][j] = sum(np.logical_and(A[i], A[j])) \
                    * 1.0 / sum(np.logical_or(A[i],A[j]))
                sim[j][i] = sim[i][j]
                #print sim[i][j]
    return sim