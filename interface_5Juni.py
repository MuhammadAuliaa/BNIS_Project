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
    selected = option_menu("Main Menu", ["Bursa Efek Indonesia", "Volume Spike (Visual)", "Volume Spike (Data)"], 
        icons=['upload', 'gear', 'activity'], menu_icon="cast", default_index=0)
    selected

if selected == 'Bursa Efek Indonesia':
    ticker_symbol = st.selectbox(
        "Please enter the stock symbol",
        ("ACES.JK", "ADRO.JK", "AKRA.JK", "AMRT.JK", "ANTM.JK", "ARTO.JK", "ASII.JK", "BBCA.JK", "BBNI.JK", "BBRI.JK", "BBTN.JK", "BMRI.JK", "BRIS.JK", "BRPT.JK", "BUKA.JK", "CPIN.JK", "EMTK.JK", "ESSA.JK", "EXCL.JK", "GGRM.JK", "GOTO.JK", "HRUM.JK", "ICBP.JK", "INCO.JK", "INDF.JK", "INKP.JK", "INTP.JK", "ITMG.JK", "KLBF.JK", "MAPI.JK", "MBMA.JK", "MDKA.JK", "MEDC.JK", "MTEL.JK", "PGAS.JK", "PGEO.JK", "PTBA.JK", "PTMP.JK", "SIDO.JK", "SMGR.JK", "SRTG.JK", "TLKM.JK", "TOWR.JK", "UNTR.JK", "UNVR.JK", "HMSP.JK")
    )
    st.write("You selected:", ticker_symbol)

    data_period = st.text_input("Period", "10d")
    data_interval = st.radio("Interval", ['5m', '15m', '30m', '1h', '1d', '5d'])

    st.header(ticker_symbol)

    ticker_data = volumeSpike.get_ticker_data(ticker_symbol, data_period, data_interval)
    st.dataframe(ticker_data[['Open', 'High', 'Low', 'Close', 'Volume']])

elif selected == 'Volume Spike (Visual)':
    # Input simbol saham
    stock_symbols = ["ACES.JK", "ADRO.JK", "AKRA.JK", "AMRT.JK", "ANTM.JK", "ARTO.JK", "ASII.JK", "BBCA.JK", "BBNI.JK", "BBRI.JK", "BBTN.JK", "BMRI.JK", "BRIS.JK", "BRPT.JK", "BUKA.JK", "CPIN.JK", "EMTK.JK", "ESSA.JK", "EXCL.JK", "GGRM.JK", "GOTO.JK", "HRUM.JK", "ICBP.JK", "INCO.JK", "INDF.JK", "INKP.JK", "INTP.JK", "ITMG.JK", "KLBF.JK", "MAPI.JK", "MBMA.JK", "MDKA.JK", "MEDC.JK", "MTEL.JK", "PGAS.JK", "PGEO.JK", "PTBA.JK", "PTMP.JK", "SIDO.JK", "SMGR.JK", "SRTG.JK", "TLKM.JK", "TOWR.JK", "UNTR.JK", "UNVR.JK", "HMSP.JK"]

    # Meminta input dari pengguna
    start_date = st.date_input("Start Date", value=pd.to_datetime('2024-01-01'))
    end_date = st.date_input("End Date", value=pd.to_datetime('2024-06-03'))
    interval = st.selectbox("Interval", ["10m", '30m', '1h', "1d", "1wk", "1mo"])
    volume_threshold = st.number_input("Volume Threshold", min_value=0)

    # Mengambil data saham dari Yahoo Finance untuk setiap simbol
    for symbol in stock_symbols:
        st.write(f"## {symbol}")
        stock_data = yf.download(symbol, start=start_date, end=end_date, interval=interval)
        volumeSpike.plot_stock_interactive(stock_data, symbol, volume_threshold)

