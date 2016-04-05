import web

from __init__ import render
from arithmeticAsianOptionPricer import ArithmeticAsianOptionPricerHtml
from impliedVol import ImpliedVolHtml


class Index(object):
    def GET(self):
        return render.index()


if __name__ == "__main__":
    urls = (
        '/im_vol', ImpliedVolHtml,
        '/aa_price', ArithmeticAsianOptionPricerHtml,
        '/', Index
    )
    app = web.application(urls, globals())
    app.run()