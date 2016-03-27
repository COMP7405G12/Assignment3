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

    def __init__(self, s0, strike_price, sigma, type, tau, risk_free_rate):
        self.sigma = float(sigma)
        self.type = type
        self.strike_price = float(strike_price)
        self.s0 = float(s0)
        self.tau = float(tau)
        self.risk_free_rate = risk_free_rate

    def get_stock_price_array(self, random_value):
        stock_price_list = []
        for zi in random_value:
            stock_price = self.s0 * math.exp((self.risk_free_rate - 0.5 * self.sigma ** 2) * self.tau +
                                             self.sigma * math.sqrt(self.tau) * zi)
            stock_price_list.append(stock_price)

        return np.array(stock_price_list)


class BasketOptions(object):
    def __init__(self, s10, s20, k, sigma1, sigma2, type, tau, rho, risk_free_rate=RISK_FREE_RATE):
        self.option1 = Option(s10, k, sigma1, type, tau, risk_free_rate)
        self.option2 = Option(s20, k, sigma2, type, tau, risk_free_rate)
        self.B0 = float(s10 + s20) / 2
        self.tau = float(tau)
        self.strike_price = float(k)
        self.type = type
        self.risk_free_rate = risk_free_rate
        self.rho = rho

    def _get_basket_price(self, path_number):
        ''' Return the basket price, this will be different as the option type difference '''

        # fix all the variable
        random.seed(0)

        z1, z2 = generate_two_correlated_random_variables([0, 0], [1, 1], self.rho, path_number)
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

        return maturity_price * math.exp(-self.risk_free_rate * self.tau), s1, s2

    def _get_geometric_price(self):
        std_bg = math.sqrt(
            self.option1.sigma ** 2 + self.option2.sigma ** 2 + 2 * self.option2.sigma * self.option1.sigma * self.rho
        ) / 2
        mean_bg = self.risk_free_rate - 0.5 * (
            self.option1.sigma ** 2 + self.option2.sigma ** 2) / 2 + 0.5 * std_bg ** 2
        bg0 = math.sqrt(self.option2.s0 * self.option1.s0)
        d1 = (math.log(bg0 / self.strike_price) + (mean_bg + 0.5 * std_bg ** 2) * self.tau) / (
            std_bg * math.sqrt(self.tau))
        d2 = d1 - std_bg * math.sqrt(self.tau)
        if self.type == PUT_OPTION:
            n1 = norm.cdf(-d1)
            n2 = norm.cdf(-d2)
            price = math.exp(-self.risk_free_rate * self.tau) * (
                self.strike_price * n2 - bg0 * math.exp(mean_bg * self.tau) * n1)
        else:
            n1 = norm.cdf(d1)
            n2 = norm.cdf(d2)
            price = math.exp(-self.risk_free_rate * self.tau) * (
                -self.strike_price * n2 + bg0 * math.exp(mean_bg * self.tau) * n1)
        return price

    def get_basket_price_with_control_variate(self, path_number):
        arithmetic_price, s1, s2 = self._get_basket_price(path_number)

        # geometric price
        basket_geo_price = np.sqrt(s1 * s2)
        if self.type == CALL_OPTION:
            maturity_price = basket_geo_price - self.strike_price
        else:
            maturity_price = basket_geo_price - self.strike_price

        # delete those negative prices
        maturity_price = np.array([max(i, 0) for i in maturity_price])
        geometric_price = math.exp(-self.risk_free_rate * self.tau) * maturity_price

        # Control Variate
        xy = geometric_price * arithmetic_price
        print geometric_price.mean() * arithmetic_price.mean()
        cov_geo_arith = (geometric_price * arithmetic_price).mean() - geometric_price.mean() * arithmetic_price.mean()
        theta = cov_geo_arith / geometric_price.std()

        control_variate = arithmetic_price + theta * (geo_mean_price - geometric_price)
        control_mean = control_variate.mean()
        control_std = control_variate.std()
        return control_mean, control_mean - 1.96 * control_std / math.sqrt(path_number), \
               control_mean + 1.96 * control_std / math.sqrt(path_number)

    def get_basket_price(self, path_number=PATH_NUMBER, has_control=False):
        if has_control:
            return self.get_basket_price_with_control_variate(path_number)
        else:
            maturity_price = self._get_basket_price(path_number)[0]
            mean = maturity_price.mean()
            std = maturity_price.std()
            return mean, mean - 1.96 * std / math.sqrt(path_number), mean + 1.96 * std / math.sqrt(path_number)


if __name__ == "__main__":
    test = BasketOptions(s10=100, s20=100, k=100, sigma1=0.3, sigma2=0.3, rho=0.5,
                         type=PUT_OPTION, tau=MATURITY_TIME, risk_free_rate=RISK_FREE_RATE)
    print test.get_basket_price()
    print test.get_basket_price(has_control=True)
    # test = ArithmeticMeanBasketOptions(10, 10, 9, 0.1, 0.1, CALL_OPTION, 1)
    # z = random.normal(size=PATH_NUMBER)

    # print a
