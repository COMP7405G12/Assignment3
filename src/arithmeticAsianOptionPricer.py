#Implement of Monte Carlo method with control variate technique for arithmetic Asian call/put options
import math
import random
import numpy
from scipy.stats import norm

class arithmeticOption:
    def __init__(self, S=float(), E=float(), sigma=float(), r=float(), T=float(), n=float(), type="", M=float(), method=int()):
        #S: the spot price of asset S(0)
        #E: strike K
        #method: 0 = no variant control; 1=geometric Asian option
        #M: the number of paths in the Monte Carlo simulation
        #tyep: Call or Put
        self.S = S
        self.E = E
        self.sigma = sigma
        self.r = r
        self.T = T
        self.N = n
        self.Dt = float(self.T)/self.N
        self.M = M
        self.type = type
        self.method = method

    def arithmeticOptPricer(self):
        #calculate geo Asian exact mean
        sigsqT, muT, d1, d2, N1, N2, geo, drift =float(), float(), float(), float(), float(), float(), float(), float()
        arithPayoff = list()
        geoPayoff = list()

        sigsqT = self.sigma*self.sigma*self.T*(self.N+1.0)*(2.0*self.N+1)/(6.0*self.N*self.N)
        muT = 0.5 * sigsqT + (self.r - 0.5*self.sigma*self.sigma)*self.T*(self.N+1.0)/(2.0*self.N)

        d1 = float((math.log(float(self.S)/self.E) + (muT + 0.5*sigsqT))/ math.sqrt(sigsqT))
        d2 = float(d1) - math.sqrt(sigsqT)

        N1 = norm.cdf(d1)
        N2 = norm.cdf(d2)
        if self.type == "Call":
            geo = max(math.exp(-self.r*self.T)*(self.S*math.exp(muT)*N1 - self.E*N2),0)
        if self.type == "Put":
            geo = max(math.exp(-self.r*self.T)*(self.E*(1-N2) - self.S*math.exp(muT)*(1-N1)),0)

        drift = math.exp((self.r-0.5*self.sigma*self.sigma)*self.Dt)
        for i in range(0, self.M):
            growthFactor = drift * math.exp(self.sigma*math.sqrt(self.Dt)*norm.rvs(loc=0, scale=1, size=1)[0])
            Spath = list()
            Spath.append(self.S*growthFactor)
            for j in range(1, self.N):
                growthFactor = drift * math.exp(self.sigma * math.sqrt(self.Dt)*norm.rvs(loc=0, scale=1, size=1)[0])
                Spath.append(Spath[j-1]*growthFactor)
            #Arithmetic mean
            arithMean = numpy.mean(Spath)

            if self.type == "Call":
                arithPayoff.append(math.exp(-self.r*self.T)*max(arithMean-self.E, 0))
            if self.type == "Put":
                arithPayoff.append(math.exp(-self.r*self.T)*max(self.E-arithMean, 0))

            #geometic mean
            geoMean = numpy.exp((numpy.mean(numpy.log(Spath))))

            if self.type == "Call":
                geoPayoff.append(numpy.exp(-self.r*self.T)*max(geoMean-self.E, 0))
            if self.type == "Put":
                geoPayoff.append(numpy.exp(-self.r*self.T)*max(self.E-geoMean, 0))

        if self.method == 0:
            #standard Monte Carlo
            Pmean = numpy.mean(arithPayoff)
            Pstd = numpy.std(arithPayoff)
            confmc = (Pmean-1.96*Pstd/math.sqrt(self.M), Pmean+1.96*Pstd/math.sqrt(self.M))
            print "no control variant"
            return confmc
        if self.method == 1:
            # control variate
            covXY = numpy.cov([arithPayoff,geoPayoff],ddof=0)[0][1]
            theta = float(covXY)/numpy.var(geoPayoff)
            Z = list()
            Z = arithPayoff + theta * (geo - geoPayoff)
            print geo
            Zmean = numpy.mean(Z)
            Zstd = numpy.std(Z)
            confcv = (Zmean-1.96*Zstd/math.sqrt(self.M), Zmean+1.96*Zstd/math.sqrt(self.M))
            print "geo contro variant"
            return confcv



if __name__=='__main__':
    # testcase 01
    aopricer= arithmeticOption(100.0,100.0,0.3,0.05,3,50,"Put",100000,0)
    confmc0=aopricer.arithmeticOptPricer()
    aopricer.__init__(100.0,100.0,0.3,0.05,3,50,"Put",100000,1)
    confmc1=aopricer.arithmeticOptPricer()
    print (confmc0,confmc1)

    # testcase 02
    aopricer.__init__(100.0,100.0,0.3,0.05,3,100,"Put",100000,0)
    confmc2=aopricer.arithmeticOptPricer()
    aopricer.__init__(100.0,100.0,0.3,0.05,3,100,"Put",100000,1)
    confmc3=aopricer.arithmeticOptPricer()
    print (confmc2,confmc3)

    # testcase 03
    aopricer.__init__(100.0,100.0,0.4,0.05,3,50,"Put",100000,0)
    confmc4=aopricer.arithmeticOptPricer()
    aopricer.__init__(100.0,100.0,0.4,0.05,3,50,"Put",100000,1)
    confmc5=aopricer.arithmeticOptPricer()
    print (confmc4,confmc5)

    # testcase 04
    aopricer.__init__(100.0,100.0,0.3,0.05,3,50,"Call",100000,0)
    confmc6=aopricer.arithmeticOptPricer()
    aopricer.__init__(100.0,100.0,0.3,0.05,3,50,"Call",100000,1)
    confmc7=aopricer.arithmeticOptPricer()
    print (confmc6,confmc7)

    # testcase 05
    aopricer.__init__(100.0,100.0,0.3,0.05,3,100,"Call",100000,0)
    confmc8=aopricer.arithmeticOptPricer()
    aopricer.__init__(100.0,100.0,0.3,0.05,3,100,"Call",100000,1)
    confmc9=aopricer.arithmeticOptPricer()
    print (confmc8,confmc9)

    # testcase 06
    aopricer.__init__(100.0,100.0,0.4,0.05,3,50,"Call",100000,0)
    confmc10=aopricer.arithmeticOptPricer()
    aopricer.__init__(100.0,100.0,0.4,0.05,3,50,"Call",100000,1)
    confmc11=aopricer.arithmeticOptPricer()
    print (confmc10,confmc11)












