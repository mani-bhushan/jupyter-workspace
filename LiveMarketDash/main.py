import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import winsound

# Data Source
import yfinance as yf

# upper, lower = 0, 0

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H6("Change the value in the text box to see callbacks in action!"),
    html.Div([
        "Upper: ",
        dcc.Input(id='my-input-up', value=1, type='number')
    ]),
    html.Div([
        "Lower: ",
        dcc.Input(id='my-input-low', value=0, type='number')
    ]),
    html.Br(),
    html.Div(id='my-output-up'),
    html.Div(id='my-output-low'),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    dcc.Graph(id="graph"),
    dcc.Interval(
        id='graph-update',
        interval=10000,
        n_intervals=0
    ),
])


@app.callback(
    Output("graph", "figure"),
    Output('my-output-up', 'children'),
    Output('my-output-low', 'children'),
    Input("graph-update", "n_intervals"),
    Input('my-input-up', 'value'),
    Input('my-input-low', 'value'))
def display_candlestick(n_intervals, input_value_up, input_value_low):
    upper = input_value_up
    lower = input_value_low

    # 'Output-Up: {}'.format(input_value_up), 'Output-Low: {}'.format(input_value_low)

    marketer = yf.download(tickers='ASHOKLEY.NS', period='1d', interval='1m')
    fig = go.Figure(
        data=[
            go.Candlestick(
                open=marketer['Open'],
                high=marketer['High'],
                low=marketer['Low'],
                close=marketer['Close'],
                x=marketer.index,
                name='market data'
            )
        ]
    )

    fig.update_layout(
        xaxis_rangeslider_visible=True,
        width=1260,
        height=768,
        title='Live share price evolution',
        yaxis_title='Stock Price (INR per Shares)'
    )

    recent = marketer['Close'].size - 1
    value = marketer['Close'][recent]
    print(str(value), str(upper), str(lower))
    checker(value, upper, lower)

    return fig, 'Up: {}'.format(input_value_up), 'Low: {}'.format(input_value_low)


def checker(value, upper, lower):
    if value > upper:
        print("Upper Limit " + str(value) + " Found > " + str(upper))
        winsound.Beep(1000, 200)
    elif value < lower:
        print("Lower Limit " + str(value) + " Found < " + str(lower))
        winsound.PlaySound("alarm-sound.wav", winsound.SND_ALIAS)


if __name__ == '__main__':
    app.run_server()
