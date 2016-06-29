# 6.00.2x Problem Set 5
# Graph optimization
#
# A set of data structures to represent graphs
#

class Node(object):
    def __init__(self, name):
        self.name = str(name)
    def getName(self):
        return self.name
    def __str__(self):
        return self.name
    def __repr__(self):
        return self.name
    def __eq__(self, other):
        return self.name == other.name
    def __ne__(self, other):
        return not self.__eq__(other)
    def __hash__(self):
        # Override the default hash method
        # Think: Why would we want to do this?
        return self.name.__hash__()

class Edge(object):
    def __init__(self, src, dest):
        self.src = src
        self.dest = dest
    def getSource(self):
        return self.src
    def getDestination(self):
        return self.dest
    def __str__(self):
        return '{0}->{1}'.format(self.src, self.dest)


class WeightedEdge(Edge):
    def __init__(self, src, dest, totalDist = 1.0, outdoorDist = 1.0):
        self.src = src
        self.dest = dest
        self.totalDist = totalDist
        self.outdoorDist = outdoorDist
    def getTotalDistance(self):
        return self.totalDist
    def getOutdoorDistance(self):
        return self.outdoorDist    
    def __str__(self):
        return str(self.src) + '->' + str(self.dest) + ' (' + str(self.totalDist) + ', '\
        + str(self.outdoorDist) + ')'
            

class Digraph(object):
    """
    A directed graph
    """
    def __init__(self):
        # A Python Set is basically a list that doesn't allow duplicates.
        # Entries into a set must be hashable (where have we seen this before?)
        # Because it is backed by a hashtable, lookups are O(1) as opposed to the O(n) of a list (nifty!)
        # See http://docs.python.org/2/library/stdtypes.html#set-types-set-frozenset
        self.nodes = set([])
        self.edges = {}
    def addNode(self, node):
        if node in self.nodes:
            # Even though self.nodes is a Set, we want to do this to make sure we
            # don't add a duplicate entry for the same node in the self.edges list.
            raise ValueError('Duplicate node')
        else:
            self.nodes.add(node)
            self.edges[node] = []
    def addEdge(self, edge):
        src = edge.getSource()
        dest = edge.getDestination()
        if not(src in self.nodes and dest in self.nodes):
            raise ValueError('Node not in graph')
        self.edges[src].append(dest)
    def childrenOf(self, node):
        return self.edges[node]
    def hasNode(self, node):
        return node in self.nodes
    def __str__(self):
        res = ''
        for k in self.edges:
            for d in self.edges[str(k)]:
                res = '{0}{1}->{2}\n'.format(res, k, d)
        return res[:-1]


class WeightedDigraph(Digraph):
    """
    A weighted directed graph
    """
    def __init__(self):
        # A Python Set is basically a list that doesn't allow duplicates.
        # Entries into a set must be hashable (where have we seen this before?)
        # Because it is backed by a hashtable, lookups are O(1) as opposed to the O(n) of a list (nifty!)
        # See http://docs.python.org/2/library/stdtypes.html#set-types-set-frozenset
        self.nodes = set([])
        self.edges = {}
    def addEdge(self, edge):
        src = edge.getSource()
        dest = edge.getDestination()
        totalDist = edge.getTotalDistance()
        outdoorDist = edge.getOutdoorDistance()
        if not(src in self.nodes and dest in self.nodes):
            raise ValueError('Node not in graph')
        self.edges[src].append([dest, (totalDist, outdoorDist)])
        
    def childrenOf(self, node):
        destNDistList = self.edges[node]
        if destNDistList != None:
            destList = []
            for elt in destNDistList:
                destList.append(elt[0])
            return destList

    def __str__(self):
        res = ''
        for sourceNode in self.edges:
            #print sourceNode
            for destNodeNDist in self.edges[sourceNode]:
                #res = '{0}{1}->{2} ({3}, {4})\n'.format(res, str(sourceNode), destNodeNDist[0], '{:.1f}'.format(destNodeNDist[1][0]), '{:.1f}'.format(destNodeNDist[1][1]))
                res = '{0}{1}->{2} ({3}, {4})\n'.format(res, str(sourceNode), destNodeNDist[0], float(destNodeNDist[1][0]), float(destNodeNDist[1][1]))
        
        return res[:-1]
        


