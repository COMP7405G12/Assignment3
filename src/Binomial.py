import numpy as np
import web

import eu_black_scholes as bs
from __init__ import render


class BinaryTreeNode:
    def __init__(self, data, left, right):
        self.left = left
        self.data = data
        self.right = right


class Binomial:
    def __init__(self, S, v, K, r, T, type, n=30):
        self.T = float(T)
        self.S = float(S)
        self.K = float(K)
        self.type = type
        self.r = r
        self.v = v
        print n
        self.delt_t = self.T / n
        self.u = np.exp(self.v * np.sqrt(self.delt_t))
        self.d = 1 / self.u
        self.p = (np.exp(r * self.delt_t) - self.d) / (self.u - self.d)
        self.len = n + 1

    def execute(self):
        if self.type not in ("call", "put"):
            return "no such option type"
        A_V = self.AmericanOption()
        E_V = self.EuropeanOption()
        if self.type == "put":
            BS_V = bs.calculate_put_black_scholes(self.S, self.K, self.T, self.v, self.r)
        else:
            BS_V = bs.calculate_call_black_scholes(self.S, self.K, self.T, self.v, self.r)
        return A_V - E_V + BS_V

    def EuropeanOption(self):
        if self.type not in ("call", "put"):
            return "no such option type"
        upowers = np.power(self.u, np.arange(self.len))
        dpowers = np.power(self.d, np.arange(self.len - 1, -1, -1))
        if self.type == "call":
            V = np.amax([self.S * upowers * dpowers - self.K, np.zeros(self.len)], axis=0)
            for i in range(1, self.len):
                V = np.exp(-1 * self.r * self.delt_t) * (
                V[1:self.len + 1 - i] * self.p + (1 - self.p) * V[0:self.len - i])
        else:
            V = np.amax([self.K - self.S * upowers * dpowers, np.zeros(self.len)], axis=0)
            for i in range(1, self.len):
                V = np.exp(-1 * self.r * self.delt_t) * (
                V[1:self.len + 1 - i] * self.p + (1 - self.p) * V[0:self.len - i])
        return V[0]

    def AmericanOption(self):
        if self.type not in ("call", "put"):
            return "no such option type"
        upowers = np.power(self.u, np.arange(self.len))
        dpowers = np.power(self.d, np.arange(self.len - 1, -1, -1))
        if self.type == "call":
            V = np.amax([self.S * upowers * dpowers - self.K, np.zeros(self.len)], axis=0)
            for i in range(1, self.len):
                V = np.amax([np.amax(
                    [self.S * upowers[0:self.len - i] * dpowers[i:self.len] - self.K, np.zeros(self.len - i)], axis=0),
                             np.exp(-1 * self.r * self.delt_t) * (
                             V[1:self.len + 1 - i] * self.p + (1 - self.p) * V[0:self.len - i])], axis=0)
        else:
            V = np.amax([self.K - self.S * upowers * dpowers, np.zeros(self.len)], axis=0)
            for i in range(1, self.len):
                V = np.amax([np.amax(
                    [self.K - self.S * upowers[0:self.len - i] * dpowers[i:self.len], np.zeros(self.len - i)], axis=0),
                             np.exp(-1 * self.r * self.delt_t) * (
                             V[1:self.len + 1 - i] * self.p + (1 - self.p) * V[0:self.len - i])], axis=0)
        return V[0]


class BinomialTreeHtml(object):
    def GET(self):
        return render.eu_Binomial()

    def POST(self):
        test = web.input()
        try:
            stock_price = float(test['underlying'])
            volatility = float(test['vol'])
            strike_price = float(test['strike'])
            maturity_time = float(test['maturity'])
            risk_free_rate = float(test['interest_rate'])
            steps = int(test['steps'])
        except ValueError, e:
            return render.eu_Binomial("Invalid input")
        try:
            bt = Binomial(stock_price, volatility, strike_price, risk_free_rate, maturity_time, test['style'], n=steps)
            option_price = bt.execute()
            return render.eu_Binomial(option_price, stock=strike_price, vol=volatility, style=test['style'],
                                      strike=strike_price, T=maturity_time, r=risk_free_rate, s=steps)
        except Exception:
            return render.eu_Binomial("Illeage input, calculate error",
                                      stock=strike_price, vol=volatility, style=test['style'],
                                      strike=strike_price, T=maturity_time, r=risk_free_rate, s=steps)


if __name__ == "__main__":
    # test = Binomial(50,0.3,50,0.05,0.25,3,"call")
    test = Binomial(50, 0.223144, 52, 0.05, 2, "put", 30)
    print test.AmericanOption()
    print test.EuropeanOption()
    print test.execute()

    #  a = np.array([1,2,3])
    #  b = np.array([0,0,0])
    #  print a[0:1]
    #  print np.amax([a, b],axis=0)
