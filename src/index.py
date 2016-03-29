#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: Assignment3
# File name: index
# Author: Mark Wang
# Date: 29/3/2016

import web

from eu_black_scholes import EuropeanOptionHtml


if __name__ == "__main__":
    render = web.template.render('.')
    urls = (
        '/eu_bs', 'EuropeanOptionHtml'
    )
    app = web.application(urls, globals())
    app.run()