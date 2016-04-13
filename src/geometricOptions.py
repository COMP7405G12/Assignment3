import numpy as np
import web
from scipy.stats import norm

from __init__ import render


def geometricAsian(S, v, r, T, K, n, type):
    S = float(S)
    T = float(T)
    K = float(K)
    n = float(n)
    v_g = v * np.sqrt((n + 1) * (2 * n + 1) / (6 * np.square(n)))
    delt_g = (r - 0.5 * np.square(v)) * ((n + 1) / (2 * n)) + 0.5 * np.square(v_g)
    d1_g = (np.log(S / K) + (delt_g + 0.5 * np.square(v_g)) * T) / (v_g * np.sqrt(T))
    d2_g = d1_g - v_g * np.sqrt(T)
    # geometric Asian Call option
    if type == "call":
        return np.exp(-1 * r * T) * (S * np.exp(delt_g * T) * norm.cdf(d1_g) - K * norm.cdf(d2_g))
    elif type == "put":
        return np.exp(-1 * r * T) * (K * norm.cdf(-1 * d2_g) - S * np.exp(delt_g * T) * norm.cdf(-1 * d1_g))
    return ""


def geometricBasket(S, v, r, T, K, p, type, n):
    v_b = 0
    n_float = float(n)
    for i in range(0, n):
        for j in range(0, n):
            v_b += v[i] * v[j] * p[i][j]
    v_b = np.sqrt(v_b) / n_float
    delt_b = np.sum(np.square(np.array(v)))
    delt_b = r - 0.5 * delt_b / n_float + 0.5 * np.square(v_b)
    B = np.cumprod(np.array(S))[-1]
    B = np.power(B, 1 / n_float)
    d1_b = (np.log(B / K) + (delt_b + 0.5 * np.square(v_b)) * T) / (v_b * np.sqrt(T))
    d2_b = d1_b - v_b * np.sqrt(T)
    if type == "call":
        return np.exp(-1 * r * T) * (B * np.exp(delt_b * T) * norm.cdf(d1_b) - K * norm.cdf(d2_b))
    elif type == "put":
        return np.exp(-1 * r * T) * (K * norm.cdf(-1 * d2_b) - B * np.exp(delt_b * T) * norm.cdf(-1 * d1_b))
    return ""


class GeometricOptionHtml(object):
    def GET(self):
        return render.eu_geometricOptions()

    def POST(self):
        test = web.input()
        try:
            stock_price = float(test['underlying'])
            volatility = float(test['vol'])
            strike_price = float(test['strike'])
            maturity_time = float(test['maturity'])
            risk_free_rate = float(test['interest_rate'])
            observation_times = float(test['observation_times'])
        except ValueError, e:
            return render.eu_geometricOptions("Invalid input, please input again")
        try:
            option_price = geometricAsian(stock_price, volatility, risk_free_rate, maturity_time, strike_price,
                                          observation_times,
                                          test['style'])
            return render.eu_geometricOptions(option_price, stock=stock_price, vol=volatility, style=test['style'],
                                              strike=strike_price, T=maturity_time, r=risk_free_rate,
                                              times=observation_times)
        except Exception, e:
            return render.eu_geometricOptions("Illeage input, calculate error: {}".format(e),
                                              stock=stock_price, vol=volatility, style=test['style'],
                                              strike=strike_price, T=maturity_time, r=risk_free_rate,
                                              times=observation_times)


class GeometricBasketHtml(object):
    def GET(self):
        return render.eu_geometricBasket()

    def POST(self):
        test = web.input()
        try:
            stock_price = str(test['stock']).split(",")
            volatility = str(test['vol']).split(",")
            strike_price = float(test['strike'])
            maturity_time = float(test['time'])
            risk_free_rate = float(test['rate'])
            asset_num = int(test['num'])
            correlation = str(test['corr']).split(",")
            type = test['type']
            if len(stock_price) != asset_num:
                return render.eu_geometricBasket(
                    "Invalid stock price input, number of stock prices doesn't equal to asset number")
            if len(volatility) != asset_num:
                return render.eu_geometricBasket(
                    "Invalid volatility input, number of volatilities doesn't equal to asset number")
            corr_num = asset_num * (asset_num - 1) / 2
            if len(correlation) != corr_num:
                return render.eu_geometricBasket(
                    "Invalid correlation input, number of correlations doesn't equal to asset number")
            # change type to float
            stock_list = [float(i.strip()) for i in stock_price]
            volatility_list = [float(i.strip()) for i in volatility]
            correlation = [float(i.strip()) for i in correlation]
            # construct correlation array
            corr_array = []
            for i in range(asset_num):
                corr_array.append([])
                for j in range(asset_num):
                    if j == i:
                        corr_array[i].append(1)
                    elif j > i:
                        corr_array[i].append(correlation.pop(0))
                    else:
                        corr_array[i].append(corr_array[j][i])
                        # print corr_array

        except ValueError, e:
            return render.eu_geometricBasket("Invalid input, please input again")
        try:
            option_price = geometricBasket(stock_list, volatility_list, risk_free_rate, maturity_time, strike_price,
                                           corr_array,
                                           type, asset_num)
            return render.eu_geometricBasket(option_price, stock=test['stock'], vol=test['vol'], type=test['type'],
                                             strike=test['strike'], time=test['time'], rate=test['rate'],
                                             corr=test['corr'], num=test['num'])
        except Exception, e:
            return render.eu_geometricBasket(option_price="Illeage input, calculate error:" + e.message,
                                             stock=test['stock'], vol=test['vol'], type=test['type'],
                                             strike=test['strike'], time=test['time'], rate=test['rate'],
                                             corr=test['corr'], num=test['num'])


if __name__ == "__main__":
    print geometricAsian(100, 0.3, 0.05, 3, 100, 50, "put")
    print geometricBasket([100, 100], [0.3, 0.3], 0.05, 3, 100, [[1, 0.5], [0.5, 1]], "put", 2)
