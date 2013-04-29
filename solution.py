import random
import copy
import FitnessFunction


class solution:
    """
    This class is the individual that will be evolved by the bbsa.
    """
    def __init__(self,settings):
        """
        This is the constructor that sets up the individual for the given problem type that the bbsa is trying to solve.
        
        currently only deceptive trap, deceptive step trap, nk-landscapes, and the all-ones problem can be used.

        """
        self.length = settings.solSet['length']
        self.bits = [random.choice([True,False])for x in xrange(self.length)]
        self.fitness = 0
        self.settings = settings
        if self.settings.problemType =='dTrap':
            self.evaluater = FitnessFunction.DeceptiveTrap({'k':settings.trapSize})
        elif self.settings.problemType=='dsTrap':
            self.evaluater= FitnessFunction.DeceptiveStepTrap({'k':settings.trapSize,'stepSize':settings.stepSize})
        elif self.settings.problemType=='nk':
            self.evaluater=FitnessFunction.NearestNeighborNK({'k':settings.nk,'dimensions':settings.dimensions,'problemSeed':0,'maximumFitness':1.0,'nkProblemFolder':''},0)

    def evaluate(self,full=False):
        """
        This function evaluates the solution.
        """
        if self.settings.curEvals>=self.settings.maxEvals and not full:
            return
        if self.settings.problemType:
            if self.settings.problemType=='nk':
                self.fitness = self.evaluater.evaluate([int(bit)for bit in self.bits])
            else:
                self.fitness = self.evaluater.evaluate(self.bits)                
            self.settings.curEvals+=1
        
        else:
            self.settings.curEvals+=1
            self.fitness = 0
            for x in self.bits:
                if x:
                    self.fitness+=1.0
            self.fitness/=len(self.bits)


    def mutate(self,rate):
        """
        This is a standard bit-flip mutation.
        """
        for i in xrange(len(self.bits)):
            if random.random()<rate:
                self.bits[i] = not self.bits[i]



    def __gt__(self,other):
        """
        Greater than operator comparing fitness'
        """
        return self.fitness>other.fitness
    
    def __lt__(self,other):
        """
        Less than operator comparing fitness'
        """
        return self.fitness<other.fitness

    def __ge__(self,other):
        """
        Greater than or equal to operator comparing fitness'
        """
        return self.fitness>=other.fitness

    def __le__(self,other):
        """
        Less than  or equal to operator comparing fitness'
        """
        return self.fitness<=other.fitness




    def duplicate(self):
        """
        This function duplicates the solution while keeping the same settings file
        """
        
        x = solution(self.settings) 
        x.fitness =0 
        for i in xrange(len(self.bits)):
            x.bits[i] = self.bits[i] 
        return x




