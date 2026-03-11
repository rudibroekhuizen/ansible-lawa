import dash
import dash_mantine_components as dmc
from dash_iconify import DashIconify
from dash import (
    Dash,
    _dash_renderer,
    html,
    dcc,
    callback,
    clientside_callback,
    Input,
    Output,
    State,
    ctx,
    page_container,
    page_registry,
    Patch,
    no_update,
    ALL
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


# Configure logging to print to console
logging.basicConfig(level=logging.INFO)

# Clickhouse multi query
common.set_setting("autogenerate_session_id", False)

# Clickhouse pool manager
big_pool_mgr = httputil.get_pool_manager(maxsize=16, num_pools=12)

theme_toggle = dmc.Switch(
    offLabel=DashIconify(
        icon="radix-icons:sun", width=15, color=dmc.DEFAULT_THEME["colors"]["yellow"][8]
    ),
    onLabel=DashIconify(
        icon="radix-icons:moon",
        width=15,
        color=dmc.DEFAULT_THEME["colors"]["yellow"][6],
    ),
    id="color-scheme-toggle",
    persistence=True,
    color="grey",
)

app = Dash(use_pages=True)

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
                   dmc.Group(
                        [
                            dmc.Group(
                                [
                                    dmc.Burger(
                                        id="burger",
                                        size="sm",
                                        hiddenFrom="sm",
                                        opened=False,
                                    ),
                                    # dmc.Image(src=logo, h=40, flex=0),
                                    dmc.Anchor(
                                        "LAWA",
                                        href="/",
                                        refresh=True,
                                        underline="never",
                                        size="xl",
                                        fw=700,
                                        # color=dmc.DEFAULT_THEME["colors"]["yellow"][6],
                                        # color=dmc.DEFAULT_THEME["colors"][PRIMARY_COLOR][6],
                                        # target="_self",
                                    ),
                                    # dmc.Title("Demo App", c="blue"),
                                ]
                            ),
                            theme_toggle,
                        ],
                        justify="space-between",
                        style={"flex": 1},
                        # style={"height": "1 !important"},
                        h="100%",
                        px="md",
                    ),
                ),
                #     [
                #         dmc.Space(h=9),
                #         header
                #     ],
                #     px=25,
                #     style={"height": "50px"}
                # ),
                dmc.AppShellNavbar(
                    id="navbar",
                    children=[
                         #"Navbar",
                         dmc.NavLink(
                             id={'type': 'navbar-link', 'index': "link-home"},
                             label="Home",
                             href="/",
                             refresh=False,
                             color=dmc.DEFAULT_THEME["colors"]["yellow"][6],
                             # color=dmc.DEFAULT_THEME["colors"][PRIMARY_COLOR][6],
                             # icon="material-symbols:rocket-launch-rounded",
                             # icon=DashIconify(icon="lucide:layout-dashboard"),
                             # active=True,
                         ),
                         dmc.NavLink(
                             #id="link-docs",
                             id={'type': 'navbar-link', 'index': "link-docs"},
                             label="Docs",
                             href="/docs",
                             refresh=False,
                             color=dmc.DEFAULT_THEME["colors"]["yellow"][6],
                         ),
                        # *[
                        #     dmc.Skeleton(height=28, mt="sm", animate=False)
                        #     for _ in range(15)
                        # ],
                    ],
                    p="md",
                ),
                dmc.AppShellMain(
                    page_container
                ),
            ],
            header={"height": 60},
            padding="md",
            navbar={
                "width": 300,
                "breakpoint": "sm",
                "collapsed": {"mobile": True},
            },
            id="appshell",
        ),
    ],
)


@callback(
    Output("appshell", "navbar"),
    Input("burger", "opened"),
    State("appshell", "navbar"),
)
def navbar_is_open(opened, navbar):
    navbar["collapsed"] = {"mobile": not opened}
    return navbar


clientside_callback(
    """
    (switchOn) => {
       document.documentElement.setAttribute('data-mantine-color-scheme', switchOn ? 'dark' : 'light');
       return window.dash_clientside.no_update
    }
    """,
    Output("color-scheme-toggle", "id"),
    Input("color-scheme-toggle", "checked"),
)


# On mobile close the navbar on update
@callback(
    Output("burger", "opened"),
    Input({'type': 'navbar-link', 'index': ALL}, 'n_clicks'),
    prevent_initial_call=True,
)
def navbar_is_open(*_):
    return False

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
