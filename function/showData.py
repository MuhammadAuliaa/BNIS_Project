import streamlit as st
import plotly.graph_objects as go

def plot_stock_interactive(data, symbol, volume_threshold):
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Close Price'))
    fig.add_trace(go.Scatter(x=data.index, y=data['Volume'], mode='lines', name='Volume', yaxis='y2'))

    average_volume = data['Volume'].mean()
    volume_spike = data['Volume'] > volume_threshold * average_volume

    data['Volume Type'] = ['buy' if (data['Close'][i] > data['Open'][i]) else 'sell' for i in range(len(data))]
    
    buy_spike = volume_spike & (data['Volume Type'] == 'buy')
    sell_spike = volume_spike & (data['Volume Type'] == 'sell')

    buy_spike_indices = data[buy_spike].index
    fig.add_trace(go.Scatter(x=buy_spike_indices, y=data.loc[buy_spike_indices, 'Volume'], mode='markers', 
                            marker=dict(color='green', size=8), name='Volume Spike Buy', yaxis='y2'))

    sell_spike_indices = data[sell_spike].index
    fig.add_trace(go.Scatter(x=sell_spike_indices, y=data.loc[sell_spike_indices, 'Volume'], mode='markers', 
                            marker=dict(color='red', size=8), name='Volume Spike Sell', yaxis='y2'))

    fig.update_layout(title=f'Stock Price and Volume ({symbol})',
                    xaxis_title='Date',
                    yaxis_title='Close Price',
                    yaxis2=dict(title='Volume', overlaying='y', side='right'),
                    template='plotly_dark')

    st.plotly_chart(fig)