#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: Assignment3
# File name: eu_bs
# Author: Mark Wang
# Date: 28/3/2016

import web

render = web.template.render('.')
urls = (
    '/', 'index',
    '/eu_bs', 'EuBs'
)
app = web.application(urls, globals())


class index(object):
    def GET(self):
        return "Hello world!"


class EuBs(object):
    def GET(self):
        return render.eu_bs()

if __name__ == "__main__":
    app.run()