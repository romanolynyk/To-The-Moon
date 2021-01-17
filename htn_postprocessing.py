# -*- coding: utf-8 -*-
"""
Created on Sat Jan 16 15:31:38 2021

@author: jlyne
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import pandas_datareader.data as web
#import streamlit as st
import plotly.express as px

'''
# r/WallStreetBets Sentiment Analysis Overview 🚀🚀🚀🌙🌙🌙

'''

end = datetime.today()
month_ago = datetime.today() - timedelta(days = 15)

#add appropriate stocks here
stocks = ['PLTR','TSLA', 'NEO']

#read in pre-processed data
df = pd.read_csv('sentiment_PLTR.csv')
#converting back to datetime
df['date'] = pd.to_datetime(df['date'])

#get stcok data
df_stock = web.DataReader(stocks,'yahoo',month_ago,end)
df_stock = df_stock['Adj Close']

#We'll classify a comment's sentiment intensity using the 
#compound score. Remember, the compound score is somewhat of a weighted average
#of  the pos,neg, and neu terms.

df['v_upset'] = np.where(df['compound'].between(-1,-0.5), -1, 0)
df['upset'] = np.where(df['compound'].between(-0.5,0), -1, 0)
df['v_happy'] = np.where(df['compound'].between(0.5,1), 1, 0)
df['happy'] = np.where(df['compound'].between(0,0.5), 1, 0)

#Take the mean compound scores of each day
daily_averages = df.groupby(by=df['date'].dt.date).mean()

#selecting required columns
df_counts = df[['date','v_upset','upset','v_happy','happy']]

#get daily count for each sentiment intensity
daily_counts = df_counts.groupby(by=df_counts['date'].dt.date).sum()
daily_counts['day'] = daily_counts.index


#streamlit specific stuff below
colors = ['DarkRed','LightCoral','DarkGreen','LightGreen']

fig = px.bar(daily_counts, x="day", y=["v_upset", "upset", "v_happy","happy"], 
             color_discrete_sequence = colors, title="Daily Sentiment Counts")
fig.update_layout(barmode='group')
fig2 = px.line(df_stock['PLTR'])

fig.add_trace(fig2.data[0])

def tohtml():
    fig.write_html("app/templates/plotly.html")

#st.plotly_chart(fig)


#st.header("PLTR Stock Price")
#st.line_chart(df_stock['PLTR'])
#st.header("Overall Daily Comment Sentiment")
#st.line_chart(daily_averages['compound'])
#st.header("Daily Sentiment Counts")
#st.bar_chart(daily_counts)
#st.markdown('---')
