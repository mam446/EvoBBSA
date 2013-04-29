import random
import solution

class persSet:
    def __init__(self,parent):
        """
        This constructor creates the node and sets it's parent
        """
        self.down = []

        self.parent = parent

        self.name = ""
        self.height = 0
        self.depth = 0
        if parent:
            self.depth = self.parent.depth+1 
        self.take = []
        self.give  = [2]
        
        self.settings = None
        if parent:
            self.settings = self.parent.settings

    def evaluate(self,sets):
        """ 
        This function evaluates the node and returns the resulting set\

        """
        if self.name not in sets['pers']:
            sets['pers'][self.name] = []
        return sets['pers'][self.name]

    def update(self,depth,sets,settings):
        """
        This function updates the heights and depths and ensures
        that the settings pointer is pointing to the right settings 
        object
        """
        self.depth = depth
        self.height = 0 
        if not sets['pers'].keys():
            sets['pers']['A'] = []
        opts = sets['pers'].keys()
        self.name = random.choice(opts)
        self.settings = settings
        return self.height
    
    def randomize(self,sets,settings):
        """
        This function randomizes the parameters of the node if there are any

        """
        if not sets['pers'].keys():
            sets['pers']['A'] = []
        opts = sets['pers'].keys()
        self.name = random.choice(opts)
        return

    def fillTerms(self,sets,settings):
        """
        After the bbsa places all of the non-terminal nodes, this funciton is called
        to place the terminal nodes at the bottom of the parse tree

        """
        return

    def toString(self):
        """
        This function is used to create a string representaion of the bbsa

        """
        string = "["+self.name+"]"
        return string

    def toDict(self):
        """

        This function is used to create a dictionary representaion of the bbsa
        """
        return"["+self.name+"]"

    def makeProg(self,numTab,var):
        """
        This function generates the code for this node for the external verification

        """
        tab = "    "
        indent = ""
        for i in xrange(numTab):
            indent+=tab
        prog= "x"+var+ "= "+self.name+"\n"+indent 
        
        return prog

    def count(self):
        """
        This function calculates the number of nodes below it and including itself
        """
        return 1

class lastSet:
    def __init__(self,parent):
        """
        This constructor creates the node and sets it's parent
        """
        self.down = []
        self.parent = parent
        self.height = 0
        self.depth = 0
        if parent:
            self.depth = self.parent.depth+1 
        self.take = []
        self.give  = [2]
        
        self.settings = None
        if parent:
            self.settings = self.parent.settings
    
    def evaluate(self,sets):
        """ 
        This function evaluates the node and returns the resulting set\

        """
        return sets['last']

    def update(self,depth,sets,settings):
        """
        This function updates the heights and depths and ensures
        that the settings pointer is pointing to the right settings 
        object
        """
        self.depth = depth
        self.height = 0 
        self.settings = settings
        return self.height

    def randomize(self,sets,settings):
        """
        This function randomizes the parameters of the node if there are any

        """
        return

    def fillTerms(self,sets,settings):
        """
        After the bbsa places all of the non-terminal nodes, this funciton is called
        to place the terminal nodes at the bottom of the parse tree

        """
        return

    def toString(self):
        """
        This function is used to create a string representaion of the bbsa

        """
        return "[Last]"

    def toDict(self):
        """

        This function is used to create a dictionary representaion of the bbsa
        """
        return"[Last]"
    
    def makeProg(self,numTab,var):
        """
        This function generates the code for this node for the external verification

        """
        tab = "    "
        indent = ""
        for i in xrange(numTab):
            indent+=tab
        prog= "x"+var+ "= last\n"+indent 
        
        return prog

    def count(self):
        """
        This function calculates the number of nodes below it and including itself
        """
        return 1

class emptySet:
    def __init__(self,parent):
        """
        This constructor creates the node and sets it's parent
        """
        self.down = []
        self.parent = parent
        self.height = 0
        self.depth = 0
        if parent:
            self.depth = self.parent.depth+1 
        self.take = []
        self.give  = [0]
        
        self.settings = None
        if parent:
            self.settings = self.parent.settings
    
    def evaluate(self,sets):
        """ 
        This function evaluates the node and returns the resulting set\

        """
        return []

    def update(self,depth,sets,settings):
        """
        This function updates the heights and depths and ensures
        that the settings pointer is pointing to the right settings 
        object
        """
        self.depth = depth
        self.height = 0 
        self.settings = settings
        return self.height

    def randomize(self,sets,settings):
        """
        This function randomizes the parameters of the node if there are any

        """
        return

    def fillTerms(self,sets,settings):
        """
        After the bbsa places all of the non-terminal nodes, this funciton is called
        to place the terminal nodes at the bottom of the parse tree

        """
        return

    def toString(self):
        """
        This function is used to create a string representaion of the bbsa

        """
        return "[ ]"

    def toDict(self):
        """

        This function is used to create a dictionary representaion of the bbsa
        """
        return"[ ]"
    
    def makeProg(self,numTab,var):
        """
        This function generates the code for this node for the external verification

        """
        tab = "    "
        indent = ""
        for i in xrange(numTab):
            indent+=tab
        prog= "x"+var+ "= []\n"+indent 
        
        return prog

    def count(self):
        """
        This function calculates the number of nodes below it and including itself
        """
        return 1

class genRandom:
    def __init__(self,parent):
        """
        This constructor creates the node and sets it's parent
        """
        self.down = []
        self.parent = parent
        self.height = 0
        self.depth = 0
        if parent:
            self.depth = self.parent.depth+1 
        self.settings = None
        self.take = []
        self.give  = [1]
    
    def evaluate(self,sets):
        """ 
        This function evaluates the node and returns the resulting set\

        """
        return [solution.solution(self.settings)]

    def update(self,depth,sets,settings):
        """
        This function updates the heights and depths and ensures
        that the settings pointer is pointing to the right settings 
        object
        """
        self.depth = depth
        self.height = 0 
        return self.height

    def randomize(self,sets,settings):
        """
        This function randomizes the parameters of the node if there are any

        """
        self.settings = settings
        return

    def fillTerms(self,sets,settings):
        """
        After the bbsa places all of the non-terminal nodes, this funciton is called
        to place the terminal nodes at the bottom of the parse tree

        """
        self.settings = settings
        return

    def toString(self):
        """
        This function is used to create a string representaion of the bbsa

        """
        return "<generator>"

    def toDict(self):
        """

        This function is used to create a dictionary representaion of the bbsa
        """
        return"<generator>"
    
    def makeProg(self,numTab,var):
        """
        This function generates the code for this node for the external verification

        """
        tab = "    "
        indent = ""
        for i in xrange(numTab):
            indent+=tab
        prog= "x"+var+ "= [solution.solution()]\n"+indent 
        
        return prog

    def count(self):
        """
        This function calculates the number of nodes below it and including itself
        """
        return 1

termNodes = [persSet,lastSet]

















