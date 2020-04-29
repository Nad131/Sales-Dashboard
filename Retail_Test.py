#######
# First Milestone Project: Develop a Store Ticker
# dashboard that either allows the user to enter
# a ticker symbol into an input box, or to select
# item(s) from a dropdown list, and uses pandas_datareader
# to look up and display stock data on a graph.
######

# EXPAND STOCK SYMBOL INPUT TO PERMIT MULTIPLE STOCK SELECTION
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
from datetime import datetime
import pandas as pd

app = dash.Dash()

nsdq = pd.read_csv('sale_data.csv')
df = nsdq.groupby(["Store","DayOfWeek"],as_index=False).agg({"Sales": "mean", "Customers": "mean"})
df1 = nsdq.groupby(["DayOfWeek"],as_index=False).agg({"Sales": "mean", "Customers": "mean"})

features = df.Store.unique()

app.layout = html.Div([
    html.H1('Retail Weekly Sales Dashboard'),
    html.Div([
        dcc.Graph(id='first_graph',
            figure={
                'data':[
                    {'x': df1['DayOfWeek'], 'y': df1['Sales'], 'type': 'bar'}
                ],
                'layout': go.Layout(
                title = 'Sales Per Day Total',
                xaxis = {'title': 'Monday to Sunday'},
                yaxis = {'title': 'Average Sales'},
                hovermode='closest')
                }
        )]),
    html.Div([
        html.H2('Weekly Sales per Store'),
        html.H3('Select Store:', style={'paddingRight':'30px'}),
        dcc.Dropdown(
            id='my_store_list',
            options=[{'label': i, 'value': i} for i in features],
            value=['1'],
            multi=True
        )
    ], style={'display':'inline-block', 'verticalAlign':'top', 'width':'30%'}),
    html.Div([
        html.Button(
            id='submit-button',
            n_clicks=0,
            children='Submit',
            style={'fontSize':24}
        ),
    ]),
    dcc.Graph(
        id='my_graph',
        figure={
            'data': [
                {'x': [1,2,3,4,5,6,7]}
            ]
        }

    )
])
@app.callback(
    [Output('my_graph', 'figure')],
    [Input('submit-button', 'n_clicks')],
    [State('my_store_list', 'value')])
def update_graph(n_clicks, selected_store):
    filtered_df = df[df['Store'] == selected_store]
    traces = []
    for store in filtered_df['Store'].unique():
        df_by_store = filtered_df[filtered_df['Store'] == store]
        traces.append({'x': df_by_store['DayOfWeek'], 'y': df_by_store['Sales'], 'type':'bar', 'name':store})
    fig = {
        'data': traces,
        'layout': go.Layout(title = ', '.join(store)+' Sales',
            xaxis = {'title': 'Monday to Sunday'},
            yaxis = {'title': 'Average Sales'},
            hovermode='closest')}
    return fig

if __name__ == '__main__':
    app.run_server()
