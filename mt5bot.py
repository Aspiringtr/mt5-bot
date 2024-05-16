import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime
import keyboard 
import time
def trend():
    i=25
    bullorbear={'bull':0,'bear':0}
    while i>0:
        if data.open.iloc[-i]<data.close.iloc[-i]:
            bullorbear['bull']+=1
        elif data.open.iloc[-i]>data.close.iloc[-i]:
            bullorbear['bear']+=1
        else:
            pass
        i-=1
    return 1 if bullorbear['bull']>bullorbear['bear'] else 0
def buyorsell(currency,type,tp,sl):
    bos=mt5.ORDER_TYPE_BUY if type==1 else mt5.ORDER_TYPE_SELL
    bb="BUY" if type==1 else "sell"
    if mt5.symbol_info_tick(currency).ask < data.high.iloc[-2] and mt5.symbol_info_tick(currency).ask > data.low.iloc[-2]:
        ord=mt5.symbol_info_tick(currency).ask
    else:
        ord="ok"

    request={
        'action':mt5.TRADE_ACTION_DEAL,
        'symbol':currency,
        'volume':2.0,#float
        'type':bos,
        'price':ord ,
        'sl':sl,
        'tp':tp,
        'deviation':20,
        'magic':234000,
        'comment':bb,
        'type_time': mt5.ORDER_TIME_GTC,
        'type_filling':mt5.ORDER_FILLING_IOC,
    }
    return request
def scalp_order(currency,trnd):
    if trnd==1:
        if data.open.iloc[-2]<data.close.iloc[-2] and data.open.iloc[-2]!=data.low.iloc[-2] and data.close.iloc[-2]!=data.high.iloc[-2] and data.close.iloc[-1]>data.low.iloc[-2] and data.close.iloc[-1]<data.high.iloc[-2]:
            placeorder=mt5.order_send(buyorsell(currency,1,data.high.iloc[-2],data.low.iloc[-2]))
            print(placeorder)
    else:
        if data.open.iloc[-2]>data.close.iloc[-2] and data.open.iloc[-2]!=data.high.iloc[-2] and data.close.iloc[-2]!=data.low.iloc[-2] and data.close.iloc[-1]>data.low.iloc[-2] and data.close.iloc[-1]<data.high.iloc[-2]:
            placeorder=mt5.order_send(buyorsell(currency,0,data.low.iloc[-2],data.high.iloc[-2]))
            print(placeorder)
mt5.initialize()
print(mt5.login(login=81816144, server="MetaQuotes-Demo",password="3hLuFbW@"))
data=pd.DataFrame(mt5.copy_rates_range("EURUSD",mt5.TIMEFRAME_M1,datetime(2024,5,13),datetime(2024,5,16)))
while True:
    i=0
    updown=trend()
    while True:

        if mt5.positions_total()==0:
            data=pd.DataFrame(mt5.copy_rates_range("EURUSD",mt5.TIMEFRAME_M5,datetime(2024,5,13),datetime(2024,5,16)))
            scalp_order("EURUSD",updown)
            time.sleep(5)
            i+=1
        else:
            continue
        #time.sleep(5)
        if i==5:
            break
    if keyboard.is_pressed('q')==True:
        break   
mt5.shutdown()