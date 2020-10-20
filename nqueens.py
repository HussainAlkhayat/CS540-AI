import copy
import random
import heapq
import math

"""
Takes in a state in 1D and return a 2D version of it
"""
def convert1Dto2D(state):
    tempState = copy.deepcopy(state)
    n = len(state)
    state2D = [[0 for i in range(n)] for j in range(n)]
    index = 0
    for queen in state:
        state2D[queen][index] = 1
        index += 1
    return state2D

"""
Given a 2D state print out an easily readable version of it 
"""
def print_make_sense(state2D):
    n = len(state2D)
    for i in range(n):
        print("")
        for j in range(n):
            print(state2D[i][j], end =" ")
            if j != n-1:
                print(",", end = " ")

"""
Given a state and a static point return a sorted valid successors
return an empty list if the static point is not satisfied 
"""
def succ(state, static_x, static_y):
    n = len(state)
    validState = []
    if state[static_x] != static_y:
        return []
    index = 0
    for queen in state:

        if index != static_x:
            if queen == 0: #only one possible move, queen down one tile
                tempState = copy.deepcopy(state)
                tempState[index] += 1
                validState.append(tempState)
            elif queen == n-1: #only one possible move, queen up one tile
                tempState = copy.deepcopy(state)
                tempState[index] -= 1
                validState.append(tempState)
            else: #two possible moves, queen up or down
                tempState1 = copy.deepcopy(state)
                tempState1[index] += 1
                validState.append(tempState1)
                tempState2 = copy.deepcopy(state)
                tempState2[index] -= 1
                validState.append(tempState2)
        index += 1
    return sorted(validState)

"""
calculates
"""
def f(state):
    attackedList = [0] * len(state)
    index = 0
    for queen in state:
        #attacked by same row
        indexRow = 0
        for queenAttacked in state:
            if index != indexRow: # it cannot attack it self...
                if queen == queenAttacked:
                    attackedList[indexRow] = 1
            indexRow += 1

        #attacked diagonal
        indexDia = 0
        for queenAttacked in state:
            if index != indexDia:  # it cannot attack it self...
                x = abs(index - indexDia)
                y = abs(queen - queenAttacked)
                if x == y:
                    attackedList[state.index(queenAttacked)] = 1
            indexDia += 1
        index +=1
    attackedNum = 0
    for value in attackedList:
        if value == 1:
            attackedNum += 1
    return attackedNum

def choose_next(curr, static_x, static_y):
    if curr[static_x] != static_y:
        return None
    validStates = succ(curr, static_x, static_y)
    validStates.append(curr)
    queue = []
    for state in validStates:
        heapq.heappush(queue,(f(state), state))

    return heapq.heappop(queue)[1]

#print(choose_next([1, 1, 2], 1, 1))
def n_queens_solver(initial_state, static_x, static_y, printValue):
    if initial_state[static_x] != static_y:
        print("Error static")
        return
    state = initial_state
    fScore = f(state)
    while True:
        if printValue:
            print(state, "- f=" + str(fScore))
        if fScore == 0:
            return state

        possibleSucc = choose_next(state, static_x, static_y)
        possiblefScore = f(possibleSucc)
        if possiblefScore == fScore:
            if printValue:
                print(possibleSucc, "- f=" + str(possiblefScore))

            return state
        state = possibleSucc
        fScore = possiblefScore

def n_queens(initial_state, static_x, static_y):
    return n_queens_solver(initial_state, static_x, static_y, True)


def n_queens_restart(n, k, static_x, static_y):
    random.seed(2)
    listOfTries = []
    for i in range(k):
        state = []
        for i in range(n):
            if i == static_x:
                state.append(static_y)
            else:
                state.append(random.randint(0, n - 1))
        solution = n_queens_solver(state, static_x, static_y, False)
        fScore = f(solution)
        if fScore == 0:
            print(solution, "- f=" + str(fScore))
            return
        heapq.heappush(listOfTries, (fScore, solution))
    print(listOfTries)
    fScoreSame = True
    currfScore = -1
    while fScoreSame:
        item = heapq.heappop(listOfTries)
        state = item[1]
        fScore = item[0]
        if currfScore == -1:
            currfScore = fScore
            print(state, "- f=" + str(fScore))
        elif fScore == currfScore:
            print(state, "- f=" + str(fScore))
        else:
            return
