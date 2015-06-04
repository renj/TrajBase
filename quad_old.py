from pympler import asizeof

g_max_depth = 1024
g_max_nodes = 100


class QuadTree:

    def __init__(self, depth=0,
                 x0=-180.0, x1=180.0, y0=-90.0, y1=90.0, ):
        """
        x0, y0 is the left bottom point
        x1, y1 is the right up point
        x0 < x1
        y0 < y1
        """
        self.nodes = {}
        self.children = []
        self.depth = depth
        self.x0 = x0
        self.x1 = x1
        self.y0 = y0
        self.y1 = y1

    def insert(self, tid, x, y):
        if self.is_leaf():
            if tid not in self.nodes.keys():
                if len(self.nodes) >= g_max_nodes:
                    if self.depth == g_max_depth:
                        print 'Insert Failure: depth overload'
                    else:
                        self._split()
                        self._insert_into_children(tid, x, y)
                    return
                else:
                    self.nodes[tid] = []
            self.nodes[tid].append((x, y))
        else:
            self._insert_into_children(tid, x, y)

    def _split(self):
        x_mid = (self.x0+self.x1) / 2
        y_mid = (self.y0+self.y1) / 2
        self.children = [
            QuadTree(self.depth+1, x0=self.x0, x1=x_mid, y0=self.y0, y1=y_mid),
            QuadTree(self.depth+1, x0=self.x0, x1=x_mid, y0=y_mid, y1=self.y1),
            QuadTree(self.depth+1, x0=x_mid, x1=self.x1, y0=self.y0, y1=y_mid),
            QuadTree(self.depth+1, x0=x_mid, x1=self.x1, y0=y_mid, y1=self.y1),
            ]
        for tid in self.nodes.keys():
            for x, y in self.nodes[tid]:
                self._insert_into_children(tid, x, y)
        self.nodes = {}

    def _insert_into_children(self, tid, x, y):
        for child in self.children:
            if child.is_contain(x, y):
                child.insert(tid, x, y)
                break

    def display(self):
        #if len(self.nodes) != 0: print len(self.nodes)
        if len(self.children) == 0:
            if len(self.nodes) == 0:
                return
            print '*'*self.depth, self.id, len(self.nodes)
        else:
            for child in self.children:
                child.display()

    """
    def generate_linked_list(self):
        ret = ''
        if len(self.children) == 0:
            for tid in self.nodes.keys():
                ret += str(self._change_cid())+'\t'+str(tid)+'\n'
        else:
            for child in self.children:
                ret += child.generate_linked_list()
        return ret
    """

    def generate_list(self):
        if self.is_leaf():
            return [self.nodes.keys()]
        else:
            ret = []
            for child in self.children:
                ret += child.generate_list()
            return ret

    def is_leaf(self):
        if len(self.children) == 0:
            return True
        return False

    def leaf_number(self):
        if self.is_leaf():
            return 1
        else:
            return sum([child.leaf_number() for child in self.children])

    def generate_leaf_list(self):
        if self.is_leaf():
            return [self.nodes.keys()]
        else:
            ret = []
            for child in self.children:
                _ret = child.generate_leaf_list()
                if _ret != []:
                    ret += _ret
            return ret

    def is_covered(self, x0, x1, y0, y1):
        return not ((x0 > self.x1) or (x1 < self.x0) or (y1 < self.y0) or (y0 > self.y1))

    def is_totaly_covered(self, x0, x1, y0, y1):
        return ((x0 < self.x0) and (x1 > self.x1) and (y0 < self.y0) and (y1 > self.y1))

    def is_contain(self, x, y):
        return ((x > self.x0) and (x < self.x1) and (y > self.y0) and (y < self.y1))

    def cover_leaf_num(self, x0, x1, y0, y1):
        if self.is_covered(x0, x1, y0, y1):
            if self.is_leaf():
                return 1
            else:
                return sum([child.cover_leaf_num(x0, x1, y0, y1) for child in self.children])
        return 0

    def cover_page_num(self, x0, x1, y0, y1, page_size):
        import math
        if self.is_covered(x0, x1, y0, y1):
            if self.is_leaf():
                return int(math.ceil(1.0 * sum([len(self.nodes[k]) for k in self.nodes.keys()]) / page_size))
            else:
                return sum([child.cover_page_num(x0, x1, y0, y1, page_size) for child in self.children])
        return 0

    def get_tid(self):
        if self.is_leaf():
            return self.nodes.keys()
        else:
            tids = []
            for child in self.children:
                tids += child.get_tid()
            return tids

    def get_tid_depth(self, depth=0):
        if self.is_leaf():
            return zip(self.nodes.keys(), [depth]*len(self.nodes))
        else:
            tids = []
            for child in self.children:
                tids += child.get_tid_depth(depth+1)
            return tids

    """
    def cover_leaf_list(self, x0, x1, y0, y1):
        if self.is_covered(x0, x1, y0, y1):
            if self.is_leaf():
                return self.nodes.keys()
            else:
                ret = []
                for child in self.children:
                    _ret = child.cover_leaf_list(x0, x1, y0, y1)
                    if _ret != None:
                        ret += _ret
                return ret
    """

    def meet_trajectories_detail_list(self, x0, x1, y0, y1):
        if self.is_covered(x0, x1, y0, y1):
            if self.is_leaf():
                return zip(self.nodes.keys(), [self.is_totaly_covered(x0, x1, y0, y1)]*len(self.nodes))
            else:
                ret = []
                for child in self.children:
                    _ret = child.meet_trajectories_detail_list(x0, x1, y0, y1)
                    if _ret is not None:
                        ret += _ret
                return ret

    def meet_trajectories_detail_set(self, x0, x1, y0, y1):
        node_list = self.meet_trajectories_detail_list(x0, x1, y0, y1)
        total_set = set([l[0] for l in node_list if l[1] is True])
        part_set = set([l[0] for l in node_list if l[1] is False])-total_set
        return total_set, part_set

    def meet_trajectories_set(self, x0, x1, y0, y1):
        total, part = self.meet_trajectories_detail_set(x0, x1, y0, y1)
        return total | part

    def cover_trajectory_detail_list(self, x0, x1, y0, y1):
        if self.is_covered(x0, x1, y0, y1):
            if self.is_leaf():
                ret = []
                flag = False
                for t in self.nodes.keys():
                    for (x, y) in self.nodes[t]:
                        #print x,y
                        if ((x > x0) and (x < x1) and (y > y0) and (y < y1)):
                            flag = True
                            break
                    ret.append((t, flag))
                return ret
            else:
                ret = []
                for child in self.children:
                    _ret = child.cover_trajectory_detail_list(x0, x1, y0, y1)
                    if _ret is not None:
                        ret += _ret
                return ret

    def cover_trajectory_detail_set(self, x0, x1, y0, y1):
        node_list = self.cover_trajectory_detail_list(x0, x1, y0, y1)
        pos_set = set([l[0] for l in node_list if l[1] is True])
        neg_set = set([l[0] for l in node_list if l[1] is False])-pos_set
        return pos_set, neg_set

    def cover_trajectories_set(self, x0, x1, y0, y1):
        pos, neg = self.cover_trajectories_detail_set(x0, x1, y0, y1)
        return pos | neg

    """
    def _change_cid(self):
        #return self.max_id
        return self.id
    """

    def remove_trajectories(self):
        if self.is_leaf() is True:
            for k in self.nodes.keys():
                self.nodes[k] = []
        else:
            for child in self.children:
                child.remove_trajectories()

    def get_size(self):
        return asizeof.asizeof(self)


