import maze as Mz
import cv2
import breadth_first_search as bfs

def findConnected(x1, x2, y1, y2):
    connectedNodes = []
    if x1 == x2:
        connectedNodes.append((x1,y1))
        for vertex in range(min(y1, y2), max(y1, y2)):
            connectedNodes.append((x1, vertex))
        connectedNodes.append((x2,y2))

    elif y1 == y2:
        connectedNodes.append((x1,y1))
        for vertex in range(min(x1,x2), max(x1,x2)):
            connectedNodes.append((vertex, y1))
        connectedNodes.append((x2,y2))
    return connectedNodes

def drawPath(path):
    #We have to connect the found path nodes here for drawing purposes
    newPath = []

    for node in range(len(path)):
        if node+1 == len(path)-1:
            for node in findConnected(path[node][0], path[node+1][0], path[node][1], path[node+1][1]):
                newPath.append(node)
            return newPath
        for node in findConnected(path[node][0], path[node+1][0], path[node][1], path[node+1][1]):
            newPath.append(node)

            
def main():
    (maze, image) = Mz.importMaze("mazeSolver/maze.png")
    (maze, start, end) = Mz.generateGraph(maze)
    path = bfs.solve(maze, start, end)
    path = drawPath(path)

    for node in path:
        #Node coordinates are (x,y), and image coordinates are reversed, because it's a nested list
        image[node[1]][node[0]][0] = 0
        image[node[1]][node[0]][1] = 0
        image[node[1]][node[0]][2] = 255
    cv2.imwrite('image.png', image)
    
    

        

if __name__ == "__main__":
    main()