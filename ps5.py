# 6.00.2x Problem Set 5
# Graph optimization
# Finding shortest paths through MIT buildings
#

import string
# This imports everything from `graph.py` as if it was defined in this file!
from graph import * 

#
# Problem 2: Building up the Campus Map
#
# Before you write any code, write a couple of sentences here 
# describing how you will model this problem as a graph. 

# This is a helpful exercise to help you organize your
# thoughts before you tackle a big design problem!
#

'''
This program will read info of MIT buildings from a file, then build a graph,
where the buildings are nodes, the paths buildings are edges, and the edges have
"weights" representing their total distance and distance outdoor.
'''

def load_map(mapFilename):
    """ 
    Parses the map file and constructs a directed graph

    Parameters: 
        mapFilename : name of the map file

    Assumes:
        Each entry in the map file consists of the following four positive 
        integers, separated by a blank space:
            From To TotalDistance DistanceOutdoors
        e.g.
            32 76 54 23
        This entry would become an edge from 32 to 76.

    Returns:
        a directed graph representing the map
    """
    print "Loading map from file..."
    g = WeightedDigraph()
        
    inFile = open(mapFilename, 'r', 0)
    for line in inFile:
        s, t, w, v = line.split()
        #print "Edge "+s+", "+t+", "+w+", "+v+" is read from file"
        try: 
            g.addNode(Node(s))
            #print "Node "+s +" added to graph"
        except ValueError:
            pass
        
        try: 
            g.addNode(Node(t))
            #print "Node "+s +" added to graph"
        except ValueError:
            pass
        
        edge = WeightedEdge(Node(s), Node(t), int(w), int(v))
        #print "Edge " + str(edge) +" added to graph"
        g.addEdge(edge)
                
    inFile.close()

    return g
    

#mitMap = load_map("mit_map.txt")
#print isinstance(mitMap, Digraph)
#print isinstance(mitMap, WeightedDigraph)   
     
#nodes = mitMap.nodes
#print nodes

#edges = mitMap.edges
#print edges

#
# Problem 3: Finding the Shortest Path using Brute Force Search
#
# State the optimization problem as a function to minimize
# and what the constraints are
#

def totalDistOnPath(graph, path):
    # function returns the total path lengths (total dist & total outdoor dist) of the path
    
    totalDist = 0
    outdoorDist = 0

    for i in range(len(path)-1): 
        isrc = path[i]
        ides = path[i+1]
        for edge in graph.edges[isrc]:
            if edge[0] == ides:
                totalDist += int(edge[1][0])
                outdoorDist += int(edge[1][1])
            
    #print totalDist, outdoorDist
    
    return (totalDist, outdoorDist)
   

def DFSShortest(graph, start, end, totalDistLim, outdoorDistLim, path = [], shortest = {}):
    #assumes graph is a Digraph
    #assumes start and end are nodes in graph
    path = path + [start]
    #print 'Current dfs path:', printPath(path)
    if start == end:
        return (path, shortest)

    newPath = [] 
    
    for node in graph.childrenOf(start):
        #print 'considering Node: ' + str(node) + ' as child of '+str(start)
        #print 'current path is: ' + str(path)
        
        if node not in path: #avoid cycles
            #print totalOutdoorDistOnPath(graph, start, node)    
            distOfPotentialPath = totalDistOnPath(graph, path+[node])
            
            #print distOfPotentialPath
            
            if shortest == None or \
            (distOfPotentialPath[0] <= totalDistLim and distOfPotentialPath[1] <= outdoorDistLim):
            
                #print 'begin recursive call from ' + str(node) + '->' + str(end) + '; current path: '+ str(path) + '; current shortest path: ' + str(shortest)
                
                newPath, newShortest = DFSShortest(graph,node,end,totalDistLim, outdoorDistLim, path)  
                
                #print newShortest, shortest
                #print newShortest.keys(), shortest.keys()
                
                if len(newShortest) != 0:
                    if len(shortest) == 0:
                        shortest = newShortest
                    else:
                        if newShortest.keys() < shortest.keys():
                            shortest = newShortest
                
                #print 'result of recursive call from ' + str(node)+'->'+str(end)+ '; current path: '+ str(newPath) + '; current shortest path: ' + str(shortest) 
        
                if (end in newPath) and (start in newPath):
                    newDist = totalDistOnPath(graph, newPath)[0]
                    if (len(shortest) == 0 or newDist < min(shortest.keys())):
                        shortest = {}
                        shortest[newDist] = newPath
                         
    return (newPath, shortest)
                    
#print DFSShortest(g, Node('a'), Node('d'), 25, 12)[1].values()[0]



