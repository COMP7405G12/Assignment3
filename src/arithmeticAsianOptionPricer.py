# Implement of Monte Carlo method with control variate technique for arithmetic Asian call/put options
import math

import numpy
import web
from numpy import random
from scipy.stats import norm

from __init__ import render


class arithmeticOption:
    def __init__(self, S=0.0, E=0.0, sigma=0.0, r=0.0, T=0.0, n=0, type="", M=0,
                 method=int()):
        # S: the spot price of asset S(0)
        # E: strike K
        # method: 0 = no variant control; 1=geometric Asian option
        # M: the number of paths in the Monte Carlo simulation
        # tyep: Call or Put
        self.S = float(S)
        self.E = E
        self.sigma = sigma
        self.r = r
        self.T = T
        self.N = n
        self.Dt = float(self.T) / self.N
        self.M = M
        self.type = type
        self.method = method

    def arithmeticOptPricer(self):
        # calculate geo Asian exact means
        sigsqT = self.sigma * self.sigma * self.T * (self.N + 1.0) * (2.0 * self.N + 1) / (6.0 * self.N * self.N)
        muT = 0.5 * sigsqT + (self.r - 0.5 * self.sigma * self.sigma) * self.T * (self.N + 1.0) / (2.0 * self.N)

        d1 = (math.log(float(self.S) / self.E) + (muT + 0.5 * sigsqT)) / math.sqrt(sigsqT)
        d2 = d1 - math.sqrt(sigsqT)

        N1 = norm.cdf(d1)
        N2 = norm.cdf(d2)
        if self.type == "Call":
            geo = max(math.exp(-self.r * self.T) * (self.S * math.exp(muT) * N1 - self.E * N2), 0)
        if self.type == "Put":
            geo = max(math.exp(-self.r * self.T) * (self.E * (1 - N2) - self.S * math.exp(muT) * (1 - N1)), 0)

        drift = math.exp((self.r - 0.5 * self.sigma * self.sigma) * self.Dt)

        random.seed(0)
        random_value = random.normal(size=(self.N, self.M))
        Spath = numpy.exp(random_value * self.sigma * math.sqrt(self.Dt)) * drift
        Spath[0] *= self.S
        for i in range(1, self.N):
            Spath[i] *= Spath[i - 1]

        arithMean = Spath.mean(0)
        geoMean = numpy.exp(numpy.log(Spath).mean(0))

        if self.type == 'Put':
            arithMean = self.E - arithMean
            geoMean = self.E - geoMean
        else:
            arithMean -= self.E
            geoMean -= self.E

        for i in range(len(arithMean)):
            arithMean[i] = max(arithMean[i], 0)
            geoMean[i] = max(geoMean[i], 0)

        arithPayoff = math.exp(-self.r * self.T) * arithMean
        geoPayoff = math.exp(-self.r * self.T) * geoMean

        if self.method == 0:
            # standard Monte Carlo
            Pmean = arithPayoff.mean()
            Pstd = arithPayoff.std()
            confmc = [Pmean - 1.96 * Pstd / math.sqrt(self.M), Pmean + 1.96 * Pstd / math.sqrt(self.M)]
            return (Pmean, confmc)
        if self.method == 1:
            # control variate
            covXY = numpy.cov([arithPayoff, geoPayoff], ddof=0)[0][1]
            theta = float(covXY) / geoPayoff.var()
            Z = arithPayoff + theta * (geo - geoPayoff)
            Zmean = Z.mean()
            Zstd = Z.std()
            confcv = [Zmean - 1.96 * Zstd / math.sqrt(self.M), Zmean + 1.96 * Zstd / math.sqrt(self.M)]
            return (Zmean, confcv)


