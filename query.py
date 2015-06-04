# -*- coding: utf8 -*-

import pickle
import pandas as pd
import numpy as np
import sys
import time
import random
import tools
import quad
import os
import json
import math
import bitlist
from pympler import asizeof

from baidumap import Map
m = Map()

T1 = 'qt-bl'
T2 = 'qt-repl'
T3 = 'qt'
T4 = 'grid-bl'

'''
def traj_page_num(d, page_size, traj_tids):
    """
    Bug: here may come 0
    """
    #print traj_tids - set([0])
    traj_tids -= set([0])
    return sum([math.ceil(1.0*d.ix[tid]/page_size) for tid in traj_tids])

'''


def trajbase(dir_map, Q, points, width):
    t1 = time.time()
    trajs = candi_traj(Q, points, width)
    delta_time = time.time() - t1
    return traj_page_num(dir_map, trajs), delta_time


def traj1(pos, dir_map, Q, points, width, page_size=1000):
    t1 = time.time()
    regions = points_to_regions(points, width)
    p1, p2, p3, p4 = regions[0]
    cover_page_num = Q.cover_page_num(p1, p2, p3, p4, page_size)
    #ret = Q.meet_trajectories_set(points[0][0]-width, points[0][0]+width, points[0][1]-width, points[0][1]+width)
    #candi = region_cover_trajectory(d, ret, points[0][0]-width, points[0][0]+width, points[0][1]-width, points[0][1]+width)
    for r in regions[1:]:
        p1, p2, p3, p4 = r
        #ret = Q.meet_trajectories_detail_set(p[0]-width, p[0]+width, p[1]-width, p[1]+width)
        #candi &= region_cover_trajectory(d, ret, p[0]-width, p[0]+width, p[1]-width, p[1]+width)
        cover_page_num = Q.cover_page_num(p1, p2, p3, p4, page_size)
    delta_time = time.time() - t1
    return (cover_page_num + traj_page_num(dir_map, pos)), delta_time


def traj2(dir_map, Q, points, width):
    t1 = time.time()
    regions = points_to_regions(points, width)
    p1, p2, p3, p4 = regions[0]
    trajs_first = Q.meet_trajectories_set(p1, p2, p3, p4)
    delta_time = time.time() - t1
    return traj_page_num(dir_map, trajs_first), delta_time


def pos_traj(d, Q, points, width):
    regions = points_to_regions(points, width)
    candi = candi_traj(Q, points, width)
    for r in regions:
        p1, p2, p3, p4 = r
        print p1, p2, p3, p4
        true, part = Q.meet_trajectories_detail_set(p1, p2, p3, p4)
        part = candi & part
        part_true = set(trajectories_covered_by_region(d, part, p1, p2, p3, p4))
        candi = candi-(part-part_true)
    return candi


def candi_traj(Q, points, width):
    regions = points_to_regions(points, width)
    p1, p2, p3, p4 = regions[0]
    trajs = Q.meet_trajectories_set(p1, p2, p3, p4)
    for r in regions[1:]:
        p1, p2, p3, p4 = r
        trajs &= Q.meet_trajectories_set(p1, p2, p3, p4)
    return trajs


def trajectories_covered_by_region(d, tids, x0, x1, y0, y1):
    ret = []
    if type(tids) is int:
        tids = list([tids])
    for tid in tids:
        tmp = d.ix[tid]
        if type(tmp) == pd.core.series.Series:
            tmp = pd.DataFrame(tmp).T
        test = tmp[(tmp.x >= x0) & (tmp.x <= x1) & (tmp.y >= y0) & (tmp.y <= y1)]
        #print tid, type(test)
        if len(test) > 0:
            ret.append(tid)
    return ret


def addrs_to_points(addrs):
    points = []
    for addr in addrs:
        if type(addr) is tuple:
            points.append(addr)
        else:
            p = m.getLocation(addr, '镇江')
            points.append((p[1], p[0]))
    return points


def points_to_regions(points, w):
    regions = []
    for p in points:
        region = (p[0]-w, p[0]+w, p[1]-w, p[1]+w)
        regions.append(region)
    return regions