def bruteForceSearch(digraph, start, end, maxTotalDist, maxDistOutdoors):    
    """
    Finds the shortest path from start to end using brute-force approach.
    The total distance travelled on the path must not exceed maxTotalDist, and
    the distance spent outdoor on this path must not exceed maxDistOutdoors.

    Parameters: 
        digraph: instance of class Digraph or its subclass
        start, end: start & end building numbers (strings)
        maxTotalDist : maximum total distance on a path (integer)
        maxDistOutdoors: maximum distance spent outdoors on a path (integer)

    Assumes:
        start and end are numbers for existing buildings in graph

    Returns:
        The shortest-path from start to end, represented by 
        a list of building numbers (in strings), [n_1, n_2, ..., n_k], 
        where there exists an edge from n_i to n_(i+1) in digraph, 
        for all 1 <= i < k.

        If there exists no path that satisfies maxTotalDist and
        maxDistOutdoors constraints, then raises a ValueError.
    """
    path = DFSShortest(digraph, Node(start), Node(end), maxTotalDist, maxDistOutdoors)

    if len(path[1]) != 0:
        sPath = []
        for elt in path[1].values()[0]:
            sPath.append(str(elt))
        
        return sPath
    else:
        raise ValueError()


#print bruteForceSearch(g, Node('a'), Node('d'), 25, 12)
#print bruteForceSearch(map2, "1", "3", 100, 100)   
#print bruteForceSearch(map2, "1", "3", 10, 10)
#print bruteForceSearch(map3, "1", "3", 100, 100)
#print bruteForceSearch(map3, "1", "3", 10, 10)
#print bruteForceSearch(map5, "1", "3", 17, 8)
#print bruteForceSearch(map5, "1", "5", 23, 11)
#print bruteForceSearch(map5, "4", "5", 21, 11)
#print bruteForceSearch(map5, "5", "1", 100, 100)
#print bruteForceSearch(map6, "1", "3", 100, 100)
#print bruteForceSearch(map6, "1", "5", 35, 9)
#print bruteForceSearch(map6, "1", "5", 35, 8)
#print bruteForceSearch(map6, "4", "5", 21, 11)
#print bruteForceSearch(map6, "4", "5", 21, 1)
#print bruteForceSearch(map6, "4", "5", 19, 1)
#print bruteForceSearch(map6, "3", "2", 100, 100)
#print bruteForceSearch(map6, "4", "5", 8, 2)


#
# Problem 4: Finding the Shorest Path using Optimized Search Method
#
def directedDFS(digraph, start, end, maxTotalDist, maxDistOutdoors):
    """
    Finds the shortest path from start to end using directed depth-first.
    search approach. The total distance travelled on the path must not
    exceed maxTotalDist, and the distance spent outdoor on this path must
	not exceed maxDistOutdoors.

    Parameters: 
        digraph: instance of class Digraph or its subclass
        start, end: start & end building numbers (strings)
        maxTotalDist : maximum total distance on a path (integer)
        maxDistOutdoors: maximum distance spent outdoors on a path (integer)

    Assumes:
        start and end are numbers for existing buildings in graph

    Returns:
        The shortest-path from start to end, represented by 
        a list of building numbers (in strings), [n_1, n_2, ..., n_k], 
        where there exists an edge from n_i to n_(i+1) in digraph, 
        for all 1 <= i < k.

        If there exists no path that satisfies maxTotalDist and
        maxDistOutdoors constraints, then raises a ValueError.
    """
    
    path = DFSShortest(digraph, Node(start), Node(end), maxTotalDist, maxDistOutdoors)

    if len(path[1]) != 0:
        sPath = []
        for elt in path[1].values()[0]:
            sPath.append(str(elt))
        
        return sPath
    else:
        raise ValueError()
    
    
    

# Uncomment below when ready to test
#### NOTE! These tests may take a few minutes to run!! ####
# if __name__ == '__main__':
#     Test cases

mitMap = load_map("mit_map.txt")
'''
print isinstance(mitMap, Digraph)
print isinstance(mitMap, WeightedDigraph)
print 'nodes', mitMap.nodes
print 'edges', mitMap.edges
'''

LARGE_DIST = 1000000

#     Test case 1
'''
print "---------------"
print "Test case 1:"
print "Find the shortest-path from Building 32 to 56"
expectedPath1 = ['32', '56']
brutePath1 = bruteForceSearch(mitMap, '32', '56', LARGE_DIST, LARGE_DIST)
dfsPath1 = directedDFS(mitMap, '32', '56', LARGE_DIST, LARGE_DIST)
print "Expected: ", expectedPath1
print "Brute-force: ", brutePath1
print "DFS: ", dfsPath1
print "Correct? BFS: {0}; DFS: {1}".format(expectedPath1 == brutePath1, expectedPath1 == dfsPath1)
'''
#     Test case 2
'''
print "---------------"
print "Test case 2:"
print "Find the shortest-path from Building 32 to 56 without going outdoors"
expectedPath2 = ['32', '36', '26', '16', '56']
brutePath2 = bruteForceSearch(mitMap, '32', '56', LARGE_DIST, 0)
dfsPath2 = directedDFS(mitMap, '32', '56', LARGE_DIST, 0)
print "Expected: ", expectedPath2
print "Brute-force: ", brutePath2
print "DFS: ", dfsPath2
print "Correct? BFS: {0}; DFS: {1}".format(expectedPath2 == brutePath2, expectedPath2 == dfsPath2)
'''

