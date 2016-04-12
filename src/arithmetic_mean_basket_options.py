#!/usr/bin/python
# -*- coding: utf-8 -*-

# Project: Assignment3
# File name: arithmetic_mean_basket_options
# Author: Mark Wang
# Date: 26/3/2016

import math

import web
import numpy as np
import numpy.random as random
from scipy.stats import norm

from __init__ import render

# Remark that used in the following code
PUT_OPTION = "Put"
CALL_OPTION = "Call"


class Option(object):
    """
    Class to represent a option
    """

    def __init__(self, s0, strike_price, sigma, option_type, tau, risk_free_rate):
        self.sigma = float(sigma)
        self.type = option_type
        self.strike_price = float(strike_price)
        self.s0 = float(s0)
        self.tau = float(tau)
        self.risk_free_rate = risk_free_rate

    def get_stock_price_array(self, random_value):
        """
        Use input random_value to calculate the stock price list
        :param random_value: a list of random value
        :return: a stock price list
        """
        stock_price_list = []
        for zi in random_value:
            stock_price = self.s0 * math.exp((self.risk_free_rate - 0.5 * self.sigma ** 2) * self.tau +
                                             self.sigma * math.sqrt(self.tau) * zi)
            stock_price_list.append(stock_price)

        return np.array(stock_price_list)


class BasketOptions(object):
    def __init__(self, stock_price, k, sigma, option_type, tau, rho, risk_free_rate):
        self.option = []
        self.option_num = len(stock_price)
        for i in range(self.option_num):
            self.option.append(Option(stock_price[i], k, sigma[i], option_type, tau, risk_free_rate))
        self.tau = float(tau)
        self.strike_price = float(k)
        self.type = option_type
        self.risk_free_rate = risk_free_rate
        self.rho = []

        # generate correlation matrix
        for i in range(self.option_num):
            self.rho.append([])
            for j in range(self.option_num):
                if j == i:
                    self.rho[i].append(1)
                elif j > i:
                    self.rho[i].append(rho.pop(0))
                else:
                    self.rho[i].append(self.rho[j][i])

    def _get_basket_price(self, path_number):
        """ Return the basket price, this will be different as the option type difference """

        # fix all the variable
        random.seed(0)

        # generate the random values and calculate all the stock price
        z = random.multivariate_normal([0] * self.option_num, self.rho, path_number).T
        b = self.option[0].get_stock_price_array(z[0])
        s = [self.option[0].get_stock_price_array(z[0])]
        for i in range(1, self.option_num):
            s.append(self.option[i].get_stock_price_array(z[i]))
            b += s[-1]

        b /= self.option_num
        if self.type == CALL_OPTION:
            maturity_price = b - self.strike_price
        else:
            maturity_price = self.strike_price - b

        vitality = math.exp(-self.risk_free_rate * self.tau)

        maturity_price = np.array([max(i, 0) * vitality for i in maturity_price])

        return maturity_price, s

    def _get_geometric_price(self):
        """
        An internal version, use to get the geometric basket option price
        :return: the geometric option price
        """

        # get average, standard deviation and basket price at time zero of current basket option
        std_bg = 0.0
        for i in range(self.option_num):
            for j in range(self.option_num):
                std_bg += self.option[i].sigma * self.option[j].sigma * self.rho[i][j]
        std_bg = math.sqrt(std_bg) / self.option_num
        mean_bg = self.risk_free_rate + 0.5 * std_bg ** 2
        bg0 = 1
        for i in range(self.option_num):
            mean_bg -= 0.5 * self.option[i].sigma ** 2 / self.option_num
            bg0 *= self.option[i].s0
        bg0 **= (1 / float(self.option_num))

        # calculate d1 and d2
        d1 = (math.log(bg0 / self.strike_price) + (mean_bg + 0.5 * std_bg ** 2) * self.tau) / (
            std_bg * math.sqrt(self.tau))
        d2 = d1 - std_bg * math.sqrt(self.tau)

        # Base on the option type, get the option price
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
        arithmetic_price, s = self._get_basket_price(path_number)
        geo_mean_price = self._get_geometric_price()

        # geometric price
        basket_geo_price = s[0]
        for i in range(1, self.option_num):
            basket_geo_price *= s[i]
        basket_geo_price = np.power(basket_geo_price, 1 / float(self.option_num))
        if self.type == CALL_OPTION:
            maturity_price = basket_geo_price - self.strike_price
        else:
            maturity_price = self.strike_price - basket_geo_price

        # delete those negative prices
        validity = math.exp(-self.risk_free_rate * self.tau)
        geometric_price = np.array([max(i, 0) * validity for i in maturity_price])

        # Control Variate
        cov_geo_arith = (geometric_price * arithmetic_price).mean() - geometric_price.mean() * arithmetic_price.mean()
        theta = cov_geo_arith / geometric_price.var()

        control_variate = arithmetic_price + theta * (geo_mean_price - geometric_price)
        control_mean = control_variate.mean()
        control_std = control_variate.std()
        return [control_mean, control_mean - 1.96 * control_std / math.sqrt(path_number),
                control_mean + 1.96 * control_std / math.sqrt(path_number)]

    def get_basket_price(self, path_number, has_control=False):
        if has_control:
            return self.get_basket_price_with_control_variate(path_number)
        else:
            maturity_price = self._get_basket_price(path_number)[0]
            mean = maturity_price.mean()
            std = maturity_price.std()
            return [mean, mean - 1.96 * std / math.sqrt(path_number), mean + 1.96 * std / math.sqrt(path_number)]


