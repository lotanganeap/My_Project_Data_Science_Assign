#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Define a Function that Makes a Graph
#Perform the following operations:
#Use yfinance to Extract Stock Data
#Use Webscraping to Extract Tesla Revenue Data
#Use yfinance to Extract Stock Data
#Use Webscraping to Extract GME Revenue Data
#Plot Tesla Stock Graph
#Plot GameStop Stock Graph


# In[2]:


import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# In[3]:


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


# In[4]:


tesla = yf.Ticker('TSLA')


# In[5]:


tesla_data = tesla.history(period="max")


# In[6]:


tesla_data.reset_index(inplace=True)
tesla_data.head(5)


# In[7]:


url = "https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue"
html_data = requests.get(url).text


# In[8]:


soup = BeautifulSoup(html_data, "html5lib")
print(soup.prettify())


# In[13]:


tesla_revenue = pd.DataFrame(columns = ["Date","Revenue"])

for table in soup.find_all('table'):
    if table.find('th').getText().startswith("Tesla Quarterly Revenue"):
        for row in table.find("tbody").find_all("tr"):
            col = row.find_all("td")
            if len(col) != 2: continue
            Date = col[0].text
            Revenue = col[1].text.replace("$","").replace(",","")
               
            tesla_revenue = tesla_revenue.append({"Date":Date, "Revenue":Revenue}, ignore_index=True)


# In[14]:


tesla_revenue.dropna(axis=0, how='all', subset=['Revenue']) #drop NaN values
tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""] #drop empty string values


# In[15]:


tesla_revenue.tail(5)


# In[16]:


gme = yf.Ticker('GME')


# In[17]:


gme_data = gme.history(period = "max")


# In[18]:


gme_data.reset_index(inplace=True)
gme_data.head(5)


# In[19]:


url = "https://www.macrotrends.net/stocks/charts/GME/gamestop/revenue"
html_data = requests.get(url).text


# In[20]:


soup = BeautifulSoup(html_data, "html5lib")
print(soup.prettify())


# In[21]:


gme_revenue = pd.DataFrame(columns = ["Date","Revenue"])

for table in soup.find_all('table'):
    if table.find('th').getText().startswith("GameStop Quarterly Revenue"):
        for row in table.find("tbody").find_all("tr"):
            col = row.find_all("td")
            if len(col) != 2: continue
            Date = col[0].text
            Revenue = col[1].text.replace("$","").replace(",","")
               
            gme_revenue = gme_revenue.append({"Date":Date, "Revenue":Revenue}, ignore_index=True)


# In[22]:


gme_revenue.tail(5)


# In[23]:


make_graph(tesla_data, tesla_revenue, 'Tesla')


# In[24]:


make_graph(gme_data, gme_revenue, 'GameStop')


# In[ ]:




