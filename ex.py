#simulated annealing
def run(self,p):
    current = p.randomInit()
    valueC = p.evaluate(current)
    (best, bestValue) = (current, valueC)
    self.whenBestFound = i = 1
    t = self.intitTemp(p)
    while True:
        t = self.tSchedule(t)
        if(t==0 or i==self._limitEval):
            break
        neighbors = p.randomMutant(current)
        valueN = p.evaluate(neighbors)

        dE = valueN-valueC

        if valueN < valueC:
            current = neighbors
            valueC = valueN
        elif random.uniform(0,1) < math.exp(-dE/t):
            current = neighbors
            valueC = valueN
        
        if valueC < bestValue:
            (best, bestValue) = (current, valueC)
            whenBestFound = i
        i += 1

    self.whenBestFound = whenBestFound
    p.storeResult(best, bestValue)

# stochastic
def run(self, p):
    current = p.randomInit()
    valueC = p.evaluate(current)
    i = 0
    while i < self._limitStuck:
        neighbors = p.mutant(current)
        successor, valueS = self.stochasticBest(neighbors,p)
        if valueS < valueC:
            current = successor
            valueC = valueS
            i = 0
        else:
            i += 1
    
    p.storeResult(current, valueC)

#gradient Descent
def run(self, p):
    current = p.randomInit()
    valueC = p.evaluate(current)
    while True:
        nextP = p.takeStep(current,valueC)
        valueN = p.evaluate(nextP)
        if valueN >= valueC:
            break
        else:
            current = nextP
            valueC = valueN
    p.storeResult(currentP, valueC)

# first-Choice
def run(self, p):
    current = p.randomInit()
    valueC = p.evaluate(current)
    i = 0
    while i < self._limitStuck:
        successor = p.randomMuntant(current)
        valueS = p.evaluate(successor)
        if valueS < valueC:
            current = successor
            valueC = valueS
            i = 0
        else:
            i += 1
    p.storeResult(current, valueC)

#steepest-Ascent
def run(self, p):
    current = p.randomInit()
    valueC = p.evaluate(current)
    while True:
        neighbors = p.mutants(current)
        successor, valueS = self.bestOf(neighbors,p)
        if valueS >= valueC:
            break
        else:
            current = successor
            valueC = valueS
    p.storeResult(current,valueC)
            