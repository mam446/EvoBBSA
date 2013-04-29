import funcs
import random
import termNodes
import solution

class mutate:
    """
    This node does a bitflip mutation while creating new solutions
    """
    def __init__(self,parent):
        """
        This constructor creates the node and sets it's parent
        """
        self.depth = 0
        self.height = 0
        
        self.rate = 0.0

        self.take = [1,2]
        self.give = [1,2] 

        self.parent = parent 
        if parent:
            self.depth = self.parent.depth+1 
        self.down = [None]
        
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
            raise "Node addSet has no right child"
        ret = []
        for x in rDown:
            y = x.duplicate()
            y.mutate(self.rate)
            ret.append(y)
        
        self.settings.curOp+=len(rDown)
        
        return ret        


    def update(self,depth,sets,settings):
        """
        This function updates the heights and depths and ensures
        that the settings pointer is pointing to the right settings 
        object
        """
        d = self.down[0].update(depth+1,sets,settings)
        self.depth = depth
        self.height = d+1
        self.settings = settings
        return self.height
    
    def randomize(self,sets,settings):
        """
        This function randomizes the parameters of the node if there are any

        """
        self.rate = random.random()
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
        string = "mutate("+str(self.rate)+") "
        string += self.down[0].toString()
        return string 
    
    def toDict(self):
        """

        This function is used to create a dictionary representaion of the bbsa
        """
        return {"mutate("+str(self.rate)+")":[self.down[0].toDict()]}

    def makeProg(self,numTab,var):
        """
        This function generates the code for this node for the external verification

        """
        tab = "    "
        indent = ""
        for i in xrange(numTab):
            indent+=tab
        prog = self.down[0].makeProg(numTab,var+"0")
        prog +="x"+var+"=[]\n"+indent
        prog+= "for i in x"+var+"0:\n"+indent+tab
        prog+= "y = i.duplicate()\n"+indent+tab
        prog+= "y.mutate("+str(self.rate)+")\n"+indent+tab
        prog+= "x"+var+".append(y)\n"+indent
        return prog

    def count(self):
        """
        This function calculates the number of nodes below it and including itself
        """
        return self.down[0].count()+1

class uniRecomb:

    def __init__(self,parent):
        """
        This constructor creates the node and sets it's parent
        """
        self.depth = 0
        self.height = 0
        self.num = 0        
        self.rate = 0.0

        self.take = [1,2]
        self.give = [1,2] 

        self.parent = parent 
        if parent:
            self.depth = self.parent.depth+1 
        self.down = [None]
        
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
            raise "Node addSet has no right child"
        self.settings.curOp+=self.num 
        ret = []
        if not rDown:
            return []
        for i in xrange(self.num):
            x = solution.solution(self.settings)
            for j in xrange(len(x.bits)):
                x.bits[j] = random.choice(rDown).bits[j]
            ret.append(x)
       
       
        
        return ret        


    def update(self,depth,sets,settings):
        """
        This function updates the heights and depths and ensures
        that the settings pointer is pointing to the right settings 
        object
        """
        d = self.down[0].update(depth+1,sets,settings)
        self.depth = depth
        self.height = d+1
        self.settings = settings
        return self.height
    
    def randomize(self,sets,settings):
        """
        This function randomizes the parameters of the node if there are any

        """
        if self.count==1:
            take = [1]
        self.num = random.randint(1,settings.maxChilds)
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
        string = "uniRecomb(count ="+str(self.num)+") "
        string += self.down[0].toString()
        return string 
    
    def toDict(self):
        """

        This function is used to create a dictionary representaion of the bbsa
        """
        return {"uniRecomb(count="+str(self.num)+")":[self.down[0].toDict()]}

    def makeProg(self,numTab,var):
        """
        This function generates the code for this node for the external verification

        """
        tab = "    "
        indent = ""
        for i in xrange(numTab):
            indent+=tab
        prog = self.down[0].makeProg(numTab,var+"0")
        prog+= "#Uniform Recombination\n"+indent
        prog+= "x"+var+"=[]\n"+indent
        prog+= "if x"+var+"0:\n"+indent+tab
        prog+= "for i in xrange("+str(self.num)+"):\n"+indent+tab+tab
        prog+= "y = solution.solution(s)\n"+indent+tab+tab
        prog+= "for j in xrange(len(y.bits)):\n"+indent+tab+tab+tab
        prog+= "y.bits[j] = random.choice(x"+var+"0).bits[j]\n"+indent+tab+tab
        prog+= "x"+var+".append(y)\n"+indent
        
        
        return prog

    def count(self):
        """
        This function calculates the number of nodes below it and including itself
        """
        return self.down[0].count()+1


