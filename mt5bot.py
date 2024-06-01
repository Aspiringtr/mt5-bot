import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime,timedelta
import time

'''                                  to install the module just type the below line in the cmd                          '''
'''                                             pip install -r requirements.txt                                         '''
'''                                              Trend identifier for scalping                                          '''

def trend():
    i=20
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

'''                                     a simple def to fill the request automatically                                  '''

def buyorsell(currency,tp,sl):
    bos=mt5.ORDER_TYPE_BUY if trend()==1 else mt5.ORDER_TYPE_SELL
    if mt5.symbol_info_tick(currency).ask < data.high.iloc[-2] and mt5.symbol_info_tick(currency).ask > data.low.iloc[-2]:
        ord=mt5.symbol_info_tick(currency).ask
    else:
        ord="aspirin"
    request={
        'action':mt5.TRADE_ACTION_DEAL,
        'symbol':currency,
        'volume':2.0,#float
        'type':bos,
        'price':ord,
        'sl':sl,
        'tp':tp,
        'deviation':20,
        'magic':234000,
        'comment':"NTS",
        'type_time': mt5.ORDER_TIME_GTC,
        'type_filling':mt5.ORDER_FILLING_IOC,
    }
    return request

'''                                      this is where the scalping algo is place                                       '''

def scalp_order(currency):
    trand=trend()
    if trand==1:
        if data.open.iloc[-2]<data.close.iloc[-2] and data.open.iloc[-2]!=data.low.iloc[-2] and data.close.iloc[-2]!=data.high.iloc[-2] and data.close.iloc[-1]>data.low.iloc[-2] and data.close.iloc[-1]<data.high.iloc[-2]:
            mt5.order_send(buyorsell(currency,data.high.iloc[-2],data.low.iloc[-2]))
            print(f"You have place a buy order at {currency} ")
            time.sleep(60)
    elif trand==0:
        if data.open.iloc[-2]>data.close.iloc[-2] and data.open.iloc[-2]!=data.high.iloc[-2] and data.close.iloc[-2]!=data.low.iloc[-2] and data.close.iloc[-1]>data.low.iloc[-2] and data.close.iloc[-1]<data.high.iloc[-2]:
            mt5.order_send(buyorsell(currency,data.low.iloc[-2],data.high.iloc[-2]))
            print(f"You have place a sell order at {currency} ")
            time.sleep(60)
    else:
        print("the market is consolidating now")

'''                                   fill the user login server details and password                                   '''

try:
    mt5.initialize()
    user_details={"log":81816144,"ser":"MetaQuotes-Demo","pass":"3hLuFbW@"}
    mt5.login(login=user_details['log'], server=user_details['ser'],password=user_details['pass'])
    print("successfully loged in to your account")
except:
    print("An error occured during login")
    quit()

'''                                     setting the data frame to get the candle info                                   '''

curr_no=int(input("1:EURUSD\n2:GBPUSD\n3:USDCHF\n4:USDJPY\n5:USDCNH\n6:USDRUB\n7:AUDUSD\n8:NZDUSD\n9:USDCAD\n10:USDSEK\nEnter the exchange number:"))
curr_lis=["EURUSD","GBPUSD","USDCHF","USDJPY","USDCNH","USDRUB","AUDUSD","NZDUSD","USDCAD","USDSEK"]
req_curr=curr_lis[curr_no-1]
print(f"The {req_curr} trading session started at:{datetime.now()}")
data=None

'''                                  scalping part where the code is executed repeatedly                                '''

while True:
    try:
        if mt5.positions_total()==0:
            data=pd.DataFrame(mt5.copy_rates_range(req_curr,mt5.TIMEFRAME_M5,datetime.now()-timedelta(days=1),datetime.now()+timedelta(days=1)))
            scalp_order(req_curr)
    except:
        mt5.shutdown()
        print(f"The {req_curr} trading session ended at: {datetime.now()}")
        break

''' 
This code is just made for entertainment and educational purposes and use it at your own risk
for more details contact :www.instagram.com/aspirin.gtr
OK bye
'''