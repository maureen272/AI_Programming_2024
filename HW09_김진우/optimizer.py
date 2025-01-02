from setup import Setup
import random
import math

# Optimizer class가 새로 생성됨
class Optimizer(Setup):
    def __init__(self):
        Setup.__init__(self)
        self._numExp = 0

    def setVariables(self, parameters):
        Setup.setVariables(self, parameters)
        self._numExp = parameters['numExp']

    def getNumExp(self):
        return self._numExp
    
    def displayNumExp(self):
        print()
        print("Number of experiments: {}".format(self._numExp))
    

class HillClimbing(Optimizer):
    def __init__(self):
        Optimizer.__init__(self)
        #self._pType = 0
        self._limitStuck = 1000 #변하는 부분
        self._numRestart = 0 #변하는 부분

    def setVariables(self, parameters):
        Optimizer.setVariables(self, parameters)
        self._limitStuck = parameters['limitStuck']
        self._numRestart = parameters['numRestart']
    
    def randomRestart(self, p):
        p.setNumEval(0)
        i = 1
        self.run(p)
        bestSolution = p.getSolution()
        bestMinimum = p.getValue()
        numEval = p.getNumEval()
        while i < self._numRestart:
            self.run(p)
            newSolution = p.getSolution()
            newMinimum = p.getValue()
            numEval += p.getNumEval()
            if newMinimum < bestMinimum:
                bestSolution = newSolution
                bestMinimum = newMinimum
            i += 1
        p.storeResult(bestSolution, bestMinimum)


    def displaySetting(self):
        if self._numRestart > 1:
            print("Number of random restarts: {}".format(self._numRestart))
            print()
        #numeric이고 gradient descent아니면 delta값 출력
        if(self._pType == 1 and self._aType != 4 and self._aType != 6):
            print("Mutation step size:", self._delta)
        # first choice or stochastic이면 limitStuck 출력
        if(self._aType == 2 or self._aType == 3):
            print("Max evaluations with no improvement: {0:,} iterations".format(self._limitStuck))
        #numeric이고 Gradient Descent일경우에는 alpha값과 dx값 출력
        elif(self._pType == 1 and self._aType == 4):
            print("Update rate:", self._alpha)
            print("Increment for calculating derivatives:", self._dx)

    def run(self):
        pass


class FirstChoice(HillClimbing):
    def displaySetting(self):
        # first-choice.py 코드의 displaySetting 부분 활용
        # HillClimb에 정의했던 displaySetting을 Super를 통해 호출해서 구현하기
        print()
        print("Search algorithm: First-Choice Hill Climbing")
        super().displaySetting()
        #print("Max evaluations with no improvement: {0:,} iterations".format(self._limitStuck))

        
    def run(self, p):
        # first-choice.py에 정의했던 firstchoice 함수를 활용해서 구현
        current = p.randomInit()
        valueC = p.evaluate(current)
        f = open("first.txt", 'w')   # 파일 생성
        i = 0
        while i < self._limitStuck:
            successor = p.randomMutant(current)
            valueS = p.evaluate(successor)
            f.write(str(valueC) + '\n') # 파일에 쓰기 -> 매 iteration마다 결과를 저장해야하기떄문
            if valueS < valueC:
                current = successor
                valueC = valueS
                i = 0
            else:
                i += 1
        f.close()
        p.storeResult(current, valueC)
 

class SteepestAscent(HillClimbing):
    def displaySetting(self):
        print()
        print("Search algorithm: Steepest-Ascent Hill Climbing")
        super().displaySetting()
    
    def run(self, p):
        current = p.randomInit() # 'current' is a list of values
        valueC = p.evaluate(current)
        f = open("SteepestAscent.txt", 'w')
        while True:
            neighbors = p.mutants(current)
            successor, valueS = self.bestOf(neighbors, p)
            f.write(str(valueC) + '\n')
            if valueS >= valueC:
                break
            else:
                current = successor
                valueC = valueS
        p.storeResult(current, valueC)
        f.close()

    def bestOf(self, neighbors, p):
            best = neighbors[0]
            bestValue = p.evaluate(best)
            for i in range(1, len(neighbors)):
                newValue = p.evaluate(neighbors[i])
                if newValue < bestValue:
                    best = neighbors[i]
                    bestValue = newValue # 새로운 값이 더 작으면(더 좋은 것이기때문에) 바꿔주기

            return best, bestValue
    

