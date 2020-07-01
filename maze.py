import math
import node as nd
import cv2
import sys
# *Example of a latticeMatrix*
# Where
# 1 == Start
# 2 == End
# 3 == Wall
# [0,0,1,0,0,0,0,0,0,
#  0,0,0,0,3,0,0,0,0,
#  0,0,0,0,3,0,0,0,0,
#  0,3,3,3,3,0,0,0,0,
#  0,0,0,0,0,0,0,0,0,
#  0,0,0,0,0,0,0,0,0,
#  0,0,0,0,0,0,0,0,0,
#  0,0,0,0,0,0,0,0,0,
#  0,0,0,0,0,2,0,0,0]

#Load a maze from a picture (jpg/png?)
def importMaze(file):
    image = cv2.imread(sys.argv[1])
    maze = []
    mRow = []
    for row in image:
        for pixel in row:
            if pixel[0] == [255]:
                mRow.append(0)
            else:
                mRow.append(1)
        maze.append(mRow)
        mRow = []
    return maze, image

#This function assumes that the incoming matrix is always a square shape (All sides same length)
#Function turns 1d array into a 2d array
def generate2dMatrix(latticeMatrix):
    maze = []
    row = []
    for idx, elem in enumerate(latticeMatrix):
        row.append(elem)
        if idx != 0 and idx % int(math.sqrt(len(latticeMatrix))) == 0:
            maze.append(row)
            row = []
    return maze

def on_maze(maze, x, y):
    return x >= 0 and x < len(maze) and y >= 0 and y < len(maze)

