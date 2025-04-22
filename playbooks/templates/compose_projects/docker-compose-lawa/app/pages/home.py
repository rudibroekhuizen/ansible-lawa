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
import plotly.graph_objects as go
from datetime import datetime
from dash.exceptions import PreventUpdate


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

PLOTLY_FMT = "%Y-%m-%d %H:%M:%S.%f"  # example: 2021-03-25 11:44:31.8968
PLOTLY_FMT_SEC = "%Y-%m-%d %H:%M:%S"  # example: 2021-03-25 11:44:31
PLOTLY_FMT_MIN = "%Y-%m-%d %H:%M"  # example: 2021-03-25 11:44
PLOTLY_FMT_DAY = "%Y-%m-%d"  # example: 2021-03-25


def plotly_to_datetime(plotly_string):
    fmts = [PLOTLY_FMT, PLOTLY_FMT_SEC, PLOTLY_FMT_MIN, PLOTLY_FMT_DAY]
    for fmt in fmts:
        try:
            dt = datetime.strptime(plotly_string, fmt)
            return dt.strftime("%Y-%m-%d")  # Format output as 'YYYY-MM-DD'
            # return datetime.strptime(plotly_string, fmt).year
        except ValueError:
            continue
    return None
    # raise ValueError('Could not parse datetime from "{}"'.format(plotly_string))


# YEAR_BOUND_INF, YEAR_BOUND_SUP, YEAR_INCREMENT = 1500, 2024, 50

# date_range = dmc.RangeSlider(
#     id="date_range",
#     marks=[
#         {"value": i, "label": i}
#         for i in range(YEAR_BOUND_INF, YEAR_BOUND_SUP, YEAR_INCREMENT)
#     ],
#     min=YEAR_BOUND_INF,
#     max=YEAR_BOUND_SUP,
#     value=[2000, 2024],
#     mb=30,
# )

