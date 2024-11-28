import streamlit as st
import numpy as np
import pandas as pd
import ccxt


if st.button("Тык сюда"):
    exchange = ccxt.bybit()
    symbols = exchange.fetch_tickers()

    res = []
    for k, v in symbols.items():
        filt1 = float(v["quoteVolume"]) > 5e6
        filt2 = k.split(":")[-1] == "USDT"
        if filt1 and filt2:
            res.append(v['symbol'])
    
    goods = []
    for ticker in res:
        print(ticker)
        x = exchange.fetch_ohlcv(ticker, '15m', limit=12)
        dfx = pd.DataFrame(x, columns = ["T", "O", "H", "L", "C", "V"])
        
        rets = dfx["C"].pct_change()[1:].values
        inds = dfx["C"].pct_change()[1:].values > 0
        
        flag_01 = sum(inds) > 8
        flag_02 = (rets + 1).prod() > 1.05
        if flag_01 or flag_02:
            goods.append(ticker)

    st.write(goods)