class ArithmeticMeanBasketOptionsHTML(object):
    def GET(self):
        return render.arithmetic_mean_basket_options()

    def POST(self):

        # init some variable values
        stock_price = '0, 0'
        volatility = '0, 0'
        strike = 0
        maturity = 0
        rate = 0
        corr = '0'
        num = None
        option_type = PUT_OPTION
        cv_type = 'GBO'

        data = web.input()
        try:
            stock_price = data['stock']
            volatility = data['vol']
            strike = float(data['strike'])
            maturity = float(data['time'])
            rate = float(data['rate'])
            corr = data['corr']
            num = data['num']
            if num and num.isdigit:
                num = int(num)
            else:
                num = None
            option_type = data['type']
            cv_type = data['cv_type']
        except ValueError, e:
            return render.arithmetic_mean_basket_options(stock=stock_price, vol=volatility,
                                                         strike=strike, corr=corr, rate=rate,
                                                         time=maturity, num=num, type=option_type, cv=cv_type,
                                                         price="Invalid input, please input again")
        try:
            stock_list = stock_price.split(',')
            volatility_list = volatility.split(',')
            corr_list = corr.split(',')
            n = len(stock_list)

            # As a basket option, there should be at least two stocks
            if n <= 1:
                return render.arithmetic_mean_basket_options(stock=stock_price, vol=volatility,
                                                             strike=strike, corr=corr, rate=rate,
                                                             time=maturity, num=num, type=option_type, cv=cv_type,
                                                             price="Not enough stock price input")

            # number of volatility and number of stocks are not equal
            elif n > len(volatility_list):
                return render.arithmetic_mean_basket_options(stock=stock_price, vol=volatility,
                                                             strike=strike, corr=corr, rate=rate,
                                                             time=maturity, num=num, type=option_type, cv=cv_type,
                                                             price="Stock price number is greater than volatility number")

            # Number of correlation does not meet the required
            elif len(corr_list) < n * (n - 1) / 2:
                return render.arithmetic_mean_basket_options(stock=stock_price, vol=volatility,
                                                             strike=strike, corr=corr, rate=rate,
                                                             time=maturity, num=num, type=option_type, cv=cv_type,
                                                             price="Not enough correlation numbers")

            else:
                try:
                    stock_list = [float(i.strip()) for i in stock_list]
                    volatility_list = [float(i.strip()) for i in volatility_list]
                    corr_list = [float(i.strip()) for i in corr_list]
                except ValueError, e:
                    return render.arithmetic_mean_basket_options(stock=stock_price, vol=volatility,
                                                                 strike=strike, corr=corr, rate=rate,
                                                                 time=maturity, num=num, type=option_type, cv=cv_type,
                                                                 price="Wrong value input {}".format(e))

            calculator = BasketOptions(stock_price=stock_list, k=strike, sigma=volatility_list, rho=corr_list,
                                       option_type=option_type, tau=maturity, risk_free_rate=rate)
            if num:

                # GBO means using control variate
                if cv_type == 'GBO':
                    price_list = list(calculator.get_basket_price(num, True))

                # without control variate
                else:
                    price_list = list(calculator.get_basket_price(num))
            else:
                price_list = "Please input a valid path number"

            return render.arithmetic_mean_basket_options(stock=stock_price, vol=volatility,
                                                         strike=strike, corr=corr, rate=rate,
                                                         time=maturity, num=num, type=option_type, cv=cv_type,
                                                         price=price_list[0], interval=str(price_list[1:]))
        except Exception, e:
            return render.arithmetic_mean_basket_options(stock=stock_price, vol=volatility,
                                                         strike=strike, corr=corr, rate=rate,
                                                         time=maturity, num=num, type=option_type, cv=cv_type,
                                                         price="Illeage input, calculate error:" + e.message)
