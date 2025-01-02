import random
import math

DELTA = 0.01   # Mutation step size
NumEval = 0    # Total number of evaluations


def createProblem(): ###
    ## Read in an expression and its domain from a file.
    ## Then, return a problem 'p'.
    ## 'p' is a tuple of 'expression' and 'domain'.
    ## 'expression' is a string.
    ## 'domain' is a list of 'varNames', 'low', and 'up'.
    ## 'varNames' is a list of variable names.
    ## 'low' is a list of lower bounds of the varaibles.
    ## 'up' is a list of upper bounds of the varaibles.
    filename = input("Enter the file name of a function: ")
    infile = open(filename, "r")
    expression = infile.readline().rstrip()
    varNames, low, up = [], [], [] # 각각 변수 이름, 최소값, 최대값을 저장할 리스트

    while(True):
        varinfo = infile.readline()
        if varinfo == "":
            break
        varinfo = varinfo.rstrip().split(",") # (변수이름, low, up) 형식으로 저장된 정보를 가져온다
        varNames.append(varinfo[0]) #
        low.append(eval(varinfo[1]))
        up.append(eval(varinfo[2]))
    domain = [varNames, low, up] 
    return expression, domain

def randomInit(p): ###
    init = []
    for i in range(len(p[1][0])): # 변수의 수만큼 무작위로 생성하기
        low = p[1][1][i]
        up = p[1][2][i]
        init.append(random.uniform(low, up)) #각 변수의 max min값을 알아낸뒤 random.uniform을 사용해 임의의 실수 저장 
    return init    # Return a random initial point
                   # as a list of values
                   
def evaluate(current, p):
    ## Evaluate the expression of 'p' after assigning
    ## the values of 'current' to the variables
    global NumEval
    
    NumEval += 1
    expr = p[0]         # p[0] is function expression
    varNames = p[1][0]  # p[1] is domain: [varNames, low, up]
    for i in range(len(varNames)):
        assignment = varNames[i] + '=' + str(current[i])
        exec(assignment)
    return eval(expr)

def mutate(current, i, d, p): ## Mutate i-th of 'current' if legal
    curCopy = current[:]
    domain = p[1]        # [VarNames, low, up]
    l = domain[1][i]     # Lower bound of i-th
    u = domain[2][i]     # Upper bound of i-th
    if l <= (curCopy[i] + d) <= u:
        curCopy[i] += d
    return curCopy

def describeProblem(p):
    print()
    print("Objective function:")
    print(p[0])   # Expression
    print("Search space:")
    varNames = p[1][0] # p[1] is domain: [VarNames, low, up]
    low = p[1][1]
    up = p[1][2]
    for i in range(len(low)):
        print(" " + varNames[i] + ":", (low[i], up[i])) 

def displayResult(solution, minimum):
    print()
    print("Solution found:")
    print(coordinate(solution))  # Convert list to tuple
    print("Minimum value: {0:,.3f}".format(minimum))
    print()
    print("Total number of evaluations: {0:,}".format(NumEval))

def coordinate(solution):
    c = [round(value, 3) for value in solution]
    return tuple(c)  # Convert the list to a tuple