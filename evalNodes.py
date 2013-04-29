
import random
import termNodes




class eval:
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
        self.take = [1,2]
        self.give  = [2]
        
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
            raise "Node eval has no child"
            
        for x in rDown:
            x.evaluate()
        
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
        string = "evaluate "
        string += self.down[0].toString()+" "
        return string

    def toDict(self):
        """

        This function is used to create a dictionary representaion of the bbsa
        """
        return {'evaluate':[self.down[0].toDict()]}


    def makeProg(self,numTab,var):
        """
        This function generates the code for this node for the external verification

        """
        tab = "    "
        indent = ""
        for i in xrange(numTab):
            indent+=tab
        prog = self.down[0].makeProg(numTab,var+"0")
        prog+= "for i in x"+var+"0:\n"+indent+tab
        prog+= "i.evaluate(True)\n"+indent
        prog+= "x"+var+"=x"+var+"0\n"+indent
        return prog

    def count(self):
        """
        This function calculates the number of nodes below it and including itself
        """
        return self.down[0].count()+1


evalNodes = [eval]















