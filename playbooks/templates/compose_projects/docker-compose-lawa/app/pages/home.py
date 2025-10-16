import dash
from dash import html, dcc, Input, Output, callback
import plotly.graph_objects as go
import logging
import datetime
import dash_leaflet as dl
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
    Patch,
    no_update,
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
from jinja2 import Template
import plotly.express as px
import numpy
import psycopg
import plotly.graph_objects as go
from dash.exceptions import PreventUpdate
import urllib.parse
import dash_ag_grid as dag

from utils import (
    get_clickhouse_client,
    plotly_to_datetime,
    data_for_track_select,
    get_resolution_from_zoom,
    get_icon_size_from_zoom,
)

# Configure logging to print to console
logging.basicConfig(level=logging.INFO)

client = get_clickhouse_client()

dash.register_page(
    __name__,
    path="/",
)


def layout(
    start_date="2024-01-01",
    end_date="2026-01-01",
    min_lat=51.75,
    max_lat=55.55,
    min_lon=None,
    max_lon=None,
    center_lat=52.8503,
    center_lon=4.3517,
    # data = ["Pandas", "NumPy", "TensorFlow", "PyTorch"]
):
    return html.Div(
        [
            dcc.Location(id="url_test", refresh=False),
            dmc.SimpleGrid(
                cols={"base": 1, "sm": 2, "lg": 2},
                spacing={"base": 10, "sm": "xl"},
                verticalSpacing={"base": "md", "sm": "xl"},
                children=[
                    dmc.Stack(
                        [
                            dl.Map(
                                style={"height": "50vh", "zIndex": 10},
                                id="map",
                                bounds=[[min_lat, min_lon], [max_lat, max_lon]],
                                center={"lat": center_lat, "lng": center_lon},
                                boxZoom=True,
                                children=[
                                    dl.TileLayer(),
                                    dl.FullScreenControl(),
                                    dl.LayerGroup(id="df_clusters2"),
                                    dl.LayerGroup(id="df_clusters_images1"),
                                    dl.LayerGroup(id="start_points"),
                                    dl.LayerGroup(id="end_points"),
                                ],
                            ),
                            dmc.Select(
                                id="select_track",
                                label="Select track",
                                placeholder="Placeholder",
                                searchable=False,
                                # w=500,
                                data=data_for_track_select(client),
                                # data=data
                            ),
                        ],
                        # align="center",
                        gap="xl",
                    ),
                    dmc.Stack(
                        [
                            dcc.Graph(
                                id="graph_date_range",
                                style={"height": "50vh", "color": "black"},
                                config={
                                    "modeBarButtonsToRemove": [
                                        "select2d",
                                        "lasso2d",
                                        "toImage",
                                        "resetScale2d",
                                        # "autoscale",
                                    ],
                                    "doubleClick": False,
                                    "showTips": False,
                                    "scrollZoom": True,
                                    "watermark": False,
                                    "displaylogo": False,
                                },
                                figure={
                                    # "data": [{"x": x_data, "y": y_data, "mode": "markers"}],
                                    "layout": {
                                        "xaxis": {
                                            "rangeselector": {
                                                "buttons": [
                                                    dict(
                                                        count=10,
                                                        label="10y",
                                                        step="year",
                                                        stepmode="backward",
                                                    ),
                                                    dict(
                                                        count=50,
                                                        label="50y",
                                                        step="year",
                                                        stepmode="backward",
                                                    ),
                                                    dict(
                                                        count=100,
                                                        label="100y",
                                                        step="year",
                                                        stepmode="backward",
                                                    ),
                                                ]
                                            },
                                            "range": [start_date, end_date],
                                            "type": "date",
                                            # "dtick": "D1",
                                            # "tickformat": "%Y-%m-%d %H:%M",
                                            "tickformat": "%Y-%m-%d",
                                            "tickformatstops": [
                                                #     # Stop showing hours/minutes when zoomed in too far
                                                #     dict(
                                                #         dtickrange=[0, 86400000],  # From 0 ms to 1 day (86,400,000 ms)
                                                #         value="%Y-%m-%d"             # Show days, also in period 0 ms to 1 day
                                                #     ),
                                                #     # Stop showing hours/minutes when zoomed in too far
                                                #     # dict(
                                                #     #     dtickrange=[0, 86400000],  # From 0 ms to 1 day (86,400,000 ms)
                                                #     #     value="%H:%M"             # Still show hours/minutes if within this range
                                                #     # ),
                                                #     dict(
                                                #         dtickrange=[86400000, None], # From 1 day onwards
                                                #         value="%Y-%m-%d"             # Show only day, month, year
                                                #     )
                                                dict(
                                                    dtickrange=[
                                                        0,
                                                        86400000 - 1,
                                                    ],  # Just shy of one day
                                                    value="%Y-%m-%d",  # Still show only day, month, year. Prevents hour/minute.
                                                ),
                                                dict(
                                                    dtickrange=[
                                                        86400000,
                                                        None,
                                                    ],  # From one day onwards
                                                    value="%Y-%m-%d",  # Show only day, month, year
                                                ),
                                            ],
                                        },
                                        "yaxis": {
                                            "fixedrange": True,
                                            "autorange": True,  # Prevent vertical zooming and panning
                                        },
                                        "hovermode": "closest",
                                    },
                                },
                            ),
                            dmc.Text(id="selected_date_range"),
                        ]
                    ),
                ],
                mb=30,
            ),
            dmc.SimpleGrid(
                cols={"base": 1, "sm": 1, "lg": 1},
                spacing={"base": 10, "sm": "xl"},
                verticalSpacing={"base": "md", "sm": "xl"},
                children=[
                    html.Div(id="nice_stack"),
                ],
                mb=30,
            ),
            html.Div(id="images1"),
            dmc.Text(
                "A nonexistent object was used in an `Output` of a Dash callback",
                id="carousel",
                style={"display": "none"},
            ),
            dmc.Text(
                "A nonexistent object was used in an `Output` of a Dash callback",
                id="image-modal",
                style={"display": "none"},
            ),
            dmc.SimpleGrid(
                cols={"base": 1, "sm": 1, "lg": 1},
                spacing={"base": 10, "sm": "xl"},
                verticalSpacing={"base": "md", "sm": "xl"},
                children=[
                    html.Div(id="datatable1"),
                ],
                mb=30,
            ),
        ]
    )


