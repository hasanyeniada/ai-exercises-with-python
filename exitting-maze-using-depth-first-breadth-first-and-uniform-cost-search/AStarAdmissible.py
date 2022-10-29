import math

def constructMaze(): #wall:50, goal:100

    mazeTemp = [[0, 0, 1, 0, 1],
                [50, 50, 2, 1, 2],
                [2, 50, 3, 0, 50],
                [0, 2, 1, 1, 50],
                [1, 0, 3, 1, 50]]
    print("MAZE: ", mazeTemp)
    return mazeTemp

def performAStarSearch(maze, startingTile, goalTile):
    frontier = []  #a priority queue
    frontier.append(startingTile)
    exploredTree = []
    exploredNormal = []

    if (startingTile == goalTile):
        return startingTile

    solutionFlag = False
    loopFlag = True

    while (loopFlag):
        if (len(frontier) == 0):
            loopFlag = False
        else:
            node = sortFrontier(frontier) #get the lowest fN tile.
            frontier.remove(node)         #remove it from frontier.

            exploredNormal.append([node[0], node[1]])
            exploredTree.append([node, []])

            if ( [node[0], node[1]] == [goalTile[0], goalTile[1]] ): #GOAL TEST
                loopFlag = False
                solutionFlag = True
                break

            pathCostUntilExploredNode = findPathCostUntilGivenTile(node, exploredTree, maze)

            possibleActions = getPossibleActionsAstar(node, maze, exploredNormal, pathCostUntilExploredNode, goalTile)
            frontier = updateFrontierAstar(possibleActions, frontier, exploredTree, exploredNormal)

    return solutionFlag, exploredTree

def updateFrontierAstar(actions, frontier, exploredTree, exploredNormal):
    for coordinat in actions:
        isExistInFrontier = controlFrontier(frontier, coordinat)
        if((not isExistInFrontier) and ( [coordinat[0], coordinat[1]] not in exploredNormal)):
            frontier.append(coordinat)
            size = len(exploredTree)-1
            exploredTree[size][1].append(coordinat)

        if(isExistInFrontier):
            replaceWithLowerCost(frontier, coordinat)

    return frontier

def getPossibleActionsAstar(expNode, maze, exploredNormal, pathCostUntilExploredNode, goal):
    actions = []
    nodeRow = expNode[0]
    nodeCol = expNode[1]

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
    else:  # COOR(+,+)
        if ((nodeRow - 1) >= 0):
            actions.append([nodeRow - 1, nodeCol])
        if ((nodeRow + 1) < len(maze[0])):
            actions.append([nodeRow + 1, nodeCol])
        if ((nodeCol - 1) >= 0):
            actions.append([nodeRow, nodeCol - 1])
        if ((nodeCol + 1) < len(maze[1])):
            actions.append([nodeRow, nodeCol + 1])

    actionsTemp = actions.copy()
    for x in actionsTemp:
        row = x[0]
        col = x[1]
        if((maze[row][col] == 50) or (x in exploredNormal)):
            actions.remove(x)

    for coor in actions:
        costOnTile = getTileValue(maze, coor) + 1 + pathCostUntilExploredNode
        heuristic = giveAdmissibleHeuristic(coor, [goal[0], goal[1]])
        fN = heuristic + costOnTile
        coor.append(fN)
    return actions

def giveAdmissibleHeuristic(tile, goalTile):
    x1 = tile[0]
    y1 = tile[1]
    x2 = goalTile[0]
    y2 = goalTile[1]
    dist = math.sqrt( (x2 - x1)**2 + (y2 - y1)**2 )

    heuristic = math.floor(dist)
    return heuristic

def findPathCostUntilGivenTile(node, exploredTree, maze):
    cost = 0
    for coordinat in exploredTree:
        if(node in coordinat[1]):
            cost += 1
            cost += getTileValue(maze, node) # each action costs 1 movement point
            cost += coordinat[0][2] #destination tile can take additional movement points as stated on tiles
    return cost

def replaceWithLowerCost(frontier, coordinat):
    for coor in frontier:
        if( (coor[0] == coordinat[0]) and (coor[1] == coordinat[1]) ):
            if(coor[2] > coordinat[2]):
                frontier.remove(coor)
                frontier.append(coordinat)

def controlFrontier(frontier, coordinat):
    isExist = False
    for coor in frontier:
        if( (coor[0] == coordinat[0]) and (coor[1] == coordinat[1]) ):
            isExist = True
    return isExist

def sortFrontier(frontier):
    coorWithMinCost = frontier[0]
    minCost = frontier[0][2]
    for coor in frontier:
        if(coor[2] <= minCost):
            coorWithMinCost = coor
            minCost = coor[2]
    return coorWithMinCost

def getTileValue(maze, coordinat):
    row = coordinat[0]
    col = coordinat[1]
    movementPoint = maze[row][col]
    return movementPoint

def findResultingPath(exploredTree, startingTile):
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

    print("A* Search algorithm is starting...")
    solutionFlagAStar, exploredAStarTree = performAStarSearch(maze, startingTile, goalTile)  # maze, start point
    print("Resulting Tree:", exploredAStarTree)
    print("Tree is in that structure: [ [parent], [childs] ]")
    print("A* Search algorithm has finished...")


    if (solutionFlagAStar):
        print("Solution is found successfully with A* Search(Admissible)...")
        print("Resulting path:")
        resultingPath, pathLen = findResultingPath(exploredAStarTree, startingTile)
        result = resultingPath[::-1]
        print(result)
        print("Path cost according to fN: ", pathLen)
    else:
        print("No solution is found by A* Search(Admissible)...")
