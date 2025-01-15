import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

st.set_page_config(page_title="Indian Gold Rate Tracker", layout="wide")

def fetch_gold_data():
    gold = yf.Ticker('GC=F')
    data = gold.history(period="max")
    return data['Close']

def calculate_purity_prices(base_price_per_10g):
    return {
        '24K': base_price_per_10g,
        '22K': base_price_per_10g * 0.916,
        '18K': base_price_per_10g * 0.750,
        '14K': base_price_per_10g * 0.585
    }

def convert_to_indian_rate(usd_price):
    usd_inr_rate = 86.55
    troy_ounce_to_grams = 31.1035
    base_price = (usd_price * usd_inr_rate / troy_ounce_to_grams)
    making_charges = 0.08 
    return base_price * (1 + making_charges) * 10

st.title("🏆 Indian Gold Rate Tracker")

st.info("""
### Understanding Gold Rates
- **Basic Gold Rate**: This is the pure gold rate based on international market prices converted to INR
- **24K Gold**: 99.9% pure gold, highest purity available
- **22K Gold**: 91.6% pure gold, commonly used for jewelry
- **18K Gold**: 75% pure gold, mixed with other metals
- **14K Gold**: 58.5% pure gold, most affordable option

All prices shown include making charges of 8%. Note that actual jewelry prices may vary based on:
- Design complexity
- Additional stones or materials
- Local market conditions
- Jeweler's policies
""")

gold_data = fetch_gold_data()
current_price_usd = gold_data[-1]
current_price_inr_10g = convert_to_indian_rate(current_price_usd)

tabs = st.tabs(["Current Rates", "Historical Analysis", "Price Comparison"])

with tabs[0]:
    st.subheader("Current Gold Rates (per 10 grams)")
    col1, col2, col3, col4 = st.columns(4)
    purity_prices = calculate_purity_prices(current_price_inr_10g)
    
    for purity, price in purity_prices.items():
        with locals()[f"col{list(purity_prices.keys()).index(purity) + 1}"]:
            prev_price = calculate_purity_prices(convert_to_indian_rate(gold_data[-2] if len(gold_data) > 1 else gold_data[-1]))[purity]
            price_change = ((price - prev_price) / prev_price) * 100
            st.metric(
                f"{purity}",
                f"₹{price:,.2f}",
                f"{price_change:.2f}%"
            )

    st.markdown("---")
    st.subheader("Gold Rates per Gram")
    for purity, price in purity_prices.items():
        st.write(f"{purity}: ₹{price/10:,.2f}/g")

with tabs[1]:
    period_options = {
        "Last Week": 7,
        "Last Month": 30,
        "Last Year": 365
    }
    period_selection = st.selectbox("Select Time Period", list(period_options.keys()))
    days = min(period_options[period_selection], len(gold_data))
    
    historical_data = gold_data[-days:]
    historical_df = pd.DataFrame(historical_data).reset_index()
    historical_df.columns = ['Date', 'Price']
    historical_df['Price_INR'] = historical_df['Price'].apply(lambda x: convert_to_indian_rate(x))
    
    fig = px.line(historical_df, x='Date', y='Price_INR', 
                  title=f'Gold Price Trend - {period_selection}',
                  labels={'Price_INR': 'Price (₹/10g)', 'Date': ''})
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

with tabs[2]:
    col1, col2 = st.columns(2)
    with col1:
        comparison_df = pd.DataFrame([
            {'Purity': k, 'Price': v} 
            for k, v in purity_prices.items()
        ])
        fig = px.bar(comparison_df, x='Purity', y='Price',
                    title='Current Prices by Purity (per 10g)',
                    labels={'Price': 'Price (₹/10g)'})
        st.plotly_chart(fig)
    
    with col2:
        timeframes = {
            'Last Week': min(7, len(gold_data)),
            'Last Month': min(30, len(gold_data)),
            'Last Year': min(365, len(gold_data))
        }
        price_changes = {}
        for timeframe, days in timeframes.items():
            if days > 0:
                old_price = convert_to_indian_rate(gold_data[-days])
                change = ((current_price_inr_10g - old_price) / old_price * 100)
                price_changes[timeframe] = change
            
        if price_changes:
            changes_df = pd.DataFrame([
                {'Period': k, 'Change %': v} 
                for k, v in price_changes.items()
            ])
            fig = px.bar(changes_df, x='Period', y='Change %',
                        title='Price Changes Over Time',
                        color='Change %',
                        color_continuous_scale='RdYlGn')
            st.plotly_chart(fig)

st.sidebar.title("About")
st.sidebar.info("""
This tracker shows current gold rates in India.
Prices include:
- International market gold rate
- Making charges (8%)
Current USD-INR Rate: ₹86.55

Basic gold price is calculated from:
1. International gold price (USD/oz)
2. Converted to INR using current exchange rate
3. Converted from troy ounce to grams
4. Adding making charges
""")

if st.sidebar.button("Refresh Data"):
    st.rerun()