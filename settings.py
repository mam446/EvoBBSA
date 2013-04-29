





class settings:
    """
    This class stores a majority of the settings that can be altered in the algorithm.
    It is also used to store the current state of a given run, to keep track of evaluations and operations.
    """

    def __init__(self):
        """
        default constructor
        """
        self.seed = None        
        
        self.problemType = 'dTrap'
                
        self.trapSize = 7
        self.stepSize = 2

        self.nk = 5
        self.dimensions = 30
        self.nkFile=''

        self.maxDepth = 5 
        self.maxEvals = 50000


        self.maxChilds = 25
 
        self.maxN = 10
        
        self.maxIterations = 10000
        self.converge = 25

        self.numRuns = 5 

        self.maxK = 25
        self.maxCount = 25
        self.solSet = {'length':210,'rate':.1}
        self.curEvals = 0
        

        self.initPop = 50

        self.curOp = 0
        self.maxOp = 500000

        self.parsimony = .001