def test_case(pos, dir_map, Q, i_type, points, width, page_size=1000):

    print points
    t1 = time.time()
    if i_type == T1:
        rst, delta_time = trajbase(dir_map, Q, points, width)
    elif i_type == T2:
        rst, delta_time = traj1(pos, dir_map, Q, points, width, page_size)
    elif i_type == T3:
        rst, delta_time = traj2(dir_map, Q, points, width)
    elif i_type == T4:
        rst, delta_time = trajbase(dir_map, Q, points, width)
    else:
        print 'Error!'
    time_interval = time.time() - t1

    #pos_traj_set = pos_traj(d, Q, points, width)
    #trajs = candi_traj(Q, points, width)

    #print 'Candidates:', len(trajs), 'Real:', len(pos_traj_set)
    print 'Total Time: %.2f ms, Delta Time: %.2f ms, Disk IO: %d' % (time_interval*1000, delta_time*1000, rst)
    return delta_time, rst
    #return pos_traj_set, pos_traj(d, G, points, width)


def query_region_number(ans, d, dir_map, Q, A, i_type, page_size=1000):
    width = 0.01

    addrss = {'region_number_1': [["镇江站"],
                                  ["镇江站", "江苏大学附属医院"],
                                  ["镇江站", "江苏大学附属医院", "天正置业广场"],
                                  ["镇江站", "江苏大学附属医院", "天正置业广场", "世纪大厦"],
                                  ["镇江站", "江苏大学附属医院", "天正置业广场", "世纪大厦", "宝塔山公园"]],
    }
    """
        'region_number_2': [[(116.3177490234375, 39.89410400390625)], [(116.3507080078125, 39.89959716796875)], [(116.3507080078125, 39.90509033203125)], [(116.3507080078125, 39.93255615234375)]],
        'region_number_1': [["三里屯"],
                            ["三里屯", "西单"],
                            ["三里屯", "西单", "中关村"],
                            ["三里屯", "西单", "中关村", "北京大学"],
                            ["首都博物馆", "西单", "中关村", "北京大学 ", "三里屯", "地坛公园"]],
        'region_number_3': [["北京南站"],
                            ["北京南站", "北京大学"],
                            ["北京南站", "西单", "中关村"],
                            ["北京南站", "西单", "中关村", "北京大学"],
                            ["首都博物馆", "西单", "中关村", "北京大学 ", "三里屯", "地坛公园"]],
        'region_number_4': [["首都博物馆"],
                            ["首都博物馆", "北京大学"],
                            ["首都博物馆", "西单", "中关村"],
                            ["首都博物馆", "西单", "中关村", "北京大学"],
                            ["首都博物馆", "西单", "中关村", "北京大学 ", "北京南站", "地坛公园"]],
        'region_number_5': [["地坛公园"],
                            ["地坛公园", "北京大学"],
                            ["地坛公园", "西单", "中关村"],
                            ["地坛公园", "西单", "中关村", "北京大学"],
                            ["首都博物馆", "西单", "中关村", "北京大学 ", "三里屯", "地坛公园"]],
    """
    """
        'region_number_1': [[(116.42143249511719, 39.907493591308594)],
                            [(116.42143249511719, 39.907493591308594), (116.42967224121094, 39.93152618408203)],
                            [(116.42143249511719, 39.907493591308594), (116.42967224121094, 39.93152618408203), (116.47361755371094, 39.907493591308594)],
                            [(116.42143249511719, 39.907493591308594), (116.42967224121094, 39.93152618408203), (116.47361755371094, 39.907493591308594), (116.43516540527344, 39.921913146972656)],
                            [(116.42143249511719, 39.907493591308594), (116.42967224121094, 39.93152618408203), (116.47361755371094, 39.907493591308594), (116.43516540527344, 39.921913146972656), (116.31706237792969, 39.896507263183594), (116.47361755371094, 39.90680694580078)]],
        'region_number_2': [[(116.47361755371094, 39.907493591308594)],
                            [(116.47361755371094, 39.907493591308594), (116.43379211425781, 39.921913146972656)],
                            [(116.47361755371094, 39.907493591308594), (116.43379211425781, 39.921913146972656), (116.36924743652344, 39.88758087158203)],
                            [(116.47361755371094, 39.907493591308594), (116.43379211425781, 39.921913146972656), (116.36924743652344, 39.88758087158203), (116.45713806152344, 39.94800567626953)],
                            [(116.47361755371094, 39.907493591308594), (116.43379211425781, 39.921913146972656), (116.36924743652344, 39.88758087158203), (116.45713806152344, 39.94800567626953), (116.36512756347656, 39.946632385253906), (116.47224426269531, 39.907493591308594)]],
        'region_number_3': [[(116.43516540527344, 39.921913146972656)],
                            [(116.43516540527344, 39.921913146972656), (116.41319274902344, 39.907493591308594)],
                            [(116.43516540527344, 39.921913146972656), (116.41319274902344, 39.907493591308594), (116.47361755371094, 39.907493591308594)],
                            [(116.43516540527344, 39.921913146972656), (116.41319274902344, 39.907493591308594), (116.47361755371094, 39.907493591308594), (116.36924743652344, 39.88758087158203)],
                            [(116.43516540527344, 39.921913146972656), (116.41319274902344, 39.907493591308594), (116.47361755371094, 39.907493591308594), (116.36924743652344, 39.88758087158203), (116.47361755371094, 39.90680694580078), (116.42143249511719, 39.907493591308594)]],
        'region_number_4': [[(116.43516540527344, 39.921913146972656)],
                            [(116.43516540527344, 39.921913146972656), (116.34864807128906, 39.93907928466797)],
                            [(116.43516540527344, 39.921913146972656), (116.34864807128906, 39.93907928466797), (116.36924743652344, 39.88758087158203)],
                            [(116.43516540527344, 39.921913146972656), (116.34864807128906, 39.93907928466797), (116.36924743652344, 39.88758087158203), (116.36512756347656, 39.946632385253906)],
                            [(116.43516540527344, 39.921913146972656), (116.34864807128906, 39.93907928466797), (116.36924743652344, 39.88758087158203), (116.36512756347656, 39.946632385253906), "三里屯", "地坛公园"]],
        'region_number_5': [["地坛公园"],
                            ["地坛公园", "北京大学"],
                            ["地坛公园", "西单", "中关村"],
                            ["地坛公园", "西单", "中关村", "北京大学"],
                            ["首都博物馆", "西单", "中关村", "北京大学 ", "三里屯", "地坛公园"]],
    }
    """

    dir_map_random = wrap_trajs(dir_map, page_size)
    dir_map_dfs = wrap_trajs(dir_map[Q.blist.transform], page_size)
    t_sort = bitlist.bitlist_sort(A)
    dir_map_sort = wrap_trajs(dir_map[t_sort], page_size)

    for row in addrss.keys():
        for i in range(len(addrss[row])):
            addrs = addrss[row][i]
            print 'addrs: ',
            for addr in addrs:
                print addr,
            print
            points = addrs_to_points(addrs)
            _row = row + '_' + str(i)
            ans['test_param'][_row] = len(addrs)
            ans['test_for'][_row] = 'region_number'
            ans['page_size'][_row] = page_size
            ans['region_number'][_row] = len(addrs)
            ans['region_size'][_row] = average_size(points, width)
            ans['file_number'][_row] = int(len(d)*1.0/page_size)
            candi = []
            pos = []
            if i_type == T2:
                candi = candi_traj(Q, points, width)
                pos = pos_traj(d, Q, points, width)
                ans['candi_num'][_row] = len(candi)
                ans['pos_num'][_row] = len(pos)

            print 'Testing: %s,width: %.3f, #addrs: %d, test for: %s' % (i_type, width, len(points), 'region_number')
            print '#traj: %d, page_size: %d, #candi: %d, #pos: %d' % (len(d), page_size, len(candi), len(pos))
            """
            t_random = test_case(d, dir_map_random, Q, i_type, addrs, width, page_size)
            ans['random_time'][_row] = t_random[0]
            ans['random_IO'][_row] = t_random[1]
            """
            t_dfs = test_case(pos, dir_map_dfs, Q, i_type, points, width, page_size)
            ans['dfs_time'][_row] = t_dfs[0]
            ans['dfs_IO'][_row] = t_dfs[1]
            """
            t_sort = test_case(d, dir_map_sort, Q, i_type, addrs, width, page_size)
            ans['sort_time'][_row] = t_sort[0]
            ans['sort_IO'][_row] = t_sort[1]
            """

    return ans


