import random
import termNodes
import copy


class kTourn:
    def __init__(self,parent):
        """
        This constructor creates the node and sets it's parent
        """
        self.parent = parent
        self.depth = 0
        self.height = 0
        if parent:
            self.depth = self.parent.depth+1
        self.down = [None]
        self.k = 0
        self.num = 0

        self.take = [1,2]
        self.give  = [1,2]


        self.settings = None
        if parent:
            self.settings = self.parent.settings

    def evaluate(self,sets):
        """ 
        This function evaluates the node and returns the resulting set\

        """
        if self.settings.curOp>=self.settings.maxOp:
            return[]
        rDown = None
        if self.down[0]:
            rDown = self.down[0].evaluate(sets)
        else:
            raise "Node kTourn has no child"
        if not rDown:
            return []
        
        ret = []

        for j in xrange(self.num):
            m = None
            for i in xrange(self.k):
                temp = random.choice(rDown)
                if not m or m.fitness< temp.fitness:
                    m = temp
            if m not in ret:
                ret.append(m)
#            if m:
 #               ret.append(m.duplicate())
                
  #              ret[-1].settings = m.settings

        self.settings.curOp+=self.num*self.k

        return ret

    def update(self,depth,sets,settings):
        """
        This function updates the heights and depths and ensures
        that the settings pointer is pointing to the right settings 
        object
        """
        self.depth = depth
        
        d = self.down[0].update(depth+1,sets,settings)
        self.height = d+1
        self.settings = settings
        return self.height

    def randomize(self,sets,settings):
        """
        This function randomizes the parameters of the node if there are any

        """
        self.k = random.randint(1,settings.maxK)
        self.num = random.randint(1,settings.maxCount)

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
        string = "kTourn(k="+str(self.k)+",count="+str(self.num)+") "
        string += self.down[0].toString()+" "
        return string

    def toDict(self):
        """

        This function is used to create a dictionary representaion of the bbsa
        """
        return {"kTourn(k="+str(self.k)+",count="+str(self.num)+")":[self.down[0].toDict()]}

    
    def makeProg(self,numTab,var):
        """
        This function generates the code for this node for the external verification

        """
        tab = "    "
        indent = ""
        for i in xrange(numTab):
            indent+=tab
        prog = self.down[0].makeProg(numTab,var+"0")
        prog += "x"+var+"=[]\n"+indent
        prog += "if x"+var+"0:\n"+indent+tab
        prog += "for i in xrange("+str(self.num)+"):\n"+indent+tab+tab

        prog+= "y = kTourn(x"+var+"0,"+str(self.k)+")\n"+indent+tab+tab
        prog+= "if y not in x"+var+":\n"+indent+tab+tab+tab
        prog+= "x"+var+".append(y)\n"+indent
        return prog

    def count(self):
        """
        This function calculates the number of nodes below it and including itself
        """
        return self.down[0].count()+1

class trunc:
    def __init__(self,parent):
        """
        This constructor creates the node and sets it's parent
        """
        self.parent = parent
        self.depth = 0
        self.height = 0
        if parent:
            self.depth = self.parent.depth+1
        self.down = [None]
        self.num = 0

        self.take = [1,2]
        self.give  = [1,2]

        self.settings = None
        if parent:
            self.settings = self.parent.settings

    def evaluate(self,sets):
        """ 
        This function evaluates the node and returns the resulting set\

        """
        if self.settings.curOp>=self.settings.maxOp:
            return[]
        rDown = None
        if self.down[0]:
            rDown = self.down[0].evaluate(sets)
        else:
            raise "Node trunc has no child"
        rDown.sort(reverse=True)

        self.settings.curOp+=1

        return rDown[:self.num]


    def update(self,depth,sets,settings):
        """
        This function updates the heights and depths and ensures
        that the settings pointer is pointing to the right settings 
        object
        """
        self.depth = depth
        
        d = self.down[0].update(depth+1,sets,settings)
        self.height = d+1
        self.settings = settings
        return self.height

    def randomize(self,sets,settings):
        """
        This function randomizes the parameters of the node if there are any

        """
        self.num = random.randint(1,settings.maxCount)

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
        string = "Trunc(count="+str(self.num)+") "
        string += self.down[0].toString()+" "
        return string

    def toDict(self):
        """

        This function is used to create a dictionary representaion of the bbsa
        """
        return {"Trunc(count="+str(self.num)+")":[self.down[0].toDict()]}

    def makeProg(self,numTab,var):
        """
        This function generates the code for this node for the external verification

        """
        tab = "    "
        indent = ""
        for i in xrange(numTab):
            indent+=tab
        prog = self.down[0].makeProg(numTab,var+"0")
        prog += "x"+var+"0.sort(reverse=True)\n"+indent
        prog+= "x"+var+ "= x"+var+"0[:"+str(self.num)+"]\n"+indent
        
        return prog

    def count(self):
        """
        This function calculates the number of nodes below it and including itself
        """
        return self.down[0].count()+1

selectNodes = [trunc,kTourn]









