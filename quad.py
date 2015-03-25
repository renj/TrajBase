max_id = 1000

class QuadTree:

	MAX_DEPTH = 30
	MAX_NODES = 30

	def __init__(self, cid, depth = 0):
		self.nodes = {}
		self.children = []
		self.cid = cid
		self.depth = depth
		global max_id
		max_id += 1
		self.id = str(max_id)

	def insert(self, tid, hashid):
		#alert(hashid[:len(self.cid)] == cid)
		if len(self.children) == 0:
			if tid not in self.nodes.keys():
				if len(self.nodes) >= self.MAX_NODES:
					if self.depth == self.MAX_DEPTH:
						print 'Insert Failure: depth overload'
					else:
						self._split()
						self._insert_into_children(tid, hashid)
					return
				else:
					self.nodes[tid] = set()
			self.nodes[tid].add(hashid)
		else:
			self._insert_into_children(tid, hashid)

	def _split(self):
		self.children = [ \
			QuadTree(self.cid+'0', self.depth+1), 
			QuadTree(self.cid+'1', self.depth+1), 
			QuadTree(self.cid+'2', self.depth+1), 
			QuadTree(self.cid+'3', self.depth+1), 
			]
		for tid in self.nodes.keys():
			for hashid in self.nodes[tid]:
				self._insert_into_children(tid, hashid)
		self.nodes = {}

	def _insert_into_children(self, tid, hashid):
		#print '_insert',self.cid, hashid, hashid[len(self.cid)]
		child = int(hashid[len(self.cid)])
		self.children[child].insert(tid, hashid)

	def display(self):
		#if len(self.nodes) != 0: print len(self.nodes)
		if len(self.children) == 0:
			if len(self.nodes) == 0: return
			print '*'*self.depth, self.cid, self.id, len(self.nodes)
		else:
			for child in self.children:
				child.display()

	def generate_linked_list(self):
		ret = ''
		if len(self.children) == 0:
			for tid in self.nodes.keys():
				ret += self._change_cid()+'\t'+tid+'\n'
		else:
			for child in self.children:
				ret += child.generate_linked_list()
		return ret

	def _change_cid(self):
		#self.max_id += 1
		#return self.max_id
		return self.id