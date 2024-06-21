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
from function import showData
import plotly.express as px
from function import screener

with st.sidebar:
    selected = option_menu("Main Menu", ["Bursa Efek Indonesia", "Volume Spike (Data)", "Layout", "Screener"], 
        icons=['upload', 'book', 'activity'], menu_icon="cast", default_index=0)
    selected

if selected == 'Bursa Efek Indonesia':
    # Define stock symbols as selectbox input
    selected_symbols = st.multiselect("Select Stock Symbols", 
                                      ["ACES.JK", "ADRO.JK", "AKRA.JK", "AMRT.JK", "ANTM.JK", "ARTO.JK", "ASII.JK", 
                                       "BBCA.JK", "BBNI.JK", "BBRI.JK", "BBTN.JK", "BMRI.JK", "BRIS.JK", "BRPT.JK", 
                                       "BUKA.JK", "CPIN.JK", "EMTK.JK", "ESSA.JK", "EXCL.JK", "GGRM.JK", "GOTO.JK", 
                                       "HRUM.JK", "ICBP.JK", "INCO.JK", "INDF.JK", "INKP.JK", "INTP.JK", "ITMG.JK", 
                                       "KLBF.JK", "MAPI.JK", "MBMA.JK", "MDKA.JK", "MEDC.JK", "MTEL.JK", "PGAS.JK", 
                                       "PGEO.JK", "PTBA.JK", "PTMP.JK", "SIDO.JK", "SMGR.JK", "SRTG.JK", "TLKM.JK", 
                                       "TOWR.JK", "UNTR.JK", "UNVR.JK", "HMSP.JK", "PTBA.JK", "HUMI.JK"])

    interval = st.selectbox("Interval", ["10m", '30m', '1h', "1d", "1wk", "1mo"])
    start_date = st.date_input("Start Date", value=pd.to_datetime('2024-01-01'))

    all_data = pd.DataFrame()

    run_button = st.button("Analysis Stock")
    if run_button:
        for symbol in selected_symbols:
            # Download stock data
            stock_data = yf.download(symbol, start=start_date, interval=interval)

            if not stock_data.empty:
                # Create a new figure for each stock symbol
                fig = go.Figure(data=[go.Candlestick(x=stock_data.index,
                                                     open=stock_data['Open'],
                                                     high=stock_data['High'],
                                                     low=stock_data['Low'],
                                                     close=stock_data['Close'])])

                fig.update_layout(title=f'Candlestick Chart for {symbol}',
                                  xaxis_title='Date',
                                  yaxis_title='Price')

                st.plotly_chart(fig)