'''
g = WeightedDigraph()
na = Node('a')
nb = Node('b')
nc = Node('c')
nd = Node('d')
g.addNode(na)
g.addNode(nb)
g.addNode(nc)
g.addNode(nd)
e1 = WeightedEdge(na, nb, 15, 10)

#print e1
#print e1.getTotalDistance()
#print e1.getOutdoorDistance()

e2 = WeightedEdge(na, nc, 14, 6)
e3 = WeightedEdge(nb, nc, 7, 4)
e4 = WeightedEdge(nb, nd, 5, 3)
e5 = WeightedEdge(nc, nd, 2, 2)

#print e2
#print e3

g.addEdge(e1)
g.addEdge(e2)
g.addEdge(e3)
g.addEdge(e4)
g.addEdge(e5)

print g

#print g.childrenOf(na)
#print g.childrenOf(nc)
'''

'''
map2 = WeightedDigraph()
na = Node('1')
nb = Node('2')
nc = Node('3')
nd = Node('4')
map2.addNode(na)
map2.addNode(nb)
map2.addNode(nc)
map2.addNode(nd)
e1 = WeightedEdge(na, nb, 10, 5)
e2 = WeightedEdge(na, nd, 5, 1)
e3 = WeightedEdge(nb, nc, 8, 5)
e4 = WeightedEdge(nd, nc, 8, 5)

#print e2
#print e3

map2.addEdge(e1)
map2.addEdge(e2)
map2.addEdge(e3)
map2.addEdge(e4)

print map2

'''
'''
map3 = WeightedDigraph()
na = Node('1')
nb = Node('2')
nc = Node('3')
nd = Node('4')
map3.addNode(na)
map3.addNode(nb)
map3.addNode(nc)
map3.addNode(nd)
e1 = WeightedEdge(na, nb, 10, 5)
e2 = WeightedEdge(na, nd, 15, 1)
e3 = WeightedEdge(nb, nc, 8, 5)
e4 = WeightedEdge(nd, nc, 8, 5)

map3.addEdge(e1)
map3.addEdge(e2)
map3.addEdge(e3)
map3.addEdge(e4)

print map3
'''
'''
map5 = WeightedDigraph()
na = Node('1')
nb = Node('2')
nc = Node('3')
nd = Node('4')
ne = Node('5')
map5.addNode(na)
map5.addNode(nb)
map5.addNode(nc)
map5.addNode(nd)
map5.addNode(ne)
e1 = WeightedEdge(na, nb, 5, 2)
e2 = WeightedEdge(nc, ne, 6, 3)
e3 = WeightedEdge(nb, nc, 20, 10)
e4 = WeightedEdge(nb, nd, 10, 5)
e5 = WeightedEdge(nd, nc, 2, 1)
e6 = WeightedEdge(nd, ne, 20, 10)

map5.addEdge(e1)
map5.addEdge(e2)
map5.addEdge(e3)
map5.addEdge(e4)
map5.addEdge(e5)
map5.addEdge(e6)

print map5

'''
map6 = WeightedDigraph()
na = Node('1')
nb = Node('2')
nc = Node('3')
nd = Node('4')
ne = Node('5')
map6.addNode(na)
map6.addNode(nb)
map6.addNode(nc)
map6.addNode(nd)
map6.addNode(ne)
e1 = WeightedEdge(na, nb, 5, 2)
e2 = WeightedEdge(nc, ne, 5, 1)
e3 = WeightedEdge(nb, nc, 20, 10)
e4 = WeightedEdge(nb, nd, 10, 5)
e5 = WeightedEdge(nd, nc, 5, 1)
e6 = WeightedEdge(nd, ne, 20, 1)

map6.addEdge(e1)
map6.addEdge(e2)
map6.addEdge(e3)
map6.addEdge(e4)
map6.addEdge(e5)
map6.addEdge(e6)

print map6


