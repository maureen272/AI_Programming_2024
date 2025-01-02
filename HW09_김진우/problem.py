import random
import math
from setup import Setup

class Problem(Setup):
    def __init__(self):
        Setup.__init__(self)
        self._solution = []
        self._value = 0
        self._numEval = 0

        # 8번째 과제에서 추가된 부분 -> 제공된 PPT 대로 추가함
        self._pfileName = '' 
        self._bestSolution = []
        self._bestMinimum = 0
        self._avgMinimum = 0
        self._avgNumEval = 0
        self._sumOfNumEval = 0
        self._avgWhen = 0

    # 파일명과 Setup에 정의된 변수들을 받아서 self._pfileName에 assign
    def setVariables(self, parameters):
        Setup.setVariables(self, parameters)
        self._pfileName = parameters['pFileName']

    # 8번째 과제에서 추가된 부분 : accessor method들 추가
    def getSolution(self):
        return self._solution
    
    def getValue(self):
        return self._value
    
    def getNumEval(self):
        return self._numEval

    def setNumEval(self, numEval):
        self._numEval = numEval

    # 결과 저장
    def storeExpResult(self, results):
        self._bestSolution  = results[0]
        self._bestMinimum   = results[1]
        self._avgMinimum    = results[2]
        self._avgNumEval    = results[3]
        self._sumOfNumEval  = results[4]
        self._avgWhen       = results[5]
    
    def randomInit(self):
        pass

    def evaluate(self):
        pass

    def mutants(self):
        pass

    def randomMutant(self, current):
        pass

    def describe(self):
        pass

    def storeResult(self, solution, value):
        self._solution = solution
        self._value = value

    def report(self):
        print()
        print("Total number of evaluations: {0:,}".format(self._sumOfNumEval))