elif selected == 'Volume Spike (Data)':
    # Main program
    stock_symbols = ["ACES.JK", "ADRO.JK", "AKRA.JK", "AMRT.JK", "ANTM.JK", "ARTO.JK", "ASII.JK", "BBCA.JK", "BBNI.JK", "BBRI.JK", 
                    "BBTN.JK", "BMRI.JK", "BRIS.JK", "BRPT.JK", "BUKA.JK", "CPIN.JK", "EMTK.JK", "ESSA.JK", "EXCL.JK", "GGRM.JK", 
                    "GOTO.JK", "HRUM.JK", "ICBP.JK", "INCO.JK", "INDF.JK", "INKP.JK", "INTP.JK", "ITMG.JK", "KLBF.JK", "MAPI.JK", 
                    "MBMA.JK", "MDKA.JK", "MEDC.JK", "MTEL.JK", "PGAS.JK", "PGEO.JK", "PTBA.JK", "PTMP.JK", "SIDO.JK", "SMGR.JK", 
                    "SRTG.JK", "TLKM.JK", "TOWR.JK", "UNTR.JK", "UNVR.JK", "HMSP.JK", "PTBA.JK", "HUMI.JK"]

    merged_file_name = st.text_input("Input File Name : ")
    start_date = st.date_input("Start Date", value=pd.to_datetime('2024-01-01'))
    # end_date = st.date_input("End Date", value=pd.to_datetime('2024-06-12'))
    interval = st.selectbox("Interval", ["10m", '30m', '1h', "1d", "1wk", "1mo"])
    volume_threshold = st.number_input("Volume Threshold", min_value=0)
    ema_period = st.number_input("EMA Period", min_value=1, value=20)  # Add input for EMA period
    all_data = pd.DataFrame()

    run_button = st.button("Analysis Stock")
    if run_button:
        for symbol in stock_symbols:
            stock_data = yf.download(symbol, start=start_date, interval=interval)
            
            if not stock_data.empty:
                stock_data['Nama Saham'] = symbol
                stock_data['Date'] = stock_data.index  # Save the original date
                all_data = pd.concat([all_data, stock_data])

        all_data['Threshold'] = volume_threshold
        average_volume_all = all_data.groupby('Nama Saham')['Volume'].transform('mean')
        all_data['Action Spike'] = 'none'
        all_data.loc[(all_data['Volume'] > volume_threshold * average_volume_all) & (all_data['Close'] > all_data['Open']), 'Action Spike'] = 'spike buy'
        all_data.loc[(all_data['Volume'] > volume_threshold * average_volume_all) & (all_data['Close'] <= all_data['Open']), 'Action Spike'] = 'spike sell'

        # Calculate Lot
        all_data['Lot'] = all_data['Volume'] // 100

        all_data_sorted = all_data.sort_values(by=['Action Spike', 'Volume'], ascending=[False, False])

        # Display Sorted Stock Data
        st.write("Sorted Stock Data:")
        st.dataframe(all_data_sorted[['Nama Saham', 'Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Lot', 'Threshold', 'Action Spike']])

        # Function to get the latest stock prices from Yahoo Finance
        def get_last_prices(symbols):
            last_prices = {}
            for symbol in symbols:
                ticker = yf.Ticker(symbol)
                data = ticker.history(period='1d')
                if not data.empty:
                    last_prices[symbol] = data['Close'].iloc[-1]
            return last_prices

        # Change to LAST data
        today_date = pd.to_datetime('2024-06-12')  # Change to the current date
        previous_day = today_date - pd.Timedelta(days=1)

        # Find valid closing data from the previous day
        while previous_day >= start_date:
            previous_day_data = all_data[all_data.index.date == previous_day.date()]
            if not previous_day_data.empty:
                break
            previous_day -= pd.Timedelta(days=1)

        # Check if previous day's data is available
        if previous_day_data.empty:
            st.warning(f"No valid data before {today_date.date()}")
        else:
            # Get the latest stock prices from Yahoo Finance
            symbols = previous_day_data['Nama Saham'].unique()
            last_prices = get_last_prices(symbols)

            # Merge previous day's closing prices with result_data
            result_data = all_data_sorted[all_data_sorted['Action Spike'].isin(['spike buy', 'spike sell'])].copy()
            result_data = result_data.merge(previous_day_data[['Nama Saham', 'Close']], on='Nama Saham', how='left', suffixes=('', ' Today'))
            
            # Replace 'Close Today' with the latest stock prices from Yahoo Finance
            result_data['Last Price'] = result_data['Nama Saham'].map(last_prices)

            result_data['Price Spike'] = result_data['Close']
            result_data['Selisih'] = result_data['Last Price'] - result_data['Close']
            result_data['Presentasi'] = (result_data['Selisih'] / result_data['Close']) * 100
            result_data['Presentasi'] = result_data['Presentasi'].map("{:.2f}%".format)
            result_data['Selisih Hari'] = (today_date - pd.to_datetime(result_data['Date'])).dt.days

            # Display Filtered Spike Data
            st.write("Filtered Spike Data:")
            st.dataframe(result_data[['Date', 'Nama Saham', 'Threshold', 'Volume', 'Lot', 'Action Spike', 'Price Spike', 'Last Price', 'Selisih', 'Presentasi', 'Selisih Hari']])
        
            # if st.button("Download Data"): 
            #     output_folder = "dataHasilVolumeSpike"
            #     os.makedirs(output_folder, exist_ok=True)
            #     output_file_path = os.path.join(output_folder, f"{merged_file_name}.xlsx")
            #     result_data.to_excel(output_file_path, index=False)

            #     st.success(f"Download Data Volume Spike berhasil!") 

        # Visualization
        for symbol in stock_symbols:
            st.write(f"## {symbol}")
            stock_data = all_data[all_data['Nama Saham'] == symbol]
            if not stock_data.empty:
                volumeSpike.plot_stock_interactive_data(stock_data, symbol, volume_threshold, ema_period)

