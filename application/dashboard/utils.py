import dash_bootstrap_components as dbc
from dash import dcc
from dash import html

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Markets", href="/dashboard/pages/markets", style={'font-size':'16px'})),
        dbc.NavItem(dbc.NavLink("News", href="/dashboard/pages/news", style={'font-size':'16px'})),
        dbc.NavItem(dbc.NavLink("Basic Search", href="/dashboard/pages/basic_search", style={'font-size':'16px'})),
        dbc.NavItem(dbc.NavLink("Security Analysis", href="/dashboard/pages/security_analysis", style={'font-size':'16px'})),
        dbc.NavItem(dbc.NavLink("Portfolio Analysis", href="/dashboard/pages/portfolio_analysis", style={'font-size':'16px'})),
        dbc.NavItem(dbc.NavLink("Portfolio Construction Risk", href="/dashboard/pages/portfolio_construction_risk", style={'font-size':'16px'})),
        dbc.NavItem(dbc.NavLink("Import", href="/dashboard/pages/import_", style={'font-size':'16px'})),
        dbc.NavItem(dbc.NavLink("Schedule", href="/dashboard/pages/schedule", style={'font-size':'16px'})),
        dbc.NavItem(dbc.NavLink("APIs", href="/dashboard/pages/apis", style={'font-size':'16px'})),
    ],
    brand="Tepilora",
    brand_href="#",
    color="#343a40",
    dark=True,
    fluid=True,
    style={'margin-bottom':'20px'}
)

spinner = dbc.Spinner(color='secondary',children=[html.Div(id="loading-output",style={'visibility':'hidden'})],fullscreen=True,fullscreen_style={'background-color':'transparent'})
