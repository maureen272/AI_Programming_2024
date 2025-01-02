from problem import Tsp

def main():
    p = Tsp()
    p.setVariables()
    steepestAscent(p) # 이건 아직 class가 아니니까 함수
    p.describe()
    displaySetting() # 이것도 아직 class가 아니니까 함수
    p.report()

def steepestAscent(p):
    current = p.randomInit()   # 'current' is a list of city ids
    valueC = p.evaluate(current)
    while True:
        neighbors = p.mutants(current)
        (successor, valueS) = bestOf(neighbors, p)
        if valueS >= valueC: # 더 좋은 이웃이 없으면
            break # 종료
        else: # 더 좋아지면
            current = successor # 현재값을 업데이트
            valueC = valueS
    p.storeResult(current, valueC)

def bestOf(neighbors,p): ###
    best = neighbors[0]
    bestValue = p.evaluate(neighbors[0]) # 첫번째 값으로 초기화
    for i in range(1, len(neighbors)): # 두번째 값부터 비교
        tmpResult = p.evaluate(neighbors[i]) # 후보들의 값을 계산
        if tmpResult < bestValue: # 더 좋은 값이 나오면 바꿈 (값이 작을 수록 좋은 것임)
            best = neighbors[i]
            bestValue = tmpResult
    return best, bestValue

def displaySetting():
    print()
    print("Search algorithm: Steepest-Ascent Hill Climbing")

main()