layout = layout


# Update the url
@callback(
    Output("url_test", "search"),
    Input("graph_date_range", "figure"),
    Input("graph_date_range", "relayoutData"),
    Input("map", "bounds"),
    Input("map", "center"),
    prevent_initial_call=True,
)
def update_url_from_slider(
    graph_date_range, graph_date_range_relayoutdata, bounds, center
):
    # def update_url_from_slider(graph_date_range, bounds, center):

    # Time
    # start_date, end_date = selected_date_range(graph_date_range)
    start_date = plotly_to_datetime(graph_date_range["layout"]["xaxis"]["range"][0])
    end_date = plotly_to_datetime(graph_date_range["layout"]["xaxis"]["range"][1])

    # logging.info(f"update_url start and end date {start_date}, {end_date}")

    # Location, center
    center_lat = center["lat"]
    center_lon = center["lng"]

    # Location, bounds
    min_lat = bounds[0][0]  # south -90
    max_lat = bounds[1][0]  # north 90
    min_lon = bounds[0][1]  # west -180
    max_lon = bounds[1][1]  # east 180

    params = {
        "start_date": start_date,
        "end_date": end_date,
        "max_lat": max_lat,
        "min_lat": min_lat,
        "max_lon": max_lon,
        "min_lon": min_lon,
        "center_lat": center_lat,
        "center_lon": center_lon,
    }
    query_string = urllib.parse.urlencode(params)
    return f"?{query_string}"


