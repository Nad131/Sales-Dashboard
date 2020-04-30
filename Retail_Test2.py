#######
# First Milestone Project: Develop a Store Ticker
# dashboard that either allows the user to enter
# item(s) from a dropdown list
# to look up and display store data on a graph.
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

colors = {
    'background': '#111111',
    'text': '#7FDBFF'}

nsdq = pd.read_csv('sale_data.csv')
nsdq['SalePerCustomer'] = nsdq['Sales']/nsdq['Customers']
df = nsdq.groupby(["Store","DayOfWeek"],as_index=False).agg({"Sales": "mean", "Customers": "mean", "SalePerCustomer": "mean"})
df1 = nsdq.groupby(["DayOfWeek"],as_index=False).agg({"Sales": "mean", "Customers": "mean", "SalePerCustomer": "mean"})

features = df.Store.unique()

app.layout = html.Div([
    html.H1('Retail Weekday Sales Dashboard',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }),
    html.Div([
        dcc.Graph(id='first_graph',
            figure={
                'data':[
                    {'x': df1['DayOfWeek'], 'y': df1['Sales'], 'type': 'bar',
                    'hovertext': ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'],
                    'hover_data': df1['SalePerCustomer']}
                ],
                'layout': go.Layout(
                title = 'Total Sales Performance Per Day',
                xaxis = {'title': 'Monday to Sunday'},
                yaxis = {'title': 'Average Sales'},
                hovermode='closest',
                plot_bgcolor= colors['background'],
                paper_bgcolor= colors['background'],
                font = {
                    'color': colors['text']
                },)
                }
        )]),
    html.Div([
        html.H2('Store Details',
            style={
                'textAlign': 'center',
                'color': colors['text']
            }),
        html.H3('Select Store:', style={'paddingRight':'30px','color': colors['text']}),
        dcc.Dropdown(
            id='my_store_list',
            options=[{'label': i, 'value': i} for i in features],
            value=['1']
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
    dcc.Graph(id='Sales_graph',
        figure={
            'layout': go.Layout(
            plot_bgcolor= colors['background'],
            paper_bgcolor= colors['background'],
            font = {
                'color': colors['text']
            },)}),
    dcc.Graph(id='Customer_graph',
        figure={
            'layout': go.Layout(
            plot_bgcolor= colors['background'],
            paper_bgcolor= colors['background'],
            font = {
                'color': colors['text']
            },)}),
    dcc.Graph(id='SpC_graph',
    figure={
        'layout': go.Layout(
        plot_bgcolor= colors['background'],
        paper_bgcolor= colors['background'],
        font = {
            'color': colors['text']
        },)})
],style={'backgroundColor': colors['background']})

@app.callback(
    Output('Sales_graph', 'figure'),
    [Input('submit-button', 'n_clicks')])

def update_graph(my_store_list):

    filtered_df = df[df.Store == my_store_list]
    traces = []
    for store in filtered_df.Store.unique():
        df_by_store = filtered_df[filtered_df['Store'] == store]
        traces.append(dict(
            x= df_by_store['DayOfWeek'],
            y= df_by_store['Sales'],
            type= 'bar',
            hovertext= ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']))
        fig = {
            'data': traces,
            'layout': go.Layout(title = 'Sales',
                xaxis = {'title': 'Monday to Sunday'},
                yaxis = {'title': 'Average Sales'},
                hovermode='closest',
                plot_bgcolor= colors['background'],
                paper_bgcolor= colors['background'],
                font = {
                    'color': colors['text']
                },)}
    return fig

@app.callback(
    Output('Customer_graph', 'figure'),
    [Input('submit-button', 'n_clicks')])

def update_graph(my_store_list):

    filtered_df = df[df.Store == my_store_list]
    traces = []
    for store in filtered_df.Store.unique():
        df_by_store = filtered_df[filtered_df['Store'] == store]
        traces.append(dict(
            x= df_by_store['DayOfWeek'],
            y= df_by_store['Customers'],
            type= 'bar',
            hovertext= ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']))
        fig = {
            'data': traces,
            'layout': go.Layout(title = 'Customers',
                xaxis = {'title': 'Monday to Sunday'},
                yaxis = {'title': 'Average Visitors'},
                hovermode='closest',
                plot_bgcolor= colors['background'],
                paper_bgcolor= colors['background'],
                font = {
                    'color': colors['text']
                },)}
    return fig

@app.callback(
    Output('SpC_graph', 'figure'),
    [Input('submit-button', 'n_clicks')])

def update_graph(my_store_list):

    filtered_df = df[df.Store == my_store_list]
    traces = []
    for store in filtered_df.Store.unique():
        df_by_store = filtered_df[filtered_df['Store'] == store]
        traces.append(dict(
            x= df_by_store['DayOfWeek'],
            y= df_by_store['SalePerCustomer'],
            type= 'bar',
            hovertext= ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']))
        fig = {
            'data': traces,
            'layout': go.Layout(title = 'Sale Per Customer',
                xaxis = {'title': 'Monday to Sunday'},
                yaxis = {'title': 'Average Sale Per Customer'},
                hovermode='closest',
                plot_bgcolor= colors['background'],
                paper_bgcolor= colors['background'],
                font = {
                    'color': colors['text']
                },)}
    return fig

if __name__ == '__main__':
    app.run_server()
