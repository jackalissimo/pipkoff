
import requests
import json
import pandas as pd
from bqplot import pyplot as plt
from bqplot import DateScale, LinearScale, Lines, Axis, Figure, OHLC, Tooltip


def show_ohlc(ticker: str, interval="day"):
    print('---hi')
    res = requests.get('http://pipkoff-api:80/api/v0/market/candles', params={'ticker': ticker, 'interval': interval})
    cont = json.loads(res.content)
    candles = cont['data']['candles']    
    dfc = pd.DataFrame(candles)
    dfc["time"] = pd.to_datetime(dfc["time"])
    dfc = dfc.set_index("time")
    
    x_date = DateScale()
    y_linear = LinearScale()
    def_tt = Tooltip(
        fields=['x', 'close','open', 'high', 'low'], 
        formats = ['%Y-%m-%d %H-%M', '.2f', '.2f', '.2f', '.2f'], 
        show_labels=True)

    ohlc = OHLC(x=dfc.index, y=dfc[["o","h","l","c"]],            
                scales={'x':x_date, 'y':y_linear},
                marker="candle",            
                stroke="#222", stroke_width=1.0,
                colors=["lime", "tomato"],
                tooltip=def_tt          
                )

    ax_x = Axis(scale=x_date, label="Date",
                label_offset="35px", grid_color="gray",
                )
    ax_y = Axis(scale=y_linear, label="Price",
                orientation="vertical", label_offset="35px",
                grid_color="gray",            
                tick_format="0.2f")

    fig = Figure(marks=[ohlc],
                 axes=[ax_x, ax_y],             
                 title="CandleStick Chart",
                 fig_margin= dict(top=60, bottom=40, left=50, right=20),
                 background_style = {"fill":"#ccc"}
          )

    fig.layout.height="600px"
    return fig
    
