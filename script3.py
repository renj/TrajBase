import bitlist
import preprocess

for day in ['02','03','04','05','06','09']:
    preprocess.trim(day)
    preprocess.split_from_trim(day, 10)
for day in ['02','03','04','05','06','09']:
    preprocess.split(day, 10)
#bitlist.get_answer(3988, 500,'0110','new')
#preprocess.split('01',10)
'''
for day in ['02','03','04','05','06','09']:
    preprocess.clean(day)
'''


"""
bitlist.get_answer(100000, 3000, 'short', 'old')
bitlist.get_answer(100000, 5000, 'short', 'old')
bitlist.get_answer(100000, 4000, 'short', 'old')
bitlist.get_answer(500, 100, 'dense250', 'new')
bitlist.get_answer_bitlist(500, 100, 'dense250', 'new')
bitlist.get_answer(5000, 100, 'dense250', 'new')
bitlist.get_answer_bitlist(5000, 100, 'dense250', 'new')
bitlist.get_answer(40000, 100, 'dense250', 'new')
bitlist.get_answer(60000, 100, 'dense250', 'new')
bitlist.get_answer(80000, 100, 'dense250', 'new')
"""
#bitlist.get_answer_bitlist(10000, 100, 'dense250', 'new')
#bitlist.get_answer(5000, 200, 'dense', 'new')

'''
dtype = 'middle'
for t_num, max_nodes in [(5000, 50)]:
    print 'Computing t_num = %d, max_nodes = %d, dtype = %s' % (t_num, max_nodes, dtype)
    bitlist.get_answer(t_num, max_nodes, dtype)
    #bitlist.get_answer_bitlist(t_num, max_nodes, dtype)
for t_num, max_nodes in [(5000, 200), (5000, 300), (5000, 500), (5000, 50)]:
    print 'Computing t_num = %d, max_nodes = %d, dtype = %s' % (t_num, max_nodes, dtype)
    #bitlist.generate_matrix(t_num, max_nodes, dtype)
    #bitlist.get_answer_bitlist(t_num, max_nodes, dtype)
    bitlist.get_answer_bitlist(t_num, max_nodes, dtype)
print """
for t_num, max_nodes in [(MIDDLE, 2000), (MIDDLE, 500), (MIDDLE, 1500), (MIDDLE, 1000)]:
"""
'''
