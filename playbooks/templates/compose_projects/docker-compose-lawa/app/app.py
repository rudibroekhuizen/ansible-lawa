import dash
import dash_mantine_components as dmc
from dash_iconify import DashIconify
from dash import (
    Dash,
    _dash_renderer,
    html,
    dcc,
    callback,
    Input,
    Output,
    State,
    ctx,
    page_container,
    page_registry,
    Patch,
    no_update,
)

# import os
import dash_leaflet as dl
from dash import dash_table
from dash.dependencies import Input, Output
import json
import logging
import pandas as pd
import clickhouse_connect
from clickhouse_connect import common
from clickhouse_connect.driver import httputil
import datetime as dt
from jinja2 import Template
import plotly.express as px
import numpy
from urllib.parse import parse_qs, urlparse


# Dash
_dash_renderer._set_react_version("18.2.0")

# Dash
stylesheets = [
    "https://unpkg.com/@mantine/dates@7/styles.css",
    "https://unpkg.com/@mantine/code-highlight@7/styles.css",
    "https://unpkg.com/@mantine/charts@7/styles.css",
    "https://unpkg.com/@mantine/carousel@7/styles.css",
    "https://unpkg.com/@mantine/notifications@7/styles.css",
    "https://unpkg.com/@mantine/nprogress@7/styles.css",
]

# Configure logging to print to console
logging.basicConfig(level=logging.INFO)

# Clickhouse multi query
common.set_setting("autogenerate_session_id", False)

# Clickhouse pool manager
big_pool_mgr = httputil.get_pool_manager(maxsize=16, num_pools=12)


icons = {
    "github": "ion:logo-github",
    "tools": "bi:tools",
}


def create_link(icon, href, text=""):
    return dmc.Anchor(
        [
            (
                dmc.ActionIcon(
                    DashIconify(icon=icon, width=25), variant="transparent", size="lg"
                )
                if icon
                else None
            ),
            text,
        ],
        href=href,
        target="_blank",
    )

# Shows when on "/"
def home_navbar_content():
    return dmc.Stack(
        [
            dmc.Text("Home Menu"),
            dmc.NavLink(
                label="Home",
                href="/",
                refresh=True,
                c="dark.9",
                # icon=DashIconify(icon="lucide:layout-dashboard"),
                # active=True,
            ),
            dmc.NavLink(
                label="Docs",
                href="/docs",
                # icon=DashIconify(icon="lucide:bar-chart-2"),
            ),
        ]
    )


def otherpage_navbar_content():
    return dmc.Stack(
        [
            dmc.Text("Other Page Menu"),
            dmc.NavLink(
                label="Settings",
                href="/settings",
                # icon=DashIconify(icon="lucide:settings"),
            ),
            dmc.NavLink(
                label="Help",
                href="/help",
                # icon=DashIconify(icon="lucide:help-circle"),
            ),
        ]
    )


burger_button = dcc.Loading(
    dmc.Burger(id="burger-button", opened=False, hiddenFrom="md"),
    overlay_style={"zIndex": 5000},
    delay_show=500,
    custom_spinner=dmc.Group(dmc.Loader(type="dots", size="sm")),
)

header = dmc.Group(
    [
        burger_button,
        dmc.Image(src="/assets/markering.jpg", h=36, w="100%"),
        # dmc.NavLink(label="LAWA", href="/", active="exact"),
        dmc.Anchor(
            "LAWA",
            href="/",
            # target="_self",
            refresh=True,
            underline="never",
            size="xl",
            fw=700,
            c="black"
        ),
        # dmc.Text(["LAWA"], size="xl", fw=700),
        dmc.Text("Nederlands Kustpad", visibleFrom="sm", size="xl"),
        dmc.Text(
            create_link(
                icons["github"], "https://github.com/rudibroekhuizen/ansible-lawa"
            ),
            ml="auto",
        ),
    ],
    justify="flex-start",
    gap="sm",
    style={"height": "1 !important"},
)


app = Dash(
    __name__,
    # external_stylesheets=stylesheets, use_pages=True, suppress_callback_exceptions=True
    external_stylesheets=stylesheets,
    use_pages=True,
)

# logging.info(dash.page_registry.values())

app.layout = dmc.MantineProvider(
    id="mantine-provider",
    children=[
        dcc.Location(
            id="url",
            # refresh="callback-nav"
            refresh=False,
        ),
        dmc.AppShell(
            children=[
                dmc.AppShellHeader(
                    [
                        dmc.Space(h=9),
                        header
                    ],
                    px=25,
                    style={"height": "50px"}
                ),
                dmc.AppShellNavbar(
                    dmc.ScrollArea(
                        [
                            dmc.Box(id="navbar-content"),
                        ],
                        offsetScrollbars=True,
                        type="scroll",
                        style={"height": "100%"},
                    ),
                    p=24,
                    style={"top": "50px"},
                ),
                dmc.AppShellMain(
                    page_container
                ),
            ],
            header={"height": 70},
            padding="xl",
            navbar={
                "width": {
                    "base": "80%",  # Full width on mobile
                    "sm": 200,  # 200px width on small screens and above
                    "lg": 300,  # 300px width on large screens and above
                },
                # "width": 375,
                "breakpoint": "md",
                "collapsed": {"mobile": True},
            },
            id="app-shell",
        ),
    ],
)


# Callback to update Navbar content based on URL pathname
@callback(
    Output("navbar-content", "children"),
    Input("url", "pathname"),
)
def update_navbar_content(pathname):
    if pathname == "/":
        return home_navbar_content()
    elif pathname == "/otherpage":
        return otherpage_navbar_content()
    # Add more conditions for other pages
    else:
        # Default content or an empty navbar for unknown pages
        return dmc.Stack(
            [
                dmc.Text("Default Menu"),
                dmc.NavLink(label="Home", href="/"),
            ]
        )


@callback(
    Output("app-shell", "navbar"),
    Input("burger-button", "opened"),
    State("app-shell", "navbar"),
)
def navbar_is_open(opened, navbar):
    navbar["collapsed"] = {"mobile": not opened}
    return navbar


# # On mobile close the navbar on update
# @callback(
#     Output("burger-button", "opened"),
#     Input("map", "bounds"),
#     # Input("date_range", "value"),
#     # Input("multi_select", "value"),
#     # Input("multi_select_collection", "value"),
#     prevent_initial_call=True,
# )
# def navbar_is_open(*_):
#     return False


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0")
