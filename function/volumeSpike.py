import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

def get_ticker_data(ticker_symbol, data_period, data_interval):
    ticker_data = yf.download(tickers=ticker_symbol, period=data_period, interval=data_interval)
    if len(ticker_data) == 0:
        st.write('Could not find the ticker data. Modify ticker symbol or reduce the Period value.')
    else:
        #Format the x-axis to skip dates with missing values
        ticker_data.index = ticker_data.index.strftime("%d-%m-%Y %H:%M")
    return ticker_data

def plot_stock_interactive(data, symbol, volume_threshold):
        fig = go.Figure()

        # Menambahkan garis untuk harga penutupan
        fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Close Price'))

        # Menambahkan garis untuk volume
        fig.add_trace(go.Scatter(x=data.index, y=data['Volume'], mode='lines', name='Volume', yaxis='y2'))

        # Menandai volume spike dengan warna merah
        average_volume = data['Volume'].mean()
        volume_spike = data[data['Volume'] > volume_threshold * average_volume]
        fig.add_trace(go.Scatter(x=volume_spike.index, y=volume_spike['Volume'], mode='markers', 
                                marker=dict(color='red', size=8), name='Volume Spike', yaxis='y2'))

        # Menambahkan judul dan label sumbu
        fig.update_layout(title=f'Stock Price and Volume ({symbol})',
                        xaxis_title='Date',
                        yaxis_title='Close Price',
                        yaxis2=dict(title='Volume', overlaying='y', side='right'),
                        template='plotly_dark')

        st.plotly_chart(fig)


# Fungsi untuk mendapatkan harga saham terbaru dari Yahoo Finance
def get_last_prices(stock_symbols):
    last_prices = {}
    for symbol in stock_symbols:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period='1d')
        if not data.empty:
            last_prices[symbol] = data['Close'].iloc[-1]
    return last_prices      

# Fungsi untuk mendapatkan harga saham terbaru dari Yahoo Finance
def get_last_prices_header(symbols):
    last_prices = {}
    for symbol in symbols:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period='1d')
        if not data.empty:
            last_prices[symbol] = data['Close'].iloc[-1]
    return last_prices 

# Function to get the latest stock prices from Yahoo Finance
def get_last_prices_detail(symbols):
    last_prices = {}
    for symbol in symbols:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period='2d')  # Fetching data for the last two days
        if len(data) >= 2:
            last_price = data['Close'].iloc[-1]
            previous_price = data['Close'].iloc[-2]
            change_percent = ((last_price - previous_price) / previous_price) * 100
            last_prices[symbol] = last_price
    return last_prices

# Function to plot stock data interactively
def plot_stock_interactive_data(data, symbol, volume_threshold, ema_period):
    fig = go.Figure()

    # Calculate EMA
    data['EMA'] = data['Close'].ewm(span=ema_period, adjust=False).mean()

    fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Close Price'))
    fig.add_trace(go.Scatter(x=data.index, y=data['Volume'], mode='lines', name='Volume', yaxis='y2'))

    # Plot EMA with transparent white fill
    fig.add_trace(go.Scatter(
        x=data.index,
        y=data['EMA'],
        mode='lines',
        name=f'EMA {ema_period}',
        line=dict(color='yellow'),
        fill='tonexty',
        fillcolor='rgba(235, 222, 52, 0.2)'  # White transparent fill
    ))

    average_volume = data['Volume'].mean()
    threshold_line = volume_threshold * average_volume

    volume_spike = data['Volume'] > threshold_line

    data['Volume Type'] = ['buy' if (data['Close'][i] > data['Open'][i]) else 'sell' for i in range(len(data))]

    buy_spike = volume_spike & (data['Volume Type'] == 'buy')
    sell_spike = volume_spike & (data['Volume Type'] == 'sell')

    buy_spike_indices = data[buy_spike].index
    fig.add_trace(go.Scatter(x=buy_spike_indices, y=data.loc[buy_spike_indices, 'Volume'], mode='markers', 
                            marker=dict(color='green', size=8), name='Volume Spike Buy', yaxis='y2'))

    sell_spike_indices = data[sell_spike].index
    fig.add_trace(go.Scatter(x=sell_spike_indices, y=data.loc[sell_spike_indices, 'Volume'], mode='markers', 
                            marker=dict(color='red', size=8), name='Volume Spike Sell', yaxis='y2'))

    fig.add_trace(go.Scatter(
        x=data.index,
        y=[threshold_line] * len(data),
        mode='lines',
        name='Volume Threshold',
        line=dict(color='white', width=2),
        fill='tonexty',
        fillcolor='rgba(255, 255, 255, 0.2)',
        yaxis='y2'
    ))

    fig.update_layout(title=f'Stock Price and Volume ({symbol})',
                    xaxis_title='Date',
                    yaxis_title='Close Price',
                    yaxis2=dict(title='Volume', overlaying='y', side='right'),
                    template='plotly_dark')

    st.plotly_chart(fig)