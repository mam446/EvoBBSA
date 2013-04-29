import random
import solution
import termNodes

class addSet:
    """
    This node takes the Union of two sets and returns the resulting set
    """
    def __init__(self,parent):
        """
        This constructor creates the node and sets it's parent
        """
        self.depth = 0
        self.height = 0
        
        self.parent = parent 
        if parent:
            self.depth = self.parent.depth+1 
        self.down = [None,None]
        self.take = [1,2]
        self.give  = [2]

        self.settings = None
        if parent:
            self.settings = self.parent.settings
        
    def evaluate(self,sets):
        """ 
        This function evaluates the node and returns the resulting set


        """
        rRight = None
        rLeft = None

        if self.down[0]:
            rLeft = self.down[0].evaluate(sets)
        else:
            raise "Node addSet has no right child"

        if self.down[1]:
            rRight = self.down[1].evaluate(sets)
        else:
            raise "Node addSet has no left child"

        ret = []

        self.settings.curOp+=len(rLeft)*len(rRight) 
        
        if self.settings.curOp>=self.settings.maxOp:
            return[]
        
        
        ret.extend(rRight)
        for i in xrange(len(rLeft)):
            if rLeft[i] not in rRight:
                ret.append(rLeft[i]) 

        return ret

    def update(self,depth,sets,settings):
        """
        This function updates the heights and depths and ensures
        that the settings pointer is pointing to the right settings 
        object
        """
        l = self.down[0].update(depth+1,sets,settings)
        r = self.down[1].update(depth+1,sets,settings)
        self.depth = depth
        self.height = max(l,r)+1
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
        
        if not self.down[0]:
            self.down[0] = random.choice(termNodes.termNodes)(self)
            self.down[0].randomize(sets,settings)
        else:
            self.down[0].fillTerms(sets,settings)
        if not self.down[1]:
            self.down[1] = random.choice(termNodes.termNodes)(self)
            self.down[1].randomize(sets,settings)
        else:
            self.down[1].fillTerms(sets,settings)

    def toString(self):
        """
        This function is used to create a string representaion of the bbsa

        """
        string = "addSet "
        string += self.down[0].toString()+" "+self.down[1].toString()+" "
        return string

    def toDict(self):
        """

        This function is used to create a dictionary representaion of the bbsa
        """
        return {"addSet":[self.down[0].toDict(),self.down[1].toDict()]}
        

    def makeProg(self,numTab,var):
        """
        This function generates the code for this node for the external verification

        """
        tab = "    "
        indent = ""
        for i in xrange(numTab):
            indent+=tab
        prog = self.down[0].makeProg(numTab,var+"0")
        prog+= self.down[1].makeProg(numTab,var+"1")
        prog+= "for y in x"+var+"1:\n"+indent+tab
        prog+= "if y not in x"+var+"0:\n"+indent+tab+tab
        prog+= "x"+var+"0.append(y)\n"+indent
        prog+= "x"+var+" = x"+var+"0\n"+indent
        return prog

    def count(self):
        """
        This function calculates the number of nodes below it and including itself
        """
        return self.down[0].count()+self.down[1].count()+1

class makeSet:
    """
    This node saves a snapshot of the set that is passed into it
    """
    def __init__(self,parent):
        """
        This constructor creates the node and sets it's parent
        """
        self.down = [None]
        
        self.parent = parent

        self.name = ""
       
        self.height = 0
        self.depth = 0
        if parent:
            self.depth = self.parent.depth+1 
        self.take = [1,2]
        self.give  = [2]
        
        self.settings = None
        if parent:
            self.settings = self.parent.settings


    def evaluate(self,sets):
        """ 
        This function evaluates the node and returns the resulting set


        """
        if self.settings.curOp>=self.settings.maxOp:
            return[]
        rDown = self.down[0].evaluate(sets)
        sets['pers'][self.name] = rDown

        self.settings.curOp+=1

        return rDown

    def update(self,depth,sets,settings):
        """
        This function updates the heights and depths and ensures
        that the settings pointer is pointing to the right settings 
        object
        """
        d = self.down[0].update(depth+1,sets,settings)
        self.depth = depth
        self.height = d+1
        opts = sets['pers'].keys()
        if not sets['pers']:
            opts.append('A')
        opts.append(chr(ord(opts[-1])+1))
        self.name = random.choice(opts)
        self.settings = settings
        return self.height

    def randomize(self,sets,settings):
        """
        This function randomizes the parameters of the node if there are any

        """
        opts = sets['pers'].keys()
        if not sets['pers']:
            opts.append('A')
        opts.append(chr(ord(opts[-1])+1))
        self.name = random.choice(opts)
        sets['pers'][self.name] = []
        return

    def fillTerms(self,sets,settings):
        """
        After the bbsa places all of the non-terminal nodes, this funciton is called
        to place the terminal nodes at the bottom of the parse tree

        """
        if not self.down[0]:
            self.down[0] = random.choice(termNodes.termNodes)(self)
            self.down[0].randomize(sets,settings)
        else:
            self.down[0].fillTerms(sets,settings)

    def toString(self):
        """
        This function is used to create a string representaion of the bbsa

        """
        string = "makeSet {"+self.name+"} "
        string += self.down[0].toString()+" "
        return string

    def toDict(self):
        """

        This function is used to create a dictionary representaion of the bbsa
        """
        return {"makeSet {"+self.name+"}":[self.down[0].toDict()]}

    def makeProg(self,numTab,var):
        """
        This function generates the code for this node for the external verification

        """
        tab = "    "
        indent = ""
        for i in xrange(numTab):
            indent+=tab
        prog = self.down[0].makeProg(numTab,var+"0")
        prog+= self.name+" = x"+var+"0\n"+indent
        prog+= "x"+var+"=x"+var+"0\n"+indent
        return prog


    def count(self):
        """
        This function calculates the number of nodes below it and including itself
        """
        return self.down[0].count()+1




setNodes = [addSet,makeSet]
