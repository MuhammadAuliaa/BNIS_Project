import streamlit as st
from streamlit_option_menu import option_menu
import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
from function import volumeSpike
import plotly.graph_objects as go
import os

with st.sidebar:
    selected = option_menu("Main Menu", ["Bursa Efek Indonesia", "Volume Spike (Visual)", "Volume Spike (Data)", "Layout"], 
        icons=['upload', 'gear', 'activity'], menu_icon="cast", default_index=0)
    selected

if selected == 'Bursa Efek Indonesia':
    ticker_symbol = st.selectbox(
        "Please enter the stock symbol",
        ("ACES.JK", "ADRO.JK", "AKRA.JK", "AMRT.JK", "ANTM.JK", "ARTO.JK", "ASII.JK", "BBCA.JK", "BBNI.JK", "BBRI.JK", 
         "BBTN.JK", "BMRI.JK", "BRIS.JK", "BRPT.JK", "BUKA.JK", "CPIN.JK", "EMTK.JK", "ESSA.JK", "EXCL.JK", "GGRM.JK", 
         "GOTO.JK", "HRUM.JK", "ICBP.JK", "INCO.JK", "INDF.JK", "INKP.JK", "INTP.JK", "ITMG.JK", "KLBF.JK", "MAPI.JK", 
         "MBMA.JK", "MDKA.JK", "MEDC.JK", "MTEL.JK", "PGAS.JK", "PGEO.JK", "PTBA.JK", "PTMP.JK", "SIDO.JK", "SMGR.JK", 
         "SRTG.JK", "TLKM.JK", "TOWR.JK", "UNTR.JK", "UNVR.JK", "HMSP.JK")
    )
    st.write("You selected:", ticker_symbol)

    data_period = st.text_input("Period", "10d")
    data_interval = st.radio("Interval", ['5m', '15m', '30m', '1h', '1d', '5d'])

    st.header(ticker_symbol)

    ticker_data = volumeSpike.get_ticker_data(ticker_symbol, data_period, data_interval)
    st.dataframe(ticker_data[['Open', 'High', 'Low', 'Close', 'Volume']])

elif selected == 'Volume Spike (Visual)':
    stock_symbols = ["ACES.JK", "ADRO.JK", "AKRA.JK", "AMRT.JK", "ANTM.JK", "ARTO.JK", "ASII.JK", "BBCA.JK", "BBNI.JK", "BBRI.JK", 
                    "BBTN.JK", "BMRI.JK", "BRIS.JK", "BRPT.JK", "BUKA.JK", "CPIN.JK", "EMTK.JK", "ESSA.JK", "EXCL.JK", "GGRM.JK", 
                    "GOTO.JK", "HRUM.JK", "ICBP.JK", "INCO.JK", "INDF.JK", "INKP.JK", "INTP.JK", "ITMG.JK", "KLBF.JK", "MAPI.JK", 
                    "MBMA.JK", "MDKA.JK", "MEDC.JK", "MTEL.JK", "PGAS.JK", "PGEO.JK", "PTBA.JK", "PTMP.JK", "SIDO.JK", "SMGR.JK", 
                    "SRTG.JK", "TLKM.JK", "TOWR.JK", "UNTR.JK", "UNVR.JK", "HMSP.JK"]

    start_date = st.date_input("Start Date", value=pd.to_datetime('2024-01-01'))
    end_date = st.date_input("End Date", value=pd.to_datetime('2024-06-03'))
    interval = st.selectbox("Interval", ["10m", '30m', '1h', "1d", "1wk", "1mo"])
    volume_threshold = st.number_input("Volume Threshold", min_value=0)

    for symbol in stock_symbols:
        st.write(f"## {symbol}")
        stock_data = yf.download(symbol, start=start_date, end=end_date, interval=interval)
        volumeSpike.plot_stock_interactive(stock_data, symbol, volume_threshold)