elif selected == 'Layout':
    st.image('img/bions.png', width=150)
    jk = '.JK'
    stock_symbols_input = st.text_input("Enter Stock Symbols :", value="")
    stock_symbols_input = stock_symbols_input + jk
    stock_symbols = [symbol.strip() for symbol in stock_symbols_input.split(',')]
    start_date = st.date_input("Start Date :", value=pd.to_datetime('2024-01-01'))
    interval = st.selectbox("Interval :", ["10m", '30m', '1h', "1d", "1wk", "1mo"])
    
    volume_thresholds = []
    for i in range(1, 5):
        default_value = i  # Nilai default sesuai dengan nomor urut
        threshold = st.number_input(f"Volume Threshold {i}:", min_value=0, value=default_value, key=f"threshold_{i}", format="%d", help=f"Enter volume threshold {i}")
        if threshold > 0:
            volume_thresholds.append(threshold)
    
    all_data = pd.DataFrame()

    run_button = st.button("Analysis Stock")

    if run_button:
        # Function to get the latest stock prices from Yahoo Finance
        def get_last_prices(symbols):
            last_prices = {}
            price_changes = {}
            for symbol in symbols:
                ticker = yf.Ticker(symbol)
                data = ticker.history(period='2d')  # Fetching data for the last two days
                if len(data) >= 2:
                    last_price = data['Close'].iloc[-1]
                    previous_price = data['Close'].iloc[-2]
                    change_percent = ((last_price - previous_price) / previous_price) * 100
                    last_prices[symbol] = last_price
                    price_changes[symbol] = change_percent
            return last_prices, price_changes

        # Add the subheader for current stock prices
        st.subheader("Current Stock Prices:")
        last_prices, price_changes = get_last_prices(stock_symbols)
        for symbol in stock_symbols:
            if symbol in last_prices:
                price = last_prices[symbol]
                change_percent = price_changes[symbol]
                color = "green" if change_percent > 0 else "red"
                st.markdown(f"**{symbol}**: {price:.2f} <span style='color:{color}'>({change_percent:.2f}%)</span>", unsafe_allow_html=True)

        st.write("")
        col1, col2, col3, col4, col5 = st.columns(5)

        for col, price_type in zip([col1, col2, col3, col4, col5], ['Open', 'High', 'Low', 'Close', 'Volume']):
            with col:
                stock_data = yf.download(stock_symbols, start=start_date, interval=interval)
                last_price = stock_data[price_type].tail(1).values[0]
                st.markdown(
                    f"<div style='border: 1px solid; padding: 10px; margin-bottom: 10px; border-radius: 10px;'>"
                    f"<p style='color: white;'>{price_type} Price : {last_price}</p>"
                    "</div>",
                    unsafe_allow_html=True
                )
        for symbol in stock_symbols:
            stock_data = yf.download(symbol, start=start_date, interval=interval)
            
            if not stock_data.empty:
                stock_data['Nama Saham'] = symbol
                stock_data['Date'] = stock_data.index
                all_data = pd.concat([all_data, stock_data])

        st.write("")
        st.subheader("Stock Data :")
        all_data['Threshold'] = volume_thresholds[0] if volume_thresholds else 0  # Use the first threshold as a default
        average_volume_all = all_data.groupby('Nama Saham')['Volume'].transform('mean')
        all_data['Action Spike'] = 'none'
        for threshold in volume_thresholds:
            all_data.loc[(all_data['Volume'] > threshold * average_volume_all) & (all_data['Close'] > all_data['Open']), 'Action Spike'] = 'spike buy'
            all_data.loc[(all_data['Volume'] > threshold * average_volume_all) & (all_data['Close'] <= all_data['Open']), 'Action Spike'] = 'spike sell'

        # Calculate Lot
        all_data['Lot'] = all_data['Volume'] // 100

        all_data_sorted = all_data.sort_values(by=['Action Spike', 'Volume'], ascending=[False, False])
        st.dataframe(all_data_sorted[['Nama Saham', 'Open', 'High', 'Low', 'Close', 'Volume']])

        # Function to get the latest stock prices from Yahoo Finance
        def get_last_prices(symbols):
            last_prices = {}
            for symbol in symbols:
                ticker = yf.Ticker(symbol)
                data = ticker.history(period='1d')
                if not data.empty:
                    last_prices[symbol] = data['Close'].iloc[-1]
            return last_prices

        # Replace with LAST data
        today_date = pd.to_datetime('2024-06-12').tz_localize(None)  # Replace with the current date and make timezone-naive
        previous_day = today_date - pd.Timedelta(days=1)

        # Find valid closing data from the previous day
        while previous_day >= pd.Timestamp(start_date):
            previous_day_data = all_data[all_data.index.date == previous_day.date()]
            if not previous_day_data.empty:
                break
            previous_day -= pd.Timedelta(days=1)

        # Check if previous day's data is available
        if previous_day_data.empty:
            st.warning(f"No valid data before {today_date.date()}")
        else:
            # Get the latest stock prices from Yahoo Finance
            symbols = previous_day_data['Nama Saham'].unique()
            last_prices = get_last_prices(symbols)

            # Merge previous day's closing prices with result_data
            result_data = all_data_sorted[all_data_sorted['Action Spike'].isin(['spike buy', 'spike sell'])].copy()
            result_data = result_data.merge(previous_day_data[['Nama Saham', 'Close']], on='Nama Saham', how='left', suffixes=('', ' Today'))
            
            # Replace 'Close Today' with the latest stock prices from Yahoo Finance
            result_data['Last Price'] = result_data['Nama Saham'].map(last_prices)

            # Convert 'Date' column to timezone-naive
            result_data['Date'] = pd.to_datetime(result_data['Date']).dt.tz_localize(None)

            # Calculate the difference and percentage change
            result_data['Price Spike'] = result_data['Close']
            result_data['Selisih'] = result_data['Last Price'] - result_data['Close']
            result_data['Presentasi'] = (result_data['Selisih'] / result_data['Close']) * 100
            result_data['Presentasi'] = result_data['Presentasi'].map("{:.2f}%".format)
            result_data['Selisih Hari'] = (today_date - result_data['Date']).dt.days

            st.subheader("Filtered Spike Data:")
            st.dataframe(result_data[['Date', 'Nama Saham', 'Threshold', 'Volume', 'Lot', 'Action Spike', 'Price Spike', 'Last Price', 'Selisih', 'Presentasi', 'Selisih Hari']])

        st.write("")
        st.subheader("Visualization :")
        for symbol in stock_symbols:
            st.write(f"## {symbol}", width=200)  # Adjust the width of the visualization
            stock_data = yf.download(symbol, start=start_date, interval=interval)
            
            if not stock_data.empty:
                stock_data['Nama Saham'] = symbol
                stock_data['Date'] = stock_data.index  # Save the original date
                for threshold in volume_thresholds:
                    showData.plot_stock_interactive(stock_data, symbol, threshold)
                all_data = pd.concat([all_data, stock_data])

