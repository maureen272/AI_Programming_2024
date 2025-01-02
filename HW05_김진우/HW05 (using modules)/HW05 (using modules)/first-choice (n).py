from numeric import *

LIMIT_STUCK = 100 # Max number of evaluations enduring no improvement


def main():
    # Create an instance of numerical optimization problem
    p = createProblem()   # 'p': (expr, domain)
    # Call the search algorithm
    solution, minimum = firstChoice(p)
    # Show the problem and algorithm settings
    describeProblem(p)
    displaySetting()
    # Report results
    displayResult(solution, minimum)

def firstChoice(p):
    current = randomInit(p)   # 'current' is a list of values
    valueC = evaluate(current, p)
    i = 0
    while i < LIMIT_STUCK:
        successor = randomMutant(current, p)
        valueS = evaluate(successor, p)
        if valueS < valueC:
            current = successor
            valueC = valueS
            i = 0              # Reset stuck counter
        else:
            i += 1
    return current, valueC

def randomMutant(current, p): ###
	i = random.randint(0, len(current) - 1)  # 몇 번째 var를 변경할 것인지를 랜덤하게 지정
	d = random.choice([DELTA, -DELTA]) # 어떻게 변경할 것인지도 랜덤하게 선택
	
	return mutate(current, i, d, p) # numeric.py의 mutate 함수를 사용해 값을 변경

def displaySetting():
    print()
    print("Search algorithm: First-Choice Hill Climbing")
    print()
    print("Mutation step size:", DELTA)

main()