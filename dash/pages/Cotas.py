from page_2_funcoes import dicionario,dloc , d_cotas , stilo , mapbox_access_token, create_navbar

#%%
import dash



from dash import dcc, html,  callback
from dash.dependencies import Output, Input
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
import pandas as pd


dash.register_page(__name__, path="/cotas")


layout = html.Div([dbc.Container([
dbc.Row([
       dbc.Col([html.H1("Cotas em estações no Paraná",className ="text-center" )],
               width=12),
       html.Div([
       dcc.RangeSlider(id = "slider_anos",
                  min = 7,
                  max =434,
                  value = [7,21],
                  marks = dicionario,
                  step = 1,
                  

           )
       ])
   
   ],style ={"background-color": "moccasin"}),

dbc.Row([
       dbc.Col([
           dcc.Graph(id='loc_map', figure={},)
        ]),
       
       dbc.Col([
           dcc.Graph(id='grafico_com_slider', figure={})
        ]),
       

   ],style = stilo),



],fluid=True)])



#%% callback mapa
@callback(
    Output('loc_map', 'figure'),
    Input('slider_anos', 'value'),

)
def update_store_data(referencia):
 
    

    locations=[go.Scattermapbox(
                  lon = dloc['longitude'],
                  lat = dloc['latitude'],
                  unselected = {"marker" : {"opacity":1}},
                  selected = {"marker" : {"opacity": 0.5 , "size" :55}},
                  mode='markers',
                  
                  text = [dloc.index[i] for i in range(dloc.shape[0])],
                  hoverinfo = "text",
                  customdata= dloc.index
                  )]


    # Return figure
    return {
        'data': locations,
        'layout': go.Layout(
            
            
            hovermode='closest',
            hoverdistance=2,
            plot_bgcolor="#F9F9F9",
            paper_bgcolor="#F9F9F9",
            autosize = True,
            margin=dict(r=0, l=0, b=0, t=0),
            width=700,
            height=810,
            mapbox=dict(
                accesstoken = mapbox_access_token,
                style='light',
                center={"lat": -24.9, "lon": -51.45},
                zoom = 6.2
                ),
            
               
            ),

        }

#%% callback grafico
nav = create_navbar()
@callback(Output("grafico_com_slider", "figure"),[Input("loc_map","clickData"),Input("slider_anos","value")])

def criando_figura2(clips,ano):
        if clips is None:
            d_layout = d_cotas[(d_cotas["dias"] >= ano[0])&(d_cotas["dias"] <= ano[1] )]
            d_layout= d_layout["Sengés"]
            d_layout= pd.DataFrame(d_layout)
            
            
            y =    dloc.loc[dloc.index == "Sengés"]
            alerta = y["ALERTA"][0]
            d_alerta=pd.DataFrame() 
            d_alerta.index = d_layout.index
            d_alerta["COTA RISCO"] = alerta
            d_alerta["COTA RISCO"] = [float(x.strip("[]").replace(",", ".")) for x in d_alerta["COTA RISCO"] ]
                    
            fig2 = go.Figure()
                        
            fig2.add_trace(go.Scatter(x = d_layout.index , y = d_layout["Sengés"],name = "Cota"))
            fig2.add_trace(go.Scatter(x= d_alerta.index,y=d_alerta["COTA RISCO"],name = "Alerta"))
            
            fig2.update_layout(
            autosize=True,
            template='plotly_white',
            margin=dict(r=0, l=0, b=0, t=0),
            hovermode="x",
            width=780,
            height=760,
            )
            return(fig2)
                    
        else:
            click = clips["points"][0]["customdata"]
            df_copia = d_cotas[(d_cotas["dias"] >= ano[0])&(d_cotas["dias"] <= ano[1])]
            df_copia = df_copia[click]
            df_copia = pd.DataFrame(df_copia)
           
                
            y = dloc.loc[dloc.index == click]
            alerta=y["ALERTA"][0]
            d_alerta= pd.DataFrame()
            
            d_alerta.index = df_copia.index
            d_alerta["COTA RISCO"] = alerta
            d_alerta["COTA RISCO"] = [float(x.strip("[]").replace(",", ".")) for x in d_alerta["COTA RISCO"] ]
            
    
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(x = df_copia.index , y = df_copia[click],name = "Cota"))
            fig.add_trace(go.Scatter(x= d_alerta.index,y=d_alerta["COTA RISCO"],name = "Alerta"))
            
            
            
            fig.update_layout(
            autosize=True,
            template='plotly_white',
            margin=dict(r=0, l=0, b=0, t=0),
            hovermode="x",
            width=800,
            height=700,
            
            )
            
            
            
            return fig