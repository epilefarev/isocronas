import osmnx as ox
from osmnx import plot_graph
from osmnx import k_shortest_paths, plot, add_edge_speeds, plot_graph_folium
import networkx
from plotly import graph_objects as go
import os


def get_map_bbox(n, s, e, w, type) -> networkx.MultiDiGraph:
    g = ox.graph_from_bbox(north=n, south=s, east=e, west=w, network_type=type)
    return g


def get_map_point(lat, lon, dist, type) -> networkx.MultiDiGraph:
    g = ox.graph_from_point(center_point=(lat, lon), dist=dist, network_type=type)
    return g


def get_and_save_all_type_map(lat, lon, dist):
    for type in ["all_private", "all", "bike", "drive", "drive_service", "walk"]:
        g = get_map_point(lat, lon, dist=dist, type=type)

        # ['osmid', 'oneway', 'lanes', 'name', 'highway', 'maxspeed', 'reversed',
        #        'length', 'geometry', 'access', 'width', 'bridge', 'tunnel', 'service']
        m = plot_graph_folium(g, popup_attribute='highway')
        m.save(os.path.join("output", "{}.html".format(type)))


lat, lon, dist = -33.4324959, -70.6271985, 500
get_and_save_all_type_map(lat, lon, dist)
# add_edge_speeds()