layout = html.Div(
    children=[
        dmc.SimpleGrid(
            cols={"base": 1, "sm": 2, "lg": 2},
            spacing={"base": 10, "sm": "xl"},
            verticalSpacing={"base": "md", "sm": "xl"},
            children=[
                dl.Map(
                    style={"height": "50vh", "zIndex": 10},
                    id="map",
                    center=[50.8503, 4.3517],
                    zoom=2,
                    children=[
                        dl.TileLayer(),
                        dl.LayerGroup(id="df_clusters"),
                        dl.LayerGroup(id="df_clusters_images"),
                    ],
                ),
                dmc.Stack(
                    [
                        dmc.Text(id="selected_date_range"),
                        dcc.Graph(
                            id="count_per_day",
                            config={
                                "modeBarButtonsToRemove": [
                                    "select2d",
                                    "lasso2d",
                                ],  # Remove lasso and rectangle select
                                "displayModeBar": True,  # Display the mode bar
                            },
                        ),
                        dmc.Text(
                            "A nonexistent object was used in an `Output` of a Dash callback",
                            id="output-selected-range",
                            style={"display": "none"},
                        ),
                    ]
                ),
                # dmc.Stack(
                #     [
                #         dcc.Graph(id="count_per_day"),
                #         date_range,
                #     ]
                # ),
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
    Output("count_per_day", "figure"),
    # Output("intermediate-value-form", "data"),
    Input("map", "bounds"),
    Input("output-selected-range", "children"),
    # Input("mode", "value"),
    # Input("date_range", "value"),
    # Input("multi_select", "value"),
    # Input("multi_select_collection", "value"),
    # Input("text_input_recordedby", "value"),
)
def get_count_per_day(
    bounds,
    date_range,
    # mode
):

    if bounds is None:
        bounds = [[-90, -180], [90, 180]]
    else:
        bounds = bounds

    parameters = (
        bounds[0][0],
        bounds[1][0],
        bounds[0][1],
        bounds[1][1],
        date_range[0],
        date_range[1],
    )

    # logging.info(f"date_range: {date_range}")

    with open("count_per_day.sql", "r") as file:
        template = Template(file.read())
        sql_query = template.render()
    result = client.query(sql_query, parameters=parameters)
    # result = client.query(sql_query)

    column_names = ["day", "cnt"]

    df = pd.DataFrame(result.result_rows, columns=column_names)

    fig = go.Figure(
        go.Scatter(
            x=df["day"],
            y=df["cnt"],
            mode="markers",
            # mode="lines+markers",
            # marker_color="blue"
        )
    )

    # logging.info(df)
    # logging.info(sql_query)
    # logging.info(parameters)

    # fig.layout.template = 'plotly_dark'

    # Add range selector and range slider to the x-axis
    fig.update_layout(
        dragmode="zoom",  # Enable selection mode
        uirevision=True,
        # selectdirection="h",
        xaxis=dict(
            rangeselector=dict(
                buttons=list(
                    [
                        dict(count=10, label="10y", step="year", stepmode="backward"),
                        dict(count=50, label="50y", step="year", stepmode="backward"),
                        dict(count=100, label="100y", step="year", stepmode="backward"),
                        # dict(count=1, label="YTD", step="year", stepmode="todate"),
                        # dict(count=1, label="1y", step="year", stepmode="backward"),
                        # dict(step="all")
                    ]
                )
            ),
            # tickmode='array',
            # tickvals=df['year'],
            # ticktext=df['year'],
            # rangeslider=dict(visible=True),
            # range=date_range or [1500, 2000],
            type="date",
            # tickformat="%Y",
            tickformat="%Y-%m-%d",
        ),
        yaxis=dict(
            fixedrange=True, autorange=True  # Prevent vertical zooming and panning
        ),
        # title="Bar Chart with Date Range Selector",
    )

    return fig


# Callback to capture and display the x-axis range
@callback(
    Output("output-selected-range", "children"),
    Input("count_per_day", "relayoutData"),
    # State('range-store', 'data')
)
def display_selected_range(relayoutData):
    # Check if x-axis range is defined in relayoutData
    start_date = None
    end_date = None

    # logging.info(relayoutData)

    if relayoutData:
        # logging.info(f"relayoutData: {relayoutData}")
        # Handle both formats of x-axis range data
        if "xaxis.range" in relayoutData:
            start_date, end_date = relayoutData["xaxis.range"]
            sd = plotly_to_datetime(start_date)
            ed = plotly_to_datetime(end_date)

            return sd, ed
        elif "xaxis.range[0]" in relayoutData and "xaxis.range[1]" in relayoutData:
            start_date = relayoutData["xaxis.range[0]"]
            end_date = relayoutData["xaxis.range[1]"]
            sd = plotly_to_datetime(start_date)
            ed = plotly_to_datetime(end_date)

            # logging.info(f"Start: {start_date}, {sd}")
            # logging.info(f"End: {end_date}, {ed}")
            return sd, ed

        else:
            raise PreventUpdate

        # Filter data if start_date and end_date are available
        # if start_date and end_date:
        #     # return f"Selected Range: {start_date} to {end_date}"
        #     return sd, ed

    # return "Select a range to see data."
    return "2024-01-01", "2025-01-01"
    # return stored_range.get('xaxis.range', [1500, 2000])


@callback(
    Output("datatable", "children"),
    Output("images", "children"),
    Input("map", "bounds"),
    Input("output-selected-range", "children"),
    # Input("my_range_slider", "value")
)
def get_records(bounds, date_range):
    if bounds is None:
        bounds = [[-90, -180], [90, 180]]

    parameters = (
        bounds[0][0],
        bounds[1][0],
        bounds[0][1],
        bounds[1][1],
        date_range[0],
        date_range[1],
    )

    with open("get_records.sql", "r") as file:
        template = Template(file.read())
        sql_query = template.render()

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
    images = (
        dmc.SimpleGrid(
            [
                html.Div(
                    dmc.Image(src=img, style={"cursor": "pointer"}),
                    id={"type": "img", "index": i},
                )
                for i, img in enumerate(image_paths)
            ],
            cols={"base": 4, "sm": 1, "lg": 4},
            spacing={"base": 10, "sm": "xl"},
            verticalSpacing={"base": "md", "sm": "xl"},
            mb=30,
        ),
        dmc.Modal(
            id="image-modal",
            size="xl",
            children=dmc.Carousel(
                [dmc.CarouselSlide(dmc.Image(src=img)) for img in image_paths],
                id="carousel",
                withIndicators=False,
                loop=True,
            ),
        ),
    )
    return table, images


# Get trackbook points clustered
@callback(
    Output("df_clusters", "children"),
    Input("map", "bounds"),
    Input("output-selected-range", "children"),
    # Input("my_range_slider", "value"),
    # Input("my-dynamic-dropdown", "value")
)
def get_clusters_in_bbox(bounds, date_range):
    if bounds is None:
        bounds = [[-90, -180], [90, 180]]

    # parameters = (bounds[0][0], bounds[1][0], bounds[0][1], bounds[1][1], my_range_slider[0], my_range_slider[1], bounds[0][0], bounds[1][0], bounds[0][1], bounds[1][1], my_range_slider[0], my_range_slider[1])
    parameters = (
        bounds[0][0],
        bounds[1][0],
        bounds[0][1],
        bounds[1][1],
        date_range[0],
        date_range[1],
        bounds[0][0],
        bounds[1][0],
        bounds[0][1],
        bounds[1][1],
        date_range[0],
        date_range[1],
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
    Input("output-selected-range", "children"),
    # Input("my_range_slider", "value"),
    # Input("my-dynamic-dropdown", "value")
)
def get_clusters_in_bbox(bounds, date_range):
    if bounds is None:
        bounds = [[-90, -180], [90, 180]]

    parameters = (
        bounds[0][0],
        bounds[1][0],
        bounds[0][1],
        bounds[1][1],
        date_range[0],
        date_range[1],
        bounds[0][0],
        bounds[1][0],
        bounds[0][1],
        bounds[1][1],
        date_range[0],
        date_range[1],
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


@callback(
    Output("selected_date_range", "children"),
    Input("output-selected-range", "children"),
)
def print_data_range(date_range):

    start_date, end_date = date_range[0], date_range[1]
    date_range_str = f"Selected date range: {start_date} to {end_date}"
    return date_range_str

@callback(
    Output("image-modal", "opened"),
    Output("carousel", "initialSlide"),
    Input({"type": "img", "index": dash.ALL}, "n_clicks"),
    prevent_initial_call=True,
)
def open_modal(n_clicks):
    index = ctx.triggered_id.index
    return True, index

