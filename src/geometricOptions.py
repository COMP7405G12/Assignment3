import numpy as np
from scipy.stats import norm
import web
from __init__ import render
def geometricAsian(S,v,r,T,K,n,type):
    S = float(S)
    T = float(T)
    K = float(K)
    n = float(n)
    v_g = v * np.sqrt((n + 1)*(2*n + 1)/(6*np.square(n)))
    delt_g = (r - 0.5*np.square(v))*((n + 1)/(2*n)) + 0.5*np.square(v_g)
    d1_g = (np.log(S/K) + (delt_g + 0.5*np.square(v_g))*T)/(v_g*np.sqrt(T))
    d2_g = d1_g - v_g*np.sqrt(T)
    #geometric Asian Call option
    if type == "call":
        return np.exp(-1*r*T)*(S*np.exp(delt_g*T)*norm.cdf(d1_g) - K*norm.cdf(d2_g))
    elif type == "put":
        return np.exp(-1*r*T)*(K*norm.cdf(-1*d2_g) - S*np.exp(delt_g*T)*norm.cdf(-1*d1_g))
    return ""

def geometricBasket(S,v,r,T,K,p,type,n):
    v_b = 0
    n_float = float(n)
    for i in range(0,n):
        for j in range(0,n):
            v_b += v[i]*v[j]*p[i][j]
    v_b = np.sqrt(v_b)/n_float
    delt_b = np.sum(np.square(np.array(v)))
    delt_b = r - 0.5*delt_b/n_float + 0.5*np.square(v_b)
    B = np.cumprod(np.array(S))[-1]
    B = np.power(B,1/n_float)
    d1_b = (np.log(B/K) + (delt_b + 0.5*np.square(v_b))*T)/(v_b*np.sqrt(T))
    d2_b = d1_b - v_b*np.sqrt(T)
    if type == "call":
        return np.exp(-1*r*T)*(B*np.exp(delt_b*T)*norm.cdf(d1_b) - K*norm.cdf(d2_b))
    elif type == "put":
        return np.exp(-1*r*T)*(K*norm.cdf(-1*d2_b) - B*np.exp(delt_b*T)*norm.cdf(-1*d1_b))
    return ""

class GeometricOptionHtml(object):
    def GET(self):
        return render.eu_geometricOptions()

    def POST(self):
        test = web.input()
        print "test"
        try:
            stock_price = float(test['underlying'])
            volatility = float(test['vol'])
            strike_price = float(test['strike'])
            maturity_time = float(test['maturity'])
            risk_free_rate = float(test['interest_rate']) / 100
            observation_times = float(test['observation_times'])
        except ValueError, e:
            return render.eu_geometricOptions("Invalid input, please input again")

        if test['style'] == 'Call':
            option_price = geometricAsian(stock_price,volatility, risk_free_rate,maturity_time,strike_price,observation_times,
                                          "call")
        else:
            option_price = geometricAsian(stock_price,volatility, risk_free_rate,maturity_time,strike_price,observation_times,
                                          "put")
        return render.eu_geometricOptions(option_price, stock=strike_price, vol=volatility, style=test['style'],
                                       strike=strike_price, T=maturity_time, r=risk_free_rate * 100, times=observation_times)

if __name__ == "__main__":
    print geometricAsian(100,0.3,0.05,3,100,50,"put")
    print geometricBasket([100,100],[0.3,0.3],0.05,3,100,[[1,0.5],[0.5,1]],"put",2)




