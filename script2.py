import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import json
import math
import bitlist
import query

T1 = 'qt-bl'
T2 = 'qt-repl'
T3 = 'qt'
T4 = 'grid-bl'

#query.get_region_number_result(10000, T1, 200, 1000, 8, 'short', 'old', 1024)
query.get_region_number_result(13936, T1, 1000, 5000, 8, 'st0110', 'new', 1024)
query.get_region_number_result(13936, T2, 1000, 5000, 8, 'st0110', 'new', 1024)
#query.get_region_number_result(100000, T2, 1500, 5000, 8, 'short', 'old', 1024)


'''
folder = './result/_backup/'
#folder = './result/'
files = os.listdir(folder)
result_data = []
for f in files:
    if not f.startswith('R_'):
        continue
    fp = open(folder+f,'r')
    result_data.append(json.load(fp))
    fp.close()
reload(bitlist)
dataframe = pd.DataFrame()
for data in result_data:
    _df = pd.DataFrame(data)
    dataframe = pd.concat([dataframe, _df])

for type, traj_num, max_nodes in set(zip(dataframe.type, dataframe.traj_num, dataframe.max_nodes)):
    #if type=='dense250': continue
    itv, tl = bitlist.read_Tl(traj_num, max_nodes, 'q', type, 'old', 1024)
    """
    if tl == 0: continue
    a = tl.get_cid_depth()
    cid, depth = zip(*a)
    deepest = max(depth)
    mean = sum(depth)*1.0/len(depth)
    print type, traj_num, max_nodes, deepest, mean
    dataframe.loc[(dataframe.traj_num==traj_num)&(dataframe.max_nodes==max_nodes)&(dataframe.type==type),'leaf_deepest'] = deepest
    dataframe.loc[(dataframe.traj_num==traj_num)&(dataframe.max_nodes==max_nodes)&(dataframe.type==type),'leaf_avg'] = mean
    """
'''

"""
T1 = 'qt-bl'
T2 = 'qt-repl'
T3 = 'qt'
T4 = 'grid-bl'

query.get_region_number_result(10000, T1, 500, 5000, 8, 'dense250', 'new', 1024)
query.get_region_number_result(10000, T2, 500, 5000, 8, 'dense250', 'new', 1024)
"""
#query.get_region_number_result(5000, T2, 100, 1000, 8, 'dense', 'new')
#query.get_region_number_result(5000, T3, 100, 1000, 8, 'dense', 'new')
#query.get_region_number_result(100000, T1, 1000, 5000, 8, 'short', 'old')
#query.get_region_number_result(100000, T2, 1000, 5000, 8, 'short', 'old')
#query.get_region_number_result(100000, T1, 1500, 5000, 8, 'short', 'old')
#query.get_region_number_result(100000, T2, 1500, 5000, 8, 'short', 'old')
#query.get_region_number_result(5000, T3, 50, 1000, 8, 'dense', 'new')
#query.get_region_number_result(5000, T1, 200, 1000, 8, 'dense', 'new')
#query.get_region_number_result(5000, T2, 200, 1000, 8, 'dense', 'new')
#query.get_region_number_result(5000, T3, 200, 1000, 8, 'dense', 'new')
"""
query.get_region_number_result(100000, T2, 1500, 5000, 8)
query.get_region_number_result(100000, T3, 1500, 5000, 8)
query.get_region_number_result(100000, T1, 1000, 5000, 8)
query.get_region_number_result(100000, T2, 1000, 5000, 8)
query.get_region_number_result(100000, T3, 1000, 5000, 8)
query.get_region_number_result(100000, T1, 500, 5000, 8)
query.get_region_number_result(100000, T2, 500, 5000, 8)
query.get_region_number_result(100000, T3, 500, 5000, 8)
"""

#query.get_region_number_result(100000, T4, 16, 5000, 8)
"""
print
query.get_region_number_result(100000, T4, 16, 5000, 8)
"""

