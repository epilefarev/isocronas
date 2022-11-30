import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output, State

from diseño.home.home import SIDEBAR_STYLE, SIDEBAR_HIDEN, CONTENT_STYLE, CONTENT_STYLE1

# iniciamos app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SKETCHY, dbc.icons.BOOTSTRAP, dbc.icons.FONT_AWESOME],
                suppress_callback_exceptions=True)
app.title = 'La Cancha'
server = app.server

# parte superior de la app
navbar = dbc.NavbarSimple(
    children=[
        dbc.Button("Home", outline=True, color="primary", className="mr-1", id="btn_sidebar"),
    ],
    brand="Administrador de partidos",
    brand_href="#",
    color="dark",
    dark=True,
    fluid=True,
)

# barra de menu
sidebar = html.Div(
    [
        html.H6("Home", className="display-4"),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Inicio", href="/source", id="source-link"),
                dbc.NavLink("Reclutamiento", href="/reclutamiento", id="reclutamiento-link"),
                dbc.NavLink("Convocatoria", href="/convocatoria", id="convocatoria-link"),
                dbc.NavLink("Historial de partidos", href="/historial", id="historial-link"),
                dbc.NavLink("Estadísticas", href="/estadistica", id="estadistica-link"),
                dbc.NavLink("Match Generator", href="/maquina", id="maquina-link"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    id="sidebar",
    style=SIDEBAR_STYLE,
)

# contenido de la pagina
content = html.Div(
    id="page-content",
    style=CONTENT_STYLE
)

app.layout = html.Div(
    [
        dcc.Store(id='side_click'),
        dcc.Location(id="url"),
        navbar,
        sidebar,
        content,
    ],
)


@app.callback(
    [
        Output("sidebar", "style"),
        Output("page-content", "style"),
        Output("side_click", "data"),
    ],
    [Input("btn_sidebar", "n_clicks")],
    [
        State("side_click", "data"),
    ]
)
def toggle_sidebar(n, nclick):
    if n:
        if nclick == "SHOW":
            sidebar_style = SIDEBAR_HIDEN
            content_style = CONTENT_STYLE1
            cur_nclick = "HIDDEN"
        else:
            sidebar_style = SIDEBAR_STYLE
            content_style = CONTENT_STYLE
            cur_nclick = "SHOW"
    else:
        sidebar_style = SIDEBAR_STYLE
        content_style = CONTENT_STYLE
        cur_nclick = 'SHOW'

    return sidebar_style, content_style, cur_nclick


# this callback uses the current pathname to set the active state of the
# corresponding nav link to true, allowing users to tell see page they are on
@app.callback(
    [Output(f"{i}-link", "active") for i in
     ['source', 'reclutamiento', 'convocatoria', 'historial', 'estadistica', 'maquina']],
    [Input("url", "pathname")],
)
def toggle_active_links(pathname):
    if pathname == "/":
        # Treat page 1 as the homepage / index
        return True, False, False, False, False, False
    return [pathname == f"/{i}" for i in
            ['source', 'reclutamiento', 'convocatoria', 'historial', 'estadistica', 'maquina']]


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    # ['source', 'reclutamiento', 'convocatoria', 'historial', 'estadistica', 'maquina']
    if pathname in ["/", "/source"]:
        return "layout_inicio"
    elif pathname == "/reclutamiento":
        return "layout_reclutamiento"
    elif pathname == "/convocatoria":
        return html.P("Acá irá el sistema de convocatoria por partido")
    elif pathname == "/historial":
        return html.P("Acá irá el historial de partidos, formación y marcador")
    elif pathname == "/estadistica":
        return html.P("Acá irá la estadistica asociada a jugadores")
    elif pathname == "/maquina":
        return html.P(
            "Este espacio es destinado a nuestros super algoritmos de Machine Learning que determinarán la mejor experiencia de partidos!")

    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )


if __name__ == "__main__":
    app.run_server(debug=True, port=8070)
