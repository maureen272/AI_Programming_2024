class Setup:
    def __init__(self):
        self._pType = 0
        self._aType = 0 # 추가된 부분
        self._delta = 0
        self._alpha = 0
        self._dx = 0

    def setVariables(self, parameters):
        self._pType = parameters['pType']
        self._aType = parameters['aType']
        self._delta = parameters['delta']
        self._alpha = parameters['alpha']
        self._dx = parameters['dx']
        
    def getAType(self):
        return self._aType
    
