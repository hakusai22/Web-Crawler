# -*- coding: utf-8 -*-
# @Author  : hakusai
# @Time    : 2023/12/10 17:21


# 运行main函数
import dash
from dash import html, dcc

app = dash.Dash()
app.layout = html.Div(
    children=[
        html.H1(children='Hello Dash'),
        html.Div(children='''Dash Framework: A web application framework for Python.'''),

        dcc.Graph(
            id='example-graph',
            figure={
                'data': [
                    {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'Delhi'},
                    {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Mumbai'},
                ],
                'layout': {
                    'title': 'Dash Data Visualization'
                }
            }
        )
    ]
)

if __name__ == '__main__':
    app.run_server(debug=True)
