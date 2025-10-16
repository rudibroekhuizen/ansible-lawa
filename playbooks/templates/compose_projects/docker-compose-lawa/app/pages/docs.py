import dash
from dash import html

dash.register_page(__name__)

layout = html.Div(
    [
        html.H1("The docs page."),
        html.Div("The docs page."),
    ]
)

