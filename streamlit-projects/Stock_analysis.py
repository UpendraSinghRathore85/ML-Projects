import streamlit as st
import yfinance as yf
import pandas as pd

# Streamlit app title
st.title("Tata Steel Stock Analysis")

# Input fields for start date, end date
start_date = st.date_input("Start Date")
end_date = st.date_input("End Date")

# create a fetch function and return the data , pass ticker as parameter
# Function to fetch stock data
def fetch_stock_data(ticker, start, end):
    try:
        # Fetch data from Yahoo Finance
        stock_data = yf.download(ticker, start=start, end=end)
        return stock_data
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None


# Fetch stock data for Tata Steel
if st.button("Fetch Data"):
    if start_date and end_date:
        try:
            # Ticker symbol for Tata Steel
            ticker = "TATASTEEL.NS"
            
            stock_data = fetch_stock_data(ticker, start=start_date, end=end_date)

            if not stock_data.empty:
                st.success("Data fetched successfully!")
                st.write("Stock Data:")
                st.dataframe(stock_data)

                # Plotting the closing price
                st.line_chart(stock_data['Close'], use_container_width=True)
            else:
                st.warning("No data found for the given date range.")
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please select both start and end dates.")