# Update the viewport of the map based on selected track
@callback(
    Output("map", "viewport"), Input("select_track", "value"), prevent_initial_call=True
)
def fly_to_selected_track(st):
    # center_lat=52
    # center_lon=4
    # zoom = 10
    # return dict(center=[51.67, 3.76], zoom=9, transition="flyTo")
    with open("select_tracks.sql", "r") as file:
        template = Template(file.read())
        sql_query = template.render(
            st=st,
        )

    df = client.query_df(sql_query)

    if not df.empty:
        center_lat = df["center_lat"].iloc[0]  # Get the first (and likely only) value
        center_lon = df["center_lon"].iloc[0]  # Get the first (and likely only) value

    return dict(center=[center_lat, center_lon], zoom=11, transition="flyTo")


# Update the date range of the graph range based on selected track
@callback(
    Output("graph_date_range", "figure", allow_duplicate=True),
    Input("select_track", "value"),
    State("graph_date_range", "figure"),
    prevent_initial_call=True,
)
def update_range(st, graph_date_range):
    with open("select_tracks.sql", "r") as file:
        template = Template(file.read())
        sql_query = template.render(
            st=st,
        )

    df = client.query_df(sql_query)
    # logging.info(f"Date range based on selected track {df}")
    # df = client.query_df("select * from trackbook_summary")
    # df = client.query_df(f"SELECT start_date, end_date FROM trackbook_summary WHERE description = '{st}'")

    if not df.empty:
        start_date = plotly_to_datetime(df["start_date"].iloc[0])
        end_date = plotly_to_datetime(df["end_date"].iloc[0])

    # logging.info(f"Update date range dcc.Graph {start_date}, {end_date}")

    graph_date_range = Patch()
    graph_date_range["layout"]["xaxis"]["range"] = [start_date, end_date]

    return graph_date_range


# Get trackbook points clustered
@callback(
    Output("df_clusters2", "children"),
    Input("graph_date_range", "figure"),
    Input("graph_date_range", "relayoutData"),
    Input("map", "bounds"),
    Input("map", "zoom"),
    prevent_initial_call=True,
)
def get_clusters_in_bbox_points(
    graph_date_range, graph_date_range_relayoutdata, bounds, zoom
):

    # if ctx.triggered_id in ["graph_date_range", "map"]:

    start_date = plotly_to_datetime(graph_date_range["layout"]["xaxis"]["range"][0])
    end_date = plotly_to_datetime(graph_date_range["layout"]["xaxis"]["range"][1])

    min_lat = bounds[0][0]  # south -90
    max_lat = bounds[1][0]  # north 90
    min_lon = bounds[0][1]  # west -180
    max_lon = bounds[1][1]  # east 180

    resolution = get_resolution_from_zoom(zoom)

    # with open("clusters_in_bbox.sql", "r") as file:
    with open("clusters_in_bbox_approx_top.sql", "r") as file:
        template = Template(file.read())

        sql_query = template.render(
            table=f"lawa.trackbook_agg_h3_{resolution}",
            min_lat=min_lat,
            max_lat=max_lat,
            min_lon=min_lon,
            max_lon=max_lon,
            start_date=start_date,
            end_date=end_date,
        )

    df = client.query_df(sql_query)

    # result = client.query(sql_query, parameters=parameters)

    logging.info(f"Zoom {zoom}")
    # logging.info(f"Query {sql_query}")
    # logging.info(df)

    # result = client.query(sql_query)
    # result = generate_sql_query(bounds, zoom, date_range, mode, "clusters_in_bbox.sql")

    # column_names = ["h3_cell", "boundary", "cnt"]

    # df = pd.DataFrame(result.result_rows, columns=column_names)

    if not df.empty:
        # Add additional column
        # df["h3_2_list"] = df["h3_2"].apply(get_geo_boundary)

        # Calculate opacity of cells
        df["opacity"] = df["cnt"] / (df["cnt"].max()).round(3) - 0.35

    pg = [
        dl.Polygon(
            # id="poly_id",
            positions=row["boundary"],
            color="blue",
            # opacity=0.15,
            opacity=1,
            weight=2,
            children=[
                # dl.Tooltip(f"Index: {row['h3_2']}"),
                # dl.Popup(f"Index: {row['h3_2']}, count: {row['cnt']}")
                # dl.Popup(f"Count: {row['cnt']}")
                dl.Popup(
                    children=[
                        # html.P(f"Track: {row['description.item']}"), # Using untuple
                        html.P(f"Track: {row['description_top_app']}"),
                        # html.P(f"Count: {row['cnt']}"), # Only count
                        # html.Small(f"Opacity: {row['cnt']}") # Smaller text
                    ]
                )
            ],
            # pathOptions={"fillOpacity": row["opacity"]},
        )
        for index, row in df.iterrows()
    ]

    return pg

    # # Define column names
    # column_names = ["cnt", "column_element", "latitude", "longitude"]

    # # Convert the list of lists into a pandas DataFrame with specified column names
    # df = pd.DataFrame(result.result_rows, columns=column_names)

    # return [
    #     dl.CircleMarker(
    #         center=[row["latitude"], row["longitude"]],
    #         radius=2,
    #         fill=True,
    #         opacity=0.5,
    #         fillOpacity=0.5,
    #         children=[dl.Tooltip(f"Number of objects: {row['cnt']}")],
    #     )
    #     for index, row in df.iterrows()
    # ]


# Get image points clustered
@callback(
    Output("df_clusters_images1", "children"),
    Input("graph_date_range", "figure"),
    Input("graph_date_range", "relayoutData"),
    Input("map", "bounds"),
    Input("map", "zoom"),
    prevent_initial_call=True,
)
def get_clusters_in_bbox(graph_date_range, graph_date_range_relayoutdata, bounds, zoom):

    start_date = plotly_to_datetime(graph_date_range["layout"]["xaxis"]["range"][0])
    end_date = plotly_to_datetime(graph_date_range["layout"]["xaxis"]["range"][1])

    min_lat = bounds[0][0]  # south -90
    max_lat = bounds[1][0]  # north 90
    min_lon = bounds[0][1]  # west -180
    max_lon = bounds[1][1]  # east 180

    resolution = get_resolution_from_zoom(zoom)

    with open("clusters_in_bbox_images.sql", "r") as file:
        template = Template(file.read())
        sql_query = template.render(
            table=f"lawa.image_exif_agg_h3_{resolution}",
            min_lat=min_lat,
            max_lat=max_lat,
            min_lon=min_lon,
            max_lon=max_lon,
            start_date=start_date,
            end_date=end_date,
        )

    df = client.query_df(sql_query)

    # result = client.query(sql_query)
    # column_names = ["h3_cell", "boundary", "cnt"]
    # df = pd.DataFrame(result.result_rows, columns=column_names)

    if not df.empty:
        # Add additional column
        # df["h3_2_list"] = df["h3_2"].apply(get_geo_boundary)

        # Calculate opacity of cells
        df["opacity"] = df["cnt"] / (df["cnt"].max()).round(3) - 0.35

    pg = [
        dl.Polygon(
            # id="poly_id",
            positions=row["boundary"],
            color="red",
            opacity=0.15,
            weight=2,
            children=[
                # dl.Tooltip(f"Index: {row['h3_2']}"),
                # dl.Popup(f"Index: {row['h3_2']}, count: {row['cnt']}")
                dl.Popup(f"Count: {row['cnt']}")
            ],
            pathOptions={"fillOpacity": row["opacity"]},
        )
        for index, row in df.iterrows()
    ]

    return pg


# Plot start points of track
@callback(
    Output("start_points", "children"),
    Input("graph_date_range", "figure"),
    Input("graph_date_range", "relayoutData"),
    Input("map", "bounds"),
    Input("map", "zoom"),
    prevent_initial_call=True,
)
def get_clusters_in_bbox(graph_date_range, graph_date_range_relayoutdata, bounds, zoom):

    start_date = plotly_to_datetime(graph_date_range["layout"]["xaxis"]["range"][0])
    end_date = plotly_to_datetime(graph_date_range["layout"]["xaxis"]["range"][1])

    min_lat = bounds[0][0]  # south -90
    max_lat = bounds[1][0]  # north 90
    min_lon = bounds[0][1]  # west -180
    max_lon = bounds[1][1]  # east 180

    resolution = get_resolution_from_zoom(zoom)

    with open("start_points.sql", "r") as file:
        template = Template(file.read())
        sql_query = template.render(
            # table=f"lawa.image_exif_agg_h3_{resolution}",
            min_lat=min_lat,
            max_lat=max_lat,
            min_lon=min_lon,
            max_lon=max_lon,
            start_date=start_date,
            end_date=end_date,
        )

    df = client.query_df(sql_query)

    # result = client.query(sql_query)
    # column_names = ["h3_cell", "boundary", "cnt"]
    # df = pd.DataFrame(result.result_rows, columns=column_names)

    # if not df.empty:
    # Add additional column
    # df["h3_2_list"] = df["h3_2"].apply(get_geo_boundary)

    # Calculate opacity of cells
    # df["opacity"] = df["cnt"] / (df["cnt"].max()).round(3) - 0.35

    marker_size = get_icon_size_from_zoom(zoom)

    markers = [
        dl.Marker(
            position=[row["start_lat"], row["start_lon"]],
            icon=dict(
                iconUrl="https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-green.png",
                iconSize=marker_size,
                iconAnchor=[marker_size[0] / 2, marker_size[1]],  # [12, 41],
                popupAnchor=[1, -marker_size[1] * 0.8],  # [1, -34],
            ),
            children=[
                # dl.Tooltip(f"Index: {index}"), # Optional tooltip
                dl.Popup(
                    f"Start marker of track {row['description']}"
                )  # Popup showing count
            ],
            # Optionally use other row data for styling or identification
            # id=f"marker-{index}"
        )
        for index, row in df.iterrows()
    ]

    logging.info(f"Icon size: {get_icon_size_from_zoom(zoom)}")
    return markers


# Plot end points of tracks
@callback(
    Output("end_points", "children"),
    Input("graph_date_range", "figure"),
    Input("graph_date_range", "relayoutData"),
    Input("map", "bounds"),
    Input("map", "zoom"),
    prevent_initial_call=True,
)
def get_clusters_in_bbox(graph_date_range, graph_date_range_relayoutdata, bounds, zoom):

    start_date = plotly_to_datetime(graph_date_range["layout"]["xaxis"]["range"][0])
    end_date = plotly_to_datetime(graph_date_range["layout"]["xaxis"]["range"][1])

    min_lat = bounds[0][0]  # south -90
    max_lat = bounds[1][0]  # north 90
    min_lon = bounds[0][1]  # west -180
    max_lon = bounds[1][1]  # east 180

    resolution = get_resolution_from_zoom(zoom)

    with open("end_points.sql", "r") as file:
        template = Template(file.read())
        sql_query = template.render(
            # table=f"lawa.image_exif_agg_h3_{resolution}",
            min_lat=min_lat,
            max_lat=max_lat,
            min_lon=min_lon,
            max_lon=max_lon,
            start_date=start_date,
            end_date=end_date,
        )

    df = client.query_df(sql_query)

    marker_size = get_icon_size_from_zoom(zoom)

    markers = [
        dl.Marker(
            position=[row["end_lat"], row["end_lon"]],
            icon=dict(
                iconUrl="https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-red.png",
                iconSize=marker_size,
                iconAnchor=[marker_size[0] / 2, marker_size[1]],  # [12, 41],
                popupAnchor=[1, -marker_size[1] * 0.8],  # [1, -34],
                # iconSize=[25, 41],
                # iconAnchor=[12, 41],
                # popupAnchor=[1, -34],
            ),
            children=[
                # dl.Tooltip(f"Index: {index}"), # Optional tooltip
                dl.Popup(
                    f"End marker of track {row['description']}"
                )  # Popup showing count
            ],
        )
        for index, row in df.iterrows()
    ]

    return markers


# Trackbook summary table
@callback(
    Output("nice_stack", "children"),
    Input("graph_date_range", "figure"),
    Input("graph_date_range", "relayoutData"),
    Input("map", "bounds"),
    Input("map", "zoom"),
    prevent_initial_call=True,
)
def summary(graph_date_range, graph_date_range_relayoutdata, bounds, zoom):

    # if ctx.triggered_id in ["graph_date_range", "map"]:

    start_date = plotly_to_datetime(graph_date_range["layout"]["xaxis"]["range"][0])
    end_date = plotly_to_datetime(graph_date_range["layout"]["xaxis"]["range"][1])

    min_lat = bounds[0][0]  # south -90
    max_lat = bounds[1][0]  # north 90
    min_lon = bounds[0][1]  # west -180
    max_lon = bounds[1][1]  # east 180

    resolution = get_resolution_from_zoom(zoom)

    with open("trackbook_summary.sql", "r") as file:
        template = Template(file.read())

        sql_query = template.render(
            table=f"lawa.trackbook_agg_h3_{resolution}",
            min_lat=min_lat,
            max_lat=max_lat,
            min_lon=min_lon,
            max_lon=max_lon,
            start_date=start_date,
            end_date=end_date,
        )

    df = client.query_df(sql_query)

    if not df.empty:

        result = [
            dag.AgGrid(
                rowData=df.to_dict("records"),
                columnDefs=[{"field": i} for i in df.columns],
            )
            # dmc.Stack(
            #     [
            #         dmc.Text(f"Description {row['description']}"),
            #         dmc.Text(f"Start {row['start_date']}"),
            #     ],
            #     align="center",
            #     gap="xl",
            # )
            # for index, row in df.iterrows()
            # WORKING:
            # dmc.Card(
            #     children=[
            #         dmc.Text(
            #             f"Description: {row['description']}",
            #             size="sm",
            #         ),
            #         dmc.Text(
            #             f"Start: {row['start_date']}",
            #             size="sm",
            #         ),
            #     ],
            #     withBorder=True,
            #     shadow="sm",
            #     radius="md",
            #     w={"base": 200, "sm": 400, "lg": 500},
            #     #w=450,
            #     mb=10,
            # )
            # for index, row in df.iterrows()
            # dl.Polygon(
            #     # id="poly_id",
            #     positions=row["boundary"],
            #     color="blue",
            #     opacity=0.15,
            #     weight=2,
            #     children=[
            #         # dl.Tooltip(f"Index: {row['h3_2']}"),
            #         # dl.Popup(f"Index: {row['h3_2']}, count: {row['cnt']}")
            #         # dl.Popup(f"Count: {row['cnt']}")
            #         dl.Popup(
            #             children=[
            #                 # html.P(f"Track: {row['description.item']}"), # Using untuple
            #                 # html.P(f"Track: {row['description_top_app']}"),
            #                 html.P(f"Count: {row['cnt']}"), # Paragraph for spacing
            #                 # html.Small(f"Opacity: {row['cnt']}") # Smaller text
            #             ]
            #         )
            #     ],
            #     pathOptions={"fillOpacity": row["opacity"]},
            # )
            # for index, row in df.iterrows()
        ]

        return result
    else:
        return None


# Create image grid and table with image info
@callback(
    Output("datatable1", "children"),
    Output("images1", "children"),
    Input("graph_date_range", "figure"),
    Input("graph_date_range", "relayoutData"),
    Input("map", "bounds"),  # map
    prevent_initial_call=True,
)
def get_records(graph_date_range, graph_date_range_relayoutdata, bounds):

    start_date = plotly_to_datetime(graph_date_range["layout"]["xaxis"]["range"][0])
    end_date = plotly_to_datetime(graph_date_range["layout"]["xaxis"]["range"][1])

    min_lat = bounds[0][0]  # south -90
    max_lat = bounds[1][0]  # north 90
    min_lon = bounds[0][1]  # west -180
    max_lon = bounds[1][1]  # east 180

    with open("get_records.sql", "r") as file:
        template = Template(file.read())
        sql_query = template.render(
            min_lat=min_lat,
            max_lat=max_lat,
            min_lon=min_lon,
            max_lon=max_lon,
            start_date=start_date,
            end_date=end_date,
        )

    # result = client.query(sql_query, parameters=parameters)
    df = client.query_df(sql_query)
    # result = client.query(sql_query)
    # column_names = ["path", "time", "lat", "lon", "make", "model", "lens_model"]
    # df = pd.DataFrame(result.result_rows, columns=column_names)

    if not df.empty:
        image_paths = df["path"].to_numpy()

        table = dag.AgGrid(
            rowData=df.to_dict("records"),
            columnDefs=[{"field": i} for i in df.columns],
        )

        # table = dash_table.DataTable(
        #     data=df.to_dict("records"),
        #     columns=[{"name": i, "id": i} for i in df.columns],
        #     style_table={"overflowX": "auto"},
        #     style_cell={
        #         "whiteSpace": "normal",
        #         "height": "auto",
        #         "font-family": "'Inter', sans-serif",
        #         "font-size": "14px",
        #         "padding": "0 1rem",
        #         "text-align": "left",
        #         "border": "1px solid #dee2e6",
        #     },
        #     style_header={"fontWeight": "bold"},
        # )
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
            # dmc.Modal(
            #     id="image-modal",
            #     size="xl",
            #     children=dmc.Carousel(
            #         [dmc.CarouselSlide(dmc.Image(src=img)) for img in image_paths],
            #         id="carousel",
            #         withIndicators=False,
            #         loop=True,
            #     ),
            # ),
            dmc.Modal(
                id="image-modal",
                # size="xl",
                fullScreen=True,
                children=dmc.Carousel(
                    [
                        dmc.CarouselSlide(
                            # dmc.Stack(
                            #     [
                            #         dmc.Image(src=row["path"]),
                            #         dmc.Text(f"Date: {row['time']}"),
                            #         dmc.Text(f"Model: {row['model']}"),
                            #     ],
                            #     align="center",
                            #     gap="xl",
                            # )
                            dmc.Image(
                                src=row["path"],
                                style={
                                    "width": "100vw",
                                    "height": "100vh",
                                    "objectFit": "contain",
                                },
                            )
                        )
                        for index, row in df.iterrows()
                    ],
                    id="carousel",
                    withIndicators=False,
                    loop=True,
                ),
            ),
        )
        return table, images
    else:
        return None, None


# Plot figure go.Scatter, count per day
@callback(
    Output("graph_date_range", "figure"),
    Input("graph_date_range", "figure"),
    Input("graph_date_range", "relayoutData"),
    Input("map", "bounds"),
    prevent_initial_call=True,
)
def get_count_per_day(graph_date_range, graph_date_range_relayoutdata, bounds):

    # logging.info(f"go.Scatter figure: {graph_date_range}")
    # logging.info(f"go.Scatter relayoutData: {graph_date_range_relayoutdata}")
    # logging.info(f"Start date count per day: {graph_date_range['layout']['xaxis']['range'][0]}")
    # logging.info(f"End date count per day: {graph_date_range['layout']['xaxis']['range'][1]}")

    start_date = plotly_to_datetime(graph_date_range["layout"]["xaxis"]["range"][0])
    end_date = plotly_to_datetime(graph_date_range["layout"]["xaxis"]["range"][1])

    # logging.info(start_date)
    # logging.info(end_date)

    min_lat = bounds[0][0]
    max_lat = bounds[1][0]
    min_lon = bounds[0][1]
    max_lon = bounds[1][1]

    with open("count_per_day.sql", "r") as file:
        template = Template(file.read())
        # sql_query = template.render()
        sql_query = template.render(
            min_lat=min_lat,
            max_lat=max_lat,
            min_lon=min_lon,
            max_lon=max_lon,
            start_date=start_date,
            end_date=end_date,
        )
    result = client.query(sql_query)

    column_names = ["day", "cnt"]

    df = pd.DataFrame(result.result_rows, columns=column_names)

    graph_date_range = Patch()
    graph_date_range["data"] = [{"x": df["day"], "y": df["cnt"], "mode": "markers"}]
    # graph_date_range["layout"]["title"]["text"] = "Time"

    return graph_date_range


@callback(
    Output("selected_date_range", "children"),
    Input("graph_date_range", "figure"),
    Input("graph_date_range", "relayoutData"),
)
def print_data_range(graph_date_range, graph_date_range_relayoutdata):

    start_date = plotly_to_datetime(graph_date_range["layout"]["xaxis"]["range"][0])
    end_date = plotly_to_datetime(graph_date_range["layout"]["xaxis"]["range"][1])

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
