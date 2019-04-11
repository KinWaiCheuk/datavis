import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import base64
import json

app = dash.Dash()
server = app.server
df = pd.read_csv('./MNIST_map.csv')

def encode_image(image_file):
    encoded = base64.b64encode(open(image_file, 'rb').read())
    return 'data:image/png;base64,{}'.format(encoded.decode())

app.layout = html.Div([
                html.Div([
                    dcc.Graph(
                        id='wheels-plot',
                        figure={
                            'data': [
                                go.Scatter(
                                    x = df['x'],
                                    y = df['y'],
                                    dy = 1,
                                    mode = 'markers',
                                    marker = {
                                        'size': 12,
                                        'color': 'rgb(51,204,153)',
                                        'line': {'width': 2}
                                        }
                                )
                                    ],
                            'layout': 
                                go.Layout(
                                    title = 'TSN-plot',
                                    xaxis = {'title': 'x-axis'},
                                    yaxis = {'title': 'y-axis','nticks':3},
                                    hovermode='closest'
                                                )
                                }
                    )], style={'width':'30%', 'float':'left'}),

    html.Div([
    html.Img(id='hover-image', src='children', height=300)
    ], style={'paddingTop':35}),

    # Debugging
    html.P(html.Div([html.Pre(id='debug-selection', style={'paddingTop':100})])),
    
])
app.logger.info('message')
### Debugging Block ###
@app.callback(
    Output('debug-selection', 'children'),
    [Input('wheels-plot', 'hoverData')])
def callback_image2(hoverData):
    print("Hello callback")
    # filename =  {'points': [{'curveNumber': 0, 'pointIndex': 1, 'pointNumber': 1, 'y': -197.04065, 'x': 14.633121}]}
    # x=hoverData['points'][0]['x']
    return json.dumps(hoverData, indent=2)
### End of Debugging Block ###

@app.callback(
    Output('hover-image', 'src'),
    [Input('wheels-plot', 'hoverData')])
def callback_image(hoverData):
    index=hoverData['points'][0]['pointIndex']
    # hoverData =  {'points': [{'curveNumber': 0, 'pointIndex': 1, 'pointNumber': 1, 'y': -197.04065, 'x': 14.633121}]}
    # x=hoverData['points'][0]['x']
    path = './MNIST_img/'
    return encode_image(path+str(index) + '.png')



if __name__ == '__main__':
    app.run_server(debug=True)
