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

def label_filter(var, value):
    filter_index = df['label'] == value
    return df[var][filter_index]

tracer_list = []
for data_class in sorted(df["label"].unique()):
    tracer = go.Scatter(
        x = label_filter('x',data_class),
        y = label_filter('y',data_class),
        dy = 1, # step sizes for y
        text = label_filter('filename', data_class),
        hoverinfo = 'text',
        mode = 'markers',
        marker = {
            'size': 12,
            #'color': 'rgb(51,204,153)',
            'line': {'width': 2}
            },
        name=str(data_class)
    )
    tracer_list.append(tracer)

app.layout = html.Div([
                html.Div([
                    dcc.Graph(
                        id='wheels-plot',
                        figure={
                            'data': tracer_list,
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
### Debugging Block ###
@app.callback(
    Output('debug-selection', 'children'),
    [Input('wheels-plot', 'hoverData')])
def callback_image2(hoverData):
    # filename =  {'points': [{'curveNumber': 0, 'pointIndex': 1, 'pointNumber': 1, 'y': -197.04065, 'x': 14.633121}]}
    # x=hoverData['points'][0]['x']
    return json.dumps(hoverData, indent=2)
### End of Debugging Block ###

@app.callback(
    Output('hover-image', 'src'),
    [Input('wheels-plot', 'hoverData')])
def callback_image(hoverData):
    # index=hoverData['points'][0]['pointIndex']
    filenamelist = label_filter('filename',hoverData['points'][0]['curveNumber'])
    filename = filenamelist.iloc[hoverData['points'][0]['pointIndex']]
    # hoverData =  {'points': [{'curveNumber': 0, 'pointIndex': 1, 'pointNumber': 1, 'y': -197.04065, 'x': 14.633121}]}
    # x=hoverData['points'][0]['x']
    path = './MNIST_img/'
    return encode_image(path+str(filename) + '.png')



if __name__ == '__main__':
    app.run_server(debug=True)
