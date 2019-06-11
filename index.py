import os

import dash
import dash_table as dt
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from plotly import tools
import plotly.graph_objs as go


from src.components.dataMaster import dfMaster, dfMasterTable

from src.components.tab1.view import renderIsiTab1
from src.components.tab2.view import renderIsiTab2
from src.components.tab3.view import renderIsiTab3
from src.components.tab4.view import renderIsiTab4

from src.components.tab1.callbacks import callbackSortingTable, callbackFilterTable
from src.components.tab2.callbacks import callbackUpdateCatGraph
from src.components.tab3.callbacks import callbackUpdateCommonWord
from src.components.tab4.callbacks import output_predict


# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__)

server=app.server

app.title='Dashboard Toxic Comments'

app.layout = html.Div([
        html.H1('Dashboard Toxic Comments Classification'),
        html.H3('''
                Created by: Brane Warren
                '''),
    dcc.Tabs(id="tabs", value='tab-1', children=[
        dcc.Tab(label='Data Toxic', value='tab-1', children = renderIsiTab1()),
        dcc.Tab(label='Categorical Plots', value='tab-2',children = renderIsiTab2()),
        dcc.Tab(label='Common Word Plots', value='tab-3', children = renderIsiTab3()),
        dcc.Tab(label='Predict Text', value='tab-4', children = renderIsiTab4()),
    ],style={
        'fontFamily': 'system-ui'
    }, content_style={
        'fontFamily':'Arial',
        'borderBottom' : '1px solid #d6d6d6',
        'borderLeft' : '1px solid #d6d6d6',
        'borderRight' : '1px solid #d6d6d6',
        'padding' : '44px'
    })
], style={
    'maxWidth' : '1200px',
    'margin' : '0 auto'
})

# Tabel Canggih
@app.callback(
    Output('table-multicol-sorting', "data"),
    [Input('table-multicol-sorting', "pagination_settings"),
     Input('table-multicol-sorting', "sorting_settings")])
def update_sort_paging_table(pagination_settings, sorting_settings):
    return callbackSortingTable(pagination_settings, sorting_settings)

# Tabel
@app.callback(
    Output(component_id='tablediv', component_property='children'),
    [Input('buttonsearch', 'n_clicks'),
    Input('filterrowstable', 'value')],
    [State('filterToxicLevel', 'value'),
    State('filterComment', 'value'),
    ])
def update_table(n_clicks,maxrows,level,comment):
    return callbackFilterTable(n_clicks,maxrows,level,comment)

# Plots
@app.callback(
    Output(component_id='categoryGraph', component_property='figure'),
    [Input(component_id='jenisPlot', component_property='value'),
    Input(component_id='xplot', component_property='value'),
    Input(component_id='yplot', component_property='value'),])
def update_category_graph(jenisplot, plotToxicLevel, textLength):
    return callbackUpdateCatGraph(jenisplot, plotToxicLevel, textLength)

# Jenis Plot
@app.callback(
    Output(component_id='yplot', component_property='disabled'),
    [Input(component_id='jenisPlot', component_property='value')])
def update_disabled_stats(jenisplot):
    if jenisplot=='Bar':
        return True
    return False

# Most Common Word Plot
@app.callback(
    Output(component_id='commonWordGraph', component_property='figure'),
    [Input(component_id='ngramPlot', component_property='value'),
    Input(component_id='categoryPlot', component_property='value'),
    Input(component_id='maxWords', component_property='value'),])
def update_common_word(ngram, category, number):
    return callbackUpdateCommonWord(int(ngram), category, int(number))

# Predict
@app.callback(
    Output(component_id='outputpredict', component_property='children'),
    [Input('buttonsearch4', 'n_clicks')],
    [State('textPredict', 'value')])
def output_predict_callback(n_clicks, text):
    if str(text)=='':
        return [html.H3('Please fill in the text')]
    else:
        return output_predict(n_clicks, text)


if __name__ == '__main__':
    app.run_server(debug=True)