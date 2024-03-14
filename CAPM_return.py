#importing labries

import streamlit as st 
import pandas as pd
import yfinance as yf 
import datetime
import pandas_datareader.data as web 
import datetime

st.set_page_config(page_title = "CAMP",
    page_icon ="chart_with_upward_trend",
    layout = 'wide')         

st.title("Capital Asset Pricing Model ")          

# getting input from user 

col1, col2 = st.columns([1,1])
with col1:
    stocks_list = st.multiselect("Choose 4 stocks ",('TESLA','APPL','NVIDIA','MSFT','AMZN','NVDA'),['TESLA','APPL','AMZN','NVIDIA'])
with col2:
    year = st.number_input("Number of years",1,20)

# downloading data for SP500
    
end  = datetime.date.today()    
start = datetime.date(datetime.date.today().year-year, datetime.date.today().month, datetime.date.today().day)
SP500 = web.DataReader(['sp500'],'fred',start,end)

stocks_df = pd.DataFrame()
    

for stock in stocks_list:
    data = yf.download(stock, period = f'{year}y')
    stocks_df[f'{stock}'] = data['Close']

print(stocks_df.head)

stocks_df.reset_index(inplace = True)
SP500.reset_index(inplace = True)

SP500.columns = ['Date', 'sp500']
stocks_df['Date'] = stocks_df['Date'].astype('datetime64[ns]')
stocks_df['Date'] = stocks_df['Date'].apply(lambda x:str(x)[:10])
stocks_df['Date'] = pd.to_datetime(stocks_df['Date'])
stocks_df = pd.merge(stocks_df , SP500, on ='Date', how = 'inner')

col1, col2 = st.columns([1,1])
with col1:
    st.markdown("### Dataframe head")
    st.dataframe(stocks_df.head(),use_container_width = True)
    
    with col2:
        st.markdown("### Dataframe tail")
        st.dataframe(stocks_df.tail(),use_container_width = True)


