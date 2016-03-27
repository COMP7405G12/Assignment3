#!/usr/bin/python
# -*- coding: utf-8 -*-

# Project: Assignment3
# File name: arithmetic_mean_basket_options
# Author: Mark Wang
# Date: 26/3/2016

import math

from scipy.stats import norm
import numpy.random as random

# Test value or other constant
PATH_NUMBER = 100000
RISK_FREE_RATE = 0.05

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

    def __init__(self, s0, strike_price, sigma, type):
        self.sigma = float(sigma)
        self.type = type
        self.strike_price = float(strike_price)
        self.s0 = float(s0)

    def get_stock_price_array(self, delta_t, random_value):
        stock_price_list = []
        stock_price = self.s0
        for zi in random_value:
            stock_price *= math.exp((RISK_FREE_RATE - 0.5 * self.sigma**2) * delta_t +
                                    self.sigma * math.sqrt(delta_t) * zi)
            stock_price_list.append(stock_price)

        return stock_price_list


class ArithmeticMeanBasketOptions(object):
    def __init__(self, s10, s20, k, sigma1, sigma2, rho, type, tau):
        random.seed(0)
        self.option1 = Option(s10, k, sigma1, type)
        self.option2 = Option(s20, k, sigma2, type)
        self.sigma_B = math.sqrt(2 * sigma2 * sigma1 * rho + sigma1 * sigma1 + sigma2 * sigma2) / 2
        self.avg_B = RISK_FREE_RATE - 0.5 * (sigma2 * sigma2 + sigma1 * sigma1) / 2 + 0.5 * self.sigma_B ** 2
        self.B0 = float(s10 + s20) / 2
        self._d1 = None
        self._d2 = None
        self.tau = tau

    @property
    def d1(self):
        ''' Function to calculate d1'''
        if self._d1:
            pass
        elif self._d2:
            self._d1 = self._d2 + self.sigma_B * math.sqrt(self.tau)
        else:
            self._d1 = (math.log(self.B0 / self.option1.strike_price)
                        + (self.avg_B + 0.5 * self.sigma_B ** 2) * self.tau) \
                       / (self.sigma_B * math.sqrt(self.tau))
        return self._d1

    @property
    def d2(self):
        ''' Function to calculate d2'''
        if self._d2:
            pass
        elif self._d1:
            self._d2 = self._d1 - self.sigma_B * math.sqrt(self.tau)
        else:
            self._d2 = (math.log(self.B0 / self.option1.strike_price)
                        + (self.avg_B - 0.5 * self.sigma_B ** 2) * self.tau) \
                       / (self.sigma_B * math.sqrt(self.tau))

        return self._d2

    def get_basket_price(self):
        ''' Return the basket price, this will be different as the option type difference '''
        if self.option1.type == PUT_OPTION:
            n1 = norm.cdf(-self.d1)
            n2 = norm.cdf(-self.d2)
            multiplier = -1
        else:
            n1 = norm.cdf(self.d1)
            n2 = norm.cdf(self.d2)
            multiplier = 1

        return multiplier * math.exp(-RISK_FREE_RATE * self.tau) * (self.B0 * math.exp(self.avg_B * self.tau) * n1
                                                                    - self.option2.strike_price * n2)


if __name__ == "__main__":
    random.seed(0)
    print generate_two_correlated_random_variables([0, 0], [1, 1], 0.3, 10)