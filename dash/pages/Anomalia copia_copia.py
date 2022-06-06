import dash
import dash_bootstrap_components as dbc
from dash import html
from dash import dcc
import plotly.express as px
from dash.dependencies import Input, Output
import pandas as pd
import json
import base64






#dados --------------------------------------------------------------------------------------------

muns = json.load(open('/home/felipe.bortolletto/Documentos/dash/dash_completo/assets/municipios_reduzidos_arlan.geojson'))
uhs = json.load(open('/home/felipe.bortolletto/Documentos/dash/dash_completo/assets/unidades_hidrograficas_arlan.geojson'))



geojsons = {'muns':muns, 'uhs':uhs}
df = pd.read_csv('/home/felipe.bortolletto/Documentos/dash/dash_completo/assets/op_resultados_202203.csv', dtype={'id':str})
df = df.set_index(['limites', 'referencia', 'agregacao']).sort_index()

refs = df.index.get_level_values('referencia').unique()


#imagem
Logo= "/home/felipe.bortolletto/Documentos/dash/dash_completo/assets/logo-simepar-atualizada.png"


encoded_image = base64.b64encode(open(Logo, 'rb').read())
image_style = {
    "width" : "258px",
    "height" : "90px"}


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# style --------------------------------------------------------------------------------------------
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "22rem",
    "padding": "2rem 1rem",
    "background-color": "moccasin",
}


CONTENT_STYLE = {
    "position": "fixed",
    "margin-left": "352px",
    "margin-right": "2rem",
    "background-color": "moccasin",
    "width":"1300",
    "height":"900"
}
dropdown_style = { 'width': '200px'}

sidebar = html.Div([



    html.Br(),
    html.H3("Hidro-PR"),
    html.H5("Anomalias de Precipitação"),
    html.Hr(style={ "height": "1%", "Color": "#b8860b"}),
    html.P('Mês de referência'),
    html.Div([
        dcc.Dropdown(
            options = refs,
            value = refs[-1],
            id = 'referencia',
            style = dropdown_style
        ),
        html.Hr(),
        dcc.RadioItems(
            options=[
                {'label': ' Municípios', 'value': 'muns'},
                {'label': ' Unidades Hidrográficas', 'value': 'uhs'},],
            value='muns',
            id = 'limites',
            labelStyle = {'display':'block'},
        ),
        html.Hr(),
        dcc.RadioItems(
            options=[
                {'label': ' Mensal', 'value': 1},
                {'label': ' Trimestral', 'value': 3},
                {'label': ' Semestral', 'value': 6},
                {'label': ' Anual', 'value': 12}],
            value=1,
            id = 'agregacao',
            labelStyle = {'display':'block'},
        ),
        html.Hr(),
        dcc.RadioItems(
            options=[
                {'label': ' Anomalia de Precipitação', 'value': 'anomalia_%'},
                {'label': ' Precipitação Total', 'value': 'acum_mm'}],
            value = 'anomalia_%',
            id = 'variavel',
            labelStyle = {'display':'block'},
        ),
    ]),
    html.Hr(),
    html.Br(),
    html.H6(
        "Para duvidas e demais informações contactar pelo email : arlan.scortegagna@simepar.br."
    ),
    html.Br(),
]

)



#app--------------------------------------------------------------------------------------------

app.layout = html.Div([

    dcc.Location(id="url"),
    html.Div(children = [sidebar], style=SIDEBAR_STYLE),
    dcc.Store(
        id="limites_dcc"
        ),
    dcc.Store(
        id="agrega_dcc"
        ),
    dcc.Store(
        id= "variavel_dcc"
        ),
    dcc.Store(
        id= "referencia_dcc"
        ),
    html.Div(id="my-div",children = [
        dcc.Graph(id='choropleth',
                  figure={'data': [px.choropleth_mapbox(
                      df["variavel_dcc","referencia_dcc","limites_dcc"],
                      color = "variavel_dcc",
                      locations = "id",
                      featureidkey ="properties.id",
                        
                      
                          )]},
                      layout={
                       "autosize":True,
                       "margin":dict(r=0, l=0, b=0, t=100),
                       "coloraxis_colorbar_x" : 0.9,
                       "hovermode" : "closest",
                       "plot_bgcolor":"#F9F9F9",
                       "paper_bgcolor":"#F9F9F9",
                       "width":1300,
                       "height":910,
                           

                       })
        ], style=CONTENT_STYLE)

])