#     Test case 3
'''
print "---------------"
print "Test case 3:"
print "Find the shortest-path from Building 2 to 9"
expectedPath3 = ['2', '3', '7', '9']
brutePath3 = bruteForceSearch(mitMap, '2', '9', LARGE_DIST, LARGE_DIST)
dfsPath3 = directedDFS(mitMap, '2', '9', LARGE_DIST, LARGE_DIST)
print "Expected: ", expectedPath3
print "Brute-force: ", brutePath3
print "DFS: ", dfsPath3
print "Correct? BFS: {0}; DFS: {1}".format(expectedPath3 == brutePath3, expectedPath3 == dfsPath3)
'''

#     Test case 4
'''
print "---------------"
print "Test case 4:"
print "Find the shortest-path from Building 2 to 9 without going outdoors"
expectedPath4 = ['2', '4', '10', '13', '9']
brutePath4 = bruteForceSearch(mitMap, '2', '9', LARGE_DIST, 0)
dfsPath4 = directedDFS(mitMap, '2', '9', LARGE_DIST, 0)
print "Expected: ", expectedPath4
print "Brute-force: ", brutePath4
print "DFS: ", dfsPath4
print "Correct? BFS: {0}; DFS: {1}".format(expectedPath4 == brutePath4, expectedPath4 == dfsPath4)
'''


#     Test case 5
'''
print "---------------"
print "Test case 5:"
print "Find the shortest-path from Building 1 to 32"
expectedPath5 = ['1', '4', '12', '32']
brutePath5 = bruteForceSearch(mitMap, '1', '32', LARGE_DIST, LARGE_DIST)
dfsPath5 = directedDFS(mitMap, '1', '32', LARGE_DIST, LARGE_DIST)
print "Expected: ", expectedPath5
print "Brute-force: ", brutePath5
print "DFS: ", dfsPath5
print "Correct? BFS: {0}; DFS: {1}".format(expectedPath5 == brutePath5, expectedPath5 == dfsPath5)
'''


#     Test case 6
'''
print "---------------"
print "Test case 6:"
print "Find the shortest-path from Building 1 to 32 without going outdoors"
expectedPath6 = ['1', '3', '10', '4', '12', '24', '34', '36', '32']
brutePath6 = bruteForceSearch(mitMap, '1', '32', LARGE_DIST, 0)
dfsPath6 = directedDFS(mitMap, '1', '32', LARGE_DIST, 0)
print "Expected: ", expectedPath6
print "Brute-force: ", brutePath6
print "DFS: ", dfsPath6
print "Correct? BFS: {0}; DFS: {1}".format(expectedPath6 == brutePath6, expectedPath6 == dfsPath6)
'''


#     Test case 7
'''
print "---------------"
print "Test case 7:"
print "Find the shortest-path from Building 8 to 50 without going outdoors"
bruteRaisedErr = 'No'
dfsRaisedErr = 'No'
try:
    bruteForceSearch(mitMap, '8', '50', LARGE_DIST, 0)
except ValueError:
    bruteRaisedErr = 'Yes'
    
try:
    directedDFS(mitMap, '8', '50', LARGE_DIST, 0)
except ValueError:
    dfsRaisedErr = 'Yes'
    
print "Expected: No such path! Should throw a value error."
print "Did brute force search raise an error?", bruteRaisedErr
print "Did DFS search raise an error?", dfsRaisedErr
'''

#     Test case 8
'''
print "---------------"
print "Test case 8:"
print "Find the shortest-path from Building 10 to 32 without walking"
print "more than 100 meters in total"
bruteRaisedErr = 'No'
dfsRaisedErr = 'No'
try:
    bruteForceSearch(mitMap, '10', '32', 100, LARGE_DIST)
except ValueError:
    bruteRaisedErr = 'Yes'
    
try:
    directedDFS(mitMap, '10', '32', 100, LARGE_DIST)
except ValueError:
    dfsRaisedErr = 'Yes'
    
print "Expected: No such path! Should throw a value error."
print "Did brute force search raise an error?", bruteRaisedErr
print "Did DFS search raise an error?", dfsRaisedErr
'''