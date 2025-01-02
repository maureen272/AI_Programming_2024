from problem import Numeric

LIMIT_STUCK = 100 # Max number of evaluations enduring no improvement


def main():
    p = Numeric()
    p.setVariables()
    firstChoice(p) # 이건 아직 class가 아니니까 함수
    p.describe()
    displaySetting(p) # 이것도 아직 class가 아니니까 함수
    p.report()

def firstChoice(p):
    current = p.randomInit()   # 'current' is a list of values
    valueC = p.evaluate(current)
    i = 0
    while i < LIMIT_STUCK: 
        successor = p.randomMutant(current)
        valueS = p.evaluate(successor)
        if valueS < valueC:
            current = successor
            valueC = valueS
            i = 0              # Reset stuck counter
        else:
            i += 1
    p.storeResult(current, valueC)

def displaySetting(p):
    print()
    print("Search algorithm: First-Choice Hill Climbing")
    print()
    print("Mutation step size:", p.getDelta())

main()