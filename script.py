import preprocess
import bitlist


bitlist.get_answer(13936, 1500, 'st0110', 'new', 1024)
bitlist.get_answer(13936, 2000, 'st0110', 'new', 1024)
bitlist.get_answer_bitlist(13936, 1500, 'st0110', 'new', 1024)
bitlist.get_answer_bitlist(13936, 2000, 'st0110', 'new', 1024)

'''
bitlist.get_answer(10000, 100, 'dense250', 'new', 16)
bitlist.get_answer(100000, 1500, 'dense250', 'new', 18)
bitlist.get_answer(100000, 1500, 'dense250', 'new', 16)
bitlist.get_answer(100000, 1000, 'dense250', 'new', 18)
bitlist.get_answer(100000, 1000, 'dense250', 'new', 16)
bitlist.get_answer(100000, 500, 'dense250', 'new', 18)
bitlist.get_answer(100000, 500, 'dense250', 'new', 16)

preprocess.sampling(1000, 50)
preprocess.sampling(5000, 50)
preprocess.sampling(10000, 50)
'''
"""
preprocess.sampling(60000, 250)
preprocess.sampling(80000, 250)
preprocess.sampling(100000, 250)
preprocess.sampling(122060, 250)
"""

'''
bitlist.generate_matrix(100000, 100, 'short')
bitlist.generate_matrix(100000, 250, 'short')
bitlist.generate_matrix(100000, 50, 'short')

query.get_max_nodes_result(100000, [50, 250, 100, 500, 750, 1000], 0.005, 5000)
query.get_max_nodes_result(100000, [50, 250, 100, 500, 750, 1000], 0.01, 5000)
print """
bitlist.generate_matrix(100000, 100, 'short')
bitlist.generate_matrix(100000, 250, 'short')
bitlist.generate_matrix(100000, 50, 'short')

query.get_max_nodes_result(100000, [50, 250, 100, 500, 750, 1000], 0.005, 5000)
query.get_max_nodes_result(100000, [50, 250, 100, 500, 750, 1000], 0.01, 5000)
"""
'''
#query.get_max_nodes_result(100000, [500, 750, 1000, 1250, 1500], 0.02, 5000)
#query.get_placement_result(5000, 100, 1000)

"""
import CBitlist
def Test(w):
    print 'Testing for base = '+str(w)
    bitlist = getattr(CBitlist, 'CBitlist_'+str(w))()
    bitlist.Init(100)
    bitlist.Insert(0, 12, 0)
    bitlist.Insert(0, 12, w-1)
    bitlist.Insert(0, 13, 7)
    bitlist.PrintInfo()
    bitlist.PrintRow(0)
    l = bitlist.GetRowPy(0)
    print l
    bitlist.GetSize()

    bitlist.Insert(99, 10, 0)
    bitlist.Insert(99, 11, w-1)
    bitlist.Insert(99, 12, 7)
    bitlist.Insert(99, 13, 7)
    bitlist.PrintInfo()
    bitlist.PrintRow(99)
    l = bitlist.GetRowPy(99)
    print l
    bitlist.GetSize()

    print '*'*30


Test(8)
Test(16)
Test(32)
Test(64)

import bitlist

dtype = 'short'
for t_num, max_nodes in [(100000, 500), (100000, 750), (100000, 1000), (100000, 1250), (100000, 1500)]:
    print 'Computing t_num = %d, max_nodes = %d, dtype = %s' % (t_num, max_nodes, dtype)
    bitlist.generate_matrix(t_num, max_nodes, dtype)
    bitlist.get_answer(t_num, max_nodes, dtype)

t_num = 80000
max_nodes = 100
print 'Computing t_num = %d, max_nodes = %d, dtype = %s' % (t_num, max_nodes, dtype)
bitlist.generate_matrix(t_num, max_nodes, dtype)
print 'Generate matrix complete'
bitlist.get_answer(t_num, max_nodes, dtype)
bitlist.get_answer_bitlist(t_num, max_nodes, dtype)
"""


'''
dtype = 'middle'
for t_num, max_nodes in [(100, 20), (500, 20), (500, 50), (1000, 50), (5000, 100)]:
    print 'Computing t_num = %d, max_nodes = %d, dtype = %s'%(t_num, max_nodes, dtype)
    bitlist.generate_matrix(t_num, max_nodes, dtype)
    bitlist.get_answer(t_num, max_nodes, dtype)

dtype = 'short'
for t_num, max_nodes in [(100, 20), (100,50),(500, 20), (500, 50), (1000,20), (1000, 50),(1000,100)]:
    print 'Computing t_num = %d, max_nodes = %d, dtype = %s'%(t_num, max_nodes, dtype)
    bitlist.generate_matrix(t_num, max_nodes, dtype)
    bitlist.get_answer(t_num, max_nodes, dtype)

dtype = 'long'
for t_num, max_nodes in [(100, 20), (100, 50), (500, 20), (500, 50)]:
    print 'Computing t_num = %d, max_nodes = %d, dtype = %s'%(t_num, max_nodes, dtype)
    bitlist.generate_matrix(t_num, max_nodes, dtype)
    bitlist.get_answer(t_num, max_nodes, dtype)


dtype = 'short'
for t_num, max_nodes in [(5000,100),(5000,50)]:
    print 'Computing t_num = %d, max_nodes = %d, dtype = %s'%(t_num, max_nodes, dtype)
    bitlist.generate_matrix(t_num, max_nodes, dtype)
    bitlist.get_answer(t_num, max_nodes, dtype)


t_num = 5000
max_nodes = 50
dtype = 'middle'
print 'Computing t_num = %d, max_nodes = %d, dtype = %s'%(t_num, max_nodes, dtype)
bitlist.generate_matrix(t_num, max_nodes, dtype)
bitlist.get_answer(t_num, max_nodes, dtype)
'''
