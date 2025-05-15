
# building a stock market prediction app using streamlit and yfinance
# You can run this code using streamlit run StockMarketApp.py

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
from datetime import datetime, timedelta
import plotly.graph_objects as go


# title of the app
st.header("""

Building stock market prediction app  

""" )

# get the start and end date , take ticker as input and plot the clsing and vloume
# Input fields for start date, end date

# two columns for start and end date
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("Start Date", datetime.now() - timedelta(days=365))

with col2:
    end_date = st.date_input("End Date", datetime.now())



ticker = st.text_input("Ticker", "NIFTYBEES.NS")   
stock = yf.Ticker(ticker)


# Get the current stock price
stock_info = stock.info
current_price = stock_info.get('currentPrice')
st.write(f"Current stock price of {ticker}: {current_price}")

# create 4 button for daily weekly monthly and yearly
# create a button for daily, weekly, monthly and yearly in a column and add a function to fetch the data
# create a function to fetch the data

col1, col2, col3, col4 = st.columns(4)
with col1:
    daily = st.button("Daily")
with col2:
    weekly = st.button("Weekly")
with col3:
    monthly = st.button("Monthly")
with col4:
    yearly = st.button("Yearly")

# fetch period based on the button clicked
if daily:
    period = "1d"
elif weekly:
    period = "1wk"
elif monthly:
    period = "1mo"
elif yearly:
    period = "1y"
else:   
    period = "1d"

hist = stock.history(period=period, start=start_date, end=end_date)
st.line_chart(hist['Close'])

# plot the above cart as candlestick chart
fig = go.Figure(data=[go.Candlestick(x=hist.index,
                                        open=hist['Open'],
                                        high=hist['High'],
                                        low=hist['Low'],
                                        close=hist['Close'])]
)
fig.update_layout(title='Tata Steel Stock Price Chart',
                    xaxis_title='Date',
                    yaxis_title='Price (INR)',
                    xaxis_rangeslider_visible=False)
st.plotly_chart(fig)
st.write("This is a candlestick chart of Tata Steel stock price.")
# add a reset button primiary type
st.button("Reset", type="primary")