def average_size(addrs, width):
    avg_dd = 0.0
    points = addrs
    """
    for addr in addrs:
        p = m.getLocation(addr, '北京')
        points.append((p[1], p[0]))
    """
    for p in points:
        avg_dd += tools.haversine(p[0]-width, p[1]-width, p[0]+width, p[1]+width)/1000.0
    avg_dd /= (1.0*len(points))
    ans = (avg_dd/math.sqrt(2))**2
    return ans


def query_region_size(ans, d, dir_map, Q, A, i_type, page_size=1000):

    #addrs = ["三里屯", "西单"]
    addrss = [
        ["三里屯", "西单", "地坛公园"],
        ["北京北站", "中关村", "西单"],
        ["北京南站", "西单", "三里屯"],
        ["三里屯", "北京大学", "首都博物馆"],
        ["地坛公园", "首都博物馆", "中关村"],
    ]
    widths = [0.001, 0.003, 0.005, 0.01, 0.02]
    name = 'region_size'

    dir_map_random = wrap_trajs(dir_map, page_size)
    dir_map_dfs = wrap_trajs(dir_map[Q.blist.transform], page_size)
    t_sort = bitlist.bitlist_sort(A)
    dir_map_sort = wrap_trajs(dir_map[t_sort], page_size)

    for i in range(len(widths)):
        width = widths[i]
        for j in range(len(addrss)):
            addrs = addrss[j]
            _row = "%s_%d_%d" % (name, i, j)
            ans['test_param'][_row] = width
            ans['test_for'][_row] = 'region_size'
            ans['region_number'][_row] = len(addrs)
            ans['region_size'][_row] = average_size(addrs, width)

            ans['page_size'][_row] = page_size
            t_random = test_case(d, dir_map_random, Q, i_type, addrs, width, page_size)
            ans['random_time'][_row] = t_random[0]
            ans['random_IO'][_row] = t_random[1]
            t_dfs = test_case(d, dir_map_dfs, Q, i_type, addrs, width, page_size)
            ans['dfs_time'][_row] = t_dfs[0]
            ans['dfs_IO'][_row] = t_dfs[1]
            t_sort = test_case(d, dir_map_sort, Q, i_type, addrs, width, page_size)
            ans['sort_time'][_row] = t_sort[0]
            ans['sort_IO'][_row] = t_sort[1]

    return ans