class GradientDescent(HillClimbing):

    def displaySetting(self):
        print()
        print("Search algorithm: Gradient Descent")
        super().displaySetting()
        #print("Udate rate:", self._alpha)
        #print("Increment for calculating derivative:", self._dx)

    def run(self,p):
        currentP = p.randomInit()  # Current point
        valueC = p.evaluate(currentP)
        f = open("GradientDescent.txt", 'w')
        while True:
            nextP = p.takeStep(currentP, valueC)
            valueN = p.evaluate(nextP)
            f.write(str(valueC) + '\n')
            if valueN >= valueC:
                break
            else:
                currentP = nextP
                valueC = valueN
        p.storeResult(currentP, valueC)
        f.close()

class Stochastic(HillClimbing):
    def __init__(self):
        pass
    def displaySetting(self):
        print()
        print("Search algorithm: Stochastic Hill Climbing")
        super().displaySetting()

    def run(self, p):
        # hint; Stochastic알고리즘은 Steepest Ascent 알고리즘과 흐름이 유사함
        current = p.randomInit()
        valueC = p.evaluate(current)
        f = open("Stochastic.txt", 'w') # 파일 생성
        i = 0
        while i < self._limitStuck: # limitStuck만큼 반복
            neighbors = p.mutants(current) # 현재 위치에서의 이웃들을 찾음
            successor, valueS = self.stochasticBest(neighbors, p) # 이웃을 확률적으로 선택
            f.write(str(valueC) + '\n')
            if valueS < valueC: # 선택된 이웃이 더 좋은 경우(값이 작은 경우)
                current = successor 
                valueC = valueS 
                i = 0
            else:
                i += 1
        p.storeResult(current, valueC)
        f.close()
    # some useful codes.py의 stochasticBest 함수를 활용    
    def stochasticBest(self, neighbors, p):
        # Smaller valuse are better in the following list
        valuesForMin = [p.evaluate(indiv) for indiv in neighbors]
        largeValue = max(valuesForMin) + 1
        valuesForMax = [largeValue - val for val in valuesForMin]
        # Now, larger values are better
        total = sum(valuesForMax)
        randValue = random.uniform(0, total)
        s = valuesForMax[0]
        for i in range(len(valuesForMax)):
            if randValue <= s: # The one with index i is chosen
                break
            else:
                s += valuesForMax[i+1]
        return neighbors[i], valuesForMin[i]

class Metaheuristics(Optimizer):
    def __init__(self):
        Optimizer.__init__(self)

    def setVariables(self, parameters):
        Optimizer.setVariables(self, parameters)
        self._numExp = parameters['numExp']
        self._numSample = 10
        self._limitEval = parameters['limitEval']

    def displaySetting(self):
        if self._pType == 1: # numeric일 경우에만 dx값 출력되도록
            print("Mutation step size:", self._delta)
    
    def getWhenBestFound(self):
        return self._whenBestFound

class SimulatedAnnealing(Metaheuristics):
    def __init__(self):
        Metaheuristics.__init__(self)
        self._numSample = 100
        self._limitEval = 10000
        self._whenBestFound = 0

    
    def displaySetting(self):
        print()
        print("Search algorithm: Simulated Annealing")
        print()
        print("Number of evaluations until termination: {0:,}".format(self._limitEval))
        super().displaySetting()

    def run(self, p):
        current = p.randomInit()
        valueC = p.evaluate(current)
        best, valueBest = current, valueC
        self.whenBestFound = i = 1
        t = self.initTemp(p)
        f = open("anneal.txt", 'w')
        while True:
            t = self.tSchedule(t) # tSchedule을 통해 t값을 업데이트
            f.write(str(valueC) + '\n')
            if(t == 0 or i==self._limitEval): #temperature가 0이 되거나 limitEval에 도달하면 종료
                break
            neighbor = p.randomMutant(current) # 현재 상태에 대한 randomMutant 생성
            valueN = p.evaluate(neighbor) # mutant 평가
            
            dE = valueN - valueC
            if(valueN - valueC < 0): # 값이 더 좋다면 업데이트
                current = neighbor
                valueC = valueN
            # 값이 안좋다면 확률적  update
            #이때 확률은 tempture에 따라 결정
            elif random.uniform(0,1) < math.exp(-dE/t):
                current = neighbor
                valueC = valueN
            # 업데이트 된 값이 best보다 좋다면 best 업데이트    
            if valueC < valueBest:
                (best, valueBest) = (current, valueC)
                whenBestFound = i

            i+=1 #iteration 증가

        self._whenBestFound = whenBestFound
        p.storeResult(best, valueBest)
        f.close()

    def initTemp(self, p): # To set initial acceptance probability to 0.5
        diffs = []
        for i in range(self._numSample):
            c0 = p.randomInit()     # A random point
            v0 = p.evaluate(c0)     # Its value
            c1 = p.randomMutant(c0) # A mutant
            v1 = p.evaluate(c1)     # Its value
            diffs.append(abs(v1 - v0))
        dE = sum(diffs) / self._numSample  # Average value difference
        t = dE / math.log(2)        # exp(–dE/t) = 0.5
        return t

    def tSchedule(self, t):
        return t * (1 - (1 / 10**4))
    
