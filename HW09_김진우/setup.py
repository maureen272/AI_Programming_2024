class Setup:
    def __init__(self):
        self._pType = 0
        self._aType = 0 
        self._delta = 0
        self._alpha = 0
        self._dx = 0
        self._resolution = 0 # 이번과제에서 추가된 변수
 
    def setVariables(self, parameters):
        self._pType = parameters['pType']
        self._aType = parameters['aType']
        self._delta = parameters['delta']
        self._alpha = parameters['alpha']
        self._dx = parameters['dx']
        self._resolution = parameters['resolution'] # 추가
        
    def getAType(self):
        return self._aType
    
