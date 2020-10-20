"""
Name: Hussain Alkhayat
Email: halkhayat@wisc.edu
"""

import copy
import heapq

"""
Takes in a state in 2D and return a 1D version of it
"""
def convert2Dto1D(state2D):
    tempState2D = copy.deepcopy(state2D)
    state = []
    for i in range(3):
        for j in range(3):
            state.append(tempState2D[i][j])

    return state

"""
Takes in a state in 1D and return a 2D version of it
"""
def convert1Dto2D(state):
    tempState = copy.deepcopy(state)
    state2D = [[0 for i in range(3)] for j in range(3)]
    Index = 0
    for i in range(3):
        for j in range(3):
            state2D[i][j] = tempState[Index]
            Index = Index + 1

    return state2D

"""
Given the indices of a value, calculate the manhattan distance to its goal state 
"""
def manhattan(i,j, val):
    Goal = [([0, 0], 1), ([0, 1], 2), ([0, 2], 3), ([1, 0], 4), ([1, 1], 5), ([1, 2], 6), ([2, 0], 7), ([2, 1], 8),
            ([2, 2], 0)] #hard-coded goal refrence
    correctIndex = 0;
    if val != 0:
        correctIndex = val - 1 #find the index of the passed in val in the goal refrence state
    else:
        #this will only be reached if the passed in value is 0
        return 0
    #calculates the manhattan distance
    correctI = i - Goal[correctIndex][0][0]
    correctJ = j - Goal[correctIndex][0][1]

    # take absolute value of the calulcated values
    if correctI < 0:
        correctI *= -1
    if correctJ < 0:
        correctJ *= -1
    return correctI + correctJ
"""
Given a 2D state return the heuristics by looping through each value in the 2D state and using teh function manhattan
return the sum of the values
"""
def heuristic(state2D):
    h = 0
    for i in range(3):
        for j in range(3):
            h += manhattan(i,j, state2D[i][j])
    return h
"""
Given a 2D state switch the two values with indices (i,j) and (x,y)
return a 2D state after switching 
"""
def switch(state2D, i,j,x,y):
    newState2D = copy.deepcopy(state2D)
    temp1 = newState2D[i][j]
    temp2 = newState2D[x][y]
    newState2D[i][j] = temp2
    newState2D[x][y] = temp1
    return newState2D
"""
Given a 2D state print out an easily readable version of it 
"""
def print_make_sense(state2D):
    for i in range(3):
        print("")
        for j in range(3):
            print(state2D[i][j], end =" ")
            if j != 2:
                print(",", end = " ")

"""
Given a 2D state find the valid moves (successors)
Case 1: "0" is in the corner, thus there are 2 valid successors 
Case 2: "0" is in the middle of a row OR a col but not both, thus there are 3 valid successors 
Case 3: "0" is in the center, thus there are 4 valid successors 
"""
def valid_moves(state2D):
    validList = []
    if state2D[0][0] == 0 or state2D[0][2] == 0 or state2D[2][0] == 0 or state2D[2][2] == 0:
        # case 1: 0 at corners = 2 succ states
        if state2D[0][0] == 0:
            #correct
            validList.append(convert2Dto1D(switch(state2D, 0, 0, 0, 1)))
            validList.append(convert2Dto1D(switch(state2D, 0, 0, 1, 0)))
            return sorted(validList)
        elif state2D[0][2] == 0:
            #correct
            validList.append(convert2Dto1D(switch(state2D, 0, 2, 0, 1)))
            validList.append(convert2Dto1D(switch(state2D, 0, 2, 1, 2)))
            return sorted(validList)
        elif state2D[2][0] == 0:
            #correct
            validList.append(convert2Dto1D(switch(state2D, 2, 0, 2, 1)))
            validList.append(convert2Dto1D(switch(state2D, 2, 0, 1, 0)))
            return sorted(validList)
        elif state2D[2][2] == 0:
            #correct
            validList.append(convert2Dto1D(switch(state2D, 2, 2, 2, 1)))
            validList.append(convert2Dto1D(switch(state2D, 2, 2, 1, 2)))
            return sorted(validList)
    elif state2D[0][1] == 0 or state2D[1][0] == 0 or state2D[1][2] == 0 or state2D[2][1] == 0:
        # case 2: 0 mid row or col but not both = 3 succ state
        if state2D[0][1] == 0:
            #correct
            validList.append(convert2Dto1D(switch(state2D, 0, 1, 0, 0)))
            validList.append(convert2Dto1D(switch(state2D, 0, 1, 0, 2)))
            validList.append(convert2Dto1D(switch(state2D, 0, 1, 1, 1)))
            return sorted(validList)
        elif state2D[1][0] == 0:
            #correct
            validList.append(convert2Dto1D(switch(state2D, 1, 0, 0, 0)))
            validList.append(convert2Dto1D(switch(state2D, 1, 0, 2, 0)))
            validList.append(convert2Dto1D(switch(state2D, 1, 0, 1, 1)))
            return sorted(validList)
        elif state2D[1][2] == 0:
            #correct
            validList.append(convert2Dto1D(switch(state2D, 1, 2, 0, 2)))
            validList.append(convert2Dto1D(switch(state2D, 1, 2, 2, 2)))
            validList.append(convert2Dto1D(switch(state2D, 1, 2, 1, 1)))
            return sorted(validList)
        elif state2D[2][1] == 0:
            #correct
            validList.append(convert2Dto1D(switch(state2D, 2, 1, 2, 0)))
            validList.append(convert2Dto1D(switch(state2D, 2, 1, 2, 2)))
            validList.append(convert2Dto1D(switch(state2D, 2, 1, 1, 1)))
            return sorted(validList)
    elif state2D[1][1] == 0:
        # case 3: 0 in center 4 succ states
        #correct
        validList.append(convert2Dto1D(switch(state2D, 1, 1, 0, 1)))
        validList.append(convert2Dto1D(switch(state2D, 1, 1, 1, 0)))
        validList.append(convert2Dto1D(switch(state2D, 1, 1, 1, 2)))
        validList.append(convert2Dto1D(switch(state2D, 1, 1, 2, 1)))
        return sorted(validList)
    else:
        return None



