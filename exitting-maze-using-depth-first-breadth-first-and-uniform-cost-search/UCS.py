
def constructMaze(): #WALL = 50,  GOAL = 100

    mazeTemp = [[0, 0, 1, 0, 1],
                [50, 50, 2, 1, 2],
                [2, 50, 3, 0, 50],
                [0, 2, 1, 1, 50],
                [1, 0, 3, 1, 50]]
    print("MAZE:", mazeTemp)
    return mazeTemp

def performUniformCostSearch(maze, startingTile, goalTile):
    frontier = []  # a priority queue
    frontier.append(startingTile)
    exploredTree = []
    exploredNormal = []

    if (startingTile == goalTile): #GOAL TEST
        return startingTile

    solutionFlag = False
    loopFlag = True
    while (loopFlag):
        if (len(frontier) == 0):
            loopFlag = False
        else:
            node = sortFrontier(frontier) #get the lowest path cost tile.
            frontier.remove(node)         #remove it from frontier.

            exploredNormal.append([node[0], node[1]])
            exploredTree.append([node, []])

            if ( [node[0], node[1]] == [goalTile[0], goalTile[1]] ): #GOAL TEST
                loopFlag = False
                solutionFlag = True
                break

            pathCostUntilExploredNode = findPathCostUntilGivenTile(node, exploredTree, maze)

            actions = getPossibleActions(node, maze, exploredNormal, pathCostUntilExploredNode) #get possible actions for an explored node
            frontier = updateFrontierUCS(actions, frontier, exploredTree, exploredNormal)  #update frontier according to possible actions

    return solutionFlag, exploredTree

def updateFrontierUCS(actions, frontier, exploredTree, exploredNormal):
    for coordinat in actions:
        isExistInFrontier = controlFrontier(frontier, coordinat)
        if((not isExistInFrontier) and ( [coordinat[0], coordinat[1]] not in exploredNormal)):
            frontier.append(coordinat)
            size = len(exploredTree)-1
            exploredTree[size][1].append(coordinat) #updates tree to find resulting path at the end

        if(isExistInFrontier): #if node is in frontier with higher path costi, replace it
            replaceWithLowerCost(frontier, coordinat)

    return frontier

def getPossibleActions(node, maze, exploredNormal, pathCostUntilExploredNode):
    actions = []
    nodeRow = node[0]
    nodeCol = node[1]

    if (nodeCol == 0 and nodeRow == 0):  # COOR(0,0)
        actions.append([nodeRow + 1, nodeCol])
        actions.append([nodeRow, nodeCol + 1])
    elif (nodeRow == 0 and nodeCol != 0):  # COOR(0,+)
        actions.append([nodeRow + 1, nodeCol])
        if ((nodeCol - 1) >= 0):
            actions.append([nodeRow, nodeCol - 1])
        if ((nodeCol + 1) < len(maze[1])):
            actions.append([nodeRow, nodeCol + 1])
    elif (nodeRow != 0 and nodeCol == 0):  # COOR(+,0)
        actions.append([nodeRow, nodeCol + 1])
        if ((nodeRow - 1) >= 0):
            actions.append([nodeRow - 1, nodeCol])
        if ((nodeRow + 1) < len(maze[0])):
            actions.append([nodeRow + 1, nodeCol])
    else:                                  # COOR(+,+)
        if ((nodeRow - 1) >= 0):
            actions.append([nodeRow - 1, nodeCol])
        if ((nodeRow + 1) < len(maze[0])):
            actions.append([nodeRow + 1, nodeCol])
        if ((nodeCol - 1) >= 0):
            actions.append([nodeRow, nodeCol - 1])
        if ((nodeCol + 1) < len(maze[1])):
            actions.append([nodeRow, nodeCol + 1])

    actionsTemp = actions.copy()
    for coordinat in actionsTemp:
        row = coordinat[0]
        col = coordinat[1]
        if((maze[row][col] ==  50) or (coordinat in exploredNormal)): #if a wall is found, remove it from actions
            actions.remove(coordinat)

    for coordinat in actions: #add path cost of each tile to end of coordinat of it.
        costOnTile = getTileValue(maze, coordinat) + 1 + pathCostUntilExploredNode
        coordinat.append(costOnTile)
    return actions

def findPathCostUntilGivenTile(node, exploredTree, maze): #gives path cost of an individual tile from starting
    cost = 0
    for coordinat in exploredTree:
        if(node in coordinat[1]):
            cost += 1
            cost += getTileValue(maze, node) # each action costs 1 movement point
            cost += coordinat[0][2] #destination tile can take additional movement points as stated on tiles
    return cost

def replaceWithLowerCost(frontier, coordinat): #if a node is in frontier with higher cost, it is replaced with lower one.
    for coor in frontier:
        if( (coor[0] == coordinat[0]) and (coor[1] == coordinat[1]) ):
            if(coor[2] > coordinat[2]):
                frontier.remove(coor)
                frontier.append(coordinat)

def controlFrontier(frontier, coordinat): #control whether given node is in frontier
    isExist = False
    for coor in frontier:
        if( (coor[0] == coordinat[0]) and (coor[1] == coordinat[1]) ):
            isExist = True
    return isExist

def sortFrontier(frontier):  #update priority queue, gives lowest cost node.
    coorWithMinCost = frontier[0]
    minCost = frontier[0][2]
    for coor in frontier:
        if(coor[2] <= minCost):
            coorWithMinCost = coor
            minCost = coor[2]
    return coorWithMinCost

def getTileValue(maze, coordinat): #getting tile extra move points.
    row = coordinat[0]
    col = coordinat[1]
    movementPoint = maze[row][col]
    return movementPoint

def findResultingPathForUCSandAStar(exploredTree, startingTile): #gives the resulting path using explored Tree.
    size = len(exploredTree)
    goalCoordinat = exploredTree[size-1][0]
    path = []
    flag = True
    temp = goalCoordinat
    while(flag):
        for coordinat in exploredTree:
            if (temp in coordinat[1]):
                path.append([temp[0], temp[1]])
                temp = coordinat[0]
            if(temp == startingTile):
                flag = False
    path.append([startingTile[0], startingTile[1]])
    return path, goalCoordinat[2]


if __name__ == "__main__":

    maze = constructMaze()
    startingTile = [0, 0, 0]
    goalTile = [4, 2, 3]

    print("UCS algorithm is starting...")
    solutionFlagUCS, exploredUCSTree = performUniformCostSearch(maze, startingTile, goalTile)  # maze, start point
    print("Resulting Tree:", exploredUCSTree)
    print("Tree is in that structure: [ [parent], [childs] ]")
    print("UCS algorithm has finished...")


    if (solutionFlagUCS):
        print("Solution is found successfully with Uniform Cost First Search...")
        print("Resulting path:")
        resultingPath, pathLen = findResultingPathForUCSandAStar(exploredUCSTree, startingTile)
        result = resultingPath[::-1]
        print(result)
        print("Path cost according to movement points: ", pathLen)
    else:
        print("No solution is found by Uniform Cost First Search...")