elif selected == 'Volume Spike (Data)':
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

    stock_symbols = ["ACES.JK", "ADRO.JK", "AKRA.JK", "AMRT.JK", "ANTM.JK", "ARTO.JK", "ASII.JK", "BBCA.JK", "BBNI.JK", "BBRI.JK", 
                    "BBTN.JK", "BMRI.JK", "BRIS.JK", "BRPT.JK", "BUKA.JK", "CPIN.JK", "EMTK.JK", "ESSA.JK", "EXCL.JK", "GGRM.JK", 
                    "GOTO.JK", "HRUM.JK", "ICBP.JK", "INCO.JK", "INDF.JK", "INKP.JK", "INTP.JK", "ITMG.JK", "KLBF.JK", "MAPI.JK", 
                    "MBMA.JK", "MDKA.JK", "MEDC.JK", "MTEL.JK", "PGAS.JK", "PGEO.JK", "PTBA.JK", "PTMP.JK", "SIDO.JK", "SMGR.JK", 
                    "SRTG.JK", "TLKM.JK", "TOWR.JK", "UNTR.JK", "UNVR.JK", "HMSP.JK", "PTBA.JK"]

    merged_file_name = st.text_input("Input File Name : ")
    start_date = st.date_input("Start Date", value=pd.to_datetime('2024-01-01'))
    end_date = st.date_input("End Date", value=pd.to_datetime('2024-06-09'))
    interval = st.selectbox("Interval", ["10m", '30m', '1h', "1d", "1wk", "1mo"])
    volume_threshold = st.number_input("Volume Threshold", min_value=0)

    all_data = pd.DataFrame()

    for symbol in stock_symbols:
        st.write(f"## {symbol}")
        stock_data = yf.download(symbol, start=start_date, end=end_date, interval=interval)
        
        if not stock_data.empty:
            stock_data['Nama Saham'] = symbol
            plot_stock_interactive(stock_data, symbol, volume_threshold)
            all_data = pd.concat([all_data, stock_data])

    all_data['Threshold'] = volume_threshold
    average_volume_all = all_data.groupby('Nama Saham')['Volume'].transform('mean')
    all_data['Action Spike'] = 'none'
    all_data.loc[(all_data['Volume'] > volume_threshold * average_volume_all) & (all_data['Close'] > all_data['Open']), 'Action Spike'] = 'spike buy'
    all_data.loc[(all_data['Volume'] > volume_threshold * average_volume_all) & (all_data['Close'] <= all_data['Open']), 'Action Spike'] = 'spike sell'
    
    # Calculate Lot
    all_data['Lot'] = all_data['Volume'] // 100

    all_data_sorted = all_data.sort_values(by=['Action Spike', 'Volume'], ascending=[False, False])

    st.write("Sorted Stock Data:")
    st.dataframe(all_data_sorted[['Nama Saham', 'Open', 'High', 'Low', 'Close', 'Volume', 'Lot', 'Threshold', 'Action Spike']])

    today_date = pd.to_datetime('today').normalize()
    result_data = all_data_sorted[all_data_sorted['Action Spike'].isin(['spike buy', 'spike sell'])].copy()
    result_data['Date'] = result_data.index
    result_data['Price Spike'] = result_data['Close']
    result_data['Close'] = result_data['Close']
    result_data['Close Today'] = result_data.groupby('Nama Saham')['Close'].shift(1)
    result_data['Selisih'] = result_data['Close Today'] - result_data['Close']
    result_data['Presentasi'] = (result_data['Selisih'] / result_data['Close']) * 100
    result_data['Presentasi'] = result_data['Presentasi'].map("{:.2f}%".format)
    result_data['Selisih Hari'] = (today_date - result_data['Date']).dt.days

    st.write("Filtered Spike Data:")
    st.dataframe(result_data[['Nama Saham', 'Threshold', 'Volume', 'Lot', 'Action Spike', 'Price Spike', 'Close Today', 'Selisih', 'Presentasi', 'Selisih Hari']])
    
    if st.button("Download Data"):
        output_folder = "dataHasilVolumeSpike"
        os.makedirs(output_folder, exist_ok=True)
        output_file_path = os.path.join(output_folder, f"{merged_file_name}.xlsx")
        result_data.to_excel(output_file_path, index=False)

        st.success(f"Download Data Volume Spike berhasil!")

elif selected == 'Layout':
    # Reference : https://adatis.co.uk/building-data-apps-with-pythons-streamlit/
    # Layout with 5 horizontal boxes
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.markdown(
            "<div style='border: 1px solid; background-color: grey; padding: 10px; margin-bottom: 10px;'>"
            "<p style='color: white;'>Open Price :</p>"
            "</div>",
            unsafe_allow_html=True
        )
        # st.line_chart(selected_data['Open'])

    with col2:
        st.markdown(
            "<div style='border: 1px solid; background-color: grey; padding: 10px; margin-bottom: 10px;'>"
            "<p style='color: white;'>High Price :</p>"
            "</div>",
            unsafe_allow_html=True
        )
        # st.line_chart(selected_data['High'])

    with col3:
        st.markdown(
            "<div style='border: 1px solid; background-color: grey; padding: 10px; margin-bottom: 10px;'>"
            "<p style='color: white;'>Low Price :</p>"
            "</div>",
            unsafe_allow_html=True
        )
        # st.line_chart(selected_data['Low'])

    with col4:
        st.markdown(
            "<div style='border: 1px solid; background-color: grey; padding: 10px; margin-bottom: 10px;'>"
            "<p style='color: white;'>Close Price :</p>"
            "</div>",
            unsafe_allow_html=True
        )
        # st.line_chart(selected_data['Close'])

    with col5:
        st.markdown(
            "<div style='border: 1px solid; background-color: grey; padding: 10px; margin-bottom: 10px;'>"
            "<p style='color: white;'>Volume :</p>"
            "</div>",
            unsafe_allow_html=True
        )
        # st.line_chart(selected_data['Volume'])

    col6, col7= st.columns(2)
    with col6:
        st.markdown(
            "<div style='border: 1px solid; background-color: grey; padding: 10px; margin-bottom: 10px;'>"
            "<p style='color: white;'>Visualization :</p>"
            "</div>",
            unsafe_allow_html=True
        )
        # st.line_chart(selected_data['Volume'])

    with col7:
        st.markdown(
            "<div style='border: 1px solid; background-color: grey; padding: 10px; margin-bottom: 10px;'>"
            "<p style='color: white;'>Data BBNI.JK :</p>"
            "</div>",
            unsafe_allow_html=True
        )
        # st.line_chart(selected_data['Volume'])
