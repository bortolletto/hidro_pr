#%%

import pandas as pd
import json
import base64


dloc = pd.read_csv(("./assets/lat_long.csv"),sep = ",",index_col = "Nome")


d_cotas= pd.read_csv(("./assets/2021_2022_cota.csv"),sep = ",",index_col=("data"),parse_dates = True)



dicionario = {'7': '2021-02-11',

 '28': '2021-03-04',

 '49': '2021-03-25',

 '70': '2021-04-15',

 '91': '2021-05-06',

 '112': '2021-05-27',

 '133': '2021-06-17',

 '154': '2021-07-08',

 '175': '2021-07-29',

 '196': '2021-08-19',

 '217': '2021-09-09',

 '238': '2021-09-30',

 '259': '2021-10-21',

 '280': '2021-11-11',

 '301': '2021-12-02',

 '322': '2021-12-22',
 
 '343': '2022-01-20',
 
 '364': '2022-02-10',

 '385': '2022-03-03',

 '406': '2022-03-24',

 '427': '2022-04-20',}
    

stilo = {"padding": "2rem 1rem",
"background-color": "moccasin"}

d_cotas.index = pd.to_datetime(d_cotas.index)
d_cotas.index= d_cotas.index.date
z=0
lista=[]
for i in range (62):
   z=z+7
   lista.append(z)


d_cotas["dias"]=lista
mapbox_access_token = "pk.eyJ1IjoiYm9ydG9sbGV0dG8iLCJhIjoiY2wwcXd2OGdiMXN2NjNjdGt3M3hraWJleSJ9.YKVNHC1tR85b2B0y5WmNPA"

#%% DataFrames e manipulação:


import dash_bootstrap_components as dbc

def create_navbar():
    
    navbar = dbc.NavbarSimple(
        children=[
            dbc.DropdownMenu(
                nav = True,
                in_navbar=True,
                label = "Menu",
                children=[
                    dbc.DropdownMenuItem("Home", href='/'), 
                    dbc.DropdownMenuItem(divider=True), 
                    dbc.DropdownMenuItem("cotas", href='/page-2'), 
                    dbc.DropdownMenuItem("cloropeth", href='/page-3'),
                    ]
                )
            ],
        brand = "Home", #texto do lado da navbar
        brand_href = "/",
        sticky = "top",
        color = "dark",
        dark = True
        )
    return navbar




#%% app cloropeth data


muns = json.load(open('./assets/municipios_reduzidos_arlan.geojson'))
bhs = json.load(open('./assets/bacias_hidrograficas_arlan.geojson'))
uhs = json.load(open('./assets/unidades_hidrograficas_arlan.geojson'))
geojsons = {'muns':muns, 'bhs':bhs, 'uhs':uhs}

df = pd.read_csv('./assets/op_resultados_202203.csv', dtype={'id':str})
# df = df.set_index(['limites', 'referencia', 'agregacao']).sort_index()

# refs = df.index.get_level_values('referencia').unique()
refs = df["referencia"].unique()

dmuns= df.loc[df["limites"] == "muns"]
dmuns = dmuns.set_index(['referencia', 'agregacao']).sort_index()

duhs= df.loc[df["limites"] == "uhs"]
duhs = duhs.set_index(['referencia', 'agregacao']).sort_index()

#imagem
Logo= "./assets/logo-simepar-atualizada.png"


encoded_image = base64.b64encode(open(Logo, 'rb').read())
image_style = {
    "width" : "258px",
    "height" : "90px"}

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



    
