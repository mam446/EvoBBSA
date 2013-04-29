import solution
import random




def diagonal(pop,n):
    """
    This is an implementation of diagonal recombination
    """
    
    
    if not pop:
        return []
    childs = [solution.solution(p.settings) for p in pop]

    pnts = [random.randint(1,pop[0].settings.solSet['length']-1) for i in xrange(n)]

    pnts.sort()
    
    pnts.append(pop[0].settings.solSet['length'])
    
        
        
    for c in childs:
        last = 0
        nex = pnts[0]
        for i in xrange(1,len(pnts)+1):
            if i!=len(pnts):
                c.bits[last:nex] = pop[i%len(pop)].bits[last:nex]
                last = nex
                nex = pnts[i]
            else:
                c.bits[last:] = pop[i%len(pop)].bits[last:]
        d = pop[0]
        pop = pop[1:]
        pop.append(d)
    
    
    return childs