def wrap_trajs(d, page_size=1000):
    ret = {}
    did = 0
    ret[did] = []
    crt_num = 0
    traj_map = {}
    for tid, num in zip(d.index, d.values):
        if crt_num+num > page_size:
            did += 1
            ret[did] = []
            crt_num = 0
        ret[did].append(tid)
        traj_map[tid] = did
        crt_num += num
    return traj_map


def traj_page_num(dir_map, traj_tids):
    dir_set = set()
    for tid in traj_tids:
        dir_set.add(dir_map[tid])
    return len(dir_set)


def get_placement_result(traj_num, max_nodes, page_size, dtype='short', version='new'):
    ans = {}

    folder_name = './result/'
    file_name = ('RPL_%d.txt' % (traj_num))

    dir_map = get_dir_map(traj_num, dtype, version)
    d = bitlist.read_D(traj_num, dtype, version)

    width = 0.005
    addrss = [
        ["三里屯", "西单"],
        ["北京北站", "中关村"],
        ["北京南站", "西单"],
        ["三里屯", "北京大学"],
        ["地坛公园", "首都博物馆"],
    ]

    time_interval, tl = bitlist.read_Tl(traj_num, max_nodes, dtype, version, max_depth)
    time_interval, bl = bitlist.read_Bl(traj_num, max_nodes, dtype, version, max_depth)
    index = quad.Index(tl, bl)

    dir_map_random = wrap_trajs(dir_map, page_size)
    dir_map_dfs = wrap_trajs(dir_map[index.blist.transform], page_size)
    A = bitlist.read_A(traj_num, max_nodes, dtype, version, max_depth)
    t_sort = bitlist.bitlist_sort(A)
    dir_map_sort = wrap_trajs(dir_map[t_sort], page_size, page_size)

    row = 'placement_%d_%d' % (traj_num, max_nodes)
    for i in range(len(addrss)):
        addrs = addrss[i]
        _row = row + '_' + str(i)
        ans[_row] = {}
        ans[_row]['traj_num'] = traj_num
        ans[_row]['max_nodes'] = max_nodes
        _ans = test_case(d, dir_map_random, index, T1, addrs, width)
        ans[_row]['random_time'] = _ans[0]
        ans[_row]['random_IO'] = _ans[1]
        _ans = test_case(d, dir_map_dfs, index, T1, addrs, width)
        ans[_row]['dfs_time'] = _ans[0]
        ans[_row]['dfs_IO'] = _ans[1]
        _ans = test_case(d, dir_map_sort, index, T1, addrs, width)
        ans[_row]['sort_time'] = _ans[0]
        ans[_row]['sort_IO'] = _ans[1]

    f = open(folder_name+file_name, 'w')
    s = json.dump(ans, f, indent=True)
    print s
    f.close()


