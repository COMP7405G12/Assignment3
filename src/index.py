#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: Assignment3
# File name: index
# Author: Mark Wang
# Date: 29/3/2016

import web

from __init__ import render
from eu_black_scholes import EuropeanOptionHtml
from arithmetic_mean_basket_options import ArithmeticMeanBasketOptionsHTML


class index(object):
    def GET(self):
        return render.index()


if __name__ == "__main__":
    urls = (
        '/am_bo', ArithmeticMeanBasketOptionsHTML,
        '/eu_bs', EuropeanOptionHtml,
        '/', index
    )
    app = web.application(urls, globals())
    app.run()
