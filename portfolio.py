# Importing libraries
import pandas as pd
import streamlit as st
from datetime import timedelta
import yfinance as yf
import plotly.express as px



# Function to load data
@st.cache_data
def load_data(companies):
    tickers_text = " ".join(companies)
    stock_data = yf.Tickers(tickers_text)

    # Carrega todos os dados históricos desejados
    stock_price = stock_data.history(period="1d", start="2010-01-01", end="2024-08-01")

    # Seleciona apenas as colunas de interesse
    stock_price = stock_price[["Close", "Open", "Dividends"]]

    return stock_price


# Lista de empresas
list_ = [
    "BBAS3.SA", "VALE3.SA", "PETR4.SA", "WEGE3.SA", "CMIG3.SA", "ITUB4.SA",
    "ABEV3.SA", "BBDC4.SA", "LEVE3.SA", "BBSE3.SA", "AGRO3.SA", "KLBN11.SA",
    "BRAP3.SA", "HCTR11.SA", "BRCO11.SA",  "CASH3.SA", "ITUB3.SA", "PETR3.SA",
    "KNCA11.SA", "SPTW11.SA", "RZAK11.SA", "TORD11.SA", "GGBR4.SA", "CPFE3.SA",
    "ASAI3.SA", "RENT3.SA", "SBSP3.SA", "SUZB3.SA", "EGIE3.SA", "EQTL3.SA",
    "CGAS3.SA", "CGAS5.SA", "VGHF11.SA", "XPCA11.SA", "ARRI11.SA", "HCTR11.SA",
    "URPR11.SA", "MXRF11.SA", "PLRI11.SA", "RECR11.SA", "KNCR11.SA", "RZTR11.SA",
    "HABT11.SA", "VGHF11.SA", "SPTW11.SA"
]

# Carregando os dados
data = load_data(list_)
my_stock = pd.read_excel("investments.xlsx", sheet_name = 'operations')
my_stock['ticker'] = [ticker + ".SA" for ticker in my_stock['ticker']]
my_stock['date'] = pd.to_datetime(my_stock['date'])
df = data["Close"]

prices = data["Close"].iloc[-1]
port_list = my_stock['ticker'].to_list()
date_to_list = my_stock['date'].to_list()
unique_list = list(set(port_list))


k = []
for i, item in enumerate(port_list):
    if item in prices:
        k.append({'ticker': item, 'current_price': prices[item]}) #For using data from 2 dataframes, it is possible turn it on a list and using enumerate to merge the data.

k = pd.DataFrame(k)
my_stock['current_price'] = my_stock['current_price'].fillna(k['current_price'])
my_stock['variation'] = my_stock['current_price'] - my_stock['buy_price']
my_stock['variation_amount'] = (my_stock['current_price'] - my_stock['buy_price']) * my_stock['qty']
my_stock['variation(%)'] = (my_stock['current_price'] - my_stock['buy_price']) / my_stock['buy_price'] * 100
my_stock['amount(current_price'] = my_stock['current_price'] * my_stock['qty']

my_stock


total_investido = my_stock['amount (cost)'].sum()
valor_atual_carteira = my_stock['amount(current_price'].sum()
variacao = my_stock['variation_amount'].sum()

retorno_ponderado = (my_stock['amount (cost)'] * ((my_stock['current_price'] - my_stock['buy_price']) / my_stock['buy_price'])).sum() / my_stock['amount (cost)'].sum()

st.write(f'Total investido: {total_investido:.2f}')
st.write(f'Valor atual da carteira: {valor_atual_carteira:.2f}')
st.write(f'Variacao: {variacao:.2f}')
st.write(f'Retorno ponderado: {retorno_ponderado:.2%}')

prices_total = data["Close"][unique_list].astype(float)
prices_total = prices_total[prices_total.index >= my_stock['date'].min()]

#st.line_chart(prices_total)


figg = px.line(prices_total, x=prices_total.index, y=prices_total.columns)
figg.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1M", step="month", stepmode="backward"),
            dict(count=6, label="6M", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1Y", step="year", stepmode="backward"),
            dict(step="all")
        ])
    )
)
st.plotly_chart(figg)
#############################################################################################

fig = px.line(data["Close"], x=data["Close"].index, y=data["Close"].columns, range_x=['2016-09-26','2024-08-20'])
fig.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1M", step="month", stepmode="backward"),
            dict(count=6, label="6M", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1Y", step="year", stepmode="backward"),
            dict(step="all")
        ])
    )
)
st.plotly_chart(fig)


