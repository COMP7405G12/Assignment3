#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: Assignment3
# File name: index
# Author: Mark Wang
# Date: 29/3/2016

import web

from eu_black_scholes import EuropeanOptionHtml
from arithmetic_mean_basket_options import ArithmeticMeanBasketOptionsHTML
from geometricOptions import GeometricOptionHtml
from Binomial import BinomialTreeHtml
from impliedVol import ImpliedVolHtml
from arithmeticAsianOptionPricer import ArithmeticAsianOptionPricerHtml


class Index(object):
    def GET(self):
        return '''<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Index page of option calculator</title>
</head>
<body>
<h1>Option Calculator</h1>
<a href="/eu_bs">European call/put option Calculator (Using Black-Scholes)</a><br>
<a href="/am_bo">Arithmetic/Geometric mean basket call/put options calculator</a><br>
<a href="/eu_goa">Geometric Asian call/put options calculator</a><br>
<a href="/eu_bt">American call/put option Calculator (Using Binomial Tree)</a><br>
<a href="/im_vol">Implied Volatility</a><br>
<a href="/aa_price">Arithmetic Asian Option Calculator (Monte Carlo)</a><br>
</body>
</html>'''

urls = (
    '/am_bo', ArithmeticMeanBasketOptionsHTML,
    '/eu_bs', EuropeanOptionHtml,
    '/eu_goa', GeometricOptionHtml,
    '/eu_bt', BinomialTreeHtml,
    '/im_vol', ImpliedVolHtml,
    '/aa_price', ArithmeticAsianOptionPricerHtml,
    '/', Index
)
app = web.application(urls, globals())


if __name__ == "__main__":
    app.run()
