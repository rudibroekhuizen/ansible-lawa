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
)
import os
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

# ClickHouse configurations
clickhouse_db = os.getenv("CLICKHOUSE_DB")
clickhouse_host = os.getenv("CLICKHOUSE_HOST")
clickhouse_user = os.getenv("CLICKHOUSE_USER")
clickhouse_pass = os.getenv("CLICKHOUSE_PASSWORD")

# Clickhouse multi query
common.set_setting("autogenerate_session_id", False)

# Clickhouse pool manager
big_pool_mgr = httputil.get_pool_manager(maxsize=16, num_pools=12)

client = clickhouse_connect.get_client(
    pool_mgr=big_pool_mgr,
    host=clickhouse_host,
    port=8123,
    user=clickhouse_user,
    password=clickhouse_pass,
    database=clickhouse_db,
)

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
        dmc.Text(["LAWA"], size="xl", fw=700),
        dmc.Text("Vanessa en Rudi stappen door", visibleFrom="sm", size="xl"),
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


navbar = dmc.ScrollArea(
    [
        # multi_select_classification,
        # multi_select_collection,
    ],
    offsetScrollbars=True,
    type="scroll",
    style={"height": "100%"},
)

app = Dash(
    external_stylesheets=stylesheets, use_pages=True, suppress_callback_exceptions=True
)

app_shell = dmc.AppShell(
    [
        dmc.AppShellHeader([dmc.Space(h=5), header], px=25, style={"height": "50px"}),
        dmc.AppShellNavbar(navbar, p=24, style={"top": "50px"}),
        dmc.AppShellMain(page_container),
    ],
    header={"height": 70},
    padding="xl",
    navbar={
        "width": 375,
        "breakpoint": "md",
        "collapsed": {"mobile": True},
    },
    id="app-shell",
)

app.layout = dmc.MantineProvider(app_shell)


@callback(
    Output("app-shell", "navbar"),
    Input("burger-button", "opened"),
    State("app-shell", "navbar"),
)
def navbar_is_open(opened, navbar):
    navbar["collapsed"] = {"mobile": not opened}
    return navbar


# On mobile close the navbar on update
@callback(
    Output("burger-button", "opened"),
    Input("map", "bounds"),
    # Input("date_range", "value"),
    # Input("multi_select", "value"),
    # Input("multi_select_collection", "value"),
    prevent_initial_call=True,
)
def navbar_is_open(*_):
    return False


if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0")
