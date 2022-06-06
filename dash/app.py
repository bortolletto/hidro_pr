import dash_bootstrap_components as dbc
import dash
import dash_labs as dl

app = dash.Dash(
    __name__, plugins=[dl.plugins.pages], external_stylesheets=[dbc.themes.BOOTSTRAP]
)


navbar = dbc.NavbarSimple(
    dbc.DropdownMenu(
        [
            dbc.DropdownMenuItem(page["name"], href=page["path"])
            for page in dash.page_registry.values()
            if page["module"] != "pages.not_found_404"
        ],
        nav=True,
        label="Menu",
        
    ),
    brand="Hidro-PR Simepar",
    color="#827839",
    dark=True,
    sticky = "top"
)

app.layout = dbc.Container(
    [navbar, dl.plugins.page_container],
    fluid=True,
)

if __name__ == "__main__":
    app.run_server(debug=True)
