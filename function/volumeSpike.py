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