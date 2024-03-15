# %%
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

#file_geopkg = "/Users/felipearaujo/Downloads/oproad_gpkg_gb/data/oproad_gb.gpkg"
file_geopkg = "datasets/data/oproad_gb.gpkg"
bbox_ons_london = [480440.641,140539.151, 559859.004,216532.923] 

roads = gpd.read_file(file_geopkg, bbox=bbox_ons_london)
roads.to_crs(epsg=4326, inplace=True)

routes = pd.read_hdf("datasets/london_formatted_filtered.h5", key="data")
routes = gpd.GeoDataFrame(
    routes, geometry=gpd.points_from_xy(routes.longitude, routes.latitude, crs="EPSG:4326")
)
routes.to_crs(epsg=4326, inplace=True)

plt.rcParams.update({
    'figure.figsize': (12, 8),
    'font.family': 'Courier New',
    'axes.labelsize': 28,
    'xtick.labelsize': 20,
    'ytick.labelsize': 20,
    'lines.linewidth': 0.8,
    'lines.color': 'black',
})

fig, ax = plt.subplots(1)
roads.geometry.plot(ax=ax)
routes.geometry.plot(ax=ax, color='r', markersize=1e-3, zorder=999,)
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
routes.to_file('datasets/routes_london.shp')
#plt.savefig("graphs/london_roads_and_routes_v2.pdf", bbox_inches='tight')
#plt.show()

#points_within = gpd.sjoin_nearest(routes, roads, distance_col='distance_in_degrees')
#points_within['distance_in_meters'] = points_within['distance_in_degrees'] * 111.12
#points_within.to_csv("datasets/points_within_filtered.csv", index=False)
#print(points_within.head())
# %%