# Agora você tem acesso às colunas 'Close', 'Open' e 'Dividends' em um único DataFrame
print(data.head())

# creating the streamlit interface
st.write("""
# Stock Portfolio
#### The graph below depicts the stock portfolio price variation
""")

# side menu bar

initial_date = data.index.min().to_pydatetime()
final_date = data.index.max().to_pydatetime()



lista_fii = ["HCTR11.SA", "BRCO11.SA",  "HABT11.SA", "KNCA11.SA", "SPTW11.SA", "RZAK11.SA", "TORD11.SA",
             "VGHF11.SA",
             "XPCA11.SA", "ARRI11.SA", "URPR11.SA", "MXRF11.SA", "PLRI11.SA", "RECR11.SA", "KNCR11.SA", "RZTR11.SA","VGHF11.SA", "SPTW11.SA"]
# filtering data by fii

# lista_fii = [x + ".SA" for x in lista_fii] #Adding '.SA' for each element

list_stocks = ["BBAS3.SA", "VALE3.SA", "PETR4.SA",
               "WEGE3.SA", "CMIG3.SA", "ITUB4.SA", "ABEV3.SA", "BBDC4.SA", "CGAS5.SA", "CASH3.SA", "ITUB3.SA",
               "BRAP3.SA", "CPFE3.SA", "ASAI3.SA", "RENT3.SA", "SBSP3.SA", "CGAS3.SA", "SUZB3.SA", "EGIE3.SA",
               "EQTL3.SA",
               "LEVE3.SA", "BBSE3.SA", "AGRO3.SA", "KLBN11.SA", "GGBR4.SA"]  # filtering stocks



# category selectbox

category = st.sidebar.selectbox("Category", ("REITs", "Stocks"), index=None, placeholder="Select an asset")
status = st.sidebar.selectbox("Status", ("Close", "Dividends"), index=None, placeholder="Select a type")


if category == "REITs": #logical to setup reits as selected
    data_reit = data["Close"][lista_fii].astype(float)
if category == "REITs" and status == "Close":
    data_reit = data["Close"][lista_fii].astype(float)
if category == "REITs" and status == "Dividends":
    data_reit = data["Dividends"][lista_fii].astype(float)
    fii = st.sidebar.multiselect("REITs Option Selected", lista_fii, placeholder="Select the REITs")
    if fii:
        data_reit = data_reit[fii]  # filtering columns (stock list)
        if len(fii) == 1:
            unique = fii[0]
            data_reit = data_reit.rename(columns={unique: "Close"})
        else:
            data_reit = data_reit[fii]


elif category == "Stocks": #logical to setup stocks as selected
    data_stock = data["Close"][list_stocks].astype(float)
if category == "Stocks" and status == "Close":
    data_stock = data["Close"][list_stocks].astype(float)
if category == "Stocks" and status == "Dividends":
    data_stock = data["Dividends"][list_stocks].astype(float)
    stock = st.sidebar.multiselect("Stock Option Selected", list_stocks, placeholder="Select the stocks")
    if stock:
        data_stock = data_stock[stock]  # filtering columns (stock list)
        if len(stock) == 1:
            unique = stock[0]
            data_stock = data_stock.rename(columns={unique: "Close"})
        else:
            data_stock = data_stock[stock]


if category not in ["REITs", "Stocks"]:
    data = data["Close"].loc[:, ["BBAS3.SA", "ITUB4.SA"]]
if category == "REITs":
    data = data_reit
if category == "Stocks":
    data = data_stock


interval_date = st.sidebar.slider("Select the period",
                                  min_value=initial_date,
                                  max_value=final_date,
                                  value=(initial_date, final_date),
                                  step=timedelta(days=1))

data = data.loc[interval_date[0]: interval_date[1]]  # filtering dataset rows



full_list = st.sidebar.multiselect("Full list", data.columns)

if full_list:
    data = data[full_list]  # filtering columns (stock list)
    if len(full_list) == 1:
        unique = full_list[0]
        data = data.rename(columns={unique: "Close"})
    else:
        data = data[full_list]

# Depicting the graph

# st.line_chart(data, x_label="Date", y_label= "Price")

import plotly.express as px