def query_max_nodes(d, dir_map, Q, index_type, width, page_size=1000):
    addrss = [
        ["三里屯", "西单", "地坛公园"],
        ["北京北站", "中关村", "西单"],
        ["北京南站", "西单", "三里屯"],
        ["三里屯", "北京大学", "首都博物馆"],
        ["地坛公园", "首都博物馆", "中关村"],
    ]
    ans = []
    for addrs in addrss:
        _ans = test_case(d, dir_map, Q, index_type, addrs, width, page_size)
        length = len(addrs)
        size = average_size(addrs, width)
        ans.append((_ans[0], _ans[1], length, size))
    return ans


def get_max_nodes_result(traj_num, max_nodes_list, width, page_size=1000, dtype='short', version='new'):
    ans = {}

    folder_name = './result/'
    file_name = ('RMN_%s_%d.txt' % (dtype, traj_num))

    if file_name in os.listdir(folder_name):
        f = open(folder_name+file_name, 'r')
        ans = json.load(f)
        f.close()

    dir_map = get_dir_map(traj_num, dtype, version)
    d = bitlist.read_D(traj_num, dtype, version)

    for max_nodes in max_nodes_list:
        for index_type in [T1, T2, T3]:
            print 'Processing', traj_num, max_nodes, index_type
            time_1, tl = bitlist.read_Tl(traj_num, max_nodes, dtype, version, max_depth)
            time_2, bl = bitlist.read_Bl(traj_num, max_nodes, dtype, version, max_depth)
            index = quad.Index(tl, bl)
            dir_map_dfs = wrap_trajs(dir_map[index.blist.transform], page_size)
            tmp = query_max_nodes(d, dir_map_dfs, index, index_type, width, page_size)
            for i in range(len(tmp)):
                row = "%s_%d_%d_%d_%f" % (index_type, traj_num, max_nodes, i, width)
                ans[row] = {}
                ans[row]['traj_num'] = traj_num
                ans[row]['max_nodes'] = max_nodes
                ans[row]['index_type'] = index_type
                ans[row]['time'] = tmp[i][0]
                ans[row]['IO'] = tmp[i][1]
                ans[row]['region_number'] = tmp[i][2]
                ans[row]['region_size'] = tmp[i][3]
                ans[row]['width'] = width
                ans[row]['page_size'] = page_size
                ans[row]['dtype'] = dtype

    f = open(folder_name+file_name, 'w')
    s = json.dump(ans, f, indent=True)
    print s
    f.close()


def get_dir_map(traj_num, dtype='short', version='new'):
    d = bitlist.read_D(traj_num, dtype, version)
    return d.groupby('tid').count()['id']


