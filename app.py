import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Output, Input

coin_marketcap_df = pd.read_csv('coin_data/coin_marketcap_data.csv')
coin_marketcap_df['Date'] = pd.to_datetime(arg=coin_marketcap_df['Date'], unit='ms')

external_stylesheets = [
    {
        'href': 'https://fonts.googleapis.com/css2?'

                'family=Lato:wght@400;700&display=swap',

        'rel': 'stylesheet',
    }
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.tile = 'Accuracy Cryptocurrency analysis'

app.layout = html.Div(
    children=[
        html.Div(
            className = 'Header',
            children=[
                html.H1(
                    children = '💵 CryptoAnalysis App 💵',
                ),
                html.H3(
                    children = 'Marketcap & Volume for tokens, Volume for exchanges',
                ),
            ]
        ),
        html.Div(
            className='Menu',
            children=[
                html.Div(children='Coin', className='menu-title'),
                dcc.Dropdown(
                    id='coin-filter',
                    options=[
                        {'label': coin, 'value': coin}
                        for coin in list(coin_marketcap_df.columns.values)[1:]
                    ],
                    value='bitcoin',
                    clearable=False,
                    className='dropdown',
                    style={'width': '50%'}
                ),
                html.Div(children='Date', className='menu-title'),
                dcc.DatePickerRange(
                    id='date-range',
                    min_date_allowed = coin_marketcap_df.Date.min().date(),
                    max_date_allowed = coin_marketcap_df.Date.max().date(),
                    start_date = coin_marketcap_df.Date.min().date(),
                    end_date = coin_marketcap_df.Date.max().date(),
                )
            ]
        ),
        html.Div(
            className = 'Graphs',
            children=[
                dcc.Graph(
                    className='Card',
                    id='marketCap-chart',
                    config={'displayModeBar': False}
                )
            ]
        )   
    ]
)

@app.callback(
    Output('marketCap-chart', 'figure'),
    [
        Input('coin-filter', 'value'),
        Input('date-range', 'start_date'),
        Input('date-range', 'end_date'),
    ]
)

def update_charts(coin, start_date, end_date):
    mask=(
        (coin_marketcap_df['Date']>=start_date)
        & (coin_marketcap_df['Date']<=end_date)
    )
    filtered_data = coin_marketcap_df[mask][['Date',coin]]
    marketcap_figure = {
        'data': [
            {
                'x': filtered_data['Date'],
                'y': filtered_data[coin],
                'type': 'lines'
            }
        ],
        'layout': {
            "title":{
                'text' : 'Marketcap Data',
                'x': 0.05,
                'xanchor': 'left',
            },
            "xaxis": {"fixedrange": False},
            "yaxis": {"fixedrange": False},
            "colorway": ["#17B897"],
        }
    }
    return marketcap_figure

if __name__ == '__main__':
    app.run_server(debug=True)