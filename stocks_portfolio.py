# importing libraries
import pandas as pd
import streamlit as st
import yfinance as yf

# creating functions to load the data
# prices MXRF11, BBAS3, VALE3, PETR4, WEGE3

@st.cache_data
def load_data(companies):
    tickers_text = " ".join(companies)
    stock_data = yf.Tickers(tickers_text)
    stock_price = stock_data.history(period="1d", start= "2010-01-01", end= "2024-07-01")
    stock_price = stock_price["Close"]
    return stock_price

list_ = ["MXRF11.SA", "BBAS3.SA", "VALE3.SA", "PETR4.SA", "WEGE3.SA", "CEMIG3.SA", "ITUB4.SA", "ABEV3.SA", "BBDC4.SA"]
data = load_data(list_)
print(data)

# creating the streamlit interface
st.write("""
# Stock Portfolio
#### The graphs below depicts the stock portfolio price variation
""")


# preparing the visualization
stock_list = st.multiselect("Choose the stocks", data.columns)

#Filtering and solving the bug for choosing only one stock
if stock_list:
    data = data[stock_list]
    if len(stock_list) == 1:
        unique_stock = stock_list[0]
        data = data.rename(columns = {unique_stock: "Close"})


#Depicting the graph

st.line_chart(data)



st.write(""" ##### This portfolio is totally customizable. Check our options in https://micheldiegocomex.wixsite.com/data-analysis-port-1""")
