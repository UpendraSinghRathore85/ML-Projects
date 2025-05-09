import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd
import numpy as np

st.set_page_config(page_title="Tata Steel Stock Price", page_icon=":bar_chart:", layout="wide")

st.write(
    """
        ## Building stock price app using Streamlit and Yahoo Finance API

        This is a simple stock price app using Streamlit and Yahoo Finance API.
        The app fetches the current stock price of Tata Steel and displays it in a line chart.
        The app also provides a candlestick chart for the last 3 years of stock data.

    """
)

# Fetch Tata Steel stock data
ticker = "TATASTEEL.NS"  # Use the NSE ticker symbol for Tata Steel
tatasteel = yf.Ticker(ticker)

# Get the current stock price
stock_info = tatasteel.info
current_price = stock_info.get('currentPrice')

st.write(f"Current stock price of Tata Steel: {current_price}")

st.title("Tata Steel Stock Price Chart")
# change end dynamically to todays data
# Get historical data for the last 1 year
# Get the current date  
today = pd.to_datetime("today").normalize()
three_years_ago = today - pd.DateOffset(years=3)
hist = tatasteel.history(period="1d", start=three_years_ago, end=today)
st.line_chart(hist['Close'])

# plot the above cart as candlestick chart
import plotly.graph_objects as go
fig = go.Figure(data=[go.Candlestick(x=hist.index,
                                      open=hist['Open'],
                                      high=hist['High'],
                                      low=hist['Low'],
                                      close=hist['Close'])])    
fig.update_layout(title='Tata Steel Stock Price Chart',
                  xaxis_title='Date',
                  yaxis_title='Price (INR)',
                  xaxis_rangeslider_visible=False)      
st.plotly_chart(fig)
st.write("This is a candlestick chart of Tata Steel stock price.")

#add a reset button primiary type
st.button("Reset", type="primary")
# with candlestick chart add 42 days moving average
hist['MA_42'] = hist['Close'].rolling(window=42).mean() 
fig = go.Figure(data=[go.Candlestick(x=hist.index,
                                      open=hist['Open'],
                                      high=hist['High'],
                                      low=hist['Low'],
                                      close=hist['Close'])])
fig.add_trace(go.Scatter(x=hist.index, y=hist['MA_42'], mode='lines', name='42 Days MA'))
fig.update_layout(title='Tata Steel Stock Price Chart with 42 Days Moving Average',
                  xaxis_title='Date',
                  yaxis_title='Price (INR)',
                  xaxis_rangeslider_visible=False)  
st.plotly_chart(fig)
st.write("This is a candlestick chart of Tata Steel stock price with 42 days moving average.")

# along with 42 days moving average add 200 and 100 days moving average
hist['MA_100'] = hist['Close'].rolling(window=100).mean()
hist['MA_200'] = hist['Close'].rolling(window=200).mean()   
fig = go.Figure(data=[go.Candlestick(x=hist.index,
                                      open=hist['Open'],
                                      high=hist['High'],
                                      low=hist['Low'],
                                      close=hist['Close'])])

fig.add_trace(go.Scatter(x=hist.index, y=hist['MA_42'], mode='lines', name='42 Days MA'))
fig.add_trace(go.Scatter(x=hist.index, y=hist['MA_100'], mode='lines', name='100 Days MA')) 

fig.add_trace(go.Scatter(x=hist.index, y=hist['MA_200'], mode='lines', name='200 Days MA'))
fig.update_layout(title='Tata Steel Stock Price Chart with 42, 100 and 200 Days Moving Average',
                  xaxis_title='Date',
                  yaxis_title='Price (INR)',
                  xaxis_rangeslider_visible=False)

st.plotly_chart(fig)    
st.write("This is a candlestick chart of Tata Steel stock price with 42, 100 and 200 days moving average.")
# add a button to download the data as csv
csv = hist.to_csv() 
st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name='tatasteel_stock_data.csv',
    mime='text/csv',
)   
st.write("This is a download button to download the data as CSV.")


            