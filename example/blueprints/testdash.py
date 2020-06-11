def testdash(app, url_prefix='/testdash', DATA_DIR=''):
  import pandas as pd
  import dash
  from dash.dependencies import Input, Output
  import dash_core_components as dcc
  import dash_html_components as html

  df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/dash-stock-ticker-demo.csv')

  testdash = dash.Dash(
    'testdash',
    server=app,
    routes_pathname_prefix=url_prefix + '/',
  )

  testdash.layout = html.Div([
      html.H1('Stock Tickers'),
      dcc.Dropdown(
          id='my-dropdown',
          options=[
              {'label': 'Tesla', 'value': 'TSLA'},
              {'label': 'Apple', 'value': 'AAPL'},
              {'label': 'Coke', 'value': 'COKE'}
          ],
          value='TSLA'
      ),
      dcc.Graph(id='my-graph')
  ], className="container")

  @testdash.callback(Output('my-graph', 'figure'),
                [Input('my-dropdown', 'value')])
  def update_graph(selected_dropdown_value):
      dff = df[df['Stock'] == selected_dropdown_value]
      return {
          'data': [{
              'x': dff.Date,
              'y': dff.Close,
              'line': {
                  'width': 3,
                  'shape': 'spline'
              }
          }],
          'layout': {
              'margin': {
                  'l': 30,
                  'r': 20,
                  'b': 30,
                  't': 20
              }
          }
      }