class diagRecomb:
    def __init__(self,parent):
        """
        This constructor creates the node and sets it's parent
        """
        self.depth = 0
        self.height = 0
        self.n = 0        
        self.rate = 0.0

        self.take = [1,2]
        self.give = [1,2] 

        self.parent = parent 
        if parent:
            self.depth = self.parent.depth+1 
        self.down = [None]
        
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
            raise "Node addSet has no right child"
        self.settings.curOp+=self.n 
       
        ret = funcs.diagonal(rDown,self.n)     
        return ret        


    def update(self,depth,sets,settings):
        """
        This function updates the heights and depths and ensures
        that the settings pointer is pointing to the right settings 
        object
        """
        d = self.down[0].update(depth+1,sets,settings)
        self.depth = depth
        self.height = d+1
        self.settings = settings
        return self.height
    
    def randomize(self,sets,settings):
        """
        This function randomizes the parameters of the node if there are any

        """
        self.n = random.randint(1,settings.maxN)
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
        string = "diagonal(n ="+str(self.n)+") "
        string += self.down[0].toString()
        return string 
    
    def toDict(self):
        """

        This function is used to create a dictionary representaion of the bbsa
        """
        return {"diagonal(n="+str(self.n)+")":[self.down[0].toDict()]}

    def makeProg(self,numTab,var):
        """
        This function generates the code for this node for the external verification

        """
        tab = "    "
        indent = ""
        for i in xrange(numTab):
            indent+=tab
        prog = self.down[0].makeProg(numTab,var+"0")
        prog+= "#diagonal Recombination\n"+indent
        prog+= "x"+var+"=diagonal(x"+var+"0,"+str(self.n)+")\n"+indent
        
        
        return prog

    def count(self):
        """
        This function calculates the number of nodes below it and including itself
        """
        return self.down[0].count()+1













class tweak:
    def __init__(self,parent):
        """
        This constructor creates the node and sets it's parent
        """
        self.depth = 0
        self.height = 0
        
        self.rate = 0.0

        self.take = [1,2]
        self.give = [1,2] 

        self.parent = parent 
        if parent:
            self.depth = self.parent.depth+1 
        self.down = [None]
        
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
            raise "Node addSet has no right child"
        for i in xrange(len(rDown)):
            rDown[i].mutate(self.rate)
        
        self.settings.curOp+=len(rDown)
        
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
        self.settings = settings
        return self.height
    
    def randomize(self,sets,settings):
        """
        This function randomizes the parameters of the node if there are any

        """
        self.rate = random.random()
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
        string = "tweak("+str(self.rate)+") "
        string += self.down[0].toString()
        return string 
    
    def toDict(self):
        """

        This function is used to create a dictionary representaion of the bbsa
        """
        return {"tweak("+str(self.rate)+")":[self.down[0].toDict()]}

    def makeProg(self,numTab,var):
        """
        This function generates the code for this node for the external verification

        """
        tab = "    "
        indent = ""
        for i in xrange(numTab):
            indent+=tab
        prog = self.down[0].makeProg(numTab,var+"0")
        prog += "x"+var+" = []\n"+indent
        prog+= "for i in xrange(len(x"+var+"0)):\n"+indent+tab
        prog+= "x"+var+"0[i].mutate("+str(self.rate)+")\n"+indent+tab
        prog+= "x"+var+" = x"+var+"0\n"+indent
        return prog

    def count(self):
        """
        This function calculates the number of nodes below it and including itself
        """
        return self.down[0].count()+1

alterNodes = [tweak,mutate,uniRecomb,diagRecomb]
