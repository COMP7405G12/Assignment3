#!/usr/bin/python
# -*- coding: utf-8 -*-

# Project: Assignment3
# File name: arithmetic_mean_basket_options
# Author: Mark Wang
# Date: 26/3/2016

import math

import numpy as np
from scipy.stats import norm
import numpy.random as random

# Test value or other constant
PATH_NUMBER = 100000
RISK_FREE_RATE = 0.05
MATURITY_TIME = 3

# Remark that used in the following code
PUT_OPTION = "Put"
CALL_OPTION = "Call"


def generate_two_correlated_random_variables(means, stds, corr, number):
    covs = [[stds[0] ** 2, stds[0] * stds[1] * corr],
            [stds[0] * stds[1] * corr, stds[1] ** 2]]
    m = random.multivariate_normal(means, covs, number).T
    return m


class Option(object):
    '''
    Class to represent a option
    '''

    def __init__(self, s0, strike_price, sigma, type, tau):
        self.sigma = float(sigma)
        self.type = type
        self.strike_price = float(strike_price)
        self.s0 = float(s0)
        self.tau = float(tau)

    def get_stock_price_array(self, random_value):
        stock_price_list = []
        for zi in random_value:
            stock_price = self.s0 * math.exp((RISK_FREE_RATE - 0.5 * self.sigma ** 2) * self.tau +
                                             self.sigma * math.sqrt(self.tau) * zi)
            stock_price_list.append(stock_price)

        return np.array(stock_price_list)


class ArithmeticMeanBasketOptions(object):
    def __init__(self, s10, s20, k, sigma1, sigma2, type, tau, risk_free_rate=RISK_FREE_RATE):
        self.option1 = Option(s10, k, sigma1, type, tau)
        self.option2 = Option(s20, k, sigma2, type, tau)
        self.B0 = float(s10 + s20) / 2
        self.tau = float(tau)
        self.strike_price = float(k)
        self.type = type
        self.risk_free_rate = risk_free_rate

    def get_basket_price(self, corr):
        ''' Return the basket price, this will be different as the option type difference '''
        z1, z2 = generate_two_correlated_random_variables([0, 0], [1, 1], corr, PATH_NUMBER)
        s1 = self.option1.get_stock_price_array(z1)
        s2 = self.option2.get_stock_price_array(z2)
        b = (s1 + s2) * 0.5
        if self.type == CALL_OPTION:
            maturity_price = b - self.strike_price
        else:
            maturity_price = self.strike_price - b

        for i in range(len(maturity_price)):
            if maturity_price[i] < 0:
                maturity_price[i] = 0

        return maturity_price * math.exp(-RISK_FREE_RATE * self.tau)

    def get_basket_price_with_control_variate(self, corr):
        z1, z2 = generate_two_correlated_random_variables([0, 0], [1, 1], corr, PATH_NUMBER)


if __name__ == "__main__":
    random.seed(0)
    test = ArithmeticMeanBasketOptions(s10=100, s20=100, k=100, sigma1=0.3, sigma2=0.3,
                                       type=PUT_OPTION, tau=MATURITY_TIME, risk_free_rate=RISK_FREE_RATE)
    b = test.get_basket_price(0.5)
    print b.mean(), b.std(), b.mean() - 1.96 * b.std() / math.sqrt(PATH_NUMBER),\
        b.mean() + 1.96 * b.std() / math.sqrt(PATH_NUMBER)
    # test = ArithmeticMeanBasketOptions(10, 10, 9, 0.1, 0.1, CALL_OPTION, 1)
    # z = random.normal(size=PATH_NUMBER)

    # print a