class Numeric(Problem):
    def __init__(self):
        Problem.__init__(self)
        self._expression = ''
        self._domain = []     # domain as a list
        self._delta = 0.01    # Step size for axis-parallel mutation

        #self._alpha = 0.01    # Update rate for gradient descent
        #self._dx = 10 ** (-4) # Increment for calculating derivative
    
    def setVariables(self, parameters): # parameters를 파라미터로 받아서 변수들을 설정
        Problem.setVariables(self, parameters) # 부모 클래스의 setVariables 호출
        filename = parameters['pFileName'] # 파일명을 filename에 저장
        infile = open(filename, "r")
        self._expression = infile.readline()
        varNames, low, up = [], [], [] # 각각 변수 이름, 최소값, 최대값을 저장할 리스트
        line = infile.readline()

        while line != "":
            data = line.split(",")
            varNames.append(data[0])
            low.append(eval(data[1]))
            up.append(eval(data[2]))
            line = infile.readline()
        infile.close()
        self._domain = [varNames, low, up] 
    
    #def getDelta(self): # new method 
        #return self._delta

    def describe(self): # describeProblem
        print()
        print("Objective function:")
        print(self._expression)
        print("Search space:")
        varNames = self._domain[0]
        low = self._domain[1]
        up = self._domain[2]
        for i in range(len(low)):
            print(" " + varNames[i] + ":", (low[i], up[i]))

    def report(self):   # 출력양식에 맞게 출력되게 코드 수정
        aType = self._aType
        print()
        print("Average objective value: {0:.3f}".format(self._avgMinimum))
        print("Average number of evaluations: {0:,}".format(self._avgNumEval))
        print()
        print("Best solution found:")
        print(self.coordinate()) 
        print("Best value: {0:,.3f}".format(self._bestMinimum))
        if 5 <= aType <= 6:
            print("Average iteration of finding the best solution: {0:,}".format(self._avgWhen))
        Problem.report(self)

    def coordinate(self):
        c = [round(value,3) for value in self._bestSolution] # bestSolution이 출력되게 수정
        return tuple(c)
    
    def randomInit(self):
        domain = self._domain
        low, up = domain[1], domain[2]
        init = []

        for i in range(len(low)):
            r = random.uniform(low[i], up[i])
            init.append(r)
        return init
    
    def evaluate(self, current):
        self._numEval += 1 # 총 eval 횟수 하나식 증가
        expr = self._expression 
        varNames = self._domain[0]
        for i in range(len(varNames)):
            assignment = varNames[i] + '=' + str(current[i]) # 변수명 = '값' 형태로 출력되게 설정
            exec(assignment) # 설정된 값을 실행
        return eval(expr) 
    
    def mutate(self, current, i, d):
        mutant = current[:]
        domain = self._domain
        l= domain[1][i]
        u = domain[2][i]
        if l <= (mutant[i] + d) <= u:
            mutant[i] += d
        return mutant
    
    # steepest-ascent
    def mutants(self, current): # steepest ascent (n)에서 Numeric problem 관련 함수를 numeric class로 이동
        neighbors = []
        for i in range(len(current)): # For each variable
            mutant = self.mutate(current, i, self._delta)
            neighbors.append(mutant)
            mutant = self.mutate(current, i, -self._delta)
            neighbors.append(mutant)
        return neighbors
    
    # first-choice
    def randomMutant(self, current): ###
        i = random.randint(0, len(current) - 1)  # 몇 번째 var를 변경할 것인지를 랜덤하게 지정
        if random.uniform(0,1) < 0.5: # 이때 D는 0.5의 확률로 증가할지 감소할지 결정되어야함
            d = self._delta
        else:
            d = - self._delta
            
        return self.mutate(current, i, d) 
    
    # gradient descent
    #def getAlpha(self): # self._alpha Accessor
        #return self._alpha
    
    #def getDx(self): # self._dx Accessor
       # return self._dx
    
    # gradient를 통해 next step을 계산
    # next step이 domain 범위 이내 일 때만 next step을 반환
    def takeStep(self, currentP, valueC):
        next = currentP[:] # 리스트 복사
        gradient = self.gradient(currentP,valueC) # gradient 값 계산
        for i in range(len(next)): # 각각의 변수에 대해
            next[i] -= self._alpha * gradient[i] # gradient 값에 따라 다음 step을 계산 -> w' = w - alpha*f'(w)
        if self.isLegal(next): # 새로 만들어진 값이 범위 내에 있다면 
            return next # 새로운 값을 반환
        else:
            return currentP # 범위 밖이면 원래 값을 반환
    
    # 주어진 변수 값들(x)이 도메인 범위 이내인지 확인하고 T/F를 반환
    def isLegal(self, x):
        low = self._domain[1]
        up = self._domain[2]
        for i in range(len(x)): # 각 변수에 대해 실행
            if(low[i] > x[i] or up[i] < x[i]): # 범위 밖이면
                return False # False 반환
        return True # 범위 안이면 True 반환
    
    # '각 변수'의 gradient를 list형으로 반환 
    def gradient(self, x, v): # x는 현재 변수 값, v는 현재 값 list
        gradient = [] # gradient 값을 저장할 리스트
        for i in range(len(x)): # 각 변수에 대해
            changedX = x[:] # 리스트 복사
            changedX[i] += self._dx # i번째 변수에 f(x+dx) 해주기
            gradient.append((self.evaluate(changedX) - v) / self._dx) # f'(x) = (f(x+dx) - f(x)) / dx 계산
        return gradient # gradient 값 반환
    # GA class
    # initializePop과 randBinStr는 GA를 위한 메소드
    def initializePop(self, size):
        pop = []
        for i in range(size):
            chromosome = self.randBinStr()
            pop.append([0, chromosome])
        return pop
    
    def randBinStr(self):
        # Numeric 문제의 변수 N (self._domain[0]) 개에 대해서,
        # 각 변수 별 self._resolution 크기의 random binary 생성
        # N=5, self._resolution=10 이라면,
        # 50길이의 [1, 0, 1, 0, 0, 1, 0, 1, …] 배열 생성하여 반환
        #k = len(self._domain[0]) * self._resolution
        k = len(self._domain[0]) * self._resolution  
        chromosome = []
        for i in range(k):
            allele = random.randint(0, 1)
            chromosome.append(allele)
        return chromosome
    
    def evalInd(self, ind):
        ind[0] = self.evaluate(self.decode(ind[1])) # [1,0,1,0,0,1...]로 표현한 값을 evaluate할 수 있도록 실수로 변환하는 decode함수 필요

    def decode(self, chromosome):
        r = self._resolution
        low = self._domain[1]
        up = self._domain[2]
        genotype = chromosome[:]
        phenotype = []
        start = 0
        end = r

        #print(start, "  ",end)
        for var in range(len(self._domain[0])):
            value = self.binaryToDecimal(genotype[start:end], low[var], up[var])
            phenotype.append(value)
            
            start += r
            end += r
        return phenotype

    
    def binaryToDecimal(self, binCode, l, u):
        # binCode [0, 1, 0, 1, …]을
        # low, upper bound내의 값으로 표현해서 return
        # l=0, u=10, binCode=[x, x, x, x] 일 때,
        # [0,0,0,0]=0, [0,0,0,1]=0.625, [0,0,1,0]=1.25
        # [0,0,1,1]=1.875, …, [1,1,1,1]=9.375
        # u가 포함 안되는데, binCode가 충분히 길다는 가정하에 포함 여부는 구현에 큰 문제없음
        r = len(binCode)
        decimalValue = 0
        for i in range(r):
            decimalValue += binCode[i] * (2 ** (r - i - 1))
        return l + (u - l) * decimalValue / (2 ** r - 1)
    
    def crossover(self, ind1, ind2, uXp):
        chr1, chr2 = self.uXover(ind1[1], ind2[1], uXp)
        return [0, chr1], [0, chr2]
    
    def uXover(self, chrInd1, chrInd2, uXp): # uniform crossover
        # chrInd1, chrInd2의 각 원소를 확률적(uXp)으로 crossover
        chr1 = chrInd1[:] # Make copies
        chr2 = chrInd2[:]
        # implement
        for i in range(len(chr1)):
            if random.uniform(0, 1) < uXp:
                chr1[i], chr2[i] = chr2[i], chr1[i]
        return chr1, chr2

    def mutation(self, ind, mrF): # bit-flip mutation
        # mrF * (1/ lnegth of individual) 확률로 ind의 개별 원소 bit-flip
        child = ind[:] # Make copy
        n = len(child[1])
        # implement
        for i in range(n):
            if random.uniform(0, 1) < mrF * (1/n):
                child[1][i] = 1 - child[1][i]
        return child
        
    def indToSol(self, ind): # ind를 solution으로 변환
        return self.decode(ind[1])

