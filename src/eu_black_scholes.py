#!/usr/bin/python
# -*- coding: utf-8 -*-

# File name:
# description: Black-Scholes Formulas for European call/put options
# Author: warn
# Date: 2/3/2016 19:12

import math

import web
from scipy.stats import norm

from __init__ import render


def calculate_d1(s, e, tau, sigma, r):
    d1 = (math.log(s / float(e)) + (r + 0.5 * sigma * sigma) * tau) / (sigma * math.sqrt(tau))
    return d1


def calculate_d2(s, e, tau, sigma, r):
    d2 = (math.log(s / float(e)) + (r - 0.5 * sigma * sigma) * tau) / (sigma * math.sqrt(tau))
    return d2


def calculate_call_black_scholes(s, e, tau, sigma, r):
    """
    main function to calculate Black-Scholes call option price
    :param s: Stock price at time t
    :param e: Strike price
    :param tau: expire time T - current time t
    :param sigma: volatility
    :param r: risk free rate
    :return: the call price of Black-Scholes
    """
    d1 = calculate_d1(s, e, tau, sigma, r)
    d2 = calculate_d2(s, e, tau, sigma, r)
    n1 = norm.cdf(d1)
    n2 = norm.cdf(d2)
    c = s * n1 - e * math.exp(-r * tau) * n2
    return c


def calculate_put_black_scholes(s, e, tau, sigma, r):
    """
    main function to calculate black scholes put option price
    :param s: Stock price at time t
    :param e: Strike price
    :param tau: expire time T - current time t
    :param sigma: volatility
    :param r: risk free rate
    :return: the put price of black_scholes
    """
    d1 = calculate_d1(s, e, tau, sigma, r)
    d2 = calculate_d2(s, e, tau, sigma, r)
    n1 = norm.cdf(-d1)
    n2 = norm.cdf(-d2)
    p = e * math.exp(-r * tau) * n2 - s * n1
    return p


class EuropeanOptionHtml(object):
    """
    Web page to show European put / call option calculator
    """
    def GET(self):
        return render.eu_black_scholes()

    def POST(self):
        test = web.input()
        try:
            stock_price = float(test['underlying'])
            volatility = float(test['vol'])
            strike_price = float(test['strike'])
            maturity_time = float(test['maturity'])
            risk_free_rate = float(test['interest_rate']) / 100
        except ValueError, e:
            return render.eu_black_scholes("Invalid input, please input again")

        if test['style'] == 'Call':
            option_price = calculate_call_black_scholes(stock_price, strike_price, maturity_time,
                                                        volatility, risk_free_rate)
        else:
            option_price = calculate_put_black_scholes(stock_price, strike_price, maturity_time,
                                                       volatility, risk_free_rate)
        return render.eu_black_scholes(option_price, stock=stock_price, vol=volatility, style=test['style'],
                                       strike=strike_price, T=maturity_time, r=risk_free_rate * 100)
