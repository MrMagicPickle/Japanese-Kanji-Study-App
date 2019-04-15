import math

e = math.exp
t = 31
s = 1

ln = math.log

for i in range (10):
    r = e(-1*t/s)
    print(str(r)+ " with s = " + str(s) + " aka: " + str(-1 * (t/ln(r)) ))
    s *= 2
    


print("-----")
zs = 512
for i in range (10):
    try:
        r = e(-1*t/s)
        print(str(r)+ " with s = " + str(s) + " aka: " + str(-1 * (t/ln(r)) ))
        s /= (2+1)
    except:
        pass

'''
for a fixed time,
the growth rate of stability inverse exponentially affects the retainment.

if our eq is R = e(-t/s)

rewrite it in terms of s: 
       s = -(t/ln R)
'''
def getT(s, r):
    ln = math.log
    return (-1 * (s * ln(r)))
def getS(r, t):
    ln = math.log
    return ( -1 * (t/ln(r)) )

def getR(s, t):
    e = math.exp
    r = e(-1*t/s)
    return r

print("----")
r = 0.05
t = 1
for i in range (31):
    s = getS(r, t)
    print(str(s) + " with t = " + str(t))
    t += 1

'''
if fail the test, set retainment to 0.05, compute s with getS
if pass the test, double stability value, compute r with getR

Our ideal stability value would be 512, if we hit 512, then it will take 1 year for us to retest.
'''

print("---")
s = 512
r = 0.49
print("Days taken to re-test after 1 month elapsed: " + str(getT(s, r)))


