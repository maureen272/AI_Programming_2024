from tsp import *

def main():
    # Create an instance of TSP
    p = createProblem()    # 'p': (numCities, locations, table)
    # Call the search algorithm
    solution, minimum = steepestAscent(p)
    # Show the problem and algorithm settings
    describeProblem(p)
    displaySetting()
    # Report results
    displayResult(solution, minimum)

def steepestAscent(p):
    current = randomInit(p)   # 'current' is a list of city ids
    valueC = evaluate(current, p)
    while True:
        neighbors = mutants(current, p)
        (successor, valueS) = bestOf(neighbors, p)
        if valueS >= valueC:
            break
        else:
            current = successor
            valueC = valueS
    return current, valueC

def mutants(current, p): # Apply inversion
    n = p[0]
    neighbors = []
    count = 0
    triedPairs = []
    while count <= n:  # Pick two random loci for inversion
        i, j = sorted([random.randrange(n) for _ in range(2)])
        if i < j and [i, j] not in triedPairs:
            triedPairs.append([i, j])
            curCopy = inversion(current, i, j)
            count += 1
            neighbors.append(curCopy)
    return neighbors

def bestOf(neighbors, p): ###
    best = neighbors[0]
    bestValue = evaluate(neighbors[0], p) # 첫번째 값으로 초기화
    for i in range(1, len(neighbors)): # 두번째 값부터 비교
        tmpResult = evaluate(neighbors[i], p) # 후보들의 값을 계산
        if tmpResult < bestValue: # 더 좋은 값이 나오면 바꿈 (값이 작을 수록 좋은 것임)
            best = neighbors[i]
            bestValue = tmpResult
    return best, bestValue

def displaySetting():
    print()
    print("Search algorithm: Steepest-Ascent Hill Climbing")

main()
