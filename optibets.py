import numpy as np

np.set_printoptions(precision=2)

#Getting vector of thetas
def getTheta(odds):
    theta = []
    a = 1-len(odds)**-1
    for o in odds:
        theta.append(o*a)
    return theta

#Creating the ymat
def yMat(k,n):
    y = np.zeros(n+1)
    y[-1] = k
    return y

#Creating the xmat
def xMat(odds):
    thetas = getTheta(odds)
    n = len(odds)+1
    q = -len(odds)**(-1)
    mat = np.zeros((n,n))
    for i in range(n):
        for j in range(n):
            if i == j and i != n-1:
                mat[i][j] = thetas[i]
            elif i != n-1 and j != n-1:
                mat[i][j] = q*odds[j]
            elif j == n-1 and i != n-1:
                mat[i][j] = -1/(2*thetas[i])
            elif i == n-1 and j != n-1:
                mat[i][j] = 1.0
    return mat

#Finding optimal bets given a total amount to bet "sats"
def optimalBets(odds,sats):
    k = len(odds) #
    shares = np.zeros(k)
    wagers = np.zeros(k)
    a = xMat(odds)
    aInv = np.linalg.inv(a)
    y = yMat(k,len(odds))
    x = np.matmul(aInv,y)
    for i in range(len(x)-1):
        shares[i] = (x[i]/k)
        wagers[i] = sats*shares[i]
    return wagers