# @app.callback(Output("choropleth","figure"),
#               Input("limites","value"),
#               Input("variavel","value"))
              
# def gera_mapa(limites,variavel):
#     dx = df.loc[limites,"2014-01",1]
    
    
        
#     fig = px.choropleth_mapbox(
#         dx,
#         geojson = geojsons[limites],
#         color = variavel,
#         locations = 'id',
#         featureidkey = 'properties.id',
#         range_color = [-110,110],
#         center = {"lat": -24.6344, "lon": -51.0150},
#         hover_name = 'nome',
#         hover_data = {'id':False, variavel:':.2f'},
#         labels = {'anomalia_%': 'Anomalia (%)', 'acum_mm':'Precipitação Total (mm)'},
#         color_continuous_scale = px.colors.diverging.BrBG,
#         opacity = 0.8,
#         mapbox_style = "open-street-map",
#         zoom=6.5)
    
#     return fig

# @app.callback(
#     Output('choropleth', 'figure'),
#     Input('referencia', 'value'),
#     Input('agregacao', 'value')
# )
# def atualiza(referencia,agregacao):
    
    
        
    
              
              
# @app.callback(
#     Output('choropleth', 'figure'),
#     Input('referencia', 'value'),
#     Input("limites","value"),
#     Input('variavel', 'value'),
#     Input('agregacao', 'value')
# )
# def update_store_data(referencia, limites ,variavel, agregacao):
    
#     if agregacao == 1:
#         agrega = "mensal"
#     elif  agregacao == 3:
#             agrega = "trimestral"
#     elif agregacao == 6:
#         agrega = "semestral"
#     elif agregacao == 12:
#         agrega ="anual"
#     if variavel == "anomalia_%":
#         range1 = [-110, 110]
#         legendaaa = ("Anomalia de precipitação")

#     else:
#         range1 = [0,350]
#         legendaaa = ("Precipitação total ")

#     dx = df.loc[limites,referencia, agregacao]
#     fig = px.choropleth_mapbox(dx,
#         geojson = geojsons[limites],
#         color = variavel,
#         locations = 'id',
#         featureidkey = 'properties.id',
#         range_color = range1,
#         center = {"lat": -24.6344, "lon": -51.0150},
#         hover_name = 'nome',
#         hover_data = {'id':False, variavel:':.2f'},
#         labels = {'anomalia_%': 'Anomalia (%)', 'acum_mm':'Precipitação Total (mm)'},
#         color_continuous_scale = px.colors.diverging.BrBG,
#         opacity = 0.8,
#         mapbox_style = "open-street-map",
#         zoom=6.5)

#     fig.update_layout(
#     autosize=True,

#     margin=dict(r=0, l=0, b=0, t=100),
#     coloraxis_colorbar_x = 0.9,
#     hovermode="closest",
#     plot_bgcolor="#F9F9F9",
#     paper_bgcolor="#F9F9F9",
#     width=1300,
#     height=910,
#     font=dict(
#         family="Courier New, monospace",

#         color="black",
#         ),
#     title=(" Dados de {},\n em escala {}, em {}.".format(legendaaa,agrega,referencia,)),

#     )
#     fig['layout']['title']['font'] = dict(size=16)
#     fig.add_layout_image(
#     dict(
#         source='data:image/png;base64,{}'.format(encoded_image.decode()),
#         xref="paper", yref="paper",
#         x=1, y=1.05,
#         sizex=0.2, sizey=0.2,
#         xanchor="right", yanchor="bottom"
#     )
# )
#     return fig


# app.clientside_callback(
#     """
#     function(data, figure) {
#         if(figure_data === undefined) {
#             return {'data': [], 'layout': {}};
#         }
#         const fig = Object.assign({}, figure_data, {
#                 'layout': {
#                     ...figure_data.layout,
#                     'title': {
#                         ...figure_data.layout.title, text: title_text
#                     }
#                 }
#         });
#         return fig;
#     }
#     """,
#     Output('choropleth', 'figure'),
#     Input('dados', 'data'),
    
# )


    



if __name__=='__main__':
    app.run_server(debug=True, port=3000)






