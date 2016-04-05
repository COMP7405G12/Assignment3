import impliedVol

if __name__ == '__main__':
    # [test case 01] output: (Bid: 0.370531  Ask: 0.388385)
    impliedV = impliedVol.impliedVol(1.95883333, 0.04, 0.2, 8.0 / 365, 1.8, 0.1547, 'Call', 0)
    CallAskVol = impliedV.impliedVol()
    impliedV.__init__(1.95883333, 0.04, 0.2, float(8) / 365, 1.8, 0.1554, 'Call', 0)
    CallBidVol = impliedV.impliedVol()

    # [test case 02] output: (Bid: 0.35686 Ask: 0.378679)
    impliedV1 = impliedVol.impliedVol(1.95883333, 0.04, 0.2, float(8) / 365, 1.8, 0.0027, 'Put', 0)
    PutAskVol = impliedV1.impliedVol()
    impliedV1.__init__(1.95883333, 0.04, 0.2, float(8) / 365, 1.8, 0.0035, 'Put', 0)
    PutBidVol = impliedV1.impliedVol()

    # [test case 03] output:(Bid: 0.703173 Ask:0.732629)
    impliedV2 = impliedVol.impliedVol(1.95720833, 0.04, 0.2, float(8) / 365, 2.6, 0.0002, 'Call', 0)
    CallAskVol1 = impliedV2.impliedVol()
    impliedV2.__init__(1.95720833, 0.04, 0.2, float(8) / 365, 2.6, 0.0003, 'Call', 0)
    CallBidVol1 = impliedV2.impliedVol()

    # [test case 04] output:(Bid: NaN Ask:2.20045)
    impliedV3 = impliedVol.impliedVol(1.95720833, 0.04, 0.2, float(8) / 365, 2.6, 0.5827, 'Put', 0)
    PutAskVol1 = impliedV3.impliedVol()
    impliedV3.__init__(1.95720833, 0.04, 0.2, float(8) / 365, 2.6, 0.725, 'Put', 0)
    PutBidVol1 = impliedV3.impliedVol()

    # [test case 05] output:(Bid: 0.393748 Ask:0.406336)
    impliedV4 = impliedVol.impliedVol(1.95795455, 0.04, 0.2, float(8) / 365, 2.15, 0.0024, 'Call', 0)
    CallAskVol2 = impliedV4.impliedVol()
    impliedV4.__init__(1.95795455, 0.04, 0.2, float(8) / 365, 2.15, 0.0028, 'Call', 0)
    CallBidVol2 = impliedV4.impliedVol()

    # [test case 06] output:(Bid: NaN Ask:0.544185)
    impliedV5 = impliedVol.impliedVol(1.95795455, 0.04, 0.2, float(8) / 365, 2.15, 0.1972, 'Put', 0)
    PutAskVol2 = impliedV5.impliedVol()
    impliedV5.__init__(1.95795455, 0.04, 0.2, float(8) / 365, 2.15, 0.2074, 'Put', 0)
    PutBidVol2 = impliedV5.impliedVol()

    print (
    "test result: ", CallAskVol, CallBidVol, PutAskVol, PutBidVol, CallAskVol1, CallBidVol1, PutAskVol1, PutBidVol1,
    CallAskVol2, CallBidVol2, PutAskVol2, PutBidVol2)

    # [test case 07] output: 0.2
    impliedV5.__init__(100, 0.01, 0, 0.5, 100, 5.3772721531, 'Put', 0)
    testVol = impliedV5.impliedVol()
    print testVol
