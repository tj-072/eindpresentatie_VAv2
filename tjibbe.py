import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
df= pd.read_csv(r"C:\Users\tjibb\Documents\school\jaar_3\minor\eind_prestentatie\weerstations6.csv")
gdf = gpd.GeoDataFrame(df, geometry=gpd.GeoSeries.from_wkt(df['WKT']))
gdf['STN']=gdf['STN_y']
gdf.drop(columns=['WKT', 'STN_x', 'STN_y'], inplace=True)
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

# Definieer een kleurenmapping op basis van de 'fid'-kolom
colormap = plt.cm.get_cmap('afmhot')  # Kies een kleurenschema (hier 'viridis')
norm = Normalize(vmin=gdf['ALT(m)'].min(), vmax=50)
sm = ScalarMappable(cmap=colormap, norm=norm)
sm.set_array([])

# Aangepaste kaartplot met kleuren op basis van 'fid'
fig, ax = plt.subplots(figsize=(10, 10))
gdf.plot(ax=ax, color=sm.to_rgba(gdf['ALT(m)']), alpha=0.5, linewidth=0.5, edgecolor='k', legend=True)

# Voeg een kleurenstaaf toe
cbar = plt.colorbar(sm, ax=ax, label='ALT(m)')

# Voeg een titel toe
plt.title("Kaart met kleuren op basis van 'ALT(m)'")

# Voeg punten toe op basis van 'LON(east)' en 'LAT(north)' kolommen
plt.scatter(gdf['LON(east)'], gdf['LAT(north)'], color='red', label='Punten')

# Toon de kaart
plt.show()