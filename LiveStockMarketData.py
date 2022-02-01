# Data Source
import yfinance as yf

# Data viz
import plotly.graph_objs as go

# Scheduler and time for new jobs per minute
import schedule
import time

# Included libraries { ctypes, winsound } with Python install.
# import ctypes
import winsound


# import sys


def createchartdata():
    print("createchartdata called.")

    # Interval required 1 minute
    data = yf.download(tickers='ASHOKLEY.NS', period='1d', interval='1m')

    # print(data.all)

    # declare figure
    fig = go.Figure()

    # Candlestick
    fig.add_trace(go.Candlestick(x=data.index,
                                 open=data['Open'],
                                 high=data['High'],
                                 low=data['Low'],
                                 close=data['Close'], name='market data'))

    # Add titles
    fig.update_layout(
        title='ASHOK LEYLAND live share price evolution',
        yaxis_title='Stock Price (INR per Shares)')

    # X-Axes
    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=15, label="15m", step="minute", stepmode="backward"),
                dict(count=45, label="45m", step="minute", stepmode="backward"),
                dict(count=1, label="HTD", step="hour", stepmode="todate"),
                dict(count=3, label="3h", step="hour", stepmode="backward"),
                dict(step="all")
            ])
        )
    )

    # Show
    fig.show()

    return data


def caller():
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    data = createchartdata()
    recent = data['Close'].size - 1
    print(data['Close'][recent] < 138)
    if data['Close'][recent] < 138:
        print("OK Found")
        winsound.Beep(1000, 200)


schedule.every(1).minutes.do(caller)
val = True
while val:
    # Checks whether a scheduled task is pending to run or not
    schedule.run_pending()
    time.sleep(1)