"""
Given a 1D state print the valid successors and their corresponding heuristic 
"""
def print_succ(state):
    valid = valid_moves(convert1Dto2D(state))
    length = len(valid)
    i = 0
    while i < length:
        print(valid[i], end = " ")
        print("h="+str(heuristic(convert1Dto2D(valid[i]))))
        i += 1

"""
perform a A* search using the following logic:
-insert the initial state in a pq
-while pq is not empty
--pop the pq
--append the popped state to a list CLOSED of visited nodes
--check if this is the goal state, if yes then trace back the moves and print them
--find the corresponding successors to the popped state
--loop through each successor
---if successor is already in teh queue, check if the new g is lower than the one in the queue, if yes updates it, otherwise do nothing
---else if successor is already in CLOSED, check if the new g is lower than the one in CLOSED, if yes then push the state to queue
---else push the successor to the queue
"""
def solve(state):
    #initilize needed local var
    GoalCheck = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    closed = []
    open = []
    h = heuristic(convert1Dto2D(state))
    g = 0
    heapq.heappush(open,(h + g, state, (g, h, -1)))
    #keep going throught the queue
    while len(open) != 0:
        parent = heapq.heappop(open)
        parent_state = parent[1]
        closed.append(parent)
        parent_Index = closed.index(parent)
        parent_g = parent[2][0] #correct
        #check if we reached goal state
        if parent_state == GoalCheck:
            print_path(parent, closed)
            return
        else:
            valid = valid_moves(convert1Dto2D(parent_state)) #get all successors
            for newState in valid: #loop through them
                IndexOpen = alreadyInList(newState, open) #this will help if current successor is in OPEN
                IndexClosed = alreadyInList(newState, closed) #this will help if current successor is in CLOSED
                if IndexOpen != -1:
                    #this case means that current successor is in OPEN
                    currentNewState = open[IndexOpen]
                    #5.2
                    g = parent_g + 1
                    if g < currentNewState[2][0]:
                        h = copy.deepcopy(currentNewState[2][1])
                        open.remove(currentNewState)
                        heapq.heappush(open ,(h + g, newState, (g, h, parent_Index)))
                elif IndexClosed != -1:
                    # this case means that current successor is in CLOSED
                    #5.2
                    currentNewState = closed[IndexClosed]
                    g = parent_g + 1
                    if g < currentNewState[2][0]:
                        h = copy.deepcopy(currentNewState[2][1])
                        heapq.heappush(open, (h + g, newState, (g, h, parent_Index)))
                else:
                    #5.1
                    h = heuristic(convert1Dto2D(newState))
                    g = parent_g + 1
                    heapq.heappush(open, (h + g, newState, (g, h, parent_Index)))

"""
Given a state and a list, check if this state is in the list 
return the index if true
return -1 otherwise
"""
def alreadyInList(state, open):
    Index = 0
    for stateInOpen in open:
        if state == stateInOpen[1]:
            return Index
        Index += 1
    return -1

"""
Given a state and the CLOSED list, follow the state parents and print each step on the way 
"""
def print_path(itemInClosed, closed):
    printingList = []
    while itemInClosed[2][2] != -1:
        printingList.append(itemInClosed)
        itemInClosed = closed[itemInClosed[2][2]]
    printingList.append(itemInClosed)
    index = len(printingList) -1
    while index > -1:
        print(printingList[index][1], "h="+ str(printingList[index][2][1]), "moves:", printingList[index][2][0])
        index -= 1