elif selected == 'Volume Spike (Data)':
    def plot_stock_interactive(data, symbol, volume_threshold):
        fig = go.Figure()

        # Menambahkan garis untuk harga penutupan
        fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Close Price'))

        # Menambahkan garis untuk volume
        fig.add_trace(go.Scatter(x=data.index, y=data['Volume'], mode='lines', name='Volume', yaxis='y2'))

        # Menandai volume spike dengan warna merah
        average_volume = data['Volume'].mean()
        volume_spike = data['Volume'] > volume_threshold * average_volume
        volume_spike_labels = volume_spike.replace({True: 'spike', False: 'none'})
        spike_indices = volume_spike_labels[volume_spike_labels == 'spike'].index
        fig.add_trace(go.Scatter(x=spike_indices, y=data.loc[spike_indices, 'Volume'], mode='markers', 
                                marker=dict(color='red', size=8), name='Volume Spike', yaxis='y2'))

        # Menambahkan judul dan label sumbu
        fig.update_layout(title=f'Stock Price and Volume ({symbol})',
                        xaxis_title='Date',
                        yaxis_title='Close Price',
                        yaxis2=dict(title='Volume', overlaying='y', side='right'),
                        template='plotly_dark')

        st.plotly_chart(fig)

    # Input simbol saham
    stock_symbols = ["ACES.JK", "ADRO.JK", "AKRA.JK", "AMRT.JK", "ANTM.JK", "ARTO.JK", "ASII.JK", "BBCA.JK", "BBNI.JK", "BBRI.JK", 
                    "BBTN.JK", "BMRI.JK", "BRIS.JK", "BRPT.JK", "BUKA.JK", "CPIN.JK", "EMTK.JK", "ESSA.JK", "EXCL.JK", "GGRM.JK", 
                    "GOTO.JK", "HRUM.JK", "ICBP.JK", "INCO.JK", "INDF.JK", "INKP.JK", "INTP.JK", "ITMG.JK", "KLBF.JK", "MAPI.JK", 
                    "MBMA.JK", "MDKA.JK", "MEDC.JK", "MTEL.JK", "PGAS.JK", "PGEO.JK", "PTBA.JK", "PTMP.JK", "SIDO.JK", "SMGR.JK", 
                    "SRTG.JK", "TLKM.JK", "TOWR.JK", "UNTR.JK", "UNVR.JK", "HMSP.JK"]

    # Meminta input dari pengguna
    merged_file_name = st.text_input("Input File Name : ")
    start_date = st.date_input("Start Date", value=pd.to_datetime('2024-01-01'))
    end_date = st.date_input("End Date", value=pd.to_datetime('2024-06-03'))
    interval = st.selectbox("Interval", ["10m", '30m', '1h', "1d", "1wk", "1mo"])
    volume_threshold = st.number_input("Volume Threshold", min_value=0)

    # Mengambil data saham dari Yahoo Finance untuk setiap simbol dan menggabungkannya ke dalam satu DataFrame
    all_data = pd.DataFrame()

    for symbol in stock_symbols:
        st.write(f"## {symbol}")
        stock_data = yf.download(symbol, start=start_date, end=end_date, interval=interval)
        
        if not stock_data.empty:
            stock_data['Nama Saham'] = symbol
            plot_stock_interactive(stock_data, symbol, volume_threshold)
            all_data = pd.concat([all_data, stock_data])

    # Tambahkan kolom baru "Threshold" ke DataFrame gabungan
    all_data['Threshold'] = volume_threshold

    # Menandai volume spike dalam DataFrame gabungan
    average_volume_all = all_data.groupby('Nama Saham')['Volume'].transform('mean')
    all_data['Volume Spike'] = (all_data['Volume'] > volume_threshold * average_volume_all).replace({True: 'spike', False: 'none'})

    # Mengurutkan data berdasarkan Volume Spike dan Volume secara descending
    all_data_sorted = all_data.sort_values(by=['Volume Spike', 'Volume'], ascending=[False, False])

    # Tampilkan DataFrame yang sudah diurutkan
    st.write("Sorted Stock Data:")
    st.dataframe(all_data_sorted[['Nama Saham', 'Open', 'High', 'Low', 'Close', 'Volume', 'Threshold', 'Volume Spike']])
    if st.button("Download Data"):
        output_folder = "dataHasilVolumeSpike"
        os.makedirs(output_folder, exist_ok=True)
        output_file_path = os.path.join(output_folder, f"{merged_file_name}.xlsx")
        all_data_sorted.to_excel(output_file_path, index=False)

        st.success(f"Download Data Volume Spike berhasil!")