class GridTree(QuadTree):

    def __init__(self, max_depth, depth=0,
                 x0=-180.0, x1=180.0, y0=-90.0, y1=90.0, ):
        """
        x0, y0 is the left bottom point
        x1, y1 is the right up point
        x0 < x1
        y0 < y1
        """
        self.nodes = {}
        self.children = []
        self.depth = depth
        self.max_depth = max_depth
        self.x0 = x0
        self.x1 = x1
        self.y0 = y0
        self.y1 = y1

    def insert(self, tid, x, y):
        if self.is_leaf():
            if tid not in self.nodes.keys():
                self.nodes[tid] = []
            self.nodes[tid].append((x, y))
        else:
            if self.children == []:
                self._split()
            self._insert_into_children(tid, x, y)

    def _split(self):
        x_mid = (self.x0+self.x1) / 2
        y_mid = (self.y0+self.y1) / 2
        self.children = [
            GridTree(self.max_depth, self.depth+1, x0=self.x0, x1=x_mid, y0=self.y0, y1=y_mid),
            GridTree(self.max_depth, self.depth+1, x0=self.x0, x1=x_mid, y0=y_mid, y1=self.y1),
            GridTree(self.max_depth, self.depth+1, x0=x_mid, x1=self.x1, y0=self.y0, y1=y_mid),
            GridTree(self.max_depth, self.depth+1, x0=x_mid, x1=self.x1, y0=y_mid, y1=self.y1),
            ]
        for tid in self.nodes.keys():
            for x, y in self.nodes[tid]:
                self._insert_into_children(tid, x, y)
        self.nodes = {}

    def _insert_into_children(self, tid, x, y):
        for child in self.children:
            if child.is_contain(x, y):
                child.insert(tid, x, y)
                break

    def is_leaf(self):
        return self.depth == self.max_depth