fig = px.line(data, x=data.index, y=data.columns, range_x=['2010-09-26','2024-08-20'], title= "Stocks Portfolio", labels={"value": "Price"},height=600, width= 1200)
fig.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1M", step="month", stepmode="backward"),
            dict(count=6, label="6M", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1Y", step="year", stepmode="backward"),
            dict(step="all")
        ])
    )
)
fig.update_layout(font_family="Calibri", font_color = "lightblue", legend_title_font_color = "lightblue", legend_title_font_size=12, font_size=16)
st.plotly_chart(fig)





performance_asset_text = ""

# if len(data) == 0:
#     data = list(data.columns)
# elif len(data) == 1:
#     data = data.rename(columns={"Close": unique})

# if category == "REITs" and len(fii) == 1:
#     data = data.rename(columns={"Close": unique})
# elif category == "Stocks" and len(stock) == 1:
#     data = data.rename(columns={"Close": unique})

# performance_asset = [data[asset].iloc[-1] / data[asset].iloc[0] - 1 for asset in stock_list]
# performance_asset = [float(x) for x in performance_asset]


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

# Text portfolio performance

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

# if 'clicked' not in st.session_state:
#     st.session_state.clicked = False
#
# def click_button():
#     st.session_state.clicked = True
#
# st.button('Click me', on_click=click_button)
#
# if st.session_state.clicked:
#     # The message and nested widget will remain on the page
#     st.write('Button clicked!')
#     st.slider('Select a value')


# if 'button' not in st.session_state:
#     st.session_state.button = False
#
# def click_button():
#     st.session_state.button = not st.session_state.button
#
# st.button('Click me', on_click=click_button)
#
# if st.session_state.button:
#     # The message and nested widget will remain on the page
#     st.write('Button is on!')
#     st.slider('Select a value')
# else:
#     st.write('Button is off!')


# if 'stage' not in st.session_state:
#     st.session_state.stage = 0
#
# def set_state(i):
#     st.session_state.stage = i
#
# if st.session_state.stage == 0:
#     st.button('Begin', on_click=set_state, args=[1])
#
# if st.session_state.stage >= 1:
#     name = st.text_input('Name', on_change=set_state, args=[2])
#
# if st.session_state.stage >= 2:
#     st.write(f'Hello {name}!')
#     color = st.selectbox(
#         'Pick a Color',
#         [None, 'red', 'orange', 'green', 'blue', 'violet'],
#         on_change=set_state, args=[3]
#     )
#     if color is None:
#         set_state(2)
#
# if st.session_state.stage >= 3:
#     st.write(f':{color}[Thank you!]')
#     st.button('Start Over', on_click=set_state, args=[0])

# RADIO BUTTON


type_asset = st.sidebar.radio(
    "Please choose one option",
    [":blue[Price]", ":green[Dividends]"]

)



# @st.cache_data
# def bov_dataf(bovespa):
#     bov_data = yf.Tickers("^BVSP")
#
#     # Carrega todos os dados históricos desejados
#     bov_price = bov_data.history(period="1d", start="2010-01-01", end="2024-08-01")
#
#     # Seleciona apenas as colunas de interesse
#     bov_price = bov_price["Close"]
#
#     return bov_price
#
# ind_bovespa = bov_dataf("^BVSP")

hasClicked, res = st.columns(2)

from streamlit_card import card

hasClicked = card(
  title="Total amount",
  text=valor_atual_carteira,
  image="http://placekitten.com/200/300",
  on_click=lambda: print("Clicked!")
)

from streamlit_card import card

res = card(
    title="Portfolio variation",
    text=["35%", "This is a subtext"],
    image="https://placekitten.com/500/500",
)


from streamlit_card import card

res = card(
    title="Streamlit Card",
    text="This is a test card",
    image="https://placekitten.com/500/500",
    styles={
        "card": {
            "width": "500px",
            "height": "500px",
            "border-radius": "60px",
            "box-shadow": "0 0 10px rgba(0,0,0,0.5)",

        },
        "text": {
            "font-family": "serif",

        }
    }
)

# import plotly.graph_objects as go
#
# fig = go.Figure(go.Waterfall(
#     name = "20", orientation = "v",
#     measure = ["relative", "relative", "total", "relative", "relative", "total"],
#     x = ["Sales", "Consulting", "Net revenue", "Purchases", "Other expenses", "Profit before tax"],
#     textposition = "outside",
#     text = ["+60", "+80", "", "-40", "-20", "Total"],
#     y = [60, 80, 0, -40, -20, 0],
#     connector = {"line":{"color":"rgb(63, 63, 63)"}},
# ))
#
# fig.update_layout(
#         title = "Profit and loss statement 2018",
#         showlegend = True
# )
#
# fig.show()