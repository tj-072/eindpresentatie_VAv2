import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
df= pd.read_csv(r"C:\Users\tjibb\Documents\school\jaar_3\minor\eind_prestentatie\weerstations5.csv", sep= ";")
gdf = gpd.GeoDataFrame(df, geometry=gpd.GeoSeries.from_wkt(df['WKT']))
# gdf is je GeoDataFrame met geometrische gegevens

# Definieer een kleurenmapping op basis van de 'fid'-kolom
colormap = plt.cm.get_cmap('viridis')  # Kies een kleurenschema (hier 'viridis')
norm = Normalize(vmin=gdf['fid'].min(), vmax=gdf['fid'].max())
sm = ScalarMappable(cmap=colormap, norm=norm)
sm.set_array([])

# Aangepaste kaartplot met kleuren op basis van 'fid'
fig, ax = plt.subplots(figsize=(10, 10))
gdf.plot(ax=ax, color=sm.to_rgba(gdf['fid']), alpha=0.5, linewidth=0.5, edgecolor='k', legend=True)

# Voeg een kleurenstaaf toe
cbar = plt.colorbar(sm, ax=ax, label='fid')

# Voeg een titel toe
plt.title("Kaart met kleuren op basis van 'fid'")

# Toon de kaart
plt.show()

# gdf is je GeoDataFrame met geometrische gegevens

# Definieer een kleurenmapping op basis van de 'fid'-kolom
colormap = plt.cm.get_cmap('viridis')  # Kies een kleurenschema (hier 'viridis')
norm = Normalize(vmin=gdf['fid'].min(), vmax=gdf['fid'].max())
sm = ScalarMappable(cmap=colormap, norm=norm)
sm.set_array([])

# Aangepaste kaartplot met kleuren op basis van 'fid'
fig, ax = plt.subplots(figsize=(10, 10))
gdf.plot(ax=ax, color=sm.to_rgba(gdf['fid']), alpha=0.5, linewidth=0.5, edgecolor='k', legend=True)

# Voeg een kleurenstaaf toe
cbar = plt.colorbar(sm, ax=ax, label='fid')

# Plaats de naam van iedere polygoon in het midden
for x, y, label in zip(gdf.geometry.centroid.x, gdf.geometry.centroid.y, gdf['NAME']):
    ax.annotate(label, xy=(x, y), xytext=(3, 3), textcoords='offset points')

# Voeg een titel toe
plt.title("Kaart met kleuren op basis van 'fid' en namen in het midden")

# Toon de kaart
plt.show()