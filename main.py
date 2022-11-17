import osmnx as ox
import geopandas as gpd

g = ox.graph_from_point(center_point=(-33.4576832,-70.6573263), dist=100)
print(g.edges)
df = gpd.geodataframe.DataFrame()
print(df)

