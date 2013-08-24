import sys
import time
import random
import settings
import bbsa
import copy
import logger

def ktourn(pop,k):

    best = None

    for i in xrange(k):
        obj = random.choice(pop)
        if not best or obj>best:
            best = obj
    return best




s = settings.settings()
if len(sys.argv)>1:

    s.problemType = sys.argv[1]
    if sys.argv[1]=='dsTrap':
        s.stepSize = int(sys.argv[2])
    if sys.argv[1]=='nk':
        s.nkFile = sys.argv[2]
else:
    s.problemType = None
s.seed =time.time()
random.seed(s.seed)
print s.problemType
s.runs = 5
mu = 50 
k = 8

pop = []
i = 0
while i<mu:
    x = bbsa.bbsa(copy.deepcopy(s))
    x.run()
    if x.aveBest!=0.0:
        pop.append(x)
        print x.aveBest
        i+=1
pop.sort()

for x in pop:
    print x.aveBest
l = logger.logger(str(s.seed)+".txt")
maxEvals = 2000
cur = mu
children = 20

while cur<maxEvals:
    
    c = 0
    childs = []
    while c<children:    
        choice = random.choice([0,1,2])
        if c+1!=children and 1==choice:
            mom = ktourn(pop,k)
            dad = ktourn(pop,k)
            x,y = mom.mate(dad)
            x.run()
            y.run()
            childs.append(x)
            childs.append(y)
            c+=2
        elif choice==2:
            x=ktourn(pop,k).mutate()
            x.run()
            childs.append(x)
            c+=1
        else:
            x = ktourn(pop,k).altMutate()
            x.run()
            childs.append(x)
            c+=1

    pop.extend(childs)
    pop.sort()
    pop.reverse()
    pop = pop[:mu]
    cur+=children

    su = 0.0
    ave = 0.0
    for i in xrange(len(pop)):
        su+=pop[i].aveBest
    ave = su/len(pop)
    
    print cur, ave,pop[0].aveBest,pop[0].aveEval,pop[0].aveOps
    
    f = open(str(pop[0].name)+"allones.py","w")
    f.write(pop[0].makeProg())
    f.close()
    l.newIter(pop,cur)
l.newRun()
l.log()
print
print pop[0].aveBest,pop[0].aveEval
print pop[0].toDict()
f = open(str(pop[0].name)+".py","w")
f.write(pop[0].makeProg())
f.close()