elif selected == "Screener":
    st.image('img/bions.png', width=150)
    screen_name = st.text_input("Screen Name :")
    description = st.text_area("Description :")
    stock_universe = st.selectbox("Stock Universe", ("IHSG", "LQ45", "Syariah"))
    st.subheader("Screening Rules :")

    # Adding screening rule inputs in one column
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        feature = st.selectbox("Select Feature", ("", "previousClose", "volume"))
    if feature:
        with col2:
            operator = st.selectbox("Select Operator", (">", "<", ">=", "<=", "=", "between"))
        with col3:
            value1 = st.number_input("Value 1", min_value=0)
            value2 = None
            if operator == 'between':
                value2 = st.number_input("Value 2", min_value=0)

    run_button = st.button("Screener")
    if run_button:
        if stock_universe:
            stocks = screener.fetch_stocks(stock_universe)
            if feature:
                filtered_stocks = screener.apply_filter(stocks, feature, operator, value1, value2)
                if filtered_stocks:
                    st.write(f"List of stocks in {stock_universe} universe with {feature} {operator} {value1} {('and ' + str(value2)) if value2 else ''}:")
                    
                    # Create a dataframe from filtered stocks
                    data = []
                    for ticker, info in filtered_stocks.items():
                        stock_data = {
                            'Symbol': ticker,
                            'Close Price': info.get('previousClose', 'N/A')
                        }
                        if feature == 'volume':
                            stock_data['Volume'] = info.get('volume', 'N/A')
                        data.append(stock_data)
                    df = pd.DataFrame(data)
                    
                    # Display the dataframe in Streamlit
                    st.dataframe(df)
                else:
                    st.write(f"No stocks found in {stock_universe} universe with {feature} {operator} {value1} {('and ' + str(value2)) if value2 else ''}.")
            else:
                st.write("Please select a feature to filter by.")
        else:
            st.write("Please select a stock universe.")