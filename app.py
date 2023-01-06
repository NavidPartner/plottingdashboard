import streamlit as st # web development
import numpy as np # np mean, np random
import pandas as pd # read csv, df manipulation
import matplotlib.pyplot as plt
import time # to simulate a real time data, time loop
import plotly.express as px # interactive charts
import ccxt
from datetime import datetime


# define exchange
exchange = ccxt.bybit()

def get_ticker_list():



             sf = exchange.fetch_markets()
             a= len(sf)
             word = 'USDT'
             l = []
             for i in range(0,a):
                    if word in sf[i]['symbol']:
                        l.append(sf[i]['symbol'])
             return(l)



def get_data(asset,time,exchange):
    bars = exchange.fetch_ohlcv(asset, timeframe=time, limit=10000)
    df = pd.DataFrame(bars, columns=['time','open','high','low','close','volume'])
    df['time'] = pd.to_datetime(df['time'], unit=('ms'))
    return(df)


def ploting(data,ylabel, xstart, xend):

    csfont = {'fontname':'DejaVu Sans Mono'}
    hfont = {'fontname':'Helvetica'}

    #white Version

    plt.style.use("classic")
    plt.rcParams['figure.dpi'] = 2000

    for param in ['text.color', 'axes.labelcolor', 'xtick.color', 'ytick.color']:
        plt.rcParams[param] = '#193957'  # very light grey

    for param in ['figure.facecolor', 'axes.facecolor', 'savefig.facecolor']:
        plt.rcParams[param] = 'white'  # bluish dark grey
    for param in ['axes.edgecolor']:
        plt.rcParams[param] = 'white'  # bluish dark grey


      # create figure and axis objects with subplots()
    fig,ax = plt.subplots(figsize=(16,9),dpi=500)

    # make a plot
    ax.plot(df.time, df['close'],color="#193957", linewidth=3)
    ax.set_ylabel(""+ylabel,color="#193957",fontsize=14,**csfont, weight = "bold")


    from matplotlib.ticker import ScalarFormatter
    for axis in [ax.yaxis]:
        axis.set_major_formatter(ScalarFormatter())

    ax.ticklabel_format(useOffset=False,axis='y')
    ax.grid(color="#193957", alpha=0.55)
    #[t.set_size(14) for t in ax.yaxis.get_ticklabels()]
    # [t.set_size(14) for t in ax.xaxis.get_ticklabels()]
    # [t.set_weight("bold") for t in ax.yaxis.get_ticklabels()]
    # [t.set_weight("bold") for t in ax.xaxis.get_ticklabels()]




    ax.text(1, -0.05,"\n\nFriedrich & Partner" ,color="#193957", horizontalalignment='right', verticalalignment='center', transform=ax.transAxes,
           bbox=dict(facecolor='none', edgecolor='none', boxstyle='round,pad=0.3'), rotation = 0, weight = "bold")

    ax.text(0.00, -0.05,"\n\nQuelle: Binance API" ,color="#193957", horizontalalignment='left', verticalalignment='center', transform=ax.transAxes,
        bbox=dict(facecolor='none', edgecolor='none', boxstyle='round,pad=0.3'), rotation = 0, weight = "bold")

    ax.text(1.015, 0.5,"www.friedrich-partner.de" ,color="#193957", horizontalalignment='center', verticalalignment='center', transform=ax.transAxes,
        bbox=dict(facecolor='none', edgecolor='none', boxstyle='round,pad=0.3'), rotation = 270, weight = "bold")

    ax.legend(edgecolor="none")
    ax.set_xlim(xstart,xend)
    return(fig)

st.set_page_config(
    page_title = 'Crypto Dashboard',
    page_icon = '✅',
    layout = 'wide'
)

# dashboard title

#st.title("Crypto Marktanalyse" )

# get all avaiable Ticker from Binance

ticker  = get_ticker_list()



# optionsbar to select Ticker from Binance

ticker_option = st.sidebar.selectbox('Select one inflation index', (ticker ))

time_option = st.sidebar.selectbox('Wähle den Timeframe', ("1m","5m","15m","1h","4h","1d","1w" ))

st.title("Crypto Marktanalyse für " + ticker_option+" ["+time_option+"]"  )



###################
# Set up main app #
###################
df = get_data(ticker_option,time_option,exchange)
df.time = pd.to_datetime(df.time)


st.title("Market")

f =  ploting(df,"Price in $",df.time[0],datetime.now())

# fig, ax = plt.subplots(figsize=(21,9))
# ax.plot(df.time,df.close, color = "red")

st.pyplot(f,dpi=600)