"""
query.get_region_size_result(100000, T1, 500, 5000, 8)
query.get_region_size_result(100000, T2, 500, 5000, 8)
query.get_region_size_result(100000, T3, 500, 5000, 8)
query.get_region_size_result(100000, T1, 1500, 5000, 8)
query.get_region_size_result(100000, T2, 1500, 5000, 8)
query.get_region_size_result(100000, T3, 1500, 5000, 8)
query.get_region_size_result(100000, T1, 1000, 5000, 8)
query.get_region_size_result(100000, T2, 1000, 5000, 8)
query.get_region_size_result(100000, T3, 1000, 5000, 8)
"""
#query.get_region_size_result(100000, T4, 16, 5000, 8)
#print "query.get_region_size_result(100000, T4, 16, 5000, 8)"

"""
for t_num, max_nodes in [(122060, 500), (122060, 1000), (122060, 1500), (122060, 100),]:
    print 'Computing t_num = %d, max_nodes = %d, dtype = %s' % (t_num, max_nodes, dtype)
    bitlist.generate_matrix(t_num, max_nodes, dtype)
    print 'Generate matrix complete'
    bitlist.get_answer(t_num, max_nodes, dtype)

dtype = ''
for t_num, max_nodes in [(500, 100), (1000, 150), (1000, 25), (1000, 200)]:
    print 'Computing t_num = %d, max_nodes = %d, dtype = %s'%(t_num, max_nodes, dtype)
    bitlist.generate_matrix(t_num, max_nodes, dtype)
    bitlist.get_answer(t_num, max_nodes, dtype)

dtype = ''
for t_num, max_nodes in [(100, 20), (500, 20), (500, 50), (1000,50), (5000, 100)]:
    print 'Computing t_num = %d, max_nodes = %d, dtype = %s'%(t_num, max_nodes, dtype)
    bitlist.dump_similarity(t_num, max_nodes, dtype, 'euclidean')
    bitlist.dump_similarity(t_num, max_nodes, dtype, 'cosine')
    bitlist.dump_similarity(t_num, max_nodes, dtype, 'manhatten')

dtype = 'short'
for t_num, max_nodes in [(100, 20), (100,50),(500, 20), (500, 50), (1000,20), (1000, 50),(1000,100)]:
    print 'Computing t_num = %d, max_nodes = %d, dtype = %s'%(t_num, max_nodes, dtype)
    bitlist.dump_similarity(t_num, max_nodes, dtype, 'euclidean')
    bitlist.dump_similarity(t_num, max_nodes, dtype, 'cosine')
    bitlist.dump_similarity(t_num, max_nodes, dtype, 'manhatten')

dtype = 'long'
for t_num, max_nodes in [(100, 20), (100, 50), (500, 20), (500, 50)]:
    print 'Computing t_num = %d, max_nodes = %d, dtype = %s'%(t_num, max_nodes, dtype)
    bitlist.dump_similarity(t_num, max_nodes, dtype, 'euclidean')
    bitlist.dump_similarity(t_num, max_nodes, dtype, 'cosine')
    bitlist.dump_similarity(t_num, max_nodes, dtype, 'manhatten')


dtype = 'short'
for t_num, max_nodes in [(5000,100),(5000,50)]:
    print 'Computing t_num = %d, max_nodes = %d, dtype = %s'%(t_num, max_nodes, dtype)
    bitlist.dump_similarity(t_num, max_nodes, dtype, 'euclidean')
    bitlist.dump_similarity(t_num, max_nodes, dtype, 'cosine')
    bitlist.dump_similarity(t_num, max_nodes, dtype, 'manhatten')


t_num = 5000
max_nodes = 50
dtype = ''
print 'Computing t_num = %d, max_nodes = %d, dtype = %s'%(t_num, max_nodes, dtype)
bitlist.dump_similarity(t_num, max_nodes, dtype, 'euclidean')
bitlist.dump_similarity(t_num, max_nodes, dtype, 'cosine')
bitlist.dump_similarity(t_num, max_nodes, dtype, 'manhatten')

"""