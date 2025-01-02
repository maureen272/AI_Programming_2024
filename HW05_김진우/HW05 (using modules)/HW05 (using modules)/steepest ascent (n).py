from numeric import *
def main():
    # Create an instance of numerical optimization problem
    p = createProblem()   # 'p': (expr, domain)
    # Call the search algorithm
    solution, minimum = steepestAscent(p)
    # Show the problem and algorithm settings
    describeProblem(p)
    displaySetting()
    # Report results
    displayResult(solution, minimum)

def steepestAscent(p):
    current = randomInit(p) # 'current' is a list of values
    valueC = evaluate(current, p)
    while True:
        neighbors = mutants(current, p)
        successor, valueS = bestOf(neighbors, p)
        if valueS >= valueC:
            break
        else:
            current = successor
            valueC = valueS
    return current, valueC

def mutants(current, p): ###
    neighbors = []
    for i in range(len(current)): # 모든 변수에 대해서 수행
        neighbors.append(mutate(current, i, DELTA, p)) # 변수의 현재 값에 DELTA만큼 더한 값을 저장
        neighbors.append(mutate(current, i, -DELTA, p)) # 변수의 현재 값에 DELTA만큼 뺀 값을 저장
    return neighbors     # Return a set of successors

def bestOf(neighbors, p): ###
    best = neighbors[0]
    bestValue = evaluate(neighbors[0], p) # 첫번째 값으로 초기화
    for i in range(1, len(neighbors)): # 두번째 값부터 비교
        tmpResult = evaluate(neighbors[i], p) # 후보들의 값을 계산
        if tmpResult < bestValue: # 더 좋은 값이 나오면 바꿈
            best = neighbors[i]
            bestValue = tmpResult

    return best, bestValue

def displaySetting():
    print()
    print("Search algorithm: Steepest-Ascent Hill Climbing")
    print()
    print("Mutation step size:", DELTA)

main()
