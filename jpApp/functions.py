import math
#--- Maths functions to compute stabiltiy / retainment.
def getS(r, t):
    ln = math.log
    return ( -1 * (t/ln(r)) )

def getR(s, t):
    e = math.exp
    r = e(-1*t/s)
    
    return r
        
def isRevisable(r):
    return r < 0.50
