# -*- coding: utf-8 -*-
"""
Created on Sat Jan 16 15:31:38 2021

@author: jlyne
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import pandas_datareader.data as web
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import codecs
f=codecs.open("index.html", 'r')
st.markdown("""
<style>

/*
 * Globals
 */


/* Custom default button */
.btn-secondary,
.btn-secondary:hover,
.btn-secondary:focus {
  color: #333;
  text-shadow: none; /* Prevent inheritance from `body` */
}


/*
 * Base structure
 */

body {
  text-shadow: 0 .05rem .1rem rgba(0, 0, 0, .5);
  box-shadow: inset 0 0 5rem rgba(0, 0, 0, .5);
  padding-top:0px;
  margin-top: 0px;
}

.cover-container {
  max-width: 42em;
}
</style>
    """, unsafe_allow_html=True)

Title_html = """
    <style>
        .title h1{
          user-select: none;
          font-size: 43px;
          color: white;
          background: repeating-linear-gradient(-45deg, red 0%, yellow 7.14%, rgb(0,255,0) 14.28%, rgb(0,255,255) 21.4%, cyan 28.56%, blue 35.7%, magenta 42.84%, red 50%);
          background-size: 600vw 600vw;
          -webkit-text-fill-color: transparent;
          -webkit-background-clip: text;
          animation: slide 10s linear infinite forwards;
        }
        @keyframes slide {
          0%{
            background-position-x: 0%;
          }
          100%{
            background-position-x: 600vw;
          }
        }
    </style> 
    
    <div class="title">
        <h1>r/WallStreetBets Sentiment Analysis Overview </h1>
    </div>
    """
st.markdown(Title_html, unsafe_allow_html=True) #Title rendering


page_html = """
        <style>
      .bd-placeholder-img {
        font-size: 1.125rem;
        text-anchor: middle;
        -webkit-user-select: none;
        -moz-user-select: none;
        user-select: none;
      }

      @media (min-width: 768px) {
        .bd-placeholder-img-lg {
          font-size: 3.5rem;
        }
      }

           .button {
        border: none;
        color: white;
        padding: 16px 32px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 20px;
        margin: 4px 2px;
        transition-duration: 0.4s;
        cursor: pointer;
        border-radius: 8px;
}

.button4 {
  background-color: white;
  color: black;
  border: 4px solid #d9d9d9;
}

.buttonselected {
  background-color: #d9d9d9;
  color: black;
  border: 4px solid #d9d9d9;
}

.button4:hover {background-color: #d9d9d9;}


.page-header {margin-top:0}
    </style>
"""
st.markdown(page_html, unsafe_allow_html=True) #Title rendering
'''
# 🚀🌙

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
df_stock['day'] = df_stock.index

#streamlit specific stuff below
colors = ['DarkRed','LightCoral','DarkGreen','LightGreen']

fig = px.bar(daily_counts, x="day", y=["v_upset", "upset", "v_happy","happy"], 
             color_discrete_sequence = colors, title="Daily Sentiment Counts")
#fig.update_layout(barmode='group')
fig2 = px.line(df_stock['PLTR'])

fig.add_trace(fig2.data[0])

st.plotly_chart(fig)


#################
# Chart w/ Overlay
fig = make_subplots(specs=[[{"secondary_y": True}]])
i=0
for col in ["v_upset", "upset", "v_happy","happy"]:
    # Add traces
    fig.add_trace(
        go.Bar(x=daily_counts["day"], y=daily_counts[col], name=col+" count",
               marker_color = colors[i]),
        secondary_y=False,
    )
    i+=1

fig.add_trace(
    go.Line(x=df_stock["day"], y=df_stock['PLTR'], name="PLTR", marker_color ='black'),
    secondary_y=True,
)

# Add figure title
fig.update_layout(
    title_text="Sentiment and Stock Price Overview",barmode='relative'
)

# Set x-axis title
fig.update_xaxes(title_text="Date")

# Set y-axes titles
fig.update_yaxes(title_text="<b>Count</b>", secondary_y=False)
fig.update_yaxes(title_text="<b>Price (USD)</b>", secondary_y=True)

st.plotly_chart(fig)



