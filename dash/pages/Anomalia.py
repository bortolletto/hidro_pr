from page_2_funcoes import geojsons, df,refs,encoded_image,SIDEBAR_STYLE,CONTENT_STYLE,dropdown_style
import pandas as pd
import dash
from dash import html,dcc, callback
import plotly.express as px
from dash.dependencies import Input, Output

dash.register_page(__name__, path="/")




#dados --------------------------------------------------------------------------------------------




# style --------------------------------------------------------------------------------------------


sidebar = html.Div([



    html.Br(),
   
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
    ], className="my-3"),
    html.Hr(),
    html.Br(),
    html.H6(
        "Para duvidas e demais informações contactar pelo email : arlan.scortegagna@simepar.br."
    ),
    html.Br(),
]

)



#app--------------------------------------------------------------------------------------------

layout = html.Div([
    
    dcc.Location(id="url"),
    html.Div(children = [sidebar], style=SIDEBAR_STYLE),
    html.Div(children = [dcc.Graph(id='choropleth')], style=CONTENT_STYLE)

])

@callback(
    Output('choropleth', 'figure'),
    Input('referencia', 'value'),
    Input('limites', 'value'),
    Input('variavel', 'value'),
    Input('agregacao', 'value')
)
def update_store_data(referencia, limites, variavel, agregacao):

    geojson = geojsons[limites]
    if limites == "muns":
        regiao = "Mapa em escala municipal"
    elif limites == "uhs":
        regiao ="Mapa das regiões hidrograficas"
    if agregacao == 1:
        agrega = "mensal"
    elif  agregacao == 3:
            agrega = "trimestral"
    elif agregacao == 6:
        agrega = "semestral"
    elif agregacao == 12:
        agrega ="anual"
    if variavel == "anomalia_%":
        range1 = [-110, 110]
        legendaaa = ("Anomalia de precipitação")

    else:
        if agregacao == 1:
            range1 = [0,350]
        elif agregacao == 3:
            range1 = [0,1050]
        elif agregacao == 6:
            range1 = [0,1650]
        elif agregacao == 12:
            range1 = [0,2400]
        legendaaa = ("Precipitação total ")

    dx = df.loc[limites, referencia, agregacao]

    fig = px.choropleth_mapbox(dx,
        geojson = geojson,
        color = variavel,
        locations = 'id',
        featureidkey = 'properties.id',
        range_color = range1,
        center = {"lat": -24.6344, "lon": -51.0150},
        hover_name = 'nome',
        hover_data = {'id':False, variavel:':.2f'},
        labels = {'anomalia_%': 'Anomalia (%)', 'acum_mm':'Precipitação Total (mm)'},
        color_continuous_scale = px.colors.diverging.BrBG,
        opacity = 0.8,
        mapbox_style = "open-street-map",
        zoom=6.5)

    fig.update_layout(
    autosize=True,

    margin=dict(r=0, l=0, b=0, t=100),
    coloraxis_colorbar_x = 0.9,
    hovermode="closest",
    plot_bgcolor="#F9F9F9",
    paper_bgcolor="#F9F9F9",
    width=1300,
    height=910,
    font=dict(
        family="Courier New, monospace",

        color="black",
        ),
    title=("{} com dados de {},\n em escala {}, em {}.".format(regiao,legendaaa,agrega,referencia,)),

    )
    fig['layout']['title']['font'] = dict(size=16)
    fig.add_layout_image(
    dict(
        source='data:image/png;base64,{}'.format(encoded_image.decode()),
        xref="paper", yref="paper",
        x=1, y=1.05,
        sizex=0.2, sizey=0.2,
        xanchor="right", yanchor="bottom"
    )
)


    return fig








