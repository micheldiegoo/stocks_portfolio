# importing libraries
import pandas as pd
import streamlit as st
from datetime import timedelta
import yfinance as yf


# creating functions to load the data

@st.cache_data
def load_data(companies):
    tickers_text = " ".join(companies)
    stock_data = yf.Tickers(tickers_text)
    stock_price = stock_data.history(period="1d", start= "2010-01-01", end= "2024-08-01")
    stock_price = stock_price["Close"]
    return stock_price

# def carregar_tickers():
#     tickers_list = pd.read_csv("acoes-b3.csv", sep=';')
#     tickers_list = list(tickers_list)
#     tickers_list = [ticker + '.SA' for ticker in tickers_list]
#     return tickers_list
#
# acoes = carregar_tickers()
#data = load_data(acoes)

list_ = ["BBAS3.SA", "VALE3.SA", "PETR4.SA",
         "WEGE3.SA", "CMIG3.SA", "ITUB4.SA", "ABEV3.SA", "BBDC4.SA", "LEVE3.SA", "BBSE3.SA", "AGRO3.SA", "KLBN11.SA",
          'HCTR11.SA', 'BRCO11.SA', 'CACR11.SA', 'EQIR11.SA', 'KNCA11.SA', 'SPTW11.SA', 'RZAK11.SA', 'TORD11.SA',
         'VGHF11.SA', 'XPCA11.SA', 'ARRI11.SA', 'HCTR11.SA', 'URPR11.SA', 'MXRF11.SA', 'PLRI11.SA', 'RECR11.SA', 'KNCR11.SA', 'RZTR11.SA', 'HABT11.SA']
data = load_data(list_)

# creating the streamlit interface
st.write("""
# Stock Portfolio
#### The graphs below depicts the stock portfolio price variation
""")

# side menu bar

initial_date = data.index.min().to_pydatetime()
final_date = data.index.max().to_pydatetime()


lista_fii = ["HCTR11.SA", "BRCO11.SA", "CACR11.SA", "EQIR11.SA", "HABT11.SA", "KNCA11.SA", "SPTW11.SA", "RZAK11.SA", "TORD11.SA", "VGHF11.SA",
 "XPCA11.SA", "ARRI11.SA", "URPR11.SA", "MXRF11.SA", "PLRI11.SA", "RECR11.SA", "KNCR11.SA", "RZTR11.SA"]
 #filtering data by fii

#lista_fii = [x + ".SA" for x in lista_fii] #Adding '.SA' for each element

list_stocks = ["BBAS3.SA", "VALE3.SA", "PETR4.SA",
         "WEGE3.SA", "CMIG3.SA", "ITUB4.SA", "ABEV3.SA", "BBDC4.SA", "LEVE3.SA", "BBSE3.SA", "AGRO3.SA", "KLBN11.SA"] # filtering stocks

#category selectbox


category = st.sidebar.selectbox("Category", ("REITs", "Stocks"), index=None, placeholder="Select an asset")

if category == "REITs":
    data = data[lista_fii].astype(float)
    fii = st.sidebar.multiselect("REITs Option Selected",lista_fii, placeholder="Select the REITs")
    if fii:
        data = data[fii]  # filtering columns (stock list)
        if len(fii) == 1:
            unique = fii[0]
            data = data.rename(columns={unique: "Close"})
        else:
            data = data[fii]
    #data = data / data.iloc[0]

elif category == "Stocks":
    data = data[list_stocks].astype(float)
    stock = st.sidebar.multiselect("Stock Option Selected",list_stocks, placeholder="Select the stocks")
    if stock:
        data = data[stock]  # filtering columns (stock list)
        if len(stock) == 1:
            unique = stock[0]
            data = data.rename(columns={unique: "Close"})
        else:
            data = data[stock]
#data = data / data.iloc[0]  # normalising data

interval_date = st.sidebar.slider("Select the period",
                          min_value= initial_date,
                          max_value= final_date,
                          value= (initial_date,final_date),
                          step=timedelta(days=1))

data = data.loc[interval_date[0] : interval_date[1]] #filtering dataset rows


if category not in ["REITs", "Stocks"]:
    data = data.loc[:, ["BBAS3.SA" , "AGRO3.SA"]]



full_list = st.sidebar.multiselect("Full list", data.columns)

if full_list:
    data = data[full_list]  # filtering columns (stock list)
    if len(full_list) == 1:
        unique = full_list[0]
        data = data.rename(columns={unique: "Close"})
    else:
        data = data[full_list]

#Depicting the graph

st.line_chart(data)

performance_asset_text = ""


# if len(data) == 0:
#     data = list(data.columns)
# elif len(data) == 1:
#     data = data.rename(columns={"Close": unique})

if category == "REITs" and len(fii) == 1:
    data = data.rename(columns={"Close": unique})
elif category == "Stocks" and len(stock) == 1:
    data = data.rename(columns={"Close": unique})



#performance_asset = [data[asset].iloc[-1] / data[asset].iloc[0] - 1 for asset in stock_list]
#performance_asset = [float(x) for x in performance_asset]


portfolio = [1000 for asset in data.columns]
total_initial = sum(portfolio)

for i, asset in enumerate(data.columns):
    performance_asset = (data[asset].iloc[-1] / data[asset].iloc[0]) - 1
    performance_asset = performance_asset.values[0] if isinstance(performance_asset,
                                                                        pd.Series) else performance_asset
    portfolio[i] = portfolio[i] * (1 + performance_asset)

    if performance_asset > 0:
        performance_asset_text = performance_asset_text + f"{asset}: :green[{performance_asset:.2%}]  \n"
    elif performance_asset < 0:
        performance_asset_text = performance_asset_text + f"{asset}: :red[{performance_asset:.2%}]  \n"
    else:
        performance_asset_text = performance_asset_text + f"{asset}: {performance_asset:.2%}]  \n"

total_final = sum(portfolio)

performance_portfolio = total_final / total_initial - 1

#Text portfolio performance

performance_portfolio_text = ""

if performance_portfolio > 0:
    performance_portfolio_text = performance_portfolio_text + f"Portfolio performance with all assets: :green[{performance_portfolio:.2%}]  \n"
elif performance_portfolio < 0:
    performance_portfolio_text = performance_portfolio_text + f"Portfolio performance with all assets: :red[{performance_portfolio:.2%}]  \n"
else:
    performance_portfolio_text = performance_portfolio_text + f"Portfolio performance with all assets: {performance_portfolio:.2%}]  \n"


st.write(f"""
### Performance assets
#### The performance on the selected period was:

{performance_asset_text}

{performance_portfolio_text}
""")
