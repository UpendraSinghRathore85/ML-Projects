import streamlit as st
import pandas as pd
import yfinance as yf
import numpy as np # Import numpy for data simulation
import plotly.graph_objects as go
from plotly.subplots import make_subplots # Import make_subplots
from datetime import date, timedelta # Import timedelta for default date calculation

# Set page config to wide layout - THIS MUST BE THE FIRST STREAMLIT COMMAND
st.set_page_config(layout="wide")

# --- Functions to Simulate Market Movers and Create Heatmaps ---
def get_simulated_market_movers(count=10):
    """Generates simulated data for top gainers and losers."""
    tickers = [f"STOCK{i:02d}.NS" for i in range(1, count * 2 + 1)]
    np.random.shuffle(tickers)
    
    gainers_data = []
    for i in range(count):
        ltp = np.random.uniform(50, 3000)
        percent_change = np.random.uniform(1.5, 15.0) # Positive change for gainers
        gainers_data.append({"Ticker": tickers[i], "LTP": ltp, "%Change": percent_change})
    
    losers_data = []
    for i in range(count):
        ltp = np.random.uniform(50, 3000)
        percent_change = np.random.uniform(-15.0, -1.5) # Negative change for losers
        losers_data.append({"Ticker": tickers[count + i], "LTP": ltp, "%Change": percent_change})
        
    gainers_df = pd.DataFrame(gainers_data).sort_values(by="%Change", ascending=False).reset_index(drop=True)
    losers_df = pd.DataFrame(losers_data).sort_values(by="%Change", ascending=True).reset_index(drop=True)
    
    return gainers_df.head(count), losers_df.head(count)

def create_market_heatmap(df, title, colorscale):
    """Creates a Plotly heatmap figure for market movers."""
    if df.empty:
        return go.Figure().update_layout(title_text=f"{title} (No Data)", height=300)

    # For heatmap, z values determine color intensity.
    # For losers, we use absolute %change for color intensity but display original negative %change.
    if 'Reds' in colorscale: # Assuming 'Reds' or similar for losers
        z_values = [df["%Change"].abs().tolist()]
    else:
        z_values = [df["%Change"].tolist()]

    fig = go.Figure(data=go.Heatmap(
        z=z_values,
        x=df["Ticker"].tolist(),
        y=['% Change'],
        text=[[f"{val:.2f}%" for val in df["%Change"]]],
        texttemplate="%{text}",
        colorscale=colorscale,
        showscale=False # Hide the color scale bar for a cleaner look
    ))
    fig.update_layout(
        title_text=title,
        height=250, # Adjust height as needed
        margin=dict(t=50, l=10, r=10, b=30),
        yaxis_visible=False # Hide the y-axis label "% Change" as it's clear
    )
    fig.update_xaxes(side="top") # Move ticker labels to the top
    return fig

# --- Display Top Gainers and Losers (Simulated) ---
st.subheader("NSE Market Movers (Simulated Data)")
st.caption("Note: The following gainers and losers data is simulated for demonstration purposes.")

gainers_df, losers_df = get_simulated_market_movers(count=10)

col1, col2 = st.columns(2)

with col1:
    fig_gainers = create_market_heatmap(gainers_df, "Top 10 Gainers", "Greens")
    st.plotly_chart(fig_gainers, use_container_width=True)

with col2:
    fig_losers = create_market_heatmap(losers_df, "Top 10 Losers", "Reds_r") # _r reverses the scale
    st.plotly_chart(fig_losers, use_container_width=True)

st.divider() # Add a visual separator

# --- Main Stock Analysis Section ---
st.title("Stocks price analysis")

