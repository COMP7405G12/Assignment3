import math
from scipy.stats import norm

class impliedVol:
    def __init__(self, S=float(), r=float(), q=float(), T=float(), K=float(), premium=float(), type="", t=float()):

        self.S = S
        self.r = r
        self.q = q
        self.T = T
        self.K = K
        self.premium = premium
        self.type = type
        self.t = t
        #print ("k=%s, S=%s, r=%s, q=%s, T=%s, primium=%s, type=%s",self.K, self.S, self.r, self.q, self.T, self.premium, self.type)


    def impliedVol(self):
        sigmahat = float()
        sigma = float()
        sigmadiff = float()
        sigmahat=math.sqrt(2 * abs((math.log(self.S / self.K) + self.r * self.T) / self.T))

        'initial guess'

        tol = 0.00000001

        sigma = sigmahat
        sigmadiff = 1
        n = 1
        nmax = 100

        while ((sigmadiff >= tol) & (n < nmax)):
            C, Cvega, P, Pvega = self.blackschole(sigma)
            if self.type == 'Call':
                if Cvega == 0:
                    return None
                else:
                    increment = float(C - self.premium)/Cvega
                    sigma -= increment
                    n += 1
                    sigmadiff = abs(increment)

            if self.type == 'Put':
                if Pvega == 0:
                    return None
                else:
                    increment = float(P - self.premium)/Pvega
                    sigma -= increment
                    n += 1
                    sigmadiff = abs(increment)
        return sigma


    def blackschole(self, sigma=float()):

        item1 = (math.log(self.S/float(self.K)) + float(self.r - self.q) * (self.T - self.t))/float(sigma * math.sqrt(self.T - self.t))
        item2 = 0.5 * sigma * math.sqrt(self.T - self.t)

        d1 = float(item1) + item2
        d2 = float(item1) - item2

        item3 = float(self.S * (math.e ** (self.q * (self.t - self.T))))
        item4 = float(self.K * (math.e ** (self.r * (self.t - self.T))))

        call = float(item3 * norm.cdf(d1) - item4 * norm.cdf(d2))
        put = float(item4 * norm.cdf(-d2) - item3 * norm.cdf(-d1))

        cvega = float(self.S * math.sqrt(self.T - self.t) * norm.pdf(d1))
        pvega = cvega

        return (call, cvega, put, pvega)