class ArithmeticAsianOptionPricerHtml(object):
    def GET(self):
        return render.arithmeticAsianOptionCalculator()

    def POST(self):
        test = web.input()
        try:
            stock_price = float(test['underlyingStock'])
            strike_price = float(test['strikePrice'])
            sigma = float(test['sigma'])
            risk_free_rate = float(test['interestRate']) / 100
            maturity_time = float(test['maturityTime'])
            n = int(test['n'])
            type = test['type']
            M = int(test['M'])
            method = int(test['method'])
        except ValueError, e:
            return render.arithmeticAsianOptionCalculator("Invalid input, please input again")

        try:
            confmc = arithmeticOption(stock_price, strike_price, sigma, risk_free_rate, maturity_time, n, type, M,
                                      method)
            result = confmc.arithmeticOptPricer()
            return render.arithmeticAsianOptionCalculator(option_price=result[0],
                                                          interval='[' + str(result[1][0]) + ',' + str(
                                                              result[1][1]) + ']', stock=stock_price,
                                                          strike=strike_price, sigmaV=sigma,
                                                          interest=risk_free_rate * 100, maturityT=maturity_time, on=n,
                                                          otype=type, oM=M, omethod=str(method))
        except Exception, e:
            return render.arithmeticAsianOptionCalculator(option_price="Illeage input, calculate error:" + e.message,
                                                          interval=0,
                                                          stock=stock_price, strike=strike_price, sigmaV=sigma,
                                                          interest=risk_free_rate * 100, maturityT=maturity_time, on=n,
                                                          otype=type, oM=M, omethod=str(method))


if __name__ == '__main__':
    # testcase 01
    aopricer = arithmeticOption(100.0, 100.0, 0.3, 0.05, 3, 50, "Put", 100000, 0)
    confmc0 = aopricer.arithmeticOptPricer()
    aopricer.__init__(100.0, 100.0, 0.3, 0.05, 3, 50, "Put", 100000, 1)
    confmc1 = aopricer.arithmeticOptPricer()
    print confmc0
    print confmc1

    # testcase 02
    aopricer.__init__(100.0, 100.0, 0.3, 0.05, 3, 100, "Put", 100000, 0)
    confmc2 = aopricer.arithmeticOptPricer()
    aopricer.__init__(100.0, 100.0, 0.3, 0.05, 3, 100, "Put", 100000, 1)
    confmc3 = aopricer.arithmeticOptPricer()
    print confmc2
    print confmc3

    # testcase 03
    aopricer.__init__(100.0, 100.0, 0.4, 0.05, 3, 50, "Put", 100000, 0)
    confmc4 = aopricer.arithmeticOptPricer()
    aopricer.__init__(100.0, 100.0, 0.4, 0.05, 3, 50, "Put", 100000, 1)
    confmc5 = aopricer.arithmeticOptPricer()
    print confmc4
    print confmc5

    # testcase 04
    aopricer.__init__(100.0, 100.0, 0.3, 0.05, 3, 50, "Call", 100000, 0)
    confmc6 = aopricer.arithmeticOptPricer()
    aopricer.__init__(100.0, 100.0, 0.3, 0.05, 3, 50, "Call", 100000, 1)
    confmc7 = aopricer.arithmeticOptPricer()
    print confmc6
    print confmc7

    # testcase 05
    aopricer.__init__(100.0, 100.0, 0.3, 0.05, 3, 100, "Call", 100000, 0)
    confmc8 = aopricer.arithmeticOptPricer()
    aopricer.__init__(100.0, 100.0, 0.3, 0.05, 3, 100, "Call", 100000, 1)
    confmc9 = aopricer.arithmeticOptPricer()
    print confmc8
    print confmc9

    # testcase 06
    aopricer.__init__(100.0, 100.0, 0.4, 0.05, 3, 50, "Call", 100000, 0)
    confmc10 = aopricer.arithmeticOptPricer()
    aopricer.__init__(100.0, 100.0, 0.4, 0.05, 3, 50, "Call", 100000, 1)
    confmc11 = aopricer.arithmeticOptPricer()
    print confmc10
    print confmc11