class Tsp(Problem):
    def __init__(self):
        Problem.__init__(self)
        self._numCities = 0
        self._locations = []       # A list of tuples
        self._distanceTable = []

    def setVariables(self,parameters): # parameters를 파라미터로 받아서 변수들을 설정
        ## Read in a TSP (# of cities, locatioins) from a file.
        ## Then, create a problem instance and return it.
        fileName = parameters['pFileName']
        Problem.setVariables(self, parameters) # 부모 클래스의 setVariables 호출
        infile = open(fileName, 'r')
        # First line is number of cities
        self._numCities = int(infile.readline())
        locations = []
        line = infile.readline()  # The rest of the lines are locations
        while line != '':
            locations.append(eval(line)) # Make a tuple and append
            line = infile.readline()
        infile.close()
        self._locations = locations
        self._distanceTable = self.calcDistanceTable()

    def calcDistanceTable(self):
            n = self._numCities
            locations = self._locations
            table = [[0] * n for _ in range(n)] # 2차원 리스트 초기화
            
            for i in range(n):
                for j in range(n):
                    if i != j:  # 같은 도시 간 거리는 계산하지 않음
                        table[i][j] = math.sqrt((locations[j][0] - locations[i][0]) ** 2 + 
                                                (locations[j][1] - locations[i][1]) ** 2) # 두 점 사이의 거리를 구하는 공식 사용해서 table에 저장
            return table  # A symmetric matrix of pairwise distances

    def randomInit(self):   # Return a random initial tour
        n = self._numCities
        init = list(range(n))
        random.shuffle(init)
        return init

    def evaluate(self, current): ###
        ## Calculate the tour cost of 'current'
        ## 'p' is a Problem instance
        ## 'current' is a list of city ids
        self._numEval += 1 # 총 eval횟수 늘이기
        n = self._numCities
        table = self._distanceTable
        cost = 0 # 비용 초기화

        # 첫 도시부터 맨 마지막 도시까지 투어하면서 distance table을 참고하여 비용 계산
        for i in range(n-1):
            locFrom = current[i]
            locTo = current[i+1]
            cost += table[locFrom][locTo]
        # 맨 마지막 도시에서 처음 도시로 돌아오는 비용을 고려해서 cost에 더해줌
        cost += table[current[-1]][current[0]]
        
        return cost
    
    #steepest-ascent
    def mutants(self, current): # Apply inversion
        n = self._numCities
        neighbors = []
        count = 0
        triedPairs = []
        while count <= n:  # Pick two random loci for inversion
            i, j = sorted([random.randrange(n) for _ in range(2)])
            if i < j and [i, j] not in triedPairs:
                triedPairs.append([i, j])
                curCopy = self.inversion(current, i, j)
                count += 1
                neighbors.append(curCopy)
        return neighbors

    def inversion(self, current, i, j):  # Perform inversion
        curCopy = current[:] # 리스트 복사
        while i < j:
            curCopy[i], curCopy[j] = curCopy[j], curCopy[i]
            i += 1
            j -= 1
        return curCopy

    #first-choice
    def randomMutant(self, current): # Apply inversion 
        while True:
            i, j = sorted([random.randrange(self._numCities) 
                        for _ in range(2)])
            if i < j:
                curCopy = self.inversion(current, i, j)
                break
        return curCopy

    def describe(self):
        print()
        n = self._numCities
        print("Number of cities:", n)
        print("City locations:")
        locations = self._locations
        for i in range(n):
            print("{0:>12}".format(str(locations[i])), end = '')
            if i % 5 == 4:
                print()

    def report(self):   #출력 형식에 맞게 출력되게 코드 수정
        aType = self._aType
        print()
        print("Average tour cost: {}".format(round(self._avgMinimum)))
        print("Average number of evaluations: {0:,}".format(self._avgNumEval))
        print()
        print("Best tour found:")
        self.tenPerRow()
        print("Best tour cost: {0:,}".format(round(self._bestMinimum)))
        if 5 <= aType <= 6:
            print("Average iteration of finding the best solution: {0:,}".format(self._avgWhen))
        Problem.report(self)

    def tenPerRow(self):
        solution = self._bestSolution # bestSolution을 저장하는 것으로 코드 수정
        for i in range(len(solution)):
            print("{0:>5}".format(solution[i]), end='')
            if i % 10 == 9: # 10개씩 출력 -> 줄바꿈
                print()

    def initializePop(self, size):
        #n = self._numCities
        pop = []
        for i in range(size):
        # tsp.randomInit 메서드 이용하여 chromosome 생성하고 pop에 추가
        # chromosome = [eval_value, [tour order]]
        # = [0, [5, 12, 17, 11, 7, 22, …]]
            chromosome = self.randomInit()
            pop.append([0, chromosome])
        return pop

    def evalInd(self, ind):
        ind[0] = self.evaluate(ind[1])

    def crossover(self, ind1, ind2, XR):
        if random.uniform(0,1) <= XR:
            chr1, chr2 = self.oXover(ind1[1], ind2[1])
        else:
            chr1, chr2 = ind1[1][:], ind2[1][:]
        return [0, chr1], [0, chr2]
    
    def oXover(self, chrInd1, chrInd2): 
        max = self._numCities
        while True:
        # 범위에 맞게 난수 2개 생성
            num1 = random.randint(1, max)
            num2 = random.randint(1, max)
            # 생성된 난수를 비교하여 작은 값을 a에, 큰 값을 b에 할당
            if num1 < num2:
                a = num1
                b = num2
            else:
                a = num2
                b = num1
            if a != b:
                break
        chr1 = chrInd1[:]
        chr2 = chrInd2[:]
        # 중복 도시 제거를 위해 교차 구간에 해당하는 도시를 -1로 표시
        for i in range(len(chr1)):
            if chr1[i] in chrInd2[a:b]:
                chr1[i] = -1
            if chr2[i] in chrInd1[a:b]:
                chr2[i] = -1
        # a:b 사이를 비우는 작업 (left shift)
        for i in range(b): 
            chr1.append(chr1[0])
            chr2.append(chr2[0])
            del chr1[0]
            del chr2[0]
        # -1 값을 제거
        chr1 = [x for x in chr1 if x != -1]
        chr2 = [x for x in chr2 if x != -1]
        # 나머지 부분 추가 (left shift 후 남은 부분 복원)
        for i in range(len(chrInd1) - b):
            chr1.append(chr1[i])
            chr2.append(chr2[i])
        del chr1[:len(chrInd1) - b]
        del chr2[:len(chrInd1) - b]
        # a:b 구간 교차
        for i in range(a, b):
            chr1.insert(i, chrInd2[i])  # chrInd2의 a:b 구간을 chr1에 삽입
            chr2.insert(i, chrInd1[i])  # chrInd1의 a:b 구간을 chr2에 삽입
        return chr1, chr2

    def mutation(self, ind, mR): # 두 지점 사이의 값을 거꾸로 뒤집는 방식으로 변이가 일어난다
        mInd = ind[:]
        if random.uniform(0,1) < mR:
            while True:
                a = random.randint(0, len(mInd[1]))
                b = random.randint(0, len(mInd[1]))
                if a < b:
                    break
            mInd[1][a:b] = mInd[1][b-1:a-1 if a != 0 else None:-1]
        return mInd
    
    def indToSol(self, ind):
        return ind[1]