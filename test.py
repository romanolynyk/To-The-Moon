from flask import Flask, render_template
import json
import plotly
import plotly.graph_objs as go
 
import numpy as np
 
app = Flask(__name__)
 

def line():
    count = 500
    xScale = np.linspace(0, 100, count)
    yScale = np.random.randn(count)
 
    # Create a trace
    trace = go.Scatter(
        x = xScale,
        y = yScale
    )
 
    data = [trace]
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON
  