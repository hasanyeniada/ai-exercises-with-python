
def constructMaze(): #WALL = 50,  GOAL = 100
    mazeTemp = [[0, 0, 1, 0, 1],
                [50, 50, 2, 1, 2],
                [2, 50, 3, 0, 50],
                [0, 2, 1, 1, 50],
                [1, 0, 100, 1, 50]]
    print("MAZE: ", mazeTemp)
    return mazeTemp

def performBreadthFirstSearch(maze, startingTile):

    frontier = [] #a FIFO queue
    frontier.append(startingTile)
    exploredTree = []
    exploredNormal = []

    if(getTileValue(maze, startingTile) == 100): #100 = GOAL TILE
        return startingTile

    solutionFlag = False
    loopFlag = True

    while(loopFlag):

        if(len(frontier) == 0):
            loopFlag = False
        else:
            frontierTemp = frontier[::-1] #copy reverse of frontier to frontierTemp
            node = frontierTemp.pop()     #pop last element which is first element of frontier
            frontier.remove(node)         #remove that element also from frontier

            exploredNormal.append(node)     #add popped node to explored
            exploredTree.append([node, []]) #that tree will give the resulting path

            if (getTileValue(maze, node) == 100):  #GOAL TEST
                loopFlag = False
                solutionFlag = True
                break

            actions = getPossibleActions(node, maze, exploredNormal) #get possible actions for an explored node
            frontier = updateFrontier(actions, frontier, exploredTree, exploredNormal) #update frontier according to possible actions

    return solutionFlag, exploredTree

def performDepthFirstSearch(maze, startingTile): #same procedure with BFS, only frontier is a stack.
    frontier = []  # a LIFO queue(stack)
    frontier.append(startingTile)
    exploredTree = []
    exploredNormal = []

    if (getTileValue(maze, startingTile) == 100): #100 = GOAL TILE
        return startingTile

    solutionFlag = False
    loopFlag = True
    while (loopFlag):

        if (len(frontier) == 0):
            loopFlag = False
        else:
            node = frontier.pop() #now frontier is a stack, we can simply pop the last element

            exploredNormal.append(node)
            exploredTree.append([node, []])

            if (getTileValue(maze, node) == 100): #100 = GOAL TILE
                loopFlag = False
                solutionFlag = True
                break

            actions = getPossibleActions(node, maze, exploredNormal)
            frontier = updateFrontier(actions, frontier, exploredTree, exploredNormal)

    return solutionFlag, exploredTree

def updateFrontier(actions, frontier, exploredTree, exploredNormal):
    for coordinat in actions:
        if((coordinat not in frontier) and (coordinat not in exploredNormal)): #if action is not in explored or frontier add it to frontier
            frontier.append(coordinat)
            size = len(exploredTree)-1
            exploredTree[size][1].append(coordinat) #updates tree to find resulting path at the end
    return frontier

def getPossibleActions(node, maze, exploredNormal):
    actions = []
    nodeRow = node[0]
    nodeCol = node[1]

    if(nodeCol == 0 and nodeRow == 0):    #COOR(0,0)
        actions.append([nodeRow+1, nodeCol])
        actions.append([nodeRow, nodeCol+1])
    elif(nodeRow == 0 and nodeCol != 0):  #COOR(0,+)
        actions.append([nodeRow + 1, nodeCol])
        if( (nodeCol - 1) >= 0):
            actions.append([nodeRow, nodeCol - 1])
        if( (nodeCol + 1) < len(maze[1]) ):
            actions.append([nodeRow, nodeCol+1])
    elif(nodeRow != 0 and nodeCol == 0):  #COOR(+,0)
        actions.append([nodeRow, nodeCol+1])
        if ( (nodeRow - 1) >= 0):
            actions.append([nodeRow-1, nodeCol])
        if( (nodeRow + 1) < len(maze[0]) ):
            actions.append([nodeRow+1, nodeCol])
    else:                                 #COOR(+,+)
        if ((nodeRow - 1) >= 0 ):
            actions.append([nodeRow-1, nodeCol])
        if( (nodeRow + 1) < len(maze[0]) ):
            actions.append([nodeRow+1, nodeCol])
        if ((nodeCol - 1) >= 0):
            actions.append([nodeRow, nodeCol-1])
        if( (nodeCol + 1) < len(maze[1]) ):
            actions.append([nodeRow, nodeCol+1])

    actionsTemp = actions.copy()
    for coordinat in actionsTemp: #if a wall is found, remove it from actions
        if((getTileValue(maze, coordinat) == 50)):
            actions.remove(coordinat)
    return actions

def getTileValue(maze, coordinat): #to check goal state and walls, tile value is getting from that function.
    row = coordinat[0]
    col = coordinat[1]
    movementPoint = maze[row][col]
    return movementPoint

def findResultingPathForBFSandDFS(exploredTree, startingTile): #gives the resulting path using explored Tree.
    size = len(exploredTree)
    goalCoordinat = exploredTree[size-1][0]
    path = []
    flag = True
    temp = goalCoordinat
    while(flag):
        for coordinat in exploredTree:
            if (temp in coordinat[1]):
                path.append([temp])
                temp = coordinat[0]
            if(temp == startingTile):
                flag = False
    path.append(exploredTree[0][0]) #starting tile is added
    return path

if __name__ == "__main__":

    maze = constructMaze() #maze is constructed here, you can change the values in that function to try different mazes
    startingTile = [0, 0]  #starting maze coordinat

    print()
    print("BFS algorithm is starting...")
    solutionFlagBFS, exploredBFSTree = performBreadthFirstSearch(maze, startingTile)  # maze, start point
    print("BFS algorithm has finished...")
    print("Resulting Tree:", exploredBFSTree)
    print("Tree is in that structure: [ [parent], [childs] ]")
    print("__________________________________")
    print()

    print("DFS algorithm is starting...")
    solutionFlagDFS, exploredDFSTree = performDepthFirstSearch(maze, startingTile)  # maze, start point
    print("DFS algorithm has finished...")
    print("Resulting Tree:", exploredDFSTree)
    print("Tree is in that structure: [ [parent], [childs] ]")
    print("__________________________________")
    print()


    if(solutionFlagBFS):
        print("Solution is found successfully with Breadth First Search...")
        print("Resulting path:")
        resultingPath = findResultingPathForBFSandDFS(exploredBFSTree, startingTile)
        result = resultingPath[::-1]
        print(result)
        print("Path cost according to path lengths: ", len(result) - 1)
    else:
        print("No solution is found by Breadth First Search...")

    print("__________________________________")
    print()

    if (solutionFlagDFS):
        print("Solution is found successfully with Depth First Search...")
        print("Resulting path:")
        resultingPath = findResultingPathForBFSandDFS(exploredDFSTree, startingTile)
        result = resultingPath[::-1]
        print(result)
        print("Path cost according to path lengths: ", len(result) - 1)
    else:
        print("No solution is found by Depth First Search...")