# --- NIFTY 50 Tickers (as of a recent date, might need updates) ---
# It's good practice to keep this list updated or fetch it dynamically if possible.
# For simplicity, we'll use a static list here.
NIFTY_50_TICKERS = {
    "ADANIENT.NS": "Adani Enterprises Ltd.",
    "ADANIPORTS.NS": "Adani Ports and Special Economic Zone Ltd.",
    "APOLLOHOSP.NS": "Apollo Hospitals Enterprise Ltd.",
    "ASIANPAINT.NS": "Asian Paints Ltd.",
    "AXISBANK.NS": "Axis Bank Ltd.",
    "BAJAJ-AUTO.NS": "Bajaj Auto Ltd.",
    "BAJFINANCE.NS": "Bajaj Finance Ltd.",
    "BAJAJFINSV.NS": "Bajaj Finserv Ltd.",
    "BPCL.NS": "Bharat Petroleum Corporation Ltd.",
    "BHARTIARTL.NS": "Bharti Airtel Ltd.",
    "BRITANNIA.NS": "Britannia Industries Ltd.",
    "CIPLA.NS": "Cipla Ltd.",
    "COALINDIA.NS": "Coal India Ltd.",
    "DIVISLAB.NS": "Divi's Laboratories Ltd.",
    "DRREDDY.NS": "Dr. Reddy's Laboratories Ltd.",
    "EICHERMOT.NS": "Eicher Motors Ltd.",
    "GRASIM.NS": "Grasim Industries Ltd.",
    "HCLTECH.NS": "HCL Technologies Ltd.",
    "HDFCBANK.NS": "HDFC Bank Ltd.",
    "HDFCLIFE.NS": "HDFC Life Insurance Company Ltd.",
    "HEROMOTOCO.NS": "Hero MotoCorp Ltd.",
    "HINDALCO.NS": "Hindalco Industries Ltd.",
    "HINDUNILVR.NS": "Hindustan Unilever Ltd.",
    "ICICIBANK.NS": "ICICI Bank Ltd.",
    "ITC.NS": "ITC Ltd.",
    "INDUSINDBK.NS": "IndusInd Bank Ltd.",
    "INFY.NS": "Infosys Ltd.",
    "JSWSTEEL.NS": "JSW Steel Ltd.",
    "KOTAKBANK.NS": "Kotak Mahindra Bank Ltd.",
    "LTIM.NS": "LTIMindtree Ltd.",
    "LT.NS": "Larsen & Toubro Ltd.",
    "M&M.NS": "Mahindra & Mahindra Ltd.",
    "MARUTI.NS": "Maruti Suzuki India Ltd.",
    "NTPC.NS": "NTPC Ltd.",
    "NESTLEIND.NS": "Nestle India Ltd.",
    "ONGC.NS": "Oil & Natural Gas Corporation Ltd.",
    "POWERGRID.NS": "Power Grid Corporation of India Ltd.",
    "RELIANCE.NS": "Reliance Industries Ltd.",
    "SBILIFE.NS": "SBI Life Insurance Company Ltd.",
    "SBIN.NS": "State Bank of India",
    "SUNPHARMA.NS": "Sun Pharmaceutical Industries Ltd.",
    "TCS.NS": "Tata Consultancy Services Ltd.",
    "TATACONSUM.NS": "Tata Consumer Products Ltd.",
    "TATAMOTORS.NS": "Tata Motors Ltd.",
    "TATASTEEL.NS": "Tata Steel Ltd.",
    "TECHM.NS": "Tech Mahindra Ltd.",
    "TITAN.NS": "Titan Company Ltd.",
    "ULTRACEMCO.NS": "UltraTech Cement Ltd.",
    "UPL.NS": "UPL Ltd.",
    "WIPRO.NS": "Wipro Ltd."
}


# --- User Inputs in Sidebar ---
st.sidebar.header("User Input")
selected_ticker_symbol = st.sidebar.selectbox(
    "Select NIFTY 50 Stock",
    options=list(NIFTY_50_TICKERS.keys()),
    format_func=lambda x: f"{x} ({NIFTY_50_TICKERS[x]})"
)
start_date = st.sidebar.date_input("Start Date", date.today() - timedelta(days=365))
end_date = st.sidebar.date_input("End Date", date.today())

# --- Data Fetching and Display ---
# Add a button to trigger data fetching after selecting inputs
if st.sidebar.button("Get Stock Data"):
    # Use the selected_ticker_symbol from the sidebar
    st.write(f"Displaying data for {selected_ticker_symbol} ({NIFTY_50_TICKERS[selected_ticker_symbol]}) from {start_date} to {end_date}")
    
    try:
        ticker = yf.Ticker(selected_ticker_symbol)
        df = ticker.history(period="1d", start=start_date, end=end_date)

        if not df.empty:
            df['SMA44'] = df['Close'].rolling(window=44).mean()
            df['SMA100'] = df['Close'].rolling(window=100).mean()
           
            st.header("Candlestick Chart with SMAs and Volume")
            with st.container():
                # Create figure with secondary y-axis
                fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                                    vertical_spacing=0.03, subplot_titles=(f'{selected_ticker_symbol} Candlestick', 'Volume'), 
                                    row_heights=[0.7, 0.3]) # Give more height to candlestick

                # Add Candlestick trace to the first row
                fig.add_trace(go.Candlestick(x=df.index,
                                             open=df['Open'],
                                             high=df['High'],
                                             low=df['Low'],
                                             close=df['Close'],
                                             name='Candlestick'), row=1, col=1)

                # Add SMA traces to the first row
                fig.add_trace(go.Scatter(x=df.index, y=df['SMA44'], mode='lines', name='SMA 44', line=dict(color='green')), row=1, col=1)
                fig.add_trace(go.Scatter(x=df.index, y=df['SMA100'], mode='lines', name='SMA 100', line=dict(color='blue')), row=1, col=1)
              
                # Add Volume trace to the second row
                fig.add_trace(go.Bar(x=df.index, y=df['Volume'], name='Volume', marker_color='rgba(100,100,255,0.5)'), row=2, col=1)
                
                # Update layout
                fig.update_layout(
                    xaxis_rangeslider_visible=False,
                    height=800,
                    legend_title_text='Legend',
                    showlegend=True
                )
                # Specifically hide the range slider for the volume chart's x-axis as well
                fig.update_xaxes(rangeslider_visible=False, row=2, col=1)
                
                # Set y-axis titles
                fig.update_yaxes(title_text="Price", row=1, col=1)
                fig.update_yaxes(title_text="Volume", row=2, col=1)

                st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning(f"No data found for {selected_ticker_symbol} in the selected date range. Please check the ticker symbol and date range.")
    except Exception as e:
        st.error(f"An error occurred while fetching data for {selected_ticker_symbol}: {e}")
        st.info("Please ensure the ticker symbol is correct (e.g., 'MSFT' for Microsoft, 'RELIANCE.NS' for Reliance Industries on NSE).")

else:
    st.info("Select a NIFTY 50 stock, a date range, and click 'Get Stock Data' in the sidebar.")
