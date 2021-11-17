from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from app import app
from pages import (
    markets,
    news,
    basic_search,
    security_analysis,
    portfolio_analysis,
    portfolio_construction_risk,
    import_,
    schedule,
    apis
)
import callbacks
from utils import navbar

app.title = "Tepilora Dashboard"


app.layout = html.Div(
                     [
                      navbar,
                      dcc.Location(id="url", refresh=False), html.Div(id="page-content")
                     ]
)

# Update page
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/pages/markets":
        return markets.create_layout(app)
    elif pathname == "/pages/news":
        return news.create_layout(app)
    elif pathname == "/pages/security_analysis":
        return security_analysis.create_layout(app)
    elif pathname == "/pages/portfolio_analysis":
        return portfolio_analysis.create_layout(app)
    elif pathname == "/pages/portfolio_construction_risk":
        return portfolio_construction_risk.create_layout(app)
    elif pathname == "/pages/import_":
        return import_.create_layout(app)
    elif pathname == "/pages/schedule":
        return schedule.create_layout(app)
    elif pathname == "/pages/apis":
        return apis.create_layout(app)
    else:
        return basic_search.create_layout(app)

if __name__ == '__main__':
    app.run_server(port=8080, debug=False)
