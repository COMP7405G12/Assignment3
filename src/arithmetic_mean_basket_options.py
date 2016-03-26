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


class Option(object):
    '''
    Class to represent a option
    '''

    def __init__(self, s0, strike_price, sigma, type):
        self.sigma = float(sigma)
        self.type = type
        self.strike_price = float(strike_price)
        self.s0 = float(s0)


class ArithmeticMeanBasketOptions(object):
    def __init__(self, s10, s20, k, sigma1, sigma2, rho, type, tau):
        random.seed(0)
        self.option1 = Option(s10, k, sigma1, type)
        self.option2 = Option(s20, k, sigma2, type)
        self.sigma_B = math.sqrt(2 * sigma2 * sigma1 * rho + sigma1 * sigma1 + sigma2 * sigma2) / 2
        self.avg_B = RISK_FREE_RATE - 0.5 * (sigma2 * sigma2 + sigma1 * sigma1) / 2 + 0.5 * self.sigma_B ** 2
        self.B0 = math.sqrt(s10 * s20)
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
