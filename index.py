import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas_datareader.data as web
import datetime
import plotly.graph_objects as go
from dash.dependencies import Input, Output

app = dash.Dash(__name__, title='Stock Market')

companies = {
    'AAPL':'Apple',
    'MSFT':'Microsoft',
    'AMZN':'Amazon',
    'GOOGL':'Google',
    'FB':'Facebook',
    'BABA':'Alibaba',
    'TSLA':'Tesla'
}

colors = {
    'background': '#1a1a1a',
    'graph-background': '#1c1c1c',
    'main': '#ffffff'
}

app.layout = html.Div([
    html.H1('Largest companies by market cap — US Stock Market', style={'color': colors['main']}),
    html.Div(children=[
                html.Div('Company name:'),
                dcc.Dropdown(
                    id='dropdown',
                    options=[
                        {'label': companies['AAPL'], 'value': 'AAPL'},
                        {'label': companies['MSFT'], 'value': 'MSFT'},
                        {'label': companies['AMZN'], 'value': 'AMZN'},
                        {'label': companies['GOOGL'], 'value': 'GOOGL'},
                        {'label': companies['FB'], 'value': 'FB'},
                        {'label': companies['BABA'], 'value': 'BABA'},
                        {'label': companies['TSLA'], 'value': 'TSLA'},
                    ],
                    value='AAPL',
                    clearable=False,
                    style={'color': '#1a1a1a', 'minWidth': '30%'},
                ),
                html.Div('Date range:'),
                dcc.DatePickerRange(
                    id='my-date-picker-range',
                    calendar_orientation='horizontal',
                    first_day_of_week=1,
                    reopen_calendar_on_clear=True,
                    clearable=True,
                    min_date_allowed=datetime.datetime(1975, 4, 4),
                    max_date_allowed=datetime.datetime.now(),
                    start_date=datetime.datetime(2010, 1, 1),
                    end_date=datetime.datetime.now(),
                    display_format='D/M/YYYY',
                    month_format='MMMM YYYY',
                    style={'color': colors['background']}
                )
        ],className='dropdown-menu'),
    html.Div(id='output-graph', style={'width': '63%', 'display': 'block', 'margin': 'auto'}),
    ])

@app.callback(
    Output(component_id='output-graph', component_property='children'),
    [Input(component_id='dropdown', component_property='value'),
     Input('my-date-picker-range', 'start_date'),
     Input('my-date-picker-range', 'end_date')]
)

def update_value(input_data, start_date, end_date):
    start = start_date
    end = end_date
    df = web.DataReader(input_data, 'yahoo', start, end)
    df.reset_index(inplace=True)
    df.set_index("Date", inplace=True)
    fig = go.Figure(
            data=[go.Scatter(x=df.index, y=df.Close, line_color=colors['main'])],
            layout_title_text=companies[input_data] + " Stock Price"
        )
    fig.update_layout(
        plot_bgcolor=colors['graph-background'],
        paper_bgcolor=colors['background'],
        font_color=colors['main']
    )
    return dcc.Graph(
        id='example-graph',
        figure= fig
    )

if __name__ == '__main__':
    app.run_server(debug=True)