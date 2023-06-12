#!/usr/bin/env python
# coding: utf-8

# In[31]:


import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# In[32]:


tsl = yf.Ticker("TSLA")


# In[33]:


tsl_share_price_data = tsl.history(period="max")


# In[34]:


tsl_share_price_data.reset_index(inplace=True)
tsl_share_price_data.head()


# In[5]:


gamestop = yf.Ticker("GME")


# In[6]:


gamestop = tsl.history(period="max")


# In[7]:


gamestop.reset_index(inplace=True)
gamestop.head()


# In[35]:


def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data.Date, infer_datetime_format=True), y=stock_data.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data.Date, infer_datetime_format=True), y=revenue_data.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
    height=900,
    title=stock,
    xaxis_rangeslider_visible=True)
    fig.show()


# In[36]:


tsl = yf.Ticker('TSLA')


# In[37]:


tsl_data = tsl.history(period="max")


# In[38]:


tsl_data.reset_index(inplace=True)
tsl_data.head(5)


# In[39]:


url = "https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue"
html_data = requests.get(url).text


# In[40]:


soup = BeautifulSoup(html_data, "html5lib")
print(soup.prettify())


# In[41]:


tsl_revenue = pd.DataFrame(columns = ["Date","Revenue"])
for table in soup.find_all('table'):
    if table.find('th').getText().startswith("Tesla Quarterly Revenue"):
        for row in table.find("tbody").find_all("tr"):
            col = row.find_all("td")
            if len(col) != 2: continue
            Date = col[0].text
            Revenue = col[1].text.replace("$","").replace(",","")
               
            tsl_revenue = tsl_revenue.append({"Date":Date, "Revenue":Revenue}, ignore_index=True)


# In[42]:


print(tsl_revenue)


# In[43]:


tsl_revenue.dropna(axis=0, how='all', subset=['Revenue']) #drop NaN values
tsl_revenue = tsl_revenue[tsl_revenue['Revenue'] != ""] #drop empty string values


# In[44]:


tsl_revenue.tail(5)


# In[30]:


make_graph(tsl_data, tsl_revenue, 'Tesla')


# In[ ]:




