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
    register_page,
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
import psycopg

register_page(__name__, path="/")


# Configure logging to print to console
logging.basicConfig(level=logging.INFO)

# Clickhouse vars
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

# Postgres vars
postgres_host = os.getenv("POSTGRES_HOST")
postgres_db = os.getenv("POSTGRES_DB")
postgres_user = os.getenv("POSTGRES_USER")
postgres_password = os.getenv("POSTGRES_PASSWORD")


# Postgres connection
def create_connection():
    conn = psycopg.connect(
        dbname=postgres_db,
        user=postgres_user,
        password=postgres_password,
        host=postgres_host,
        port=5432,
    )
    return conn


# Postgres connection
conn = create_connection()

base_map = dl.Map(
    style={"height": "50vh", "zIndex": 10},
    id="map",
    center=[50.8503, 4.3517],
    zoom=2,
    children=[
        dl.TileLayer(),
        dl.LayerGroup(id="df_clusters"),
        dl.LayerGroup(id="df_clusters_images"),
    ],
)

YEAR_BOUND_INF, YEAR_BOUND_SUP, YEAR_INCREMENT = 1500, 2024, 50

date_range = dmc.RangeSlider(
    id="date_range",
    marks=[
        {"value": i, "label": i}
        for i in range(YEAR_BOUND_INF, YEAR_BOUND_SUP, YEAR_INCREMENT)
    ],
    min=YEAR_BOUND_INF,
    max=YEAR_BOUND_SUP,
    value=[2000, 2024],
    mb=30,
)

layout = html.Div(
    children=[
        dmc.SimpleGrid(
            cols={"base": 1, "sm": 2, "lg": 2},
            spacing={"base": 10, "sm": "xl"},
            verticalSpacing={"base": "md", "sm": "xl"},
            children=[
                html.Div(base_map),
                dmc.Stack(
                    [
                        dcc.Graph(id="count_per_year"),
                        date_range,
                    ]
                ),
            ],
            mb=30,
        ),
        html.Div(id="images"),
        dmc.SimpleGrid(
            cols={"base": 1, "sm": 1, "lg": 1},
            spacing={"base": 10, "sm": "xl"},
            verticalSpacing={"base": "md", "sm": "xl"},
            children=[
                html.Div(id="datatable"),
            ],
            mb=30,
        ),
    ],
)


@callback(
    Output("datatable", "children"),
    Output("images", "children"),
    Input("map", "bounds"),
    # Input("my_range_slider", "value")
)
def get_records(bounds, recordedby=None):
    if bounds is None:
        bounds = [[-90, -180], [90, 180]]

    parameters = (bounds[0][0], bounds[1][0], bounds[0][1], bounds[1][1])

    with open("get_records.sql", "r") as file:
        template = Template(file.read())
        sql_query = template.render(recordedby=recordedby)

    result = client.query(sql_query, parameters=parameters)
    column_names = ["path", "time", "lat", "lon", "make", "model", "lens_model"]
    df = pd.DataFrame(result.result_rows, columns=column_names)

    image_paths = df["path"].to_numpy()

    # Border color same as dmc.Table
    table = dash_table.DataTable(
        data=df.to_dict("records"),
        columns=[{"name": i, "id": i} for i in df.columns],
        style_table={"overflowX": "auto"},
        style_cell={
            "whiteSpace": "normal",
            "height": "auto",
            "font-family": "'Inter', sans-serif",
            "font-size": "14px",
            "padding": "0 1rem",
            "text-align": "left",
            "border": "1px solid #dee2e6",
        },
        style_header={"fontWeight": "bold"},
    )
    images = dmc.SimpleGrid(
        cols={"base": 4, "sm": 1, "lg": 4},
        spacing={"base": 10, "sm": "xl"},
        verticalSpacing={"base": "md", "sm": "xl"},
        children=[dmc.Image(radius="sm", src=p) for p in image_paths],
        mb=30,
    )
    return table, images


# Get trackbook points clustered
@callback(
    Output("df_clusters", "children"),
    Input("map", "bounds"),
    # Input("my_range_slider", "value"),
    # Input("my-dynamic-dropdown", "value")
)
def get_clusters_in_bbox(bounds):
    if bounds is None:
        bounds = [[-90, -180], [90, 180]]

    # parameters = (bounds[0][0], bounds[1][0], bounds[0][1], bounds[1][1], my_range_slider[0], my_range_slider[1], bounds[0][0], bounds[1][0], bounds[0][1], bounds[1][1], my_range_slider[0], my_range_slider[1])
    parameters = (
        bounds[0][0],
        bounds[1][0],
        bounds[0][1],
        bounds[1][1],
        bounds[0][0],
        bounds[1][0],
        bounds[0][1],
        bounds[1][1],
    )
    with open("clusters_in_bbox.sql", "r") as file:
        template = Template(file.read())
        # sql_query = template.render(recordedby=recordedby, classification=my_dynamic_dropdown)
        sql_query = template.render()
    result = client.query(sql_query, parameters=parameters)

    # Define column names
    column_names = ["cnt", "column_element", "latitude", "longitude"]

    # Convert the list of lists into a pandas DataFrame with specified column names
    df = pd.DataFrame(result.result_rows, columns=column_names)

    # logging.info(my_dynamic_dropdown)
    # logging.info(bounds)

    return [
        dl.CircleMarker(
            center=[row["latitude"], row["longitude"]],
            radius=2,
            fill=True,
            opacity=0.5,
            fillOpacity=0.5,
            children=[dl.Tooltip(f"Number of objects: {row['cnt']}")],
        )
        for index, row in df.iterrows()
    ]


# Get image points clustered
@callback(
    Output("df_clusters_images", "children"),
    Input("map", "bounds"),
    # Input("my_range_slider", "value"),
    # Input("my-dynamic-dropdown", "value")
)
def get_clusters_in_bbox(bounds):
    if bounds is None:
        bounds = [[-90, -180], [90, 180]]

    # parameters = (bounds[0][0], bounds[1][0], bounds[0][1], bounds[1][1], my_range_slider[0], my_range_slider[1], bounds[0][0], bounds[1][0], bounds[0][1], bounds[1][1], my_range_slider[0], my_range_slider[1])
    parameters = (
        bounds[0][0],
        bounds[1][0],
        bounds[0][1],
        bounds[1][1],
        bounds[0][0],
        bounds[1][0],
        bounds[0][1],
        bounds[1][1],
    )
    with open("clusters_in_bbox_images.sql", "r") as file:
        template = Template(file.read())
        # sql_query = template.render(recordedby=recordedby, classification=my_dynamic_dropdown)
        sql_query = template.render()
    result = client.query(sql_query, parameters=parameters)

    # Define column names
    column_names = ["cnt", "column_element", "latitude", "longitude"]

    # Convert the list of lists into a pandas DataFrame with specified column names
    df = pd.DataFrame(result.result_rows, columns=column_names)

    # logging.info(my_dynamic_dropdown)
    # logging.info(bounds)

    return [
        dl.CircleMarker(
            center=[row["latitude"], row["longitude"]],
            radius=5,
            fill=True,
            opacity=0.6,
            fillOpacity=0.6,
            color="red",
            children=[dl.Tooltip(f"Number of objects: {row['cnt']}")],
        )
        for index, row in df.iterrows()
    ]
