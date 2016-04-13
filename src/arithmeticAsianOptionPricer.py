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
        return render.arithmeticAsianOptionCalculatorResponsive()

    def POST(self):
        test = web.input()
        stock_price = 100
        strike_price = 100
        sigma = 0.3
        risk_free_rate = 0.05
        maturity_time = 3
        n = 10
        type = 'Call'
        M = 1000
        method = 1
        try:
            stock_price = float(test['underlyingStock'])
            strike_price = float(test['strikePrice'])
            sigma = float(test['sigma'])
            risk_free_rate = float(test['interestRate'])
            maturity_time = float(test['maturityTime'])
            n = int(test['n'])
            type = test['type']
            M = int(test['M'])
            method = int(test['method'])
            confmc = arithmeticOption(stock_price, strike_price, sigma, risk_free_rate, maturity_time, n, type, M,
                                      method)
            result = confmc.arithmeticOptPricer()
            return render.arithmeticAsianOptionCalculatorResponsive(option_price=result[0],
                                                                    interval='[' + str(result[1][0]) + ',' + str(
                                                                        result[1][1]) + ']', stock=stock_price,
                                                                    strike=strike_price, sigmaV=sigma,
                                                                    interest=risk_free_rate, maturityT=maturity_time,
                                                                    on=n, otype=type, oM=M, omethod=method)
        except ValueError, e:
            return render.arithmeticAsianOptionCalculatorResponsive("Invalid input, please input again",
                                                                    stock=stock_price, strike=strike_price,
                                                                    sigmaV=sigma, interest=risk_free_rate,
                                                                    maturityT=maturity_time, on=n, otype=type, oM=M,
                                                                    omethod=method)
