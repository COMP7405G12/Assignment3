#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: Assignment3
# File name: index
# Author: Mark Wang
# Date: 29/3/2016

import web

from eu_black_scholes import EuropeanOptionHtml
from arithmetic_mean_basket_options import ArithmeticMeanBasketOptionsHTML
from geometricOptions import GeometricOptionHtml, GeometricBasketHtml
from Binomial import BinomialTreeHtml
from impliedVol import ImpliedVolHtml
from arithmeticAsianOptionPricer import ArithmeticAsianOptionPricerHtml


class MyApplication(web.application):
    def run(self, port=8080, *middleware):
        func = self.wsgifunc(*middleware)
        return web.httpserver.runsimple(func, ('127.0.0.1', port))


urls = (
    '/am_bo', ArithmeticMeanBasketOptionsHTML,
    '/eu_bs', EuropeanOptionHtml,
    '/eu_goa', GeometricOptionHtml,
    '/eu_gob', GeometricBasketHtml,
    '/eu_bt', BinomialTreeHtml,
    '/im_vol', ImpliedVolHtml,
    '/aa_price', ArithmeticAsianOptionPricerHtml,
    '/', ImpliedVolHtml
)
app = MyApplication(urls, globals())

if __name__ == "__main__":
    app.run()