# 추가된 알고리즘
class GA(Metaheuristics):
    def __init__(self):
        Metaheuristics.__init__(self)
        self._popSize = 0     # Population size
        self._uXp = 0   # Probability of swappping a locus for Xover
        self._mrF = 0   # Multiplication factor to 1/n for bit-flip mutation
        self._XR = 0    # Crossover rate for permutation code
        self._mR = 0    # Mutation rate for permutation code
        self._pC = 0    # Probability parameter for Xover
        self._pM = 0    # Probability parameter for mutation

    def setVariables(self, parameters):
        Metaheuristics.setVariables(self, parameters)
        self._popSize = parameters['popSize']
        self._uXp = parameters['uXp']
        self._mrF = parameters['mrF']
        self._XR = parameters['XR']
        self._mR = parameters['mR']
        if self._pType == 1:
            self._pC = self._uXp
            self._pM = self._mrF
        if self._pType == 2:
            self._pC = self._XR
            self._pM = self._mR

    def run(self, p):
       # Population 생성
        pop = p.initializePop(self._popSize)
        # Population 중 최적해 찾기
        best = self.evalAndFindBest(pop, p)
        numEval = p.getNumEval()
        whenBestFound = numEval
        # limitEval 까지 [다음세대 생성–평가] 반복
        while numEval < self._limitEval:
            newPop = []
            I = 0
        # 다음 세대 생성; start
            while I < self._popSize:
                par1, par2 = self.selectParents(pop)
                ch1, ch2 = p.crossover(par1, par2, self._pC)
                newPop.extend([ch1, ch2])
                I += 2
            newPop = [p.mutation(ind, self._pM) for ind in newPop]
            pop = newPop
            # 다음 세대 생성; end
            # 다음 세대 값 평가 및 best 업데이트
            newBest = self.evalAndFindBest(pop, p)
            numEval = p.getNumEval()
            if newBest[0] < best[0]:
                best = newBest
                whenBestFound = numEval
        self._whenBestFound = whenBestFound
        bestSolution = p.indToSol(best)
        p.storeResult(bestSolution, best[0])

    def evalAndFindBest(self, pop, p):
        best = pop[0]
        p.evalInd(best)
        bestValue = best[0]
        for i in range(1, len(pop)):
            p.evalInd(pop[i])
            newValue = pop[i][0]
            if newValue < bestValue:
                best = pop[i]
                bestValue = newValue
        return best

    def selectParents(self, pop):
        ind1, ind2 = self.selectTwo(pop)
        par1 = self.binaryTournament(ind1, ind2)
        ind1, ind2 = self.selectTwo(pop)
        par2 = self.binaryTournament(ind1, ind2)
        return par1, par2
    
    def selectTwo(self, pop):
    # pop에서 random하게 2개의 individuals 선택해서 반환
        popCopy = pop[:]
        random.shuffle(popCopy)
        return popCopy[0], popCopy[1]

    def binaryTournament(self, ind1, ind2):
    # 2개의 individuals 중 더 좋은 ind 선택해서 반환
        if ind1[0] < ind2[0]:
            return ind1
        else:
            return ind2
        
    def displaySetting(self):
        print()
        print("Search Algorithm: Genetic Algorithm")
        print()
        Metaheuristics.displaySetting(self)
        print()
        print("Population size:", self._popSize)
        if self._pType == 1:   # Numerical optimization
            print("Number of bits for binary encoding:", self._resolution)
            print("Swap probability for uniform crossover:", self._uXp)
            print("Multiplication factor to 1/L for bit-flip mutation:",
                  self._mrF)
        elif self._pType == 2: # TSP
            print("Crossover rate:", self._XR)
            print("Mutation rate:", self._mR)