def generateGraph(matrix):
    graph = {}
    visitedNodes = []
    unvisitedNodes = []
    start = (0,0)
    end = (0,0)
    for x, row in enumerate(matrix):
        for y, vertex in enumerate(row):
            unvisitedNodes.append((x,y))

    while(len(unvisitedNodes) > 0):
        node = unvisitedNodes.pop()
        if matrix[node[0]][node[1]] == 1:
            continue
        elif on_maze(matrix, node[0]-1, node[1]) == True and on_maze(matrix, node[0]+1, node[1]) == True and on_maze(matrix, node[0], node[1]-1) == True and on_maze(matrix, node[0], node[1]+1) == True and matrix[node[0]-1][node[1]] == 0 and matrix[node[0]+1][node[1]] == 0 and matrix[node[0]][node[1]-1] == 1 and matrix[node[0]][node[1]+1] == 1:
            continue
        elif on_maze(matrix, node[0]-1, node[1]) == True and on_maze(matrix, node[0]+1, node[1]) == True and on_maze(matrix, node[0], node[1]-1) == True and on_maze(matrix, node[0], node[1]+1) == True and matrix[node[0]-1][node[1]] == 1 and matrix[node[0]+1][node[1]] == 1 and matrix[node[0]][node[1]-1] == 0 and matrix[node[0]][node[1]+1] == 0:
            continue
        else:
            #This node is never a wall
            #We also set the node's distance attribute to the node's depth in maze (y value)
            #nNode = nd.Node(None, node, 0, float('inf'))
            #EDIT:: We don't create nodes here for easier graph-adjacency list making
            #We also need to reverse x and y, since currently x = row and y = node
            visitedNodes.append((node[1], node[0]))

    #We can connect nodes by iterating the visitedNodes list and checking if there's a node that's either in the same X or same Y axis
    #We do this for each node and create adjacency list for algorithm's to use
    #next((x for x in visitedNodes if x.nPos[0] == node[0] or x.nPos[1] == node[1]), None)
    #Adjacency list is in format: {'x' : ['a', 'b', 'c']}
    
    #Sort the visitedNodes array to go from top to bottom and left to right
    visitedNodes.sort(key=lambda x: (x[1], x[0]))

    #Initialize the adjacency list
    for node in visitedNodes:
        graph[node] = {}    
    
    for node in visitedNodes:
        #Below line is only used if we'd have objects here
        #childNode = next((x for x in visitedNodes if x != node and (x.nPos[0] == node.nPos[0] or x.nPos[1] == node.nPos[1])), None)
        
        #Find all nodes that are on the same x or y axis
        #Only keep the nearest nodes
        #Check if the path to the found nodes is clear (not wall)
        #Connect the valid nodes and find their distances to the parent node (weight)

        childNodes = [x for x in visitedNodes if x != node and (x[0] == node[0] or x[1] == node[1])]

        yAxis = []
        xAxis = []

        for cNode in childNodes:
            if cNode[0] == node[0]:
                xAxis.append(cNode)

            elif cNode[1] == node[1]:
                yAxis.append(cNode)

        xAxis.append(node)
        xAxis = sorted(xAxis, key=lambda tup: tup[1])
        xNeighbours = []

        #Find the nearest neighbours with same x coordinate
        if xAxis.index(node)-1 >= 0:
            xNeighbours.append(xAxis[xAxis.index(node)-1])
        if xAxis.index(node)+1 < len(xAxis):
            xNeighbours.append(xAxis[xAxis.index(node)+1])

        yAxis.append(node)
        yAxis = sorted(yAxis, key=lambda tup: tup[0])
        yNeighbours = []
        #Find the nearest neighbours with same x coordinate
        if yAxis.index(node)-1 >= 0:
            yNeighbours.append(yAxis[yAxis.index(node)-1])
        if yAxis.index(node)+1 < len(yAxis):
            yNeighbours.append(yAxis[yAxis.index(node)+1])
        
        neighbourNodes = xNeighbours + yNeighbours

        #Now we have to check if the neighbours are reachable from the node
        
        for nNode in neighbourNodes:
            
            #If the found node was on the same y-axis
            if nNode[0] == node[0]:
                #Check if all the vertices between the nodes are walkable path in maze (and in y-axis)
                pathClear = True
                for vertice in range(min(nNode[1], node[1]), max(nNode[1], node[1])):
                    if matrix[vertice][nNode[0]] == 1:
                        pathClear = False
                if pathClear == True:
                    #Create edge between nodes
                    if node in graph:
                        graph[node].update({nNode: abs(min(nNode[1], node[1]) - max(nNode[1], node[1]))})

            if nNode[1] == node[1]:
                #Check if all the vertices between the nodes are walkable path in maze (and in y-axis)
                pathClear = True

                #Here we do the above checking
                #We could also just find all the nodes in the same axis at once and then find the closest nodes
                #Then we check if these nodes are not blocked by a wall (one by one)
                #And continue normally

                for vertice in range(min(nNode[0], node[0]), max(nNode[0], node[0])):
                    #We need to iterate the y axis since we're iterating the nodes in the row of the matrix
                    #This is a bit confusing since outside accessing the matrix indices we're using node[0] for x and node[1] for y
                    if matrix[nNode[1]][vertice] == 1:
                        pathClear = False

                if pathClear == True:
                    #Create edge between nodes
                    graph[node].update({nNode: abs(min(nNode[0], node[0]) - max(nNode[0], node[0]))})

        #Get the start and end positions
        if node[1] == 0:
            start = node
        if node[1] == len(matrix)-1:
            end = node

    #We can use node object data structures because in algorithms we usually mark traversed neighbour nodes as visited
    #Convert the adjacency list items into Node objects
    #Since tuples are immutable, we need to create a temporary copy of the graph in memory
    
    nodeCounter = 0
    temp = {}
    for key, values in graph.items():
        nodeCounter += 1
        key = nd.Node(None, key, 0, float('inf'))
        temp[key] = {}
        for node, weight in values.items():
            node = nd.Node(None, node, 0, float('inf'))
            temp[key].update({node: weight})
    graph = temp
    print("Total nodes in the graph: " + str(nodeCounter))
    return graph, start, end