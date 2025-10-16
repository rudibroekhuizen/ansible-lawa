import logging
import clickhouse_connect
from clickhouse_connect import common
from clickhouse_connect.driver import httputil
from dash.exceptions import PreventUpdate
import datetime
import os


def get_resolution_from_zoom(zoom):
    """
    Calculates the H3 resolution to use, based on zoom level.
    """
    if zoom > 17:
        return 13
    elif zoom == 17:
        return 13
    elif zoom == 16:
        return 13
    elif zoom == 15:
        return 12
    elif zoom == 14:
        return 11
    elif zoom == 13:
        return 10
    elif zoom == 12:
        return 10
    elif zoom == 11:
        return 9
    elif zoom == 10:
        return 9
    elif zoom == 9:
        return 8
    elif zoom == 8:
        return 7
    elif zoom == 7:
        return 6
    elif zoom == 6:
        return 5
    elif zoom == 5:
        return 5
    elif zoom == 4:
        return 4
    elif zoom == 3:
        return 3
    else:
        return 2


def get_icon_size_from_zoom(zoom: int) -> list[int]:
    """
    Calculates the size [width, height] for a marker icon based on the map's zoom level
    by applying a proportional scaling factor to a base size.
    """
    BASE_WIDTH = 25
    BASE_HEIGHT = 41

    if zoom > 17:
        scale_factor = 1.0 #1.5 # 50% larger
    elif zoom >= 15:
        scale_factor = 0.9 #1.2 # 20% larger
    elif zoom >= 12:
        scale_factor = 0.8 #1.0 # Base size
    elif zoom >= 9:
        scale_factor = 0.7 #0.8 # Base size
    else:
        scale_factor = 0.6  # 20% smaller for low zoom (regional view)

    new_width = int(BASE_WIDTH * scale_factor)
    new_height = int(BASE_HEIGHT * scale_factor)

    return [new_width, new_height]



# def get_icon_size_from_zoom(zoom):
#     """
#     Calculates the H3 resolution to use, based on zoom level.
#     """
#     if zoom > 17:
#         return 13
#     elif zoom == 17:
#         return 13
#     elif zoom == 16:
#         return 13
#     elif zoom == 15:
#         return 12
#     elif zoom == 14:
#         return 11
#     elif zoom == 13:
#         return 10
#     elif zoom == 12:
#         return 10
#     elif zoom == 11:
#         return 9
#     elif zoom == 10:
#         return 9
#     elif zoom == 9:
#         return 8
#     elif zoom == 8:
#         return 7
#     elif zoom == 7:
#         return 6
#     elif zoom == 6:
#         return 5
#     elif zoom == 5:
#         return 5
#     elif zoom == 4:
#         return 4
#     elif zoom == 3:
#         return 3
#     else:
#         return [20, 40]


# class SingleTone(type):
#     _instances: dict = {}
# 
#     def __call__(cls, *args, **kwargs):
#         if cls not in cls._instances:
#             cls._instances[cls] = super().__call__(*args, **kwargs)
# 
#         return cls._instances[cls]
# 
# 
# class ClickClient(metaclass=SingleTone):
#     def __init__(self):
#         #load_dotenv()
# 
#         common.set_setting("autogenerate_session_id", False)
# 
#         self._host = os.environ.get("CLICKHOUSE_HOST")
#         self._port = 8123
#         self._user = os.environ.get("CLICKHOUSE_USER")
#         self._password = os.environ.get("CLICKHOUSE_PASSWORD")
#         self._database = os.environ.get("CLICKHOUSE_DB")
#         self._click_client = clickhouse_connect.get_client(
#             host=self._host,
#             port=self._port,
#             user=self._user,
#             password=self._password,
#             database=self._database,
#         )


def get_clickhouse_client():
    # ClickHouse env vars
    clickhouse_db = os.getenv("CLICKHOUSE_DB")
    clickhouse_host = os.getenv("CLICKHOUSE_HOST")
    clickhouse_user = os.getenv("CLICKHOUSE_USER")
    clickhouse_pass = os.getenv("CLICKHOUSE_PASSWORD")

    # Clickhouse multi query
    common.set_setting("autogenerate_session_id", False)

    # Clickhouse pool manager
    big_pool_mgr = httputil.get_pool_manager(maxsize=16, num_pools=12)

    try:
        client = clickhouse_connect.get_client(
            pool_mgr=httputil.get_pool_manager(maxsize=16, num_pools=12),
            host=clickhouse_host,
            port=8123,
            user=clickhouse_user,
            password=clickhouse_pass,
            database=clickhouse_db,
        )
        # Optional: Test the connection to ensure it's valid
        client.ping()
        print("Successfully connected to ClickHouse!")
        return client
    except Exception as e:
        print(f"Error connecting to ClickHouse: {e}")
        return None


# def plotly_to_datetime(plotly_string):
#     """
#     Converts a Plotly-formatted date string to a datetime object.
#     Tries multiple formats to handle different levels of granularity.
#     """
#     fmts = [
#         "%Y-%m-%d %H:%M:%S.%f",  # example: 2021-03-25 11:44:31.8968
#         "%Y-%m-%d %H:%M:%S",     # example: 2021-03-25 11:44:31
#         "%Y-%m-%d %H:%M",        # example: 2021-03-25 11:44
#         "%Y-%m-%d"               # example: 2021-03-25
#     ]
# 
#     for fmt in fmts:
#         try:
#             return datetime.strptime(plotly_string, fmt).year
#         except ValueError:
#             continue
# 
#     return None


def plotly_to_datetime(plotly_string):
    PLOTLY_FMT = "%Y-%m-%d %H:%M:%S.%f"  # example: 2021-03-25 11:44:31.8968
    PLOTLY_FMT_SEC = "%Y-%m-%d %H:%M:%S"  # example: 2021-03-25 11:44:31
    PLOTLY_FMT_MIN = "%Y-%m-%d %H:%M"  # example: 2021-03-25 11:44
    PLOTLY_FMT_DAY = "%Y-%m-%d"  # example: 2021-03-25
    fmts = [PLOTLY_FMT, PLOTLY_FMT_SEC, PLOTLY_FMT_MIN, PLOTLY_FMT_DAY]
    for fmt in fmts:
        try:
            dt = datetime.datetime.strptime(plotly_string, fmt)
            return dt.strftime("%Y-%m-%d")  # Format wanted
        except ValueError:
            continue
    return None


# def selected_date_range(relayoutData):
#     if relayoutData is None:
#         raise PreventUpdate
# 
#     if "xaxis.range" in relayoutData:
#         start_date, end_date = relayoutData["xaxis.range"]
#         sd = plotly_to_datetime(start_date)
#         ed = plotly_to_datetime(end_date)
# 
#         return sd, ed
#     elif "xaxis.range[0]" in relayoutData and "xaxis.range[1]" in relayoutData:
#         start_date = relayoutData["xaxis.range[0]"]
#         end_date = relayoutData["xaxis.range[1]"]
#         sd = plotly_to_datetime(start_date)
#         ed = plotly_to_datetime(end_date)
# 
#         # logging.info(f"Start: {start_date}, {sd}")
#         # logging.info(f"End: {end_date}, {ed}")
#         return sd, ed
# 
#     else:
#         raise PreventUpdate





def data_for_track_select(client):
    # with open("select_tracks.sql", "r") as file:
    #     template = Template(file.read())

        # sql_query = template.render(
        #     table=table,
        #     min_lat=min_lat,
        #     max_lat=max_lat,   
        #     min_lon=min_lon,
        #     max_lon=max_lon,
        #     start_date=start_date,
        #     end_date=end_date,
        # )

    # df = client.query_df(sql_query)

    df = client.query_df("select * from trackbook_summary")

    description_array = df["description"].to_list()

    # If you specifically need a NumPy array:
    # import numpy as np
    # description_numpy_array = df["description"].to_numpy()

    # print(description_array)

    return description_array




# def graph_date_range_selector():
#     # with conn.cursor() as cur:
#     #     cur.execute("SELECT name FROM requestor")
#     #     rows = cur.fetchall()
# 
#     # column_names = ["requestor"]
#     # df_a = pd.DataFrame(rows, columns=column_names)
#     # df = df_a["requestor"].to_numpy()
#     return [2005, 2040]

# def graph_date_range_selector(conn):
#     with conn.cursor() as cur:
#         cur.execute("SELECT name FROM requestor")
#         rows = cur.fetchall()
# 
#     column_names = ["requestor"]
#     df_a = pd.DataFrame(rows, columns=column_names)
#     df = df_a["requestor"].to_numpy()
#     return df



# def generate_sql_query(bounds, zoom, date_range, sql_file):
#     """Generates an SQL query based on area and date range.
#
#     Args:
#         bounds: A list of lists representing the bounds [[min_lat, min_lon], [max_lat, max_lon]].
#         date_range: A list representing the date range [start_date, end_date].
#
#     Returns:
#         The generated SQL query string.
#     """
# 
#     if zoom > 13:
#         table = "db1.gbif_agg_h3_10"
#     elif zoom == 13:
#         table = "db1.gbif_agg_h3_7"
#     elif zoom == 12:
#         table = "db1.gbif_agg_h3_7"
#     elif zoom == 11:
#         table = "db1.gbif_agg_h3_6"
#     elif zoom == 10:
#         table = "db1.gbif_agg_h3_6"
#     elif zoom == 9:
#         table = "db1.gbif_agg_h3_5"
#     elif zoom == 8:
#         table = "db1.gbif_agg_h3_4"
#     elif zoom == 7:
#         table = "db1.gbif_agg_h3_4"
#     elif zoom == 6:
#         table = "db1.gbif_agg_h3_3"
#     elif zoom == 5:
#         table = "db1.gbif_agg_h3_2"
#     elif zoom == 4:
#         table = "db1.gbif_agg_h3_2"
#     elif zoom == 3:
#         table = "db1.gbif_agg_h3_1"
#     else:
#         table = "db1.gbif_agg_h3_1"
# 
#     start_date = plotly_to_datetime(graph_date_range["layout"]["xaxis"]["range"][0])
#     end_Date = plotly_to_datetime(graph_date_range["layout"]["xaxis"]["range"][1])
# 
#     min_lat = bounds[0][0]  # south -90
#     max_lat = bounds[1][0]  # north 90
#     min_lon = bounds[0][1]  # west -180
#     max_lon = bounds[1][1]  # east 180
# 
#     try:
#         with open(sql_file, "r") as file:
#             template = Template(file.read())
#             sql_query = template.render(
#                 min_lat=min_lat,
#                 max_lat=max_lat,
#                 min_lon=min_lon,
#                 max_lon=max_lon,
#                 start_date=start_date,
#                 end_date=end_date,
#                 table=table,
#             )
#         result = client.query(sql_query, parameters=parameters)
#         return result
#     except FileNotFoundError:
#         return f"Error: SQL file '{sql_file}' not found."
#     except Exception as e:
#         return f"An error occurred: {e}"



