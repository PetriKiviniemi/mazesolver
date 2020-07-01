import PriorityQueue as pQueue

def solve(maze, start, end):
    pq = pQueue.PQ()
    visitedNodes = []
    startNode = next((x for x in maze if x.nPos == start), None)
    visitedNodes.append(start)
    pq.insert(startNode)

    while pq.isEmpty() != True:
        q = pq.pop()

        if q.nPos == end:
            print("Found end")
            #Lets backtrack and trace until we find the start
            pq.queue.clear()
            path = []
            current = q
            while current.nPos != start:
                path.append(current.nPos)
                current = current.parent
            path.append(start)
            return path
            
        #Next we iterate through every neighbour node of the current node (maze[q].items())
        for neighbour, weight in maze[q].items():
            if neighbour.nPos not in visitedNodes:
                visitedNodes.append(neighbour.nPos)
                neighbour.parent = q
                pq.insert(neighbour)
                    
                    