def get_query_result(traj_num, index_type, index_para, max_nodes, page_size, base, dtype, version, query_type, max_depth):
    """
    index_type = 'qt, qt-bl, qt-repl, grid-bl'
    query_type = 'size','number'
    index_para = {
                 'qt-bl': max_nodes,
                 'qt': max_nodes,
                 'qt-repl': max_nodes,
                 'grid-bl': depth,
                 }
    """
    print 'Processing', traj_num, index_type, index_para

    ans = {}

    folder_name = './result/'
    if query_type == 'size':
        file_name = ('RZ_%s_%d_%s_%d_%d_%d_%d.txt' % (dtype, traj_num, index_type, index_para, max_depth, page_size, base))
    elif query_type == 'number':
        file_name = ('RN_%s_%d_%s_%d_%d_%d_%d.txt' % (dtype, traj_num, index_type, index_para, max_depth, page_size, base))
    else:
        print 'Error query_type = ', query_type

    ans['traj_num'] = traj_num
    ans['index_type'] = index_type
    ans['index_para'] = index_para
    ans['base'] = base
    ans['page_size'] = page_size
    ans['dtype'] = dtype
    ans['max_depth'] = max_depth

    print 'Read TL Start'
    time_1, tl = bitlist.read_Tl(traj_num, index_para, index_type, dtype, version, max_depth)
    print 'Read TL End'
    print 'Read BL Start'
    time_2, bl = bitlist.read_Bl(traj_num, index_para, base, index_type, dtype, version, max_depth)
    print 'Read BL End'
    if index_type[0] is 'q':
        A = bitlist.read_A(traj_num, index_para, dtype, version, max_depth)
    elif index_type[0] is 'g':
        A = bitlist.read_AG(traj_num, index_para, dtype, version, max_depth)
    else:
        print 'Error index_type = ', index_type
    index = quad.Index(tl, bl)

    dir_map = get_dir_map(traj_num, dtype, version)
    d = bitlist.read_D(traj_num, dtype, version)

    if index_type in [T1, T4]:
        ans['index_size'] = tl.get_size()+bl.bitlist.GetSize()
        ans['build_time'] = time_1+time_2
    else:
        ans['index_size'] = tl.get_size()
        ans['build_time'] = time_1
    ans['leaf_number'] = tl.leaf_number()

    ans['random_time'] = {}
    ans['random_IO'] = {}
    ans['dfs_time'] = {}
    ans['dfs_IO'] = {}
    ans['sort_time'] = {}
    ans['sort_IO'] = {}
    ans['test_param'] = {}
    ans['test_for'] = {}
    ans['page_size'] = {}
    ans['region_number'] = {}
    ans['region_size'] = {}
    ans['file_number'] = {}
    ans['candi_num'] = {}
    ans['pos_num'] = {}
    if query_type == 'size':
        ans = query_region_size(ans, d, dir_map, index, A, index_type, page_size)
    elif query_type == 'number':
        ans = query_region_number(ans, d, dir_map, index, A, index_type, page_size)

    """
    if file_name in os.listdir(folder_name):
        f = open(folder_name+file_name, 'r')
        _ans = json.load(f)
        f.close()
    """

    f = open(folder_name+file_name, 'w')
    s = json.dump(ans, f, indent=True)
    print s
    f.close()


def get_region_size_result(traj_num, index_type, index_para, page_size, base, dtype, version, max_nodes=1024):
    get_query_result(traj_num, index_type, index_para, max_nodes,  page_size, base, dtype, version, 'size', max_nodes)


def get_region_number_result(traj_num, index_type, index_para, page_size, base, dtype, version, max_nodes=1024):
    get_query_result(traj_num, index_type, index_para, max_nodes, page_size, base, dtype, version, 'number', max_nodes)

"""
        'region_number_1': [["三里屯"],
                            ["三里屯", "西单"],
                            ["三里屯", "西单", "中关村"],
                            ["三里屯", "西单", "中关村", "北京大学"],
                            ["首都博物馆", "西单", "中关村", "北京大学 ", "三里屯", "地坛公园"]],
        'region_number_3': [["北京南站"],
                            ["北京南站", "北京大学"],
                            ["北京南站", "西单", "中关村"],
                            ["北京南站", "西单", "中关村", "北京大学"],
                            ["首都博物馆", "西单", "中关村", "北京大学 ", "三里屯", "地坛公园"]],
        'region_number_4': [["首都博物馆"],
                            ["首都博物馆", "北京大学"],
                            ["首都博物馆", "西单", "中关村"],
                            ["首都博物馆", "西单", "中关村", "北京大学"],
                            ["首都博物馆", "西单", "中关村", "北京大学 ", "北京南站", "地坛公园"]],
        'region_number_5': [["地坛公园"],
                            ["地坛公园", "北京大学"],
                            ["地坛公园", "西单", "中关村"],
                            ["地坛公园", "西单", "中关村", "北京大学"],
                            ["首都博物馆", "西单", "中关村", "北京大学 ", "三里屯", "地坛公园"]],
"""