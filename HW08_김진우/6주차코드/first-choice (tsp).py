from problem import Tsp

LIMIT_STUCK = 100 # Max number of evaluations enduring no improvement


def main():
    p = Tsp()
    p.setVariables()
    firstChoice(p)
    p.describe()
    displaySetting()
    p.report()

def firstChoice(p):
    current = p.randomInit()   # 'current' is a list of city ids
    valueC = p.evaluate(current)
    i = 0
    while i < LIMIT_STUCK:
        successor = p.randomMutant(current) # 값을 random하게 바꿔줌
        valueS = p.evaluate(successor)
        if valueS < valueC: # 더 좋은 이웃이 있으면
            current = successor
            valueC = valueS # 현재값을 업데이트
            i = 0              # Reset stuck counter
        else:
            i += 1
    p.storeResult(current, valueC) 

def displaySetting():
    print()
    print("Search algorithm: First-Choice Hill Climbing")

main()